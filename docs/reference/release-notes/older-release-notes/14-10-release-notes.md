(reference-release-notes-14-10)=
# 14.10 release notes

## Major changes from previous stable release

 * OpenStack Autopilot Beta
 * Juju integration
 * Throttled package updates
 * New theme
 * API incompatibilities
 * New logging format
 * Demo license
 * Public package repository
 * '''Changes in LDS 14.10.1''':
  * possibility to file a bug with autopilot logs for failed runs
  * increased the MySQL max connection limit to allow for bigger cloud deployments
 * '''Changes in LDS 14.10.2''':
  * parent activity status missing after upgrading from releases older than 14.10 (#1394760)
  * made available for Ubuntu 12.04 LTS ("precise")
 * '''Changes in LDS 14.10.3''':
  * XSS security fix

Read on for details.

## Changes and new features
This section describes the changes and new features in more detail.

## LDS 14.10.1
This is a maintenance point release that only has changes for the !OpenStack Autopilot:

 * should a cloud deployment fail, Landscape will automatically collect the necessary logs and allow the administrator to optionally file a bug about it
 * the connection limit for the MySQL service used by !OpenStack has been raised to allow for bigger cloud deployments

## LDS 14.10.2
This release fixes an issue when upgrading from LDS older than 14.10. The status of parent activities was not correctly migrated to a new format, which resulted in it being missing in the activity pages and API results. It's also the first 14.10 release that is made available for Ubuntu 12.04 LTS ("precise").

## LDS 14.10.3
This release fixes a XSS (cross-site scripting) security issue.

## OpenStack Autopilot Beta
The !OpenStack Autopilot integrates with MAAS and Juju to deploy an !OpenStack cloud. This reference !OpenStack install is Landscape's component of the Canonical Distribution of Ubuntu !OpenStack. 

## Juju integration
As part of the work to create the !OpenStack Autopilot, Landscape now has Juju support. Once a juju environment is registered, Landscape will keep track of the units as they come and go. New units of a service will automatically become registered computers in Landscape, and when units are destroyed, or even full services are removed, the corresponding Landscape computers will also be removed.

## Demo license
Starting with LDS 14.10, a demonstration license for 10 full seats plus 10 virtual machines (including LXC containers) is included with the package.

## Public package repository
LDS 14.10 is also available through a public package repository. To install the repository, run these commands:

```
    sudo add-apt-repository ppa:landscape/14.10
    sudo apt-get update
```

## Throttled updates
Throttled updates allow the administrator to spread out over time package activities on the selected computers so that they don't happen at the same time. This is useful if, for example, there are several containers or virtual machines running on the same host. By randomly spreading the activity over a given amount of time, the load on that host is reduced.
The throttled updates option is available on upgrade profiles and regular package activities.

## Logging
The logging format has changed. The access logs were merged into the regular logs. For example, before we would have `appserver_access-1.log` and `appserver-1.log`. Now the content of both logs have been merged into `appserver-1.log`. Existing log parsing scripts will have to be adapted.

## MAAS provisioning
MAAS provisioning has been changed and is now available only as part of the OpenStack Autopilot. It's no longer possible to provision new computers directly.

## API incompatibilities
Some API incompatibilities are being introduced in this release of LDS:

 * UnknownAccessGroupsError was changed to UnknownAccessGroupError (plural to singular)
 * New field `access_group` in pending computers API call
 * Call to register a new MAAS controller is now RegisterMAASRegionController

## Non-quickstart deployment
For a non-quickstart deployment, where the database is separated from the application server, please go [[LDS/ManualInstallation14.10|here]].

## Upgrading LDS
LDS 14.10.2 supports Ubuntu 12.04 LTS ("precise") and Ubuntu 14.04 LTS ("trusty"). It can only be upgraded to from LDS 13.09.X.

## Large database schema changes
Some database schema changes required by LDS 14.10 might take a while to run depending on how much data you have and how performant the database server is. These changes are prefixed with a "WARNING" that shows up in the terminal during the upgrade.

## Quickstart upgrade
If you used the `landscape-server-quickstart` package to install LDS 13.09.X, then you can use this method to upgrade it.

Select new version of LDS in your hosted account at https://landscape.canonical.com and then run:

```
sudo apt-get update
sudo apt-get dist-upgrade
```

When prompted, reply with `N `to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically.

## Non-quickstart upgrade
Follow these steps to perform a non-quickstart upgrade, that is, you did not use the `landscape-server-quickstart` package when installing LDS 13.09.X:

 * stop all landscape services on all machines that make up your non-quickstart deployment, except the database service
 * on the database server, edit `/etc/postgresql/<version>/main/postgresql.conf` (replace `<version>` with your postgresql version) and set `max_prepared_transactions` to the same value as `max_connections`. Then restart the database services with `sudo postgresql restart`.
 * edit `/etc/landscape/service.conf` on all machines except the database and remove `store_user` and `store_password` from the `[maintenance]` section
 * select the new version of LDS in your hosted account at https://landscape.canonical.com. Alternatively, you can just add the LDS 14.10 PPA directly instead with `sudo add-apt-repository ppa:landscape/14.10`.
 * update the LDS packages via `sudo apt-get update && sudo apt-get dist-upgrade`. '''Important:''' reply with N to any dpkg questions regarding configuration files, so the original file is kept in place.
 * if `UPGRADE_SCHEMA` was disabled in `/etc/default/landscape-server`, services will fail to start after the packages are upgraded. That's normal. Run the schema upgrade command manually now '''on one machine only''':

```
  sudo setup-landscape-server
  sudo lsctl start
```

 * start the landscape services on the remaining machines:

```
  sudo lsctl start
```

## OpenStack Autopilot Beta: Known Issues
 * Aborting a cloud deployment right after the abort button becomes available can fail and leak MAAS nodes. Furthermore, Landscape will probably have failed to clear the deployment from its database, so if a new deployment is attempted with the exact same region and cloud names, it will fail.

