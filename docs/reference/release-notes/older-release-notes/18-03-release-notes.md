(reference-release-notes-older-release-notes-18-03-release-notes)=
# 18.03 release notes

Title: Landscape Release Notes 18.03

## Landscape Release 18.03

These are the release notes for Landscape 18.03.

## Highlights

Landscape 18.03 is a major release with the following:

 * Ubuntu 18.04 LTS ("bionic") support
 * OpenStack autopilot removed
 * edit-pocket should have option to toggle udeb support
 * A user with a restricted role can't schedule package upgrades. For users with limited access to the Global Access group, scheduling packages operations on machines in child groups was previously returning Unauthorized errors, even when the user had a role to manage machines from within that access group. This allows back the scheduling of packages from the web, consistently with the api.
 * "landscape.no_proxy" setting not advertised from settings API. Landscape-api now exposes the landscape.no_proxy setting from the api, consistently with the web interface.
 * Add autoremove to Landscape. An option has been added to the update profiles to automatically remove packages marked as auto-installed but no longer required to satisfy a dependency.
 * Missing API call to rename computer. Up to now, it was only possible to change the title of a computer from the web interface. The equivalent API call was added.
 * Display a computer's repository profiles on the info page. Although repository profiles are still managed from the API, they are now listed on the computer info pages on which they apply.
 * Variable delay to USN refresh to avoid timeouts. Security database updates are now scheduled over a time window.

Landscape 18.03.1 contains the following fix:

 * Unscalable layout for roles table.

## Upgrade notes

Landscape 18.03 supports Ubuntu 18.04 LTS ("bionic") and Ubuntu 16.04 LTS ("xenial").

It can only be upgraded from Landscape 17.03 running on Ubuntu 16.04 LTS ("xenial") all the way up to Landscape 18.03 running on Ubuntu 18.04 LTS release.

## Quickstart upgrade

If you used the landscape-server-quickstart package to install Landscape 17.03 then you can use this method to upgrade it.

If you are a <https://landscape.canonical.com> customer, you can select new version of Landscape in your hosted account at <https://landscape.canonical.com> and then run:

```
sudo apt-get update
sudo apt-get dist-upgrade
```

Alternatively, just add
the Landscape 18.03 PPA and run the same commands as above:

```
sudo add-apt-repository -u ppa:landscape/18.03
sudo apt-get dist-upgrade
```

When prompted, reply with \`N\` to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically.

## Non-quickstart upgrade

Follow these steps to perform a non-quickstart upgrade, that is, you did not use the landscape-server-quickstart package when installing Landscape 17.03:

 * stop all landscape services on all machines that make up your non-quickstart deployment, except the database service: `sudo lsctl stop`
 * double check that `UPGRADE_SCHEMA` is set to `no` in `/etc/default/landscape-server`
 * disable all the landscape-server cron jobs from `/etc/cron.d/landscape-server` in all app servers
 * Restart apache using `sudo service apache2 restart`
 * add the Landscape 18.03 PPA: `sudo add-apt-repository -u ppa:landscape/18.03`
 * update and upgrade: `sudo apt-get update && sudo apt-get dist-upgrade`
 * answer with `N` to any dpkg questions about Landscape configuration files
 * if you have `UPGRADE_SCHEMA` enabled in `/etc/default/landscape-server`, then the required schema upgrade will be performed as part of the package upgrade and all services will be running at the end. The upgrade is finished.
 * if `UPGRADE_SCHEMA` is disabled, then you will have failures when the services are restarted at the end of the upgrade. That's expected. You now have to perform the schema upgrade manually with this command:
```
sudo setup-landscape-server
```
  After all these steps are completed, the Landscape services can be started:
```
sudo lsctl restart
```
 * re-enable the landscape-server cron jobs in `/etc/cron.d/landscape-server` in all app servers

 * It is also recommended to disable TLSv1.0 as it is deprecated. Add the `-TLSv1` to the list of disabled protocols in the HTTPS vhost configuration like so:
```
SSLProtocol all -TLSv1 -SSLv3 -SSLv2
```

## Charm upgrade
Starting with Landscape 15.10, juju deployed Landscape can be upgraded
in place.  If you have just one landscape server unit, please follow
this procedure:

```
# Juju 1.x:
juju upgrade-charm landscape-server
juju set landscape-server source=ppa:landscape/18.03
juju action do landscape-server/0 pause
juju action do landscape-server/0 upgrade
juju action do landscape-server/0 migrate-schema
juju action do landscape-server/0 resume

