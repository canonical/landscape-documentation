(how-to-guides-iot-for-devices-configure-the-snap)=
# How to configure the snap

```{note}
You must have the Landscape Client snap installed on at least one client device before configuring it with `landscape-client.config`. For instructions, see [how to install the Landscape Client snap](/how-to-guides/iot-for-devices/install-the-snap).
```

This document describes how to configure the Landscape Client snap in multiple ways. If you’re using the Debian package instead of the snap, see [how to configure Landscape Client](/how-to-guides/landscape-installation-and-set-up/configure-landscape-client).

## Use `landscape-client.config`

After you’ve installed the `landscape-client` snap, you can use `landscape-client.config` to configure it on your client devices. Running `landscape-client.config` without any arguments starts the configuration, and you’ll be prompted to provide any information needed to run.

Some example commands with `landscape-client.config` are:

```bash
sudo landscape-client.config
```

```bash
sudo landscape-config --silent --account-name="standalone"
```

To view all possible configuration options for `landscape-client.config`, visit the help page with:

```bash
landscape-client.config --help
```

### SSL certificates

If you’re using Ubuntu Core and require your own SSL certificates, you must place the certificate in `/var/snap/landscape-client/` and provide the full path to the `--ssl-public-key` option. For example, if you place the CA file in `/var/snap/landscape-client/ssl/server.pem`, then you can register the computer with:
```bash
sudo landscape-config --ssl-public-key /var/snap/landscape-client/ssl/server.pem
```

## Auto-register new devices

```{note}
These steps are for automatically registering devices that are manually configured. If you’re registering a large-scale deployment of Ubuntu Core devices, you may want to auto-register them through the build image configuration. For more information, see [how to create an Ubuntu Core image with Landscape Client included](/how-to-guides/iot-for-devices/create-a-core-image).
```

You can automatically register new Landscape Client snap devices when they’re configured using a registration key. This eliminates the need for manual approval of each device. This feature is enabled by default.

To use this feature in the Landscape web portal:

1. Navigate to your **Account** tab

2. If the **Registration key** field is blank, set a new registration key. You can set the registration key to be whatever you want, but trailing spaces, semi-colon (**;**) or hash (**#**) characters are not allowed.

3. Select **Auto register new computers** if it’s not already selected. Clearing this checkbox will disable the auto-registration feature.

4. Click **Save**

When this feature is enabled, new devices must be enrolled using the key that’s defined in the **Registration key** field. You can’t auto-register new computers if there is no registration key provided.

Once you’ve defined a registration key and enabled the auto-registration feature, you can auto-register new computers by passing the `--registration-key` argument into `landscape-client.config`. For example, the following code registers a new Landscape Client computer with a registration key. The `{ACCOUNT_NAME}`, `{COMPUTER_TITLE}` and `{REGISTRATION_KEY}` placeholders must be changed to the appropriate values for your configuration.

```bash
sudo landscape-client.config --account-name={ACCOUNT_NAME} --computer-title={COMPUTER_TITLE} --registration-key={REGISTRATION_KEY}
```

## Manage script execution

The Landscape Client snap has a plugin that allows an administrator to execute scripts remotely on any client snap device. This plugin is enabled by default, although you can manually disable it.

If you want to disable remote script execution, you can disable it by manually editing `/var/snap/landscape-client/common/etc/landscape-client.conf`. Delete the following line from the `[client]` section of that file:

```bash
include_manager_plugins=ScriptExecution
```

To re-enable it, add that line back to the `client.conf` file, or run the following:

```bash
sudo landscape-client.config --include-manager-plugins=ScriptExecution
```

## Managed device mode

> This configuration is available for Rev 383 or higher.

After you've installed the Landscape Client snap, you can set your device to “managed mode”. This is a configuration that tells SnapD not to automatically refresh or update any snaps and that Landscape Client will now undertake those responsibilities remotely.

This setting is recommended for IoT devices where it's often important to control if, and exactly when, snaps get updated to later versions.

To enable this setting, run the following command: (note this will only work if you have the Landscape client snap installed)

```
sudo snap set system refresh.timer="managed"
```

## Log rotation

The Landscape Client Snap includes built-in log rotation with similar configuration to the [Debian package](/how-to-guides/landscape-installation-and-set-up/configure-landscape-client.md#log-rotation). Log rotation is done by the `landscape-client.logrotate` daemon weekly on Sunday. Due to the nature of snap applications, the rotation schedule cannot be modified.

To view the daemon’s logs, run:

```bash
$ snap logs landscape-client.logrotate
```

To disable log rotation, run:

```bash
$ snap stop --disable landscape-client.logrotate
```

To enable log rotation, run:

```bash
$ snap start --enable landscape-client.logrotate
```
