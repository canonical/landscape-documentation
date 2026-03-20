---
myst:
  html_meta:
    description: "Release notes for Landscape version 15.01 (January 2015). Features reduced machine requirements for Autopilot deployments, syslog support, event logs, and package-search service."
---

(reference-release-notes-15-01)=
# 15.01 release notes

## Major changes from previous stable release

 * less machines required for !AutoPilot cloud deployments
 * syslog support
 * audit logs replaced by event logs
 * package upgrades and reboots are disabled for !AutoPilot computers
 * new service: package-search
 * '''LDS 15.01.1-0ubuntu1 point release''':
  * Removed Unity desktop webapp integration
  * Fixed an issue where a tag added to a computer did not associate it with a removal profile
 * '''LDS 15.01.1-0ubuntu2 point release''':
  * require a newer `python-convoy` package to fix a fixes a XSS (cross-site scripting) security issue.
 * '''LDS 15.01.2-0ubuntu1 point release''':
  * support Juju 1.22 for Autopilot runs
 * '''LDS 15.01.3-0ubuntu2 point release''':
  * force juju agent version to 1.22.1 to prevent unwanted agent upgrades (Autopilot related only)
Read on for details.

## Changes and new features
This section describes the changes and new features in more detail.

## Machine requirement for AutoPilot
LDS 15.01 introduces a new deployment layout where we require less machines to deploy a fully functional !OpenStack cloud. The minimum number of machines is now only 3 when selecting Ceph for both object and block storage.

## Syslog support
LDS 15.01 now uses rsyslog for its logging. A new configuration file is installed as `/etc/rsyslog.d/20-landscape.conf` which directs all Landscape logging to `/var/log/landscape-server/`. Logging from multiple processes of the same kind is aggregated into one file only. For example, if you have 4 message servers, instead of having one log file for each process, all will log to the same `message-server.log` file.

Landscape can also be instructed to log to another machine. To do that, just change the `syslog-address` line in `/etc/landscape/service.conf` to point at the server and port where you have a syslog-compatible server running. For example:

```text
    [global]
    oops-path # /var/lib/landscape/landscape-oops
    syslog-address # 10.50.2.1:514
```

### Logging format changes
The logging format changed quite significantly. If you have scripts that parse the Landscape logs, they will need fixing. Here is what changed:

 * new log files
 * filename changes
 * format change


## Event log
Event log replaces the existing audit log activities. Having audit activities mixed with regular activities was a bit confusing and noisy. Event log is specific for auditing and won't be mixed with other activities in Landscape.


## AutoPilot reboots and package upgrades
To prevent accidental damage to the infrastructure nodes in clouds deployed using Landscape AutoPilot, package management and reboot alerts have been disabled on those computers. 

## API changes
The results of the API call `GetComputers` now includes `vm_info` and `container_info` that can be used to determine if the computer in question is running inside a VM or container.

## Package search service
A new service is available with this release to speed up package related operations for large installations. This service is called `package-search` and it will be automatically used if you have more than 800 computers registered.

Package search significantly increases the speed by which Landscape processes package information, but at a cost: it will use roughly 0.5Gb of RSS RAM per thousand registered computers.

If you have more than 800 registered computers and not enough RAM, you can disable package-search by changing the `account-threshold` value in the `[package-search]` section of `/etc/landscape/service.conf` to a higher value and restarting all services with `sudo lsctl restart`. For example:

```text
   [package-search]
   port # 9099
   stores # main package resource-1
   pid-path # /var/run/landscape/landscape-package-search-1.pid
   account-threshold # 100000
```

That value of 100000 means that the `package-search` service will only kick into action when your account has more than 100k computers.


## Non-quickstart deployment
For a non-quickstart deployment, where the database is separated from the application server, please go [[LDS/ManualInstallation15.01|here]].

## Upgrading LDS
LDS 15.01 supports Ubuntu 14.04 LTS ("trusty"). It can only be upgraded to from LDS 14.10.X.

## Important upgrade notes
All existing audit log activities will be deleted during the upgrade to LDS 15.01 and later. The new auditing system is called Event Log and is incompatible with the previous one.

## Quickstart upgrade
If you used the `landscape-server-quickstart` package to install LDS 14.10.X then you can use this method to upgrade it.

If you are a landscape.canonical.com customer, you can select new version of LDS in your hosted account at https://landscape.canonical.com and then run:

```text
    sudo apt-get update
    sudo apt-get dist-upgrade
```

Alternatively, just add the LDS 15.01 PPA and run the same commands as above:

```text
    sudo add-apt-repository ppa:landscape/15.01
    sudo apt-get update
    sudo apt-get dist-upgrade
```

When prompted, reply with `N `to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically.

