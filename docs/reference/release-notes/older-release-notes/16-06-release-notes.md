(reference-release-notes-16-06)=
# 16.06 release notes

These are the release notes for Landscape 16.06.

## Highlights
  

 - **Landscape 16.06.1 point release:**
   - [16.07 OpenStack charms]
 - Automatic update of Ubuntu images in the cloud (trusty and xenial)
 - OpenStack Mitaka
 - Ubuntu 16.04 LTS ("xenial") support

## Changes and new features 
This section describes the changes and new features in more detail.

### Ubuntu 16.04 LTS support 
Landscape 16.06 is the first Landscape release to support both Ubuntu 14.04 LTS 
("trusty") and Ubuntu 16.04 LTS ("xenial").

### OpenStack Mitaka 
The Autopilot in Landscape 16.06 will deploy an OpenStack Mitaka cloud using the OpenStack charms.

### Automatic cloud image refresh 
The OpenStack Mitaka cloud deployed by the Autopilot includes two amd64 images 
by default: Ubuntu 14.04 LTS ("trusty") and Ubuntu 16.04 LTS ("xenial"). These 
images will be refreshed daily, so if new releases are available, they will be 
downloaded and made available in OpenStack's Glance.

## Upgrade notes 
Landscape 16.06 supports Ubuntu 16.04 LTS ("xenial") and Ubuntu 14.04 LTS 
("trusty"). It can only be upgraded from Landscape 16.03.

You can upgrade a Landscape 16.03 running on Ubuntu 14.04 LTS ("trusty") all the 
way up to Landscape 16.06 running on Ubuntu 16.04 LTS ("xenial").

### Quickstart upgrade 
If you used the landscape-server-quickstart package to install Landscape 16.03 
then you can use this method to upgrade it.

If you are a https://landscape.canonical.com customer, you can select new 
version of Landscape in your hosted account at https://landscape.canonical.com 
and then run:

```bash
    sudo apt-get update
    sudo apt-get dist-upgrade
```


Alternatively, just add the Landscape 16.06 PPA and run the same commands as 
above:

```bash
    sudo add-apt-repository ppa:landscape/16.06
    sudo apt-get update
    sudo apt-get dist-upgrade
```


When prompted, reply with `N` to any dpkg questions about configuration files so 
the existing files stay untouched. The quickstart package will make any needed 
modifications to your configuration files automatically. 

### Non-quickstart upgrade

Follow these steps to perform a non-quickstart upgrade, that is, you did not use 
the landscape-server-quickstart package when installing Landscape 16.03:

 - stop all landscape services on all machines that make up your non-quickstart 
   deployment, except the database service: `sudo lsctl stop`
 - add the Landscape 16.06 PPA: `sudo add-apt-repository ppa:landscape/16.06`
 - refresh the apt database and upgrade: 
   `sudo apt-get update && sudo apt-get dist-upgrade`
 - answer with `N` to any dpkg questions about Landscape configuration files
 - if you have `UPGRADE_SCHEMA` enabled in `/etc/default/landscape-server`, then 
   the required schema upgrade will be performed as part of the package upgrade and 
   all services will be running at the end. The upgrade is finished.
 - if `UPGRADE_SCHEMA` is disabled, then you will have failures when the 
   services are restarted at the end of the upgrade. That's expected. You now have 
   to perform the schema upgrade manually with this command: 

```bash
sudo setup-landscape-server
```


After all these steps are completed, the Landscape services can be started: 

```bash
sudo lsctl start
```

### Charm upgrade 


Starting with Landscape 15.10, Juju deployed Landscape can be upgraded in place. 

If you have just one landscape server unit, please follow this procedure:

```bash
juju upgrade-charm landscape-server
juju set landscape-server source=ppa:landscape/16.06
juju action do landscape-server/0 pause
juju action do landscape-server/0 upgrade
juju action do landscape-server/0 migrate-schema
juju action do landscape-server/0 resume
```


For multiple landscape-server units, you should pause all of them, upgrade one 
by one, run the migrate-schema command on only one, and then resume all units.

Each action returns an identifier that should be used to check its outcome with 
the fetch command before running the next action:

```bash
juju action fetch <uuid>
```


For example:

