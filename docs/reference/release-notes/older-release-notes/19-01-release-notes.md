(reference-release-notes-19-01)=
# 19.01 release notes


## Highlights

 * Improvements to security updates detection.
 * Create script to unblock stuck repository activities.
 * Disable TLS 1.0 in apache2 config (quickstart install)
 * ComputerOfflineAlert flapping when exchanges are not happening
 * Option to randomize delivery of manual upgrade requests
 * Activity scheduling widget should reject dates in the past
 * Landscape appears to hang after hitting 'remove computer'
 * Segmentation fault in `landscape-env.sh`
 * Can't run a script on more than 100 clients using the API
 * last_exchange_time should be visible in a couple key places
 * Landscape should display CVEs alongside USNs
 * Landscape-server-quickstart fails if there is no eth0
 * Landscape should include GPG material for Bionic.
 * There are no special upgrade instructions for Landscape 19.01, regardless of the installation method.

Landscape 19.01.1 contains the following fix:

 * unscalable layout for roles table.

## Upgrade notes

Landscape 19.01 supports Ubuntu 18.04 LTS ("bionic"). It can only be upgraded from Landscape 18.03 also running on the same Ubuntu 18.04 LTS release.

For upgrading from Landscape 17.03 to 19.01 you'll have to go through the upgrade to Landscape 18.03 first while still on Ubuntu 16.04. Then go through the [Ubuntu release upgrade](/reference/release-notes/older-release-notes/18-03-release-notes.md#ubuntu-release-upgrade) from Ubuntu 16.04 LTS to Ubuntu 18.04 LTS.

To upgrade a Landscape 18.03 running on Ubuntu 16.04 LTS ("xenial") to Landscape 19.01, first you need to upgrade your Ubuntu release to 18.04 LTS ("bionic"), and then upgrade Landscape to 19.01.

## Quickstart upgrade
If you used the landscape-server-quickstart package to install Landscape 18.03 then you can use this method to upgrade it.

