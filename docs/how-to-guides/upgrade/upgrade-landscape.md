(how-to-upgrade)=
# How to upgrade your Landscape server

This document is for upgrading Landscape Server 23.03 or later to a newer version. If you’re upgrading from a version of Landscape earlier than 23.03, see the manual upgrade guides for a [quickstart installation](https://discourse.ubuntu.com/t/upgrade-a-landscape-19-10-quickstart-installation-to-landscape-23-03/34336) and [manual installation](https://discourse.ubuntu.com/t/upgrade-a-landscape-19-10-manual-installation-to-landscape-23-03/34335).

Note that you don’t need to upgrade your client machines when you upgrade your Landscape server.

## Prepare to upgrade

> See also: {ref}`how-to-backup-and-restore`

We strongly recommend you backup your database and configuration files before performing an upgrade. You should backup:

- **Database**
- **Apache2 configuration file**: This is commonly located in `/etc/apache2/sites-available/<hostname>.conf`.
- **Service configuration file**: This is commonly located in `/etc/landscape/service.conf`.

## Upgrade your Landscape server

```{note}
When you upgrade, you should use your existing configuration file. This file is typically located in `/etc/landscape/service.conf`.
```

To upgrade your existing Landscape server:

1. Add the new PPA. If you’re upgrading to Landscape 24.04 LTS, run:
    
    ```bash
    sudo add-apt-repository ppa:landscape/self-hosted-24.04 -y
    ```
    
2. Update the lists of available packages and dependencies in your local system:
    
    ```bash
    sudo apt update
    ```
    
3. Upgrade the Landscape server using the newly configured PPA:
    
    ```bash
    sudo apt full-upgrade
    ```

During your upgrade, you may be asked if you want to replace your configuration file with a later version. **Do not replace your configuration; you should keep your existing configuration file.** 

If you accidentally replace your configuration file, you can put your previous configuration back by overwriting your `service.conf` file with the one you backed up earlier.

## (If needed) Upgrade the database schema

If you’re not using a quickstart deployment of Landscape, you need to manually update your database schema. You only need to run the database schema updates once, even if your deployment has multiple servers.

For Juju deployments, see {ref}`how-to-heading-upgrade-juju` in this guide. For manual installations of Landscape, follow these steps to manually update your database schema:

1. Stop Landscape
    
    ```bash
    sudo lsctl stop
    ```
    
2. Run the setup command. This performs all necessary schema updates against the currently configured database.
    
    ```bash
    sudo setup-landscape-server
    ```
    
3. Restart Landscape
    
    ```bash
    sudo lsctl restart
    ```
    
(how-to-heading-upgrade-juju)=
## Upgrade Juju deployments

> See also: [Landscape-server charm on Charmhub](https://charmhub.io/landscape-server)

To upgrade a basic Juju deployment:

1. Upgrade the `landscape-server` charm
    
    ```bash
    juju refresh landscape-server
    ```
    
2. Update the Landscape self-hosted PPA configured in Juju. For example, if you’re upgrading to Landscape 24.04 LTS, run:
    
    ```bash
    juju config landscape-server landscape_ppa="ppa:landscape/self-hosted-24.04"
    
    juju ssh landscape-server/0 "sudo add-apt-repository ppa:landscape/self-hosted-24.04 -y"
    ```
    
    If you’re upgrading to a different version of Landscape, use the appropriate PPA.
    
    **Note**: At the moment, the `landscape-server` charm only adds the PPA source during installation, so you will need to manually update this PPA on each of the `landscape-server` units. When the charm is updated, this will no longer be necessary.
    
3. Pause Landscape services on all `landscape-server` units
    
    ```bash
    juju run landscape-server/0 pause
    juju run landscape-server/1 pause
    juju run landscape-server/2 pause
    ...
    juju run landscape-server/n pause
    ```
    
4. Upgrade the Landscape server packages from the updated PPA on all `landscape-server` units
    
    ```bash
    juju run landscape-server/0 upgrade
    juju run landscape-server/1 upgrade
    juju run landscape-server/2 upgrade
    ...
    juju run landscape-server/n upgrade
    ```
    
5. Update the database schema. Run this only once, and on one `landscape-server` unit
    
    ```bash
    juju run landscape-server/0 migrate-schema
    ```
    
6. Re-start the Landscape services again on all `landscape-server` units
    
    ```bash
    juju run landscape-server/0 resume
    juju run landscape-server/1 resume
    juju run landscape-server/2 resume
    ...
    juju run landscape-server/n resume
    ```

## Add additional configurations

Landscape commonly has version-specific configurations that must be added to complete your upgrade.

If you're upgrading to Landscape 24.04 LTS, follow {ref}`how-to-upgrade-to-24-04-lts`.