During quickstart upgrades, you will see a backtrace about a "bad interpolation" error in `/etc/landscape/service.conf`. It's expected and unfortunate, but harmless. It happens because the new code needs a small change to the configuration file, a change that is only performed a bit later in the upgrade process, so the earlier stages complain.

## Non-quickstart upgrade
Follow these steps to perform a non-quickstart upgrade, that is, you did not use the landscape-server-quickstart package when installing LDS 15.01: 

 * stop all landscape services on all machines that make up your non-quickstart deployment, except the database service: `sudo lsctl stop`
 * on the database server, edit `/etc/postgresql/<version>/main/postgresql.conf` (replace `<version>` with your postgresql version) and set `max_prepared_transactions` to the same value as `max_connections` if it's not like that already. Then restart the database services with `sudo postgresql restart`.
 * edit `/etc/landscape/service.conf` on all machines except the database and perform these changes:
  * remove the `log-path` line from the `[global]` section
  * add `syslog-address # /dev/log` to the `[global]` section
  * change '''all''' `mailer-path` lines to `mailer-path # /var/lib/landscape/landscape-mail-queue`. There are such lines in the `[landscape]`, `[job-handler]`, `[api]`, `[maintenance]`, `[scripts]` and `[package-upload]` sections
  * change the `account-threshold` in the `[package-search]` section to `800`: `account-threshold # 800`
 * in the Landscape apache vhost file, usually `/etc/apache2/sites-enabled/landscape.conf`, perform these changes:
  * In all `ErrorDocument` lines, change the path component `/static/offline/` to just `/offline`. For example: `ErrorDocument 403 /static/offline/unauthorized.html` becomes `ErrorDocument 403 /offline/unauthorized.html`
  * Add this alias to the http (*:80) and https (*:443) virtual hosts alongside the existing ones: `Alias /offline /opt/canonical/landscape/canonical/landscape/offline`
  * Add this rewrite condition to the http (*:80) and https (*:443) virtual hosts alongside the existing ones: `RewriteCond %{REQUEST_URI} !/offline`
  * Add this proxy pass rule to the https (*:443) virtual host '''only''' alongside the existing ones: `ProxyPass /offline !`
 * Restart apache with `sudo service apache2 restart`
 * Run this script on all machines except the database:

```text
    #!/bin/bash
    BASEDIR=/var/lib/landscape
    mv $BASEDIR/landscape-mail-queue-1/ $BASEDIR/landscape-mail-queue
    for msg in $(find $BASEDIR/landscape-mail-queue-* -type f 2>/dev/null); do
        mv $msg $BASEDIR/landscape-mail-queue/$(basename $(dirname $msg))
    done
    rm -rf $BASEDIR/landscape-mail-queue-*
```

 * grab the landscape user password for the rabbitmq-server from `/etc/landscape/service.conf`. It's in the `[broker]` section
 * run these commands on the machine where rabbitmq-server is running, usually your APP server. Replace `<password>` with the rabbitmq-server password for the landscape user grabbed above:

```text
    sudo rabbitmqctl stop_app
    sudo rabbitmqctl reset
    sudo rabbitmqctl start_app
    sudo rabbitmqctl add_user landscape <password>
    sudo rabbitmqctl add_vhost landscape
    sudo rabbitmqctl set_permissions -p landscape landscape ".*" ".*" ".*"
```

 * add the LDS 15.01 PPA: `sudo add-apt-repository ppa:landscape/15.01`
 * refresh the apt database and upgrade: `sudo apt-get update && sudo apt-get dist-upgrade`
 * answer with "N" to any dpkg questions about Landscape configuration files
 * if you have `UPGRADE_SCHEMA` enabled in `/etc/default/landscape-server`, then the required schema upgrade will be performed as part of the package upgrade and all services will be running at the end. The upgrade is finished.
 * if `UPGRADE_SCHEMA` is disabled, then you will have failures when the services are restarted at the end of the upgrade. That's expected. You now have to perform the schema upgrade manually with this command:

```text
    sudo setup-landscape-server
```

 * after it succeeds, the Landscape services can be started:

```text
    sudo lsctl start
```

## Upgrade of a juju-deployed LDS
Upgrading of a juju-deployed LDS is not yet directly supported. Please follow the non-quickstart upgrade steps.

## OpenStack Autopilot Beta: Known Issues
 * Aborting a cloud deployment right after the abort button becomes available can fail and leak MAAS nodes. Furthermore, Landscape will probably have failed to clear the deployment from its database, so if a new deployment is attempted with the exact same region and cloud names, it will fail.

 * OpenStack clouds deployed with 15.01 will not be able to be upgraded to cloud architectures of future releases.

