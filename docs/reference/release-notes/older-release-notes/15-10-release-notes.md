(reference-release-notes-older-release-notes-15-10-release-notes)=
# 15.10 release notes

## Highlights
 * Autopilot only supported on MAAS 1.8.X only
 * New charm to deploy Landscape
 * Juju deployed Landscape can be upgraded to future versions
 * HA (High Availability) cloud deployment
 * OpenStack Kilo cloud deployment
 * Add hardware to existing cloud

Read on for details.

## Changes and new features
This section describes the changes and new features in more detail.

## Machine requirement for Autopilot
In addition to one machine for MAAS and another one for LDS, an Autopilot cloud deployment requires:
 * non-HA cloud: 3 machines
 * HA cloud: 6 machines

## MAAS version
The OpenStack Autopilot component of LDS now requires MAAS base version 1.8. It won't complain version 1.7 is registered, but this configuration is no longer supported.

## New charm for LDS
When deployed with juju, LDS requires a newer version of the charm. Previous deployments cannot be upgraded to the new charm, nor can LDS in those deployments be upgraded.

This new charm, however, allows LDS to be upgraded to future versions.

## High Availability cloud deployment
Starting with LDS 15.10, OpenStack deployments can be made highly available if enough nodes are used. Autopilot will show the requirements depending on the services chosen.

## OpenStack Kilo deployment
Autopilot in LDS 15.10 will deploy OpenStack Kilo clouds.

## Adding hardware to an existing cloud
Starting with LDS 15.10, Autopilot can add more nodes to a cloud after it is deployed. This is a beta feature, and it only works with clouds that were deployed with LDS 15.10 or later.

## Upgrade notes
LDS 15.10 supports Ubuntu 14.04 LTS ("trusty"). It can only be upgraded from LDS 15.01.X.

## Quickstart upgrade
If you used the landscape-server-quickstart package to install LDS 15.01.X then you can use this method to upgrade it.

If you are a https://landscape.canonical.com customer, you can select new version of LDS in your hosted account at https://landscape.canonical.com and then run:
```text
    sudo apt-get update
    sudo apt-get dist-upgrade
```
Alternatively, just add the LDS 15.10 PPA and run the same commands as above:
```text
    sudo add-apt-repository ppa:landscape/15.10
    sudo apt-get update
    sudo apt-get dist-upgrade
```
When prompted, reply with N to any dpkg questions about configuration files so the existing files stay untouched. The quickstart package will make any needed modifications to your configuration files automatically. 

## Non-quickstart upgrade
Follow these steps to perform a non-quickstart upgrade, that is, you did not use the landscape-server-quickstart package when installing LDS 15.01:
 * stop all landscape services on all machines that make up your non-quickstart deployment, except the database service: `sudo lsctl stop`
 * edit the apache2 vhost file for landscape, usually `/etc/apache2/sites-enabled/landscape.conf` and change the `RewriteRule` lines for combo loader:
  ||from:||`RewriteRule ^/combo http://localhost:9070/ [P,L]`||
  ||to:  ||`RewriteRule ^/combo(.*) http://localhost:8080/combo$1 [P,L]`||
 * restart apache2: `sudo service apache2 restart`
 * add the LDS 15.10 PPA: `sudo add-apt-repository ppa:landscape/15.10`
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

## Charm upgrade
Upgrading of a juju-deployed LDS 15.01 is not yet directly supported. Please follow the non-quickstart upgrade steps.

## OpenStack Autopilot Beta issues
Here are some of the known issues with this release of OpenStack Autopilot in LDS 15.10.

## Add hardware cancellation
It is not yet possible to cancel an add hardware operation.

## Add hardware with older clouds
You can only add hardware to clouds deployed with LDS 15.10 to begin with. Attempts to do it with a cloud that was deployed with an older version of LDS will fail.

