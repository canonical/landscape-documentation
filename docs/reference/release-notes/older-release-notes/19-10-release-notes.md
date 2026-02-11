---
myst:
  html_meta:
    description: "Release notes for Landscape version 19.10 (October 2019). Improved ESM USN detection, OpenID Connect authentication support, automatic activity cleanup, and bug fixes."
---

(reference-release-notes-19-10)=
# 19.10 release notes

## Landscape Release 19.10
These are the release notes for Landscape 19.10.

**Warning**:
    For manual and juju upgrades, make sure the database server has the `postgresql-plpython3-10` package, which replaces the obsolete `postgresql-plpython-10` package.


## Highlights

 * Improvement for USN detection on ESM
 * Report by CVE causes oops
 * Underflow updating computers active-process-info
 * Slow activity queries on the account dashboard
 * Roles table does not scroll
 * Automatically clean X days-old activities and events.
 * UI issue in Computers API doc
 * Feature request - enable landscape to authenticate users with OpenID-Connect
 * Landscape should add GPG material for Bionic

Landscape 19.10.1 contains the following fixes:

 * Packaging of unblock-repo-activities script.
 * Quickstart cert generation with long FQDN.
 * Remove old dependency to ceph-common.

Landscape 19.10.2 contains the following fixes:

 * OIDC login loop when missing end_session_endpoint
 * Landscape doesn't support focal hash-ids

Landscape 19.10.3 contains the following fixes:

 * Cron jobs don't get proxy setting from landscape
 * Landscape API doesn't support GPG subkeys

Landscape 19.10.4 contains the following fixes:

 * Timeouts when modifying package-profiles
 * Server fails to receive binary script output
 * Low admin limit of juju-bootstrapped deployment

Landscape 19.10.5 contains the following fixes:

 * Block mod-status by default on quickstart.
 * HTTP header injection fix.
 * Replace insecure tokens generator.
 * Open redirection vulnerability.
 * NVMe hardware storage listing.

Landscape 19.10.6 contains the following fix:

 * Pam authentication does not handle non-ascii characters.

Landscape 19.10.7 contains the following fix:

 * Charm configs don't get updated in database.

Landscape 19.10.8 contains the following fixes:

 * Alert when a UA preference file disables ESM.
 * Make logo link in offline pages relative.
 * Set `umask` in hashid script.
 * Fix bugs associate with clone status not getting updated. Also UI improvements to clones
 * Support newer virtio hardware info
 * Adds content policy headers
 * Changes to receive message from client containing computer tag info
 * Trim whitespace on email fields in settings and invite admin pages
 * Limit processing of HEAD requests
 * Clamp monitoring graph range.
 * Quote CSV fields which would be interpreted as formula by Excel
 * Blocked when the license expires today
 * Allow PendingComputer edition for users with limited access context
 * Escape DB store credentials in schema setup.
 * Validate registration key characters.
 * Disable nested access roles on admin disable.
 * Allow reporting about older USNs in compliance report.

## Upgrade notes

Landscape 19.10 supports Ubuntu 18.04 LTS ("bionic"). It can only be upgraded from Landscape 19.01 also running on the same Ubuntu 18.04 LTS release.

For upgrading from a prior Landscape version, you'll have to go through the upgrade to Landscape 19.01 first.

## Quickstart upgrade
If you used the landscape-server-quickstart package to install Landscape 19.01 then you can use this method to upgrade it.

