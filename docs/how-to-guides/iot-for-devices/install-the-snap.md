(how-to-install-the-client-snap)=
# How to install the snap

This document describes how to install the Landscape Client snap and some general limitations of the snap. If you want to install the Debian package instead of the snap, see [how to install Landscape Client](/how-to-guides/landscape-installation-and-set-up/install-landscape-client).

## Install and set up the Landscape Client snap

```{note}
You must be running a self-hosted Landscape server version 23.10 or later (or beta) to use the snap.
```

The Landscape Client snap is available in the [Snap Store](https://snapcraft.io/landscape-client). This installation method is suitable for Ubuntu Core devices but can also be used on classic Ubuntu systems.

### Install

To install the snap, run:

```bash
sudo snap install landscape-client
```

The installation of the snap will also automatically connect the necessary interfaces for the client, granting it permission to remotely manage the device through Landscape.

### Configure

After you’ve installed `landscape-client` snap, you’ll need to provide some basic configuration values to finish setting up the snap. There are three possible methods to configure the snap.

**Method #1: Use the configuration wizard**

You can use the configuration wizard to guide you through the configuration process. To do this, run:

```bash
sudo landscape-client.config
```
Then follow the prompts and provide an requested information.

**Method #2: Provide the information as parameters**

You can provide any necessary information directly as parameters. To do this, run:

```bash
sudo landscape-client.config --silent --account-name="${LANDSCAPE_ACCOUNT_NAME}" --computer-title="${LANDSCAPE_COMPUTER_TITLE}" --tags='' --ping-url="http://${LANDSCAPE_FQDN}/ping" --url="https://${LANDSCAPE_FQDN}/message-system"
```

Replacing the placeholder variables with their appropriate values.

- `{LANDSCAPE_ACCOUNT_NAME}`: Self-hosted Landscape users should set this to `standalone`.

- `{LANDSCAPE_COMPUTER_TITLE}`: The name of the computer you’re installing the snap on. You choose this name.

- `{LANDSCAPE_FQDN}`: The FQDN used during your Landscape Server installation.

When the configuration is complete, you’ll receive confirmation that the client was registered successfully or if an error occurred.

**Method #3: Use `set` to set individual configuration values**

You can use the snap `set` command to set individual configuration values. For example:

```bash
snap set landscape-client computer-title {LANDSCAPE_COMPUTER_TITLE}
snap set landscape-client url {LANDSCAPE_URL}
```

After setting any configuration variables using `set`, you’ll need to restart the client snap for the new configuration to be applied:

```bash
snap restart landscape-client
```

The options you can set with snap `set` are:

- `account-name`

- `computer-title`

- `landscape-url`

- `log-level`

- `script-users`

- `manager-plugins`

- `monitor-plugins`

- `access-group`

- `registration-key`

### Accept the registration

```{note}
If you’re using a registration key, you don’t need to accept the registration. Your device will enroll automatically. For more information on auto-registration, see how to auto-register new devices.
```

If you didn’t specify a registration key, you’ll need to accept the registration request in the Landscape web portal. You’ll receive an alert that a pending computer/device needs approval. If you’re re-installing a device that previously existed in Landscape, you can select it during this stage of the registration if you want to reuse the instance.

To accept the registration from the alerts menu in the header:

1. Click on the alert

2. Confirm that the device attempting to enroll is your device

3. Click **Accept**

Your device will then appear in your list of computers, which is found in the **Computers** page in the header. It may take a few minutes to start populating information.