```bash
$ juju action do landscape-server/0 pause
Action queued with id: 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
$ juju action fetch 72fd7975-3e0b-4b6d-84b9-dbd76d50f6af
status: completed
timing:
  completed: 2015-06-23 19:24:39 +0000 UTC
  enqueued: 2015-06-23 19:24:32 +0000 UTC
  started: 2015-06-23 19:24:33 +0000 UTC
```


As an example of when it fails, here we are trying to upgrade a unit that hasn't 
been paused before:

```bash
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


Also, you may want to keep this open in another window, to get an idea of when 
the system goes back to idle between each step:

```bash
juju status --format=tabular
# or
watch juju status --format=tabular
```


### Ubuntu release upgrade 

You can take advantage of the fact that Landscape 16.06 supports both Ubuntu 
14.04 LTS ("trusty") and Ubuntu 16.04 LTS ("xenial") and upgrade your Landscape 
deployment from "trusty" to "xenial". This section details the upgrade procedure 
depending on how you deployed Landscape.

#### Release upgrade for quickstart deployments 
Follow these steps in order:

 * Upgrade Landscape 16.03 to 16.06 while still on Ubuntu 14.04 LTS ("trusty") 

using the quickstart upgrade method.

 * Configure the release update manager to keep third-party repositories enabled 

by running this command:

```bash
echo -e "[Sources]\nAllowThirdParty=yes" | sudo tee 
/etc/update-manager/release-upgrades.d/allow.cfg
```


 * Upgrade Ubuntu 14.04 LTS ("trusty") to Ubuntu 16.04 LTS ("xenial") using the 

`do-release-upgrade` tool. First try using the tool as is:

```bash
sudo do-release-upgrade
```


If it tells you that no new releases are available, try adding the `-d` 
parameter:

```bash
sudo do-release-upgrade -d
```


Pay close attention to its output: it should say that it is starting an upgrade 
to "xenial". Reboot after the upgrade is done.

 * Stop all Landscape services:

```bash
sudo lsctl stop
```


 * Install the 9.5 postgresql packages:

```bash
sudo apt install postgresql-9.5 postgresql-plpython-9.5 postgresql-contrib-9.5 
postgresql-client-9.5 postgresql-9.5-debversion
```


If you get a warning about `/etc/postgresql-common/createcluster.conf` while 
configuring `postgresql-common`, select to keep the local version.

 * Drop the newly created 9.5 cluster:

```bash
sudo pg_dropcluster 9.5 main --stop
```


 * Upgrade the 9.3 cluster:

```bash
sudo pg_upgradecluster 9.3 main
```


 * Start Landscape services:

```bash
sudo lsctl start
```


 * Verify that Landscape is working correctly.
 * If you are happy with the upgrade results, the previous 9.3 cluster can be 

dropped:

```bash
sudo pg_dropcluster 9.3 main
```

#### Release upgrade for manual (non-quickstart) deployments 


The release upgrade process for the manual non-quickstart deployment is a bit 
more complicated and needs to be done in steps.

Upgrade the APP server first:

 - Upgrade Landscape 16.03 to 16.06 in the APP server, still on Ubuntu 14.04 LTS ("trusty"), 

 following the steps outlined in the non-quickstart upgrade section.

 - Configure the release update manager to keep third-party repositories enabled by running this command:  

```bash
echo -e "[Sources]\nAllowThirdParty=yes" | sudo tee 
/etc/update-manager/release-upgrades.d/allow.cfg
```


 - Upgrade Ubuntu 14.04 LTS ("trusty") to Ubuntu 16.04 LTS ("xenial") using the 

`do-release-upgrade` tool. First try using the tool as is:

```bash
sudo do-release-upgrade
```


  - If you get a message that no new releases are available, try adding the `-d` parameter:

```bash
sudo do-release-upgrade -d
```


  Pay close attention to its output: it should say that it is starting an upgrade 
  to "xenial". Reboot after the upgrade is done.
  - Verify that Landscape is still operating normally.
  - Stop all Landscape services:

```bash
sudo lsctl stop
```


Now we will upgrade the database server:

 - While still on postgresql 9.3, upgrade the server from Ubuntu 14.04 LTS 
  ("trusty") to Ubuntu 16.04 LTS ("xenial") using the `do-release-upgrade` tool 
  just like before.
 - Install the 9.5 postgresql packages:

```bash
sudo apt install postgresql-9.5 postgresql-plpython-9.5 postgresql-contrib-9.5  
postgresql-client-9.5 postgresql-9.5-debversion
```


  If you get a warning about `/etc/postgresql-common/createcluster.conf` while 
  configuring `postgresql-common`, select to keep the local version.
 -  Drop the newly created 9.5 cluster:

```bash
sudo pg_dropcluster 9.5 main --stop
```


 - Upgrade the 9.3 cluster:

```bash
sudo pg_upgradecluster 9.3 main
```


 - Start the Landscape services:

```bash
sudo lsctl start
```


 - Verify that Landscape is working correctly.
 - If you are happy with the upgrade results, the previous 9.3 cluster can be dropped:

```bash
sudo pg_dropcluster 9.3 main
```


### Release upgrade for Juju deployments

Upgrading the Ubuntu release of servers within a Juju deployment is not 
supported at this time.

## Other changes of note 

### Storage devices referenced by IDs
OpenStack Autopilot deployments will use disk IDs when referencing block devices 
for storage charms. This requires virtual machines to be configured to supply 
these IDs.

If using libvirt (or virt-manager) with KVM, for example, a simple way to 
accomplish this is to add a serial number to each disk:

![]kvm-disk-serial.png

Other virtualization technologies have similar concepts. Sometimes it's called a 
"disk UUID". Please consult the corresponding documentation.


### Known issues
This section describes some relevant known issues that might affect your usage 
of Landscape 16.06.

#### Upgrading Landscape with existing clouds
Clouds deployed with a previous version of Landscape will remain working after 
Landscape is upgraded to 16.06, but add-hardware cannot be used until the cloud 
is redeployed with the upgraded Landscape.

#### package-search disabled after upgrade to xenial 
If Landscape 16.06 on trusty is upgraded to xenial, the 
`landscape-package-search` service will be left disabled due to a 
bug in the transitioning 
from upstart to systemd. As a result, if the host where this service lives is 
rebooted, the service will not start on its own.

To fix this, please run this command:

```bash
    sudo systemctl enable landscape-package-search
