---
myst:
  html_meta:
    description: "Install and configure Landscape Server in a single LXD container for testing. Set up cloud-init, configure environment variables, and provision resources."
---

(how-to-install-in-lxd-container)=
# How to install and configure Landscape Server in a single LXD container

```{note}
You can also use this guide to test Landscape inside a single LXD container.
```

## Install and configure cloud-init

### Download the cloud-init configuration file

To download the cloud-init configuration file and save it as `cloud-init.yaml`, run:

```bash
curl -o cloud-init.yaml https://raw.githubusercontent.com/canonical/landscape-scripts/main/provisioning/cloud-init-quickstart.yaml
```

### Set cloud-init variables

To set the variables needed by the cloud-init configuration file, run:

```bash
declare -A VARIABLES=(
  [EMAIL]='{EMAIL_ADDRESS}'
  [TOKEN]='{PRO_TOKEN}'
  [HOSTNAME]='{HOST_NAME}'
  [DOMAIN]='{DOMAIN}'
  [TIMEZONE]='{TIME_ZONE}'
  [SMTP_HOST]='{SMTP_HOST}'
  [SMTP_PORT]='{SMTP_PORT}'
  [SMTP_USERNAME]='{SMTP_USERNAME}'
  [SMTP_PASSWORD]='{SMTP_PASSWORD}'
  [LANDSCAPE_PPA_NAME]='{LANDSCAPE_PPA_NAME}'
)
```

This code block includes the following values that must be changed:

`{EMAIL_ADDRESS}`: The email address that you’ll share with LetsEncrypt for your SSL certificate.

`{PRO_TOKEN}`: Your Ubuntu Pro token from [`https://ubuntu.com/pro/dashboard`](https://ubuntu.com/pro/dashboard). If you’re running an Ubuntu Pro instance on Azure, AWS, or Google Cloud, leave this as an empty string.

`{HOST_NAME}`: The hostname from your FQDN. For example, `server` from `server.domain.com`.

`{DOMAIN}`: The top-level domain (TLD) for your FQDN. For example, `domain.com` from `server.domain.com`.

`{TIME_ZONE}`: Your timezone as represented in `/usr/share/zoneinfo`. If you leave this as an empty string, UTC time will be used.

`{SMTP_HOST}`: The hostname or IP address of the SMTP server provided by your email service provider. If you’re using SendGrid, enter `smtp.sendgrid.net`.

`{SMTP_PORT}`: The port number on which the SMTP server is listening for incoming connections. If you’re using SendGrid, enter `587` for port 587.

`{SMTP_USERNAME}`: The username required to authenticate with the SMTP server. This is provided by your email service provider. If you’re using SendGrid, enter `apikey`.

`{SMTP_PASSWORD}`: The password or API key associated with the SMTP username. If you’re using SendGrid, use an API Key from [`https://app.sendgrid.com/settings/api_keys`](https://app.sendgrid.com/settings/api_keys)

`{LANDSCAPE_PPA_NAME}`: The version of Landscape you will install. Enter `self-hosted-24.04`, `self-hosted-25.10`, `self-hosted-beta`, or `latest-stable`.

### Populate the cloud-init configuration file with your variables

To populate `cloud-init.yaml` with your variables, run:

```bash
for VALUE in "${!VARIABLES[@]}"; do sed -i "s|{% set $VALUE = '.*' %}|{% set $VALUE = '${VARIABLES[$VALUE]}' %}|" cloud-init.yaml; done
```

## Install and configure LXD

### Install or update LXD

To install or update the LXD snap, run:

```bash
snap list lxd &> /dev/null && sudo snap refresh lxd --channel latest/stable || sudo snap install lxd --channel latest/stable
```

This command checks if the LXD snap is installed. If it’s already installed, this command updates it to the latest version. If it’s not installed, this command installs the latest version.

### Configure LXD

To configure LXD with predefined settings without requiring user input, run:

```bash
lxd init --auto
```

## Configure network settings

### Identify the default network adapter and check MTU configuration

To identify the default network adapter on the machine and check the MTU configuration on this adapter, run:

```bash
read -r INTERFACE < <(ip route | awk '$1=="default"{print $5; exit}')
```

### Adjust LXD network MTU settings

If your network uses jumbo frames (e.g., MTU 9000) or an MTU smaller than 1500, you’ll need to use a matching MTU on `lxdbr0`. Note that Google Cloud VMs use MTUs smaller than 1500.

To change the LXD bridge MTU to match the network’s configuration, run:

```bash
lxc network set lxdbr0 bridge.mtu=$(ip link show $INTERFACE | awk '/mtu/ {print $5}')
```

## Install and configure Landscape Quickstart

```{note}
It’s recommended to install Landscape on the latest Ubuntu LTS, but you can also use 20.04 if you require that version.
```

You can configure ports 6554, 443 and 80 to allow for connections to the Landscape instance inside the LXD container.

**Step 1:** Install Landscape Quickstart inside a LXD container using `cloud-init.yaml`, run:

 ```bash
lxc launch ubuntu:24.04 landscape --config=user.user-data="$(cat cloud-init.yaml)" 
```

**Step 2:** Capture the IP address of the "landscape" LXD container:

 ```bash
LANDSCAPE_IP=$(lxc list landscape --format csv -c 4 | awk '{print $1}')
```

**Step 3:** Configure port forwarding for Port 6554, 443, and 80:

```bash
for PORT in 6554 443 80; do lxc config device add landscape tcp${PORT}proxyv4 proxy listen=tcp:0.0.0.0:${PORT} connect=tcp:${LANDSCAPE_IP}:${PORT}; done
```

Allowing TCP traffic on these ports in the host machine’s firewall settings and the network router  configuration or enterprise firewall configuration enables the Landscape Quickstart instance to be  accessible to the public Internet. This allows certbot to obtain a valid SSL certificate if a DNS record  exists with the FQDN pointing to your host machine’s public IP address.

**Step 4:** To observe the progress, run:

```bash
lxc exec landscape -- bash -c "tail -f /var/log/cloud-init-output.log"
```

When the cloud-init process is complete, you’ll receive two lines similar to this:

```text
Cloud-init v. 25.2-0ubuntu1~24.04.1 finished at Fri, 20 Feb 2026 18:36:19 +0000. Datasource DataSourceLXD.  Up 408.07 seconds
```

**Step 5:** Press `CTRL + C` to terminate the tail process in your terminal window.