If you are a [Landscape](https://landscape.canonical.com) customer, you can select new version of Landscape in your hosted account at [https://landscape.canonical.com](https://landscape.canonical.com) and then run:
```
sudo apt-get update
sudo apt-get dist-upgrade
```

Alternatively, just add the Landscape 19.01 PPA and run the same commands as above:
```
sudo add-apt-repository -u ppa:landscape/19.01
sudo apt-get dist-upgrade
```
When prompted, reply with `N` to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically.

## Upgrading a manual installation deployment

Follow these steps to perform a non-quickstart upgrade, that is, you did not use the landscape-server-quickstart package when installing Landscape 19.01:

Stop all Landscape services on all machines that make up your non-quickstart deployment, except the database service:

```
sudo lsctl stop
```

Change `UPGRADE_SCHEMA` to `no` in `/etc/default/landscape-server`:
```
...
UPGRADE_SCHEMA="no"
...
```

Disable all the landscape-server cron jobs from `/etc/cron.d/landscape-server` in all app servers:
```
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
```
# Disable insecure TLSv1
  SSLProtocol all -SSLv3 -SSLv2 -TLSv1
  SSLHonorCipherOrder On
  SSLCompression Off
  # Disable old/vulnerable ciphers. Note: one very long line
  SSLCipherSuite EECDH+AESGCM+AES128:EDH+AESGCM+AES128:EECDH+AES128:EDH+AES128:ECDH+AESGCM+AES128:aRSA+AESGCM+AES128:ECDH+AES128:DH+AES128:aRSA+AES128:EECDH+AESGCM:EDH+AESGCM:EECDH:EDH:ECDH+AESGCM:aRSA+AESGCM:ECDH:DH:aRSA:HIGH:!MEDIUM:!aNULL:!NULL:!LOW:!3DES:!DSS:!EXP:!PSK:!SRP:!CAMELLIA:!DHE-RSA-AES128-SHA:!DHE-RSA-AES256-SHA:!aECDH
```

Restart apache
```
sudo service apache2 restart
```

Add the Landscape 19.01 PPA:
```
sudo add-apt-repository -u ppa:landscape/19.01
```

Update and upgrade:
```
sudo apt-get update && apt-get dist-upgrade
```

!!! Note:
    Answer with `N` to any dpkg questions about Landscape configuration files

Since `UPGRADE_SCHEMA` is disabled, you will have failures when the services are restarted at the end of the upgrade. That's expected. You now have to perform the schema upgrade manually with this command:
```
sudo setup-landscape-server
```
After all these steps are completed, the Landscape services can be started:
```
sudo lsctl restart
```

Re-enable the landscape-server cron jobs in `/etc/cron.d/landscape-server` in all app servers:
```
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

## Upgrading a Juju deployment

Starting with Landscape 15.10, Juju deployed Landscape can be upgraded in place. The method for upgrading varies based upon using Juju 1.x or Juju 2.x and using a single unit for deployment vs multiple unit deployment.

!!! Note:
    Newer landscape-server charm deprecates the `source` configuration key in favor of `install_sources`. The procedures in this document reflect this change.

### Using Juju 2.x

#### Single unit deployment
If you have just one landscape-server unit, please follow this procedure:

```
juju upgrade-charm landscape-server
juju config landscape-server source="" install_sources="['ppa:landscape/19.01']"
juju run-action landscape-server/0 pause
juju run-action landscape-server/0 upgrade
juju run-action landscape-server/0 migrate-schema
juju run-action landscape-server/0 resume
```

#### Multiple unit deployment

When upgrading a multiple unit deployment, you will need to update each unit individually.

!!! Warning:
    When upgrading a deployment with multiple units, prior to moving to the next step, you should verify that the previous step has completed.

Each action returns an identifier that should be used to check its outcome with the `show-action-output` command before running the next action:

```
juju show-action-output --wait 0 <uuid>
```

For example:

```
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

```
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
```
juju upgrade-charm landscape-server
```

Next, switch to the Landscape 19.01 PPA:
```
juju config landscape-server source="" install_sources="['ppa:landscape/19.01']"
```
Pause all of the units by issuing a command similar to this for each landscape-server unit:
```
juju run-action landscape-server/0 pause
```

Upgrade landscape-server by issuing a command similar to this for each landscape-server unit:
```
juju run-action landscape-server/0 upgrade
```

Run the migrate-schema command on **only one** landscape-server unit:
```
juju run-action landscape-server/0 migrate-schema
```

Resume landscape-server by issuing a command similar to this for each landscape-server unit:
```
juju run-action landscape-server/0 resume
```

### Using Juju 1.x

#### Single unit deployment
If you have just one landscape-server unit, please follow this procedure:

```
juju upgrade-charm landscape-server
juju set landscape-server source="" install_sources="['ppa:landscape/19.01']"
juju action do landscape-server/0 pause
juju action do landscape-server/0 upgrade
juju action do landscape-server/0 migrate-schema
juju action do landscape-server/0 resume
```

#### Multiple unit deployment

When upgrading a multiple unit deployment, you will need to update each unit individually.

!!! Warning:
    When upgrading a deployment with multiple units, prior to moving to the next step, you should verify that the previous step has completed.

Each action returns an identifier that should be used to check its outcome with the `fetch` command before running the next action:

```
juju action fetch <uuid>
```

For example:

```
$ juju action do landscape-server/0 pause
Action queued with id: 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
$ juju action fetch 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
status: completed
timing:
  completed: 2016-06-23 19:24:39 +0000 UTC
  enqueued: 2016-06-23 19:24:32 +0000 UTC
  started: 2016-06-23 19:24:33 +0000 UTC
```

As an example of when it fails and what kind of output to expect, here
we are trying to upgrade a unit that hasn't been paused before the upgrade:

```
$ juju action do landscape-server/0 upgrade
Action queued with id: f3d2343c-33e4-4faf-8c4e-59f796124dd4
$ juju action fetch f3d2343c-33e4-4faf-8c4e-59f796124dd4
message: This action can only be called on a unit in paused state.
status: failed
timing:
  completed: 2016-06-23 19:26:40 +0000 UTC
  enqueued: 2016-06-23 19:26:36 +0000 UTC
  started: 2016-06-23 19:26:38 +0000 UTC
```

Lets get started! First, let's upgrade the Landscape charm:
```
juju upgrade-charm landscape-server
```

Next, switch to the Landscape 19.01 PPA:
```
juju set landscape-server source="" install_sources="['ppa:landscape/19.01']"
```

Pause all of the units by issuing a command similar to this for each landscape-server unit:
```
juju action do landscape-server/0 pause
```

Upgrade landscape-server by issuing a command similar to this for each landscape-server unit:
```
juju action do landscape-server/0 upgrade
```
Run the migrate-schema command on **only one** landscape-server unit:
```
juju action do landscape-server/0 migrate-schema
```
Resume landscape-server by issuing a command similar to this for each landscape-server unit:
```
juju action do landscape-server/0 resume
```

## Known issues

This section describes some relevant known issues that might affect your usage of Landscape 19.01.

 * The `landscape-package-search` service ignores the `RUN_*` variable settings in `/etc/default/landscape-server` and will always try to start. This is only noticeable using multiple application servers. To disable this run:
```
sudo systemctl disable landscape-package-search
sudo service landscape-package-search stop
```

 * To upgrade to 19.01 from Ubuntu 16.04, you must first `do-release-upgrade` to Ubuntu 18.04.

 * When the landscape-server package is installed or upgraded, its postinst step runs a `chown landscape:landscape -R /var/lib/landscape` command. If you have the repository management files mounted via NFS in the default location `/var/lib/landscape/landscape-repository` and with the NFS `root_squash` option set, then this command will fail. There are two workarounds:
    * temporarily enable the `no_root_squash` option on the NFS server, which will allow the command to complete
    * mount the repository elsewhere, outside of the `/var/lib/landscape` tree. For example, to mount it under `/landscape-repository`, follow these steps:
```
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

