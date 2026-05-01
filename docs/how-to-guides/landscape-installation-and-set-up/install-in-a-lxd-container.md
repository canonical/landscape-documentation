---
myst:
  html_meta:
    description: "Install and configure Landscape Server in a single LXD container for testing. Set up cloud-init, configure environment variables, and provision resources."
---

(how-to-install-in-lxd-container)=
# How to install Landscape Server in a LXD container using cloud-init

This guide shows you how to deploy Landscape Server in a single LXD container using cloud-init. This approach is intended for testing and development environments, as it automates the entire setup process with a single cloud-init configuration file. Cloud-init handles the installation of all Landscape components, configuration of networking, certificates, and system settings.

## Prepare your cloud-init configuration

This guide uses a sample cloud-init file created by the Landscape team. You can see other sample files and scripts in the [Landscape scripts repository on GitHub](https://github.com/canonical/landscape-scripts).

### Download the cloud-init file

To download the cloud-init configuration file and save it as `cloud-init.yaml`, run:

```bash
curl -o cloud-init.yaml https://raw.githubusercontent.com/canonical/landscape-scripts/main/provisioning/cloud-init-quickstart.yaml
```

### Set cloud-init variables

Set the variables cloud-init will use by running this command with your own values:

```bash
declare -A VARIABLES=(
  [EMAIL]='<EMAIL_ADDRESS>'
  [TOKEN]='<PRO_TOKEN>'
  [HOSTNAME]='<HOST_NAME>'
  [DOMAIN]='<DOMAIN>'
  [TIMEZONE]='<TIME_ZONE>'
  [SMTP_HOST]='<SMTP_HOST>'
  [SMTP_PORT]='<SMTP_PORT>'
  [SMTP_USERNAME]='<SMTP_USERNAME>'
  [SMTP_PASSWORD]='<SMTP_PASSWORD>'
  [LANDSCAPE_PPA]='<LANDSCAPE_PPA>'
)
```

Replace the following values with your configuration:

`<EMAIL_ADDRESS>`: The email address that you’ll share with LetsEncrypt for your SSL certificate.

`<PRO_TOKEN>`: Your Ubuntu Pro token from [`https://ubuntu.com/pro/dashboard`](https://ubuntu.com/pro/dashboard). If you’re running an Ubuntu Pro instance on Azure, AWS, or Google Cloud, leave this as an empty string.

`<HOST_NAME>`: The hostname from your FQDN. For example, `server` from `server.domain.com`.

`<DOMAIN>`: The top-level domain (TLD) for your FQDN. For example, `domain.com` from `server.domain.com`.

`<TIME_ZONE>`: Your timezone as represented in `/usr/share/zoneinfo`. If you leave this as an empty string, UTC time will be used.

`<SMTP_HOST>`: The hostname or IP address of the SMTP server provided by your email service provider. If you’re using SendGrid, enter `smtp.sendgrid.net`.

`<SMTP_PORT>`: The port number on which the SMTP server is listening for incoming connections. If you’re using SendGrid, enter `587` for port 587.

`<SMTP_USERNAME>`: The username required to authenticate with the SMTP server. This is provided by your email service provider. If you’re using SendGrid, enter `apikey`.

`<SMTP_PASSWORD>`: The password or API key associated with the SMTP username. If you’re using SendGrid, use an API Key from [`https://app.sendgrid.com/settings/api_keys`](https://app.sendgrid.com/settings/api_keys)

```{include} /reuse/landscape-ppa-description.md
```

### Apply variables to cloud-init

Populate the cloud-init configuration file with your variables:

```bash
for VALUE in "${!VARIABLES[@]}"; do sed -i "s|{% set $VALUE = '.*' %}|{% set $VALUE = '${VARIABLES[$VALUE]}' %}|" cloud-init.yaml; done
```

## Set up LXD

Install or update LXD to the latest stable version:

```bash
snap list lxd &> /dev/null && sudo snap refresh lxd --channel latest/stable || sudo snap install lxd --channel latest/stable
```

This command checks if the LXD snap is installed. If it’s already installed, this command updates it to the latest version. If it’s not installed, this command installs the latest version.

Then, initialize LXD with default settings:

```bash
lxd init --auto
```

## Configure networking

Identify the default network adapter on the machine and check the MTU configuration on this adapter:

```bash
read -r INTERFACE < <(ip route | awk '$1=="default"{print $5; exit}')
```

If your network uses non-standard MTU settings (jumbo frames with MTU 9000 or smaller than 1500), configure LXD to match. Google Cloud VMs, for example, use MTU values smaller than 1500.

To set the LXD bridge MTU to match your network:

```bash
lxc network set lxdbr0 bridge.mtu=$(ip link show $INTERFACE | awk '/mtu/ {print $5}')
```

## Deploy Landscape with cloud-init

Cloud-init will automatically deploy Landscape and configure port forwarding for ports 80, 443, and 6554 to make the instance accessible.

**Step 1:** Install Landscape Quickstart inside a LXD container using `cloud-init.yaml`. This command installs Landscape on Ubuntu 24.04 LTS.

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
