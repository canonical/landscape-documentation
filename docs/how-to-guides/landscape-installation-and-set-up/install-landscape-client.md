(how-to-install-landscape-client)=
# How to install Landscape Client

> See also: {ref}`how-to-attach-ubuntu-pro`, {ref}`how-to-ubuntu-pro-enable-landscape`

There are multiple ways to install Landscape Client. This document describes each method.

## Install Landscape Client from Ubuntu's `main` repository

Landscape Client is available in Ubuntu's `main` repository in all [Ubuntu releases](https://ubuntu.com/about/release-cycle), and is published independently of the self-hosted Landscape releases. This method is suitable when performing the installation through a terminal or shell scripting. To install Landscape Client from Ubuntu's `main` repository:

1. Install the `landscape-client` package:

   ```bash
   sudo apt update && sudo apt install -y landscape-client
   ```

1. Set environment variables:

   ```bash
   LANDSCAPE_ACCOUNT_NAME='{ACCOUNT_NAME}'
   LANDSCAPE_FQDN='{FQDN}'
   LANDSCAPE_COMPUTER_TITLE='{COMPUTER_NAME}'
   ```

   This code block includes the following values which must be changed:

   `{ACCOUNT_NAME}`: Self-hosted Landscape users should set this to `standalone`. Landscape SaaS users should specify the account name in their Landscape account.

   `{FQDN}`: Self-hosted Landscape users should set this to the FQDN used during their Landscape Server installation. Landscape SaaS users should set this to `landscape.canonical.com`.

   `{COMPUTER_NAME}`: The name of the computer you’re installing Landscape Client on. You choose this name.

1. Configure:

   ```bash
   sudo landscape-config --silent --account-name="${LANDSCAPE_ACCOUNT_NAME}" --computer-title="${LANDSCAPE_COMPUTER_TITLE}" --tags="" --script-users='nobody,landscape,root' --ping-url="http://${LANDSCAPE_FQDN}/ping" --url="https://${LANDSCAPE_FQDN}/message-system"
   ```

When you install Landscape Client from Ubuntu's `main` repository, you install the version of Landscape Client that's included in that version of Ubuntu. For the latest features, install Landscape Client from the PPA.

## Install Landscape Client from a PPA

This method is suitable when performing the installation through a terminal or shell scripting. To install Landscape Client from a PPA:

1. Install the prerequisites:

   ```bash
   sudo apt update && sudo apt install -y software-properties-common
   ```

1. Add the PPA, replacing `{LANDSCAPE_PPA}` with the appropriate repository:

   ```bash
   sudo add-apt-repository -y {LANDSCAPE_PPA}
   ```

    - `{LANDSCAPE_PPA}`: The PPA for the specific Landscape installation you’re using. The PPA for the most recent Landscape LTS is: `ppa:landscape/self-hosted-24.04`.  The PPA for Landscape's stable rolling release is: `ppa:landscape/latest-stable`. We recommend using an LTS for production deployments.

1. Install the `landscape-client` package:

   ```bash
   sudo apt update && sudo apt install -y landscape-client
   ```

1. Set environment variables:

   ```bash
   LANDSCAPE_ACCOUNT_NAME='{ACCOUNT_NAME}'
   LANDSCAPE_FQDN='{FQDN}'
   LANDSCAPE_COMPUTER_TITLE='{COMPUTER_NAME}'
   ```

   This code block includes the following values which must be changed:

   `{ACCOUNT_NAME}`: Self-hosted Landscape users should set this to `standalone`. Landscape SaaS users should specify the account name in their Landscape account.

   `{FQDN}`: Self-hosted Landscape users should set this to the FQDN used during their Landscape Server installation. Landscape SaaS users should set this to `landscape.canonical.com`.

   `{COMPUTER_NAME}`: The name of the computer you’re installing Landscape Client on. You choose this name.

1. Configure:

   ```bash
   sudo landscape-config --silent --account-name="${LANDSCAPE_ACCOUNT_NAME}" --computer-title="${LANDSCAPE_COMPUTER_TITLE}" --tags='' --script-users='nobody,landscape,root' --ping-url="http://${LANDSCAPE_FQDN}/ping" --url="https://${LANDSCAPE_FQDN}/message-system"
   ```

## Install Landscape Client with the subordinate charm

> See also: [Landscape-client charm on Charmhub](https://charmhub.io/landscape-client)

This method is suitable when using charmed operators. To install Landscape Client with the subordinate charm:

1. Set environment variables:

   ```bash
   LANDSCAPE_ACCOUNT_NAME='{ACCOUNT_NAME}'
   LANDSCAPE_FQDN='{FQDN}'
   ```

   This code block includes the following values which must be changed:

   `{ACCOUNT_NAME}`: Self-hosted Landscape users should set this to `standalone`. Landscape SaaS users should specify the account name in their Landscape account.

   `{FQDN}`: Self-hosted Landscape users should set this to the FQDN used during their Landscape Server installation. Landscape SaaS users should set this to `landscape.canonical.com`.

1. Deploy the charm:

   ```bash
   juju deploy landscape-client --config account-name='standalone' --config tags='' --config script-users='nobody,landscape,root' --config ping-url="http://${LANDSCAPE_FQDN}/ping" --config url="https://${LANDSCAPE_FQDN}/message-system"
   ```

1. Relate the charm:

   ```bash
   juju relate landscape-client <charm-name>
   ```

For more information on the Landscape client charm, see the [Charmhub documentation](https://charmhub.io/landscape-client).

## Install Landscape Client with Cloud-init

This method is suitable if it’s available during a machine’s provisioning stage. To install Landscape Client with cloud-init:

1. Install `landscape-client` from a PPA:

   ```yaml
   apt:
     sources:
       trunk-testing-ppa:
         source: ppa:landscape/self-hosted-24.04
   ```

1. Configure `landscape-client`. Landscape SaaS users should omit `url` and `ping_url`:

   ```yaml
   landscape:
     client:
       account_name: {ACCOUNT_NAME}
       computer_title: "{COMPUTER_NAME}"
       url: "https://{FQDN}/message-system"
       ping_url: "http://{FQDN}/ping"
   ```

   This code block includes the following values which must be changed:

   `{ACCOUNT_NAME}`: Self-hosted Landscape users should set this to `standalone`. Landscape SaaS users should specify the account name in their Landscape account.

   `{COMPUTER_NAME}`: The name of the computer you’re installing Landscape Client on. You choose this name.

   `{FQDN}`: Self-hosted Landscape users should set this to the FQDN used during their Landscape Server installation. Landscape SaaS users should omit `url` and `ping_url`.

   For additional information, see the [cloud-init Landscape module documentation](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#landscape).

## Install the `landscape-client` snap

```{note}
The Landscape Client snap doesn’t support management of Debian packages.
```

```{note}
You must be running a self-hosted Landscape server version 23.10 or later (or beta) to use the snap.
```

The snap is generally used for Ubuntu Core devices. You can install the Landscape Client snap from the [Snap Store](https://snapcraft.io/landscape-client) or the command line. For more detailed instructions and information on the snap's limitations, see {ref}`how-to-install-the-client-snap`.