# Juju 2.x:
juju upgrade-charm landscape-server
juju config landscape-server source=ppa:landscape/18.03
juju run-action landscape-server/0 pause
juju run-action landscape-server/0 upgrade
juju run-action landscape-server/0 migrate-schema
juju run-action landscape-server/0 resume
```

For multiple landscape-server units, you should pause all of them,
upgrade one by one, run the migrate-schema command on only one, and
then resume all units.

Each action returns an identifier that should be used to check its
outcome with the fetch command before running the next action:

```
# Juju 1.x:
juju action fetch <uuid>

# Juju 2.x:
juju show-action-output --wait 0 <uuid>
```

For example:

```
# Juju 1.x:
$ juju action do landscape-server/0 pause
Action queued with id: 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
$ juju action fetch 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
status: completed
timing:
  completed: 2018-06-23 19:24:39 +0000 UTC
  enqueued: 2018-06-23 19:24:32 +0000 UTC
  started: 2018-06-23 19:24:33 +0000 UTC

# Juju 2.x:
$ juju run-action landscape-server/0 pause
Action queued with id: 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
$ juju show-action-output --wait 0 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
status: completed
timing:
  completed: 2018-03-24 04:27:57 +0000 UTC
  enqueued: 2018-03-24 04:27:46 +0000 UTC
  started: 2018-03-24 04:27:47 +0000 UTC
```

As an example of when it fails and what kind of output to expect, here
we are trying to upgrade a unit that hasn't been paused before, other
than command line structure, this has not changed in Juju 2.x:

```
# Juju 1.x:
$ juju action do landscape-server/0 upgrade
Action queued with id: f3d2343c-33e4-4faf-8c4e-59f796124dd4
$ juju action fetch f3d2343c-33e4-4faf-8c4e-59f796124dd4
message: This action can only be called on a unit in paused state.
status: failed
timing:
  completed: 2018-06-23 19:26:40 +0000 UTC
  enqueued: 2018-06-23 19:26:36 +0000 UTC
  started: 2018-06-23 19:26:38 +0000 UTC