```

And start the service up manually one last time:

```bash
    sudo service landscape-package-search start
```

#### Ceph as object autopilot failures 

When Ceph is used as object storage (ceph-radosgw), sometimes a bug can be hit 
where the radosgw service won't be running. This will 
usually manifest itself in the Autopilot as a "Wait for SimpleStreams to sync an 
image" activity that stays "In progress" forever.

The workaround is to abort the deployment and try again.


#### Swift storage accounting incomplete in the Autopilot OpenStack dashboard 
When Swift is used for storage, it's possible that the amount of storage 
reported in the Autopilot OpenStack dashboard graphs is less than the amount 
available.

This is being tracked as 
an internal bug and 
the workaround is to restart landscape-client on all swift-storage units.

Here are some examples on how to do that depending on how Landscape itself was 
deployed:

##### Juju deployed Landscape 

 * First, get to the landscape-server/0 unit inside the proper environment. Run 

this from wherever you deployed the Landscape bundle  (this is one long line):

```bash
juju ssh landscape-server/0 sudo 'JUJU_HOME=/var/lib/landscape/juju-homes/`sudo 
ls -rt /var/lib/landscape/juju-homes/ | tail -1` sudo -u landscape -E bash'
```


 * Once there, you will have access to the OpenStack environment. Now it's just 

a matter of issuing the restart command to all swift-storage units:

```bash
juju run --service swift-storage 'sudo service landscape-client restart'
```

#### Quickstart and Manual (non-quickstart) 


 * First you have to ssh into the Landscape server. Something like this:

```bash
ssh ubuntu@<server-ip>
```

 * Now enter the landscape user in the right juju environment (this is one long 

line):

```bash
sudo JUJU_HOME=/var/lib/landscape/juju-homes/`sudo ls -rt 
/var/lib/landscape/juju-homes/ | tail -1` sudo -u landscape -E bash
```


 * And now restart the client service in all swift-storage units:

```bash
juju run --service swift-storage 'sudo service landscape-client restart'
```

