(how-to-quickstart-installation)=
# How to install Landscape Server with quickstart mode

The quickstart mode of deploying Landscape consists of installing all the necessary software on a single machine. Quickstart mode has limited scalability, so it may not be ideal for large production deployments.

```{note}
If you have an Ubuntu Pro subscription, we recommend you attach your Pro token for easy access to your Pro services. For more information, see {ref}`how-to-attach-ubuntu-pro` and {ref}`how-to-ubuntu-pro-enable-landscape`.
```

## Check minimum requirements

The following minimum requirements are needed to install Landscape Server:

- **Operating system**: Ubuntu 22.04 LTS (Jammy Jellyfish) or Ubuntu 24.04 LTS (Noble Numbat)
- **Hardware**: A dual-core 2 GHz processor, 4 GB of RAM, and 20 GB of disk space
- **Networking**: An IP address and FQDN with TCP communication allowed for SSH (typically port 22), HTTP (port 80), and HTTPS (port 443)
- If you wish to use LetsEncrypt to obtain an SSL certificate, DNS administration access for the hostname you’ll use to access Landscape

## Install Landscape Server

### Install prerequisites

To install prerequisites, run:

```bash
sudo apt update && sudo apt install -y ca-certificates software-properties-common
```

The `add-apt-packages` command line utility is necessary to add the PPA which contains the Landscape Server software. The `software-properties-common` package must be added to access `add-apt-packages`.

### Set environment variables

To set the necessary environment variables, run:

```bash
HOST_NAME={HOST_NAME}
DOMAIN={DOMAIN_NAME}
FQDN=$HOST_NAME.$DOMAIN
```

This code block includes the following values that must be changed:

`{HOST_NAME}`: The host name you’re using for the Landscape installation

`{DOMAIN_NAME}`: The domain name you’re using for the Landscape installation

It’s important to set `HOST_NAME`, `DOMAIN` and `FQDN` correctly prior to installing Landscape Server. These variables are used by other commands later.

### Set the machine’s host name

To set the machine’s host name, run:

```bash
sudo hostnamectl set-hostname "$FQDN"
```

When Landscape Server is installed, it will read the machine’s host name and use it in the Apache configuration.

### Install `landscape-server-quickstart`

To install `landscape-server-quickstart`:

1. Add the PPA for Landscape Server, replacing `{LANDSCAPE_PPA}` with the appropriate repository:
    
    ```bash
    sudo add-apt-repository -y {LANDSCAPE_PPA}
    ```
    
    - `{LANDSCAPE_PPA}`: The PPA for the specific Landscape installation you’re using. The PPA for the most recent Landscape LTS is: `ppa:landscape/self-hosted-24.04`.  The PPA for Landscape's stable rolling release is: `ppa:landscape/latest-stable`. We recommend using an LTS for production deployments.

2. Update packages and dependencies in your local system:
    
    ```bash
    sudo apt-get update
    ```
    
3. Install `landscape-server-quickstart`:

    ```bash
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y landscape-server-quickstart
    ```

   - This installation takes approximately five minutes.

## Install an SSL certificate

```{note}
If you have the `fullchain.pem` and `privkey.pem` files for your SSL certificate, skip these steps and configure Apache manually. For more details, see {ref}`how to configure the web server <how-to-heading-manual-install-configure-web-server>` in the Landscape manual installation guide.
```

### Install Certbot

Certbot is a command line utility which makes acquiring and renewing SSL certificates from LetsEncrypt an easy, free and automated process. You can install Certbot with the `snap` or `apt` package manager.

To install Certbot with `snap`:

```bash
sudo snap install certbot --classic
```
Or `apt`:

```bash
sudo apt-get install certbot python3-certbot-apache -y
```

### Get an SSL certificate from LetsEncrypt

If your Landscape instance has a public IP, and your FQDN resolves to that public IP, run the following code to get a valid SSL certificate from LetsEncrypt:

```bash
sudo certbot --non-interactive --apache --no-redirect --agree-tos --email {EMAIL@ADDRESS.COM} --domains $FQDN
```

But, replace `{EMAIL@ADDRESS.COM}` with an email address where certificate renewal reminders can be sent.

## Create a global administrator account

At this point, visiting `https://HOST_NAME.DOMAIN` prompts you to create Landscape’s first Global Administrator account. To add administrators:

1. Click **Settings**
2. Set a valid outgoing email address in the **System email address** field
3. Click **Save**

By default, the email address will be pre-filled with *noreply@HOST_NAME.DOMAIN*. You may want to change this to *noreply@DOMAIN*, or another valid email address.

## (Optional) Configure Postfix for email

You can configure Postfix to handle Landscape Server email notifications and alerts. For details, see {ref}`how-to-configure-postfix`.

