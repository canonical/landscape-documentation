(how-to-install-airgapped)=
# How to install Landscape in an air-gapped or offline environment

This guide provides a high-level overview of how to install Landscape in an offline environment. These instructions can be used for air-gapped deployments.

Note that this guide only covers how to install Landscape in the offline environment and some basic set-up. This guide doesn’t cover setting up repository management. For details on setting up repository management in an air-gapped environment, see {ref}`how-to-manage-repos-airgapped`.

## Overview

The process of installing Landscape in an offline or air-gapped environment is relatively straightforward—you need to download all the relevant packages from an online machine (outside your environment) and transfer those packages into the offline environment.

You won’t need the online machine anymore after you’ve downloaded the packages, so the online machine can be ephemeral.

## Install Landscape Server

```{note}
This example uses {ref}`reference-release-notes-24-04-lts` and the {ref}`how-to-quickstart-installation` package.
```

### Add the Landscape Server PPA

On an online machine with network access, you need to add the Landscape Server PPA. To add the Landscape Server 24.04 LTS PPA, run:

```bash
sudo add-apt-repository -y ppa:landscape/self-hosted-24.04
```

### Download the Landscape Server packages

Run the following commands to update the list of packages, clear the downloaded package cache from APT, and download all the packages required for Landscape Server (Quickstart):

```bash
sudo apt update
sudo apt clean
sudo apt --download-only -y install landscape-server-quickstart
```

All of the necessary packages for Landscape Server should now be downloaded to the APT cache directory: `/var/cache/apt/archives`.

### Install Landscape Server in the offline environment

Copy the downloaded `.deb` packages, carry them into the offline or air-gapped environment, and manually transfer and install them onto your machine with `dpkg`. You can install the packages with a command similar to:

```bash
sudo dpkg -i /PATH/TO/PACKAGES/*.deb
```

Once Landscape Server is installed, you can finish setting up Landscape similar to how you would with an online server. See the {ref}`Quickstart <how-to-quickstart-installation>` and {ref}`Manual <how-to-manual-installation>` installation guides for more details. This also includes setting up your first administrator and attaching your {ref}`explanation-licenses`.

## Install Landscape Client

```{note}
This section assumes you already have a Landscape PPA added on your online machine. If you don’t have a PPA, see the previous section on installing Landscape Server for these instructions.
```

If you’ve already installed Landscape Server, the process to install Landscape Client is very similar.

### Download the Landscape Client packages

Run the following commands to update the list of packages, clear the downloaded package cache from APT, and download all the packages required for Landscape Client:

```bash
sudo apt update
sudo apt clean
sudo apt --download-only -y install landscape-client
```

All of the necessary packages for Landscape Client should now be downloaded to the APT cache directory: `/var/cache/apt/archives`.

### Install Landscape Client in an offline environment

Copy the downloaded `.deb` packages, carry them into the offline or air-gapped environment, and manually transfer and install them onto your machine with `dpkg`. You can install the packages with a command similar to:

```bash
sudo dpkg -i /PATH/TO/PACKAGES/*.deb
```

Once Landscape Client is installed, you can configure the client and register it with your Landscape server similar to how you would in an online environment. See {ref}`how-to-configure-landscape-client` for more details.

## (Optional) Add more administrators

If no mail delivery is possible in your offline environment and you need to add more administrators, there are a few extra steps. Instead of sending a standard invitation email from Landscape Server to the new administrator, you’ll need to manually create the invite link by retrieving the invite code(s) from the PostgreSQL database.

### Get the invitation codes (secure IDs)

From the database server machine, run the following query to get the invitation codes:

```bash
sudo -u postgres -- psql landscape-standalone-main -c "select secure_id from account_invitation;"
```

This query should output a result similar to the following, with a list of pending invitation IDs (`secure_id`).

```bash
           secure_id            
--------------------------------
 Vd0pMIsD4DIcls6Yt4nRYvmyDJZZRV
(1 row)
```

The `secure_id` can be listed with a given user email invitation in the database, but the IDs aren’t attached to a specific invitation. You can use any given `secure_id` to invite a given user. When that invitation is accepted, that pending `secure_id` will be removed from the database.

### Generate the invite URL

You can generate the invite URL(s) in the following format:

```text
https://<YOUR_LANDSCAPE_URL>/accept-invitation/<SECURE_ID>
```

Replace `<YOUR_LANDSCAPE_URL>` with the URL of your Landscape server, and `<SECURE_ID>` with the value from the database query.

### Accept the invitation

Provide the invite URL to the user. The user should be able to accept the invitation and create their new admin user on the Landscape server.

## Additional considerations

Landscape Server expects to be able to access the following external resources that likely won’t be available in an offline environment:

* [https://landscape.canonical.com](https://landscape.canonical.com)
* [https://usn.ubuntu.com/usn-db/database.json.bz2](https://usn.ubuntu.com/usn-db/database.json.bz2)

Without access to these resources, you may get some errors.

### USN database

You’ll get errors related to the `update_security_db.sh` script. This is expected because this script tries to download and import the USN database from the previously mentioned URL.

To work around this, you could modify the `update_security_db.sh` script to pull from a file that’s been downloaded manually and transferred to the offline server.