If you are a [Landscape](https://landscape.canonical.com) customer, you can select new version of Landscape in your hosted account at [https://landscape.canonical.com](https://landscape.canonical.com) and then run:

```text
sudo apt-get update
sudo apt-get dist-upgrade
```


Alternatively, just add the Landscape 19.10 PPA and run the same commands as above:

```text
sudo add-apt-repository -u ppa:landscape/19.10
sudo apt-get dist-upgrade
```

When prompted, reply with `N` to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically.

## Upgrading a manual installation deployment

!!! Warning:
    Prior to upgrading, make sure the database server has the `postgresql-plpython3-10` package installed. This replaces the obsolete `postgresql-plpython-10` dependency. Failing to have that new database requirement, the schema upgrade will fail.

```text
sudo apt install postgresql-plpython3-10
```


Follow these steps to perform a non-quickstart upgrade, that is, you did not use the landscape-server-quickstart package when installing Landscape 19.10:

Stop all Landscape services on all machines that make up your non-quickstart deployment, except the database service:

```text
sudo lsctl stop
```


Change `UPGRADE_SCHEMA` to `no` in `/etc/default/landscape-server`:

```text
...
UPGRADE_SCHEMA="no"
...
```


Disable all the landscape-server cron jobs from `/etc/cron.d/landscape-server` in all app servers:

```text
# This runs the daily maintenance updates
# 0 03 * * * landscape /opt/canonical/landscape/scripts/maintenance.sh
# Security Updates
# 35 * * * * landscape /opt/canonical/landscape/scripts/update_security_db.sh
# Update Alerts
# */5 * * * * landscape ( /opt/canonical/landscape/scripts/update_alerts.sh; /opt/canonical/landscape/scripts/landscape_profiles.sh; /opt/canonical/landscape/scripts/process_alerts.sh )
# Build hash-id databases
# 30 3 * * 0 landscape /opt/canonical/landscape/scripts/hash_id_databases.sh
# Update meta-release information
# 30 2 * * * landscape /opt/canonical/landscape/scripts/meta_releases.sh
# Update LDS releases
# 45 2 * * * landscape /opt/canonical/landscape/scripts/sync_lds_releases.sh
# Publish Anonymous metrics
# 55 2 * * * landscape /opt/canonical/landscape/scripts/report_anonymous_metrics.sh
```


Update the Landscape apache vhost as follows, adding the following SSL directives to the HTTPS vhost:

```text
# Disable insecure TLSv1
  SSLProtocol all -SSLv3 -SSLv2 -TLSv1
  SSLHonorCipherOrder On
  SSLCompression Off
  # Disable old/vulnerable ciphers. Note: one very long line
  SSLCipherSuite EECDH+AESGCM+AES128:EDH+AESGCM+AES128:EECDH+AES128:EDH+AES128:ECDH+AESGCM+AES128:aRSA+AESGCM+AES128:ECDH+AES128:DH+AES128:aRSA+AES128:EECDH+AESGCM:EDH+AESGCM:EECDH:EDH:ECDH+AESGCM:aRSA+AESGCM:ECDH:DH:aRSA:HIGH:!MEDIUM:!aNULL:!NULL:!LOW:!3DES:!DSS:!EXP:!PSK:!SRP:!CAMELLIA:!DHE-RSA-AES128-SHA:!DHE-RSA-AES256-SHA:!aECDH
```


Unless you require it and take necessary steps to secure that endpoint, it is recommended to disable mod-status:

```text
sudo a2dismod status
```


Restart apache

```text
sudo service apache2 restart
```


Add the Landscape 19.10 PPA:

```text
sudo add-apt-repository -u ppa:landscape/19.10
```


Update and upgrade:

```text
sudo apt-get update && apt-get dist-upgrade
```


**Note**:
    Answer with `N` to any dpkg questions about Landscape configuration files

Since `UPGRADE_SCHEMA` is disabled, you will have failures when the services are restarted at the end of the upgrade. That's expected. You now have to perform the schema upgrade manually with this command:

```text
sudo setup-landscape-server
```

After all these steps are completed, the Landscape services can be started:

```text
sudo lsctl restart
```


Re-enable the landscape-server cron jobs in `/etc/cron.d/landscape-server` in all app servers:

```text
# This runs the daily maintenance updates
0 03 * * * landscape /opt/canonical/landscape/scripts/maintenance.sh
# Security Updates
35 * * * * landscape /opt/canonical/landscape/scripts/update_security_db.sh
# Update Alerts
*/5 * * * * landscape ( /opt/canonical/landscape/scripts/update_alerts.sh; /opt/canonical/landscape/scripts/landscape_profiles.sh; /opt/canonical/landscape/scripts/process_alerts.sh )
# Build hash-id databases
30 3 * * 0 landscape /opt/canonical/landscape/scripts/hash_id_databases.sh
# Update meta-release information
30 2 * * * landscape /opt/canonical/landscape/scripts/meta_releases.sh
# Update LDS releases
45 2 * * * landscape /opt/canonical/landscape/scripts/sync_lds_releases.sh
# Publish Anonymous metrics
55 2 * * * landscape /opt/canonical/landscape/scripts/report_anonymous_metrics.sh
```

## Upgrading a Juju 2.x deployment



Prior to upgrading landscape-server units, make sure the database servers have the newly required `postgresql-plpython3-VERSION`. That version requirement might already be fulfilled if deployed from a recent bundle. Otherwise, add it to the postgresql units:

```text
juju config postgresql extra_packages='python-apt postgresql-contrib postgresql-.*-debversion postgresql-plpython.*'
```


Juju deployed Landscape can be upgraded in place, but it does depend if it is a single unit or multiple unit deployment.

**Note**:
    Newer landscape-server charm deprecates the `source` configuration key in favor of `install_sources`. The procedures in this document reflect this change.

### Single unit deployment
If you have just one landscape-server unit, please follow this procedure:

```text
juju upgrade-charm landscape-server
juju config landscape-server source="" install_sources="['ppa:landscape/19.10']"
juju run-action landscape-server/0 pause
juju run-action landscape-server/0 upgrade
juju run-action landscape-server/0 migrate-schema
juju run-action landscape-server/0 resume
```

### Multiple unit deployment


When upgrading a multiple unit deployment, you will need to update each unit individually.

**Warning**:
    When upgrading a deployment with multiple units, prior to moving to the next step, you should verify that the previous step has completed.

Each action returns an identifier that should be used to check its outcome with the `show-action-output` command before running the next action:

```text
juju show-action-output --wait 0 <uuid>
```


For example:

```text
$ juju run-action landscape-server/0 pause
Action queued with id: 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
$ juju show-action-output --wait 0 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
status: completed
timing:
  completed: 2019-01-11 04:27:57 +0000 UTC
  enqueued: 2019-01-11 04:27:46 +0000 UTC
  started: 2019-01-11 04:27:47 +0000 UTC
```


As an example of when it fails and what kind of output to expect, here
we are trying to upgrade a unit that hasn't been paused before the upgrade:

```text
$ juju run-action landscape-server/0 upgrade
Action queued with id: f3d2343c-33e4-4faf-8c4e-59f796124dd4
$ juju show-action-output --wait 0 f3d2343c-33e4-4faf-8c4e-59f796124dd4
message: This action can only be called on a unit in paused state.
status: failed
timing:
  completed: 2016-06-23 19:26:40 +0000 UTC
  enqueued: 2016-06-23 19:26:36 +0000 UTC
  started: 2016-06-23 19:26:38 +0000 UTC
```


Lets get started! First, let's upgrade the Landscape charm:

```text
juju upgrade-charm landscape-server
```


Next, switch to the Landscape 19.10 PPA:

```text
juju config landscape-server source="" install_sources="['ppa:landscape/19.10']"
```


Pause all of the units by issuing a command similar to this for each landscape-server unit:

```text
juju run-action landscape-server/0 pause
```


Upgrade landscape-server by issuing a command similar to this for each landscape-server unit:

```text
juju run-action landscape-server/0 upgrade
```


Run the migrate-schema command on **only one** landscape-server unit:

```text
juju run-action landscape-server/0 migrate-schema
```


Resume landscape-server by issuing a command similar to this for each landscape-server unit:

```text
juju run-action landscape-server/0 resume
```

## Known issues


This section describes some relevant known issues that might affect your usage of Landscape 19.10.

 * The `landscape-package-search` service ignores the `RUN_*` variable settings in `/etc/default/landscape-server` and will always try to start. This is only noticeable using multiple application servers. To disable this run:

```text
sudo systemctl disable landscape-package-search
sudo service landscape-package-search stop
```


 * To upgrade to 19.10 from Ubuntu 16.04, you must first `do-release-upgrade` to Ubuntu 18.04.

 * When the landscape-server package is installed or upgraded, its postinst step runs a `chown landscape:landscape -R /var/lib/landscape` command. If you have the repository management files mounted via NFS in the default location `/var/lib/landscape/landscape-repository` and with the NFS `root_squash` option set, then this command will fail. There are two workarounds:
    * temporarily enable the `no_root_squash` option on the NFS server, which will allow the command to complete
    * mount the repository elsewhere, outside of the `/var/lib/landscape` tree. For example, to mount it under `/landscape-repository`, follow these steps:

```text
    sudo mkdir -m 0755 /landscape-repository
    sudo chown landscape:landscape /landscape-repository
    sudo vi /etc/landscape/service.conf <-- change repository-path to /landscape-repository
    sudo vi /etc/apache2/sites-enabled/<yourvhost> <-- change "Alias /repository /var/lib/landscape/landscape-repository" to "Alias /repository /landscape-repository"
    sudo lsctl stop
    sudo service apache2 stop
    sudo umount /var/lib/landscape/landscape-repository # may have to kill gpg-agent processes to be allowed to umount
    sudo mount <nfserver>:<export> -t nfs -o rw /landscape-repository
    # check that /landscape-repository and files/directories under it are still owned by landscape:landscape
    sudo service apache2 start
    sudo lsctl start
    # update /etc/fstab regarding the new mount point, to avoid surprises after a reboot
```


 * Also due to the `chown` command run during postinst explained above, the upgrade can take a long time if the repository files are mounted somewhere `/var/lib/landscape`, depending on the size of the repository. On an experiment with two machines on the same gigabit switch and a 150Gb repository mounted via NFS, a test upgrade spent about 30min just in that `chown` command. While that happens, the service is down. Until a fix is explicitly mentioned in the release notes, we suggest the same workaround as for the previous case: mount the repository outside of the `/var/lib/landscape/` tree.

