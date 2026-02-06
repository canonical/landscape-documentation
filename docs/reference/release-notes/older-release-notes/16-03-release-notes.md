(reference-release-notes-16-03)=
# 16.03 release notes

## Highlights

 * Machine roles
 * Nagios
 * New charms
 * New alert type: duplicate computers
 * OPL 16.03.1 point release:
   * fix for performance regression in the account page
   * Autopilot only: updated Keystone charm can handle upcoming OpenStack Stable Release Update for Ubuntu 16.04 LTS ("trusty")

## Changes and new features

## Autopilot: Machine roles

You can now select from 4 roles for machines through the autopilot - Storage, Compute, Control, Network.  This gives you the control of where services are placed, which machines use the public network and a host of other options.  Of course you can always skip this step and let the autopilot choose for you.  Access this feature after choosing the components for your cloud.

## Autopilot: Nagios

The autopilot will now allow Nagios integration at cloud deployment time.  Each charm in OpenStack ships with sensible monitoring thresholds already enabled as defaults. You may choose to let the autopilot deploy a new Nagios server or use an existing one in your infrastructure.

## Autopilot: New charms

16.01 Charm Changes have been incorporated, giving you the latest performance improvements and bug fixes for your newly deployed OpenStack clouds.

## New alert
There is a new alert type that triggers when more than one computer has the same hostname.

## Upgrade notes
OPL 16.03 supports Ubuntu 14.04 LTS ("trusty"). It can only be upgraded from OPL 15.11. Ubuntu 16.04 LTS ("xenial") is NOT supported by OPL 16.03.


## Quickstart upgrade
If you used the landscape-server-quickstart package to install OPL 15.11 then you can use this method to upgrade it.

If you are a https://landscape.canonical.com customer, you can select new version of OPL in your hosted account at https://landscape.canonical.com and then run:

```text
    sudo apt-get update
    sudo apt-get dist-upgrade
```

Alternatively, just add the OPL 16.03 PPA and run the same commands as above:

```text
    sudo add-apt-repository ppa:landscape/16.03
    sudo apt-get update
    sudo apt-get dist-upgrade
```

When prompted, reply with `N` to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically. 

## Non-quickstart upgrade
Follow these steps to perform a non-quickstart upgrade, that is, you did not use the landscape-server-quickstart package when installing OPL 15.11:

 * stop all landscape services on all machines that make up your non-quickstart deployment, except the database service: `sudo lsctl stop`
 * add the OPL 16.03 PPA: `sudo add-apt-repository ppa:landscape/16.03`
 * refresh the apt database and upgrade: `sudo apt-get update && sudo apt-get dist-upgrade`
 * answer with `N` to any dpkg questions about Landscape configuration files
 * if you have `UPGRADE_SCHEMA` enabled in `/etc/default/landscape-server`, then the required schema upgrade will be performed as part of the package upgrade and all services will be running at the end. The upgrade is finished.
 * if `UPGRADE_SCHEMA` is disabled, then you will have failures when the services are restarted at the end of the upgrade. That's expected. You now have to perform the schema upgrade manually with this command: 

```text
    sudo setup-landscape-server
```

 * Modify one of the `RewriteCond` lines in `/etc/apache2/sites-available/landscape.conf`. You should see a single line which reads:

```text
    RewriteCond %{REQUEST_URI} !/config
```

  it must be changed to:

```text
    RewriteCond %{REQUEST_URI} !^/config/
```

  After all these steps are completed, the Landscape services can be started: 

```text
    sudo lsctl start
```

## Charm upgrade

Starting with OPL 15.10, juju deployed OPL can be upgraded in place.  If you have just one landscape server unit, please follow this procedure:

```text
juju upgrade-charm landscape-server
juju set landscape-server source=ppa:landscape/16.03
juju action do landscape-server/0 pause
juju action do landscape-server/0 upgrade
juju action do landscape-server/0 migrate-schema
juju action do landscape-server/0 resume
```

For multiple landscape-server units, you should pause all of them, upgrade one by one, run the migrate-schema command on only one, and then resume all units.

Each action returns an identifier that should be used to check its outcome with the fetch command before running the next action:

```text
juju action fetch <uuid>
```

For example:

```text
$ juju action do landscape-server/0 pause
Action queued with id: 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
$ juju action fetch 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
status: completed
timing:
  completed: 2015-06-23 19:24:39 +0000 UTC
  enqueued: 2015-06-23 19:24:32 +0000 UTC
  started: 2015-06-23 19:24:33 +0000 UTC
```

As an example of when it fails, here we are trying to upgrade a unit that hasn't been paused before:

```text
$ juju action do landscape-server/0 upgrade
Action queued with id: f3d2343c-33e4-4faf-8c4e-59f796124dd4
$ juju action fetch f3d2343c-33e4-4faf-8c4e-59f796124dd4
message: This action can only be called on a unit in paused state.
status: failed
timing:
  completed: 2015-06-23 19:26:40 +0000 UTC
  enqueued: 2015-06-23 19:26:36 +0000 UTC
  started: 2015-06-23 19:26:38 +0000 UTC
```

## Other changes of note

 * Repository management now works if your OPL installation is behind a proxy.
 * OPL will send back usage data to Canonical to help improve the product.  You may opt-out of this behavior globally in the settings page or by setting the "do-not-track" browser flag. 

## Known issues

### Upgrading OPL with existing clouds

Clouds deployed with a previous version of Landscape will not be correctly handled by Landscape 16.03. In particular:
 * Ceph storage graph will stop working
 * The add-hardware operation will fail, and possibly allocate a resource in your MAAS controller without releasing it.

### Repository management "weak digest"
Starting with Ubuntu 16.04 LTS ("xenial"), apt will complain when a repository was signed using a "weak digest". The error or warning is similar to this:

```text
W: http://<server>/path/foo/Release.gpg: Signature by key <somekey> uses weak digest algorithm (SHA1)
```

Repositories created by Landscape 16.03 and earlier will exhibit this behavior. To fix this without upgrading to Landscape 16.05, follow these steps on the Landscape server machine, as root:

 * obtain the `repository-path` value:

```text
# grep repository /etc/landscape/service.conf 
repository-path # /var/lib/landscape/landscape-repository
```

 * update the `gpg` configuration file, using the directory above:

```text
cd /var/lib/landscape/landscape-repository/standalone
echo "personal-digest-preferences SHA512 SHA384 SHA256 SHA224" > .gnupg/gpg.conf
chown landscape:landscape .gnupg/gpg.conf
```

 * Regenerate the index files for a distribution:

```text
cd /var/lib/landscape/landscape-repository/standalone/<distribution>
reprepro export
```

Repeat the above for each distribution that you have created via the Landscape repository management API.