```



## Ubuntu release upgrade

You can take advantage of the fact that Landscape 18.03 supports both Ubuntu 16.04 LTS ("xenial") and Ubuntu 18.04 LTS ("bionic") to upgrade your Landscape deployment from "xenial" to "bionic". This section details the upgrade procedure depending on how you deployed Landscape.

### Release upgrade for quickstart deployments

Follow these steps in order:

 * Upgrade Landscape 17.03 to 18.03 while still on Ubuntu 16.04 LTS ("xenial") using the quickstart upgrade method.
 * Configure the release update manager to keep third-party repositories enabled by running this command:
```
echo -e "[Sources]\nAllowThirdParty=yes" | sudo tee /etc/update-manager/release-upgrades.d/allow.cfg
```
 * Upgrade Ubuntu 16.04 LTS ("xenial") to Ubuntu 18.04 LTS ("bionic") using the `do-release-upgrade` tool. First try using the tool as is:
```
sudo do-release-upgrade
```
If it tells you that no new releases are available, try adding the `-d` parameter:
```
sudo do-release-upgrade -d
```
Pay close attention to its output: it should say that it is starting an upgrade to "bionic". Reboot after the upgrade is done.

 * Stop all Landscape services:
```
sudo lsctl stop
```
 * Install the 10 postgresql packages:
```
sudo apt install postgresql-10 postgresql-plpython-10 postgresql-contrib-10 postgresql-client-10 postgresql-10-debversion
```
!!! Note:
    If you get a warning about `/etc/postgresql-common/createcluster.conf` while configuring `postgresql-common`, select to keep the local version.

 * Drop the newly created 10 cluster:
```
sudo pg_dropcluster 10 main --stop
```
 * Upgrade the 9.5 cluster:
```
sudo pg_upgradecluster 9.5 main
```
 * Start Landscape services:
```
sudo lsctl start
```
 * Verify that Landscape is working correctly.
 * If you are happy with the upgrade results, the previous 9.5 cluster can be dropped:
```
sudo pg_dropcluster 9.5 main
```

### Release upgrade for manual (non-quickstart) deployments
The release upgrade process for the manual non-quickstart deployment is a bit more complicated and needs to be done in steps. A summary is shown in the table below, in the order the steps should happen:


LDS           | Ubuntu (LDS) | PostgreSQL | Ubuntu (PostgreSQL) |
---           | ---          | ---        | ---                 |
 `17.03 (1)`  | Xenial       | 9.5        | Xenial              |
 `18.03 (2)`  | `Xenial (3)` | 9.5        | Xenial              |
 18.03        | `Bionic (4)` | 9.5        | `Xenial (5)`        |
 18.03        | Bionic       | `9.5 (7)`  | `Bionic (6)`        |
 18.03        | Bionic       | `10 (8)`   | Bionic              |

Upgrade the APP server first:

 * Upgrade Landscape 17.03 to 18.03 in the APP server, still on Ubuntu 16.04 LTS ("xenial"), following the steps outlined in the non-quickstart upgrade section.
 * Configure the release update manager to keep third-party repositories enabled by running this command:
```
echo -e "[Sources]\nAllowThirdParty=yes" | sudo tee /etc/update-manager/release-upgrades.d/allow.cfg
```
 * Upgrade Ubuntu 16.04 LTS ("xenial") to Ubuntu 18.04 LTS ("bionic") using the `do-release-upgrade` tool. First try using the tool as is:
```
sudo do-release-upgrade
```
 * If it tells you that no new releases are available, try adding the `-d` parameter:
```
sudo do-release-upgrade -d
```
!!! Note:
    Pay close attention to its output: it should say that it is starting an upgrade to "bionic".

 * Reboot after the upgrade is done:
```
sudo reboot
```
 * Stop all Landscape services:
```
sudo lsctl stop
```
Now we will upgrade the database server:

 * While still on postgresql 9.5, upgrade the server from Ubuntu 16.04 LTS ("bionic") to Ubuntu 18.04 LTS ("bionic") using the `do-release-upgrade` tool just like before.
 * Install the 10 postgresql packages:
```
sudo apt install postgresql-10 postgresql-plpython-10 postgresql-contrib-10 postgresql-client-10 postgresql-10-debversion
```
!!! Note:
    If you get a warning about `/etc/postgresql-common/createcluster.conf` while configuring `postgresql-common`, select to keep the local version.

 * Drop the newly created 10 cluster:
```
sudo pg_dropcluster 10 main --stop
```
 * Upgrade the 9.5 cluster:
```
sudo pg_upgradecluster 9.5 main
```
 * If the `UPGRADE_SCHEMA` is set to `no` in `/etc/default/landscape-server` run the setup script manually to perform the database schema upgrade:
```
sudo setup-landscape-server
```
 * Start the Landscape services:
```
sudo lsctl start
```
 * Verify that Landscape is working correctly.
 * If you are happy with the upgrade results, the previous 9.5 cluster can be dropped:
```
sudo pg_dropcluster 9.5 main
```

### Release upgrade for juju deployments
Upgrading the Ubuntu release of servers within a juju deployment is not supported at this time.


## Other changes of note

* Landscape will send back anonymous usage data to Canonical to help improve the product. You may opt-out of this behavior globally in the settings page.

* Copying package profiles no longer applies the copied profile to the same set of computers by default -- it applies to no computers instead.

## Known issues

This section describes some relevant known issues that might affect your usage of Landscape 18.03.

* The `landscape-package-search` service ignores the `RUN_*` variable settings in `/etc/default/landscape-server` and will always try to start. To configure it not to start, run this command: `sudo systemctl disable landscape-package-search`. If it was already running, you will also have to stop it: `sudo service landscape-package-search stop`. This is only noticeable using multiple application servers.


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

