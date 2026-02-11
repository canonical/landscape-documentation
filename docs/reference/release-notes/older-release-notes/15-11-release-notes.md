---
myst:
  html_meta:
    description: "Release notes for Landscape version 15.11 (November 2015). OpenStack Liberty deployment support, Juju upgrade handling improvements, and database connection fixes."
---

(reference-release-notes-15-11)=
# 15.11 release notes

## Highlights

 * --(OpenStack Liberty cloud deployment)-- '''NOTE: in order to use the Autopilot to deploy OpenStack clouds, please use a more recent version of Landscape.'''
 * '''LDS 15.11.3 point release''':
  * This replaces LDS 15.11.2 in the 15.11 PPA
  * Use `--no-auto-upgrade` when bootstrapping to prevent juju from upgrading the tools on its own
  * `get-distributed-lock` now ignores maintenance flag
  * Fix package-search crash when encountering missing computer ids
  * Fix USN script !KeyError when purging package buffers
  * Require juju-core 1.25.3 or higher
  * Fix removal profile page layout
 * '''LDS 15.11.2 point release''':
  * This replaces LDS 15.11.1 in the 15.11 PPA
  * Update OpenStack charm revisions to handle changes in liberty from the UCA
 * '''LDS 15.11.1 point release''':
  * This replaces LDS 15.11 in the 15.11 PPA.
  * Fix for stale idle in transaction connections to the database
  * Configure Juju to not upgrade the agent when deploying a cloud
  * Do not truncate the administrator name in the top right corner so easily

## Changes and new features
This section describes the changes and new features in more detail.

## OpenStack Liberty deployment
--(Autopilot in LDS 15.11 will deploy OpenStack Liberty clouds.)-- Due to https://bugs.launchpad.net/ubuntu/+source/nova/+bug/1559935, please use a newer version of Landscape if you want to use the Autopilot. In particular, version 16.03.1 at the time of this writing is the preferred way to deploy OpenStack Liberty.

## MAAS supported version
Autopilot in LDS 15.11 supports MAAS 1.8.x only.

## Upgrade notes
LDS 15.11 supports Ubuntu 14.04 LTS ("trusty"). It can only be upgraded from LDS 15.10.X or an earlier version in the 15.11 series.

## Quickstart upgrade
If you used the landscape-server-quickstart package to install LDS 15.10.X or an earlier LDS 15.11 then you can use this method to upgrade it.

If you are a https://landscape.canonical.com customer, you can select new version of LDS in your hosted account at https://landscape.canonical.com and then run:

```text
    sudo apt-get update
    sudo apt-get dist-upgrade
```

Alternatively, just add the LDS 15.11 PPA and run the same commands as above:

```text
    sudo add-apt-repository ppa:landscape/15.11
    sudo apt-get update
    sudo apt-get dist-upgrade
```

When prompted, reply with N to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically. 

## Non-quickstart upgrade
Follow these steps to perform a non-quickstart upgrade, that is, you did not use the landscape-server-quickstart package when installing LDS 15.10.X or an earlier LDS 15.11:

 * stop all landscape services on all machines that make up your non-quickstart deployment, except the database service: `sudo lsctl stop`
 * add the LDS 15.11 PPA: `sudo add-apt-repository ppa:landscape/15.11`
 * refresh the apt database and upgrade: `sudo apt-get update && sudo apt-get dist-upgrade`
 * answer with "N" to any dpkg questions about Landscape configuration files
 * if you have `UPGRADE_SCHEMA` enabled in `/etc/default/landscape-server`, then the required schema upgrade will be performed as part of the package upgrade and all services will be running at the end. The upgrade is finished.
 * if `UPGRADE_SCHEMA` is disabled, then you will have failures when the services are restarted at the end of the upgrade. That's expected. You now have to perform the schema upgrade manually with this command: 

```text
    sudo setup-landscape-server
```

  after it succeeds, the Landscape services can be started: 

```text
    sudo lsctl start
```

## Upgrading a Juju deployed LDS

Starting with LDS 15.10, juju deployed LDS can be upgraded in place.  Please follow this procedure:

```text
juju upgrade-charm landscape-server
juju set landscape-server source=ppa:landscape/15.11
juju action do landscape-server/0 pause
juju action do landscape-server/0 upgrade
juju action do landscape-server/0 migrate-schema
juju action do landscape-server/0 resume
```

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

## Known Issues
This section describes important known issues with this release.

## Autopilot Cloud Deployments
Due to a version change in keystone (https://bugs.launchpad.net/ubuntu/+source/nova/+bug/1559935), a component of OpenStack, this release of the Autopilot cannot deploy OpenStack Liberty clouds anymore. Please use a newer version of Landscape if you want to use the Autopilot.

