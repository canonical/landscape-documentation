(reference-release-notes-17-03)=
# 17.03 release notes

Title: Landscape Release Notes 17.03
## Landscape Release 17.03
These are the release notes for Landscape 17.03.

## Highlights

 * Autopilot
 * Nova-LXD
 * Ubuntu Xenial
 * 17.02 OpenStack charms
 * MAAS 2.1 support
 * Juju 2.1 support
 * OpenStack Ocata
 * Landscape Release 17.03.4 with bug fixes and changes
 * Variable delay to USN refresh to avoid timeouts.
 * Landscape Release 17.03.3 with bug fixes and changes
 * Adding suite in Release file for mirrors to allow using landscape-managed mirrors in netinstall.
 * Retrying after errors during computer removal to handle database reconnections.
 * Landscape Release 17.03.2 with repository management bug fixes and changes.
 * ValueError when handling reprepro error. When storing the repository management files in an NFS mount, the gpg-agent process that is spawned indirectly by reprepro will hold a file descriptor open on an deleted file, triggering the [NFS silly rename](http://nfs.sourceforge.net/#faq_d2) behavior. Landscape will fail to remove this special file and the repository operation will be interrupted. As soon as the gpg-agent process dies, the file will be removed on its own, that's why the operation ends up working if tried multiple times. The fix for this bug is to just ignore that particular failure.
 * Create/derive-series does not inherit udeb setting. Add a include-udeb option to create-series so that the optional pockets that can be created with this API call can also include udebs if so desired. Additionally, derive-series was fixed to honor the udeb setting from the parent series on the new derived series.
 * Edit-pocket should have option to toggle udeb support. To help with systems that have derived series already created and without udebs, the edit-pocket API call also received a new `unclude-udeb` option to allow changing this setting on already existing pockets. 
 * To use the new udeb related parameters in the landscape API, please also upgrade the `landscape-api` package to version 17.03.2. If you use the raw API, then just adjust your code for the new optional parameters if you intend to use them.
 * Important new known issue that can affect how long the `landscape-server` takes to upgrade: please read the Known Issues section at the end of this document.
 * There are no special upgrade instructions for Landscape 17.03.2, regardless of the installation method.

## Changes and new features

This section describes the changes and new features in more detail.

### Nova LXD (On-prem)

The OpenStack Autopilot now allows the deployment of [nova-lxd](https://github.com/OpenStack/nova-lxd), bringing system containers to OpenStack using nova-lxd. With this feature, it's possible to pick a percentage of cores to deploy with KVM and LXD hypervisors across your compute servers.  LXD needs different images from KVM, but most workloads will operate transparently on this hypervisor choice that allows significantly denser deployments than KVM.

### OpenStack Ocata, 17.02 OpenStack Charms (On-prem)

The Autopilot in Landscape 17.03 will deploy an [OpenStack Ocata](https://releases.OpenStack.org/ocata) cloud using the [17.02 OpenStack charms](http://docs.OpenStack.org/developer/charm-guide/1702.html).

### MAAS 2.1 (On-prem)

[MAAS](https://maas.io) support is now exclusive to version 2.1.3 and newer.  This is the default version of MAAS in Ubuntu 16.04.  MAAS is the way the OpenStack Autopilot provisions machines, and needs to be setup fully before using it with Landscape.

When specifying MAAS nodes via the Landscape API to deploy a cloud, use only the first part of the name (i.e. 'my-node' instead of 'my-node.maas').

### Juju 2.1 (On-prem)

Juju support is now exclusive to version 2.1 and newer.  Juju is installed automatically as a dependency of landscape, and should be transparent to you as an operator.  For more advanced debugging and maintenance of your cloud, some commands have changed.

As a result of the exclusive support for Juju 2.1, registered Juju 1 environments are no longer supported. When upgrading to Landscape 17.03, remove any registered Juju 1 environments with:

```
landscape-api get-juju-environments
landscape-api remove-juju-environment <environment_name>
```

It's also recommended to destroy and re-deploy your cloud if you want to continue to use the management features of the OpenStack Autopilot.

### Portable URLs - SAAS

It is now possible to share Landscape URLs to other people without knowing their account name.

e.g. URLs like `https://landscape.acme.com/~/how-to-register` will translate to `https://landscape.acme.com/account/MY-ACCOUNT/how-to-register`

This also makes it possible to have static documentation which is portable across many Landscape users.

## Upgrade notes

Landscape 17.03 supports Ubuntu 16.04 LTS ("xenial"). It can only be upgraded from Landscape 16.06 also running on the same Ubuntu 16.04 LTS release.

To upgrade a Landscape 16.06 running on Ubuntu 14.04 LTS ("trusty") to Landscape 17.03, first you need to upgrade your Ubuntu release to 16.04 LTS ("xenial"), and then upgrade Landscape to 17.03.

## Quickstart upgrade
If you used the landscape-server-quickstart package to install Landscape 16.06 then you can use this method to upgrade it.

If you are a [Landscape](https://landscape.canonical.com) customer, you can select new version of Landscape in your hosted account at [https://landscape.canonical.com](https://landscape.canonical.com) and then run:
```
sudo apt-get update
sudo apt-get dist-upgrade
```
Alternatively, just add the Landscape 17.03 PPA and run the same commands as above:
```
sudo add-apt-repository -u ppa:landscape/17.03
sudo apt-get dist-upgrade
```
When prompted, reply with `N` to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically.

## Non-quickstart upgrade

Follow these steps to perform a non-quickstart upgrade, that is, you did not use the landscape-server-quickstart package when installing Landscape 16.06:

 * stop all landscape services on all machines that make up your non-quickstart deployment, except the database service:
 ```
 sudo lsctl stop
 ```
 * double check that `UPGRADE_SCHEMA` is set to what you want in `/etc/default/landscape-server`
 * disable all the landscape-server cron jobs from `/etc/cron.d/landscape-server` in all app servers
 * Update the Landscape apache vhost as follows:
  * Add a `Location </static>` definition to both the HTTP and HTTPS vhosts like this:
```
  <Location "/static">
    Header always append X-Frame-Options SAMEORIGIN
  </Location>
```
  * Add the following SSL directives to the HTTPS vhost:
```
# Disable to avoid POODLE attack
  SSLProtocol all -SSLv3 -SSLv2
  SSLHonorCipherOrder On
  SSLCompression Off
  # Disable old/vulnerable ciphers. Note: one very long line
  SSLCipherSuite EECDH+AESGCM+AES128:EDH+AESGCM+AES128:EECDH+AES128:EDH+AES128:ECDH+AESGCM+AES128:aRSA+AESGCM+AES128:ECDH+AES128:DH+AES128:aRSA+AES128:EECDH+AESGCM:EDH+AESGCM:EECDH:EDH:ECDH+AESGCM:aRSA+AESGCM:ECDH:DH:aRSA:HIGH:!MEDIUM:!aNULL:!NULL:!LOW:!3DES:!DSS:!EXP:!PSK:!SRP:!CAMELLIA:!DHE-RSA-AES128-SHA:!DHE-RSA-AES256-SHA:!aECDH
```
  * Update the existing `RewriteCond` regular expressions in the HTTP vhost like shown in this diff:
```
-    RewriteCond %{REQUEST_URI} !/server-status
-    RewriteCond %{REQUEST_URI} !/icons
-    RewriteCond %{REQUEST_URI} !/static
-    RewriteCond %{REQUEST_URI} !/offline
-    RewriteCond %{REQUEST_URI} !/repository
-    RewriteCond %{REQUEST_URI} !/message-system
+    RewriteCond %{REQUEST_URI} !^/server-status
+    RewriteCond %{REQUEST_URI} !^/icons
+    RewriteCond %{REQUEST_URI} !^/static/
+    RewriteCond %{REQUEST_URI} !^/offline/
+    RewriteCond %{REQUEST_URI} !^/repository/
+    RewriteCond %{REQUEST_URI} !^/message-system
```
  * Remove the `[L]` flag from the first `RewriteRule` in the HTTP vhost like shown in this diff:
```
-    RewriteRule ^/r/([^/]+)/(.*) /$2 [L]
+    RewriteRule ^/r/([^/]+)/(.*) /$2
```
  * Update the existing `RewriteCond` regular expressions in the HTTPS vhost like shown in this diff:
```
-    RewriteCond %{REQUEST_URI} !/robots.txt
-    RewriteCond %{REQUEST_URI} !/favicon.ico
-    RewriteCond %{REQUEST_URI} !/offline
-    RewriteCond %{REQUEST_URI} !/static
+    RewriteCond %{REQUEST_URI} !^/robots.txt$
+    RewriteCond %{REQUEST_URI} !^/favicon.ico$
+    RewriteCond %{REQUEST_URI} !^/offline/
+    RewriteCond %{REQUEST_URI} !^/(r/[^/]+/)?static/
     RewriteCond %{REQUEST_URI} !^/config/
-    RewriteCond %{REQUEST_URI} !/hash-id-databases
+    RewriteCond %{REQUEST_URI} !^/hash-id-databases/
```
 * Restart apache using
```
sudo service apache2 restart
```
 * add the Landscape 17.03 PPA:
```
sudo add-apt-repository -u ppa:landscape/17.03
```
 * update and upgrade:
```
sudo apt-get update && apt-get dist-upgrade
```
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

## Charm upgrade

Starting with Landscape 15.10, juju deployed Landscape can be upgraded
in place.  If you have just one landscape server unit, please follow
this procedure:

```
# Juju 1.x:
juju upgrade-charm landscape-server
juju set landscape-server source=ppa:landscape/17.03
juju action do landscape-server/0 pause
juju action do landscape-server/0 upgrade
juju action do landscape-server/0 migrate-schema
juju action do landscape-server/0 resume

# Juju 2.x:
juju upgrade-charm landscape-server
juju config landscape-server source=ppa:landscape/17.03
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
  completed: 2016-06-23 19:24:39 +0000 UTC
  enqueued: 2016-06-23 19:24:32 +0000 UTC
  started: 2016-06-23 19:24:33 +0000 UTC

# Juju 2.x:
$ juju run-action landscape-server/0 pause
Action queued with id: 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
$ juju show-action-output --wait 0 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
status: completed
timing:
  completed: 2017-03-24 04:27:57 +0000 UTC
  enqueued: 2017-03-24 04:27:46 +0000 UTC
  started: 2017-03-24 04:27:47 +0000 UTC
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
  completed: 2016-06-23 19:26:40 +0000 UTC
  enqueued: 2016-06-23 19:26:36 +0000 UTC
  started: 2016-06-23 19:26:38 +0000 UTC
```


## Other changes of note

 * Landscape will send back anonymous usage data to Canonical to help
 improve the product. You may opt-out of this behavior globally in the
 settings page.
 * Copying package profiles no longer applies the copied profile to the
 same set of computers by default -- it applies to no computers instead.
 * The minimum recommended machine specs for an OpenStack node is:
    * 64G of Ram
    * 4 cores
    * no less than 8G of memory per core
    * 100G of root disk storage
    * 100G of secondary disk storage
    * 10 physical systems is enough for a staging/demonstration cloud.  For production clouds, you will need to [purchase more seats](https://buy.ubuntu.com). Canonical recommends a starting cloud size of 15 physical systems.

## Known issues

This section describes some relevant known issues that might affect your usage of Landscape 17.03.

 * When launching new instances using Horizon's UI, un-check the "create a new volume" during instance creation to avoid a timeout error reported in the UI.
 * Deployed clouds will get nagios alerts on conntrack checks not working.
 * Deployed clouds will get nagios alerts on metering.sample rabbit queue size.
 * There are known memory leaks in juju 2.1.2 (used to deploy the cloud) and it may eventually fail to gracefully recover.  "Add Hardware" and other OpenStack administration tasks may fail.  Standard recovery options (restarting juju daemons) should be used in the event this happens.
 * Juju 2.1.2 can sometimes take a while to release nodes gracefully.  Currently landscape gives a 2 minute timeout for this graceful termination before the nodes are directly released in MAAS.
 * The `landscape-package-search` service ignores the `RUN_*` variable settings in `/etc/default/landscape-server` and will always try to start. To configure it not to start, run this command: `sudo systemctl disable landscape-package-search`. If it was already running, you will also have to stop it: `sudo service landscape-package-search stop`. This is only noticeable using multiple application servers.
 * To upgrade to 17.03 from 16.06, you must first `do-release-upgrade` to xenial.
 * Juju does not support Ubuntu release upgrades currently. To upgrade from 16.06 to 17.03 there you must tear down and redeploy, migrating data where necessary/desired.
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
 * Also due to the `chown` command run during postinst explained above, the upgrade can take a long time if the repository files are mounted somewhere `/var/lib/landscape`, depending on the size of the repository. On an experiment with two machines on the same gigabit switch and a 150Gb repository mounted via NFS, a test upgrade spent about 30min just in that `chown` command. While that happens, the service is down. This is being tracked as an internal bug and until a fix is explicitly mentioned in the release notes, we suggest the same workaround as for the previous case: mount the repository outside of the `/var/lib/landscape/` tree.

## In 17.03.2 only
 * The API documentation was not re-generated for this build. This means that the new `include_udeb` options are not documented in the included API docs visible on the server under the `static/doc/api/repositories.html` URL path component. The help output of the updated landscape-api 17.03.2 package, however, has the updated documentation and can be used as a reference in the meantime. Additionally, as soon as [landscape.canonical.com](https://landscape.canonical.com) gets the same code updates, the API documentation available on that site will also contain the updated API call description.

