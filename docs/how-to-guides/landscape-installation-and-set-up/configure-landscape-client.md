(how-to-configure-landscape-client)=
# How to configure Landscape Client

> See also: {ref}`how-to-install-landscape-client`

This guide describes how to configure the Landscape Client Debian package in multiple ways. 

If you're using the snap instead of the Debian package, see {ref}`how-to-configure-the-client-snap`.

If you're using the charm, you'll need to configure the client with `juju config`. For more information, see the [Juju documentation](https://juju.is/docs/juju) and [Charmhub's documentation on the Landscape client charm](https://charmhub.io/landscape-client).

## Use `landscape-config`

After you’ve installed `landscape-client`, you can use `landscape-config` to configure it on your client machines. Running `landscape-config` without any arguments starts the configuration, and you’ll be prompted to provide any information needed to run Landscape Client. When the configuration is complete, you’ll receive confirmation that the client was registered successfully or if an error occurred.

Some sample commands with `landscape-config` are:

```bash
sudo landscape-config
```

```bash
sudo landscape-config --silent --account-name="standalone"
```

To view all possible options for `landscape-config`, visit the man page with:

```bash
man landscape-config
```

## Update the `client.conf` file

See the Landscape Client GitHub project for an [example `client.conf` file](https://github.com/canonical/landscape-client/blob/main/example.conf). This file contains all the existing configuration options available. 

The Landscape Client configuration file is located in `/etc/landscape/client.conf` for the Debian package. If you change any configurations in this file, you’ll need to restart Landscape Client:

```bash
sudo systemctl restart landscape-client
```

(howto-heading-client-autoregister)=
## Auto-register new computers

```{note}
You must have a registration key defined in your Landscape account for this feature to be available. If you don’t have a registration key yet, you can create a new one during this configuration process.
```

You can automatically register new Landscape Client computers when they’re configured using a registration key. This eliminates the need for manual approval of each computer. This feature is enabled by default.

To use this feature in the Landscape web portal:

1. Navigate to your **Account** tab

2. If the **Registration key** field is blank, set a new registration key. You can set the registration key to be whatever you want, but trailing spaces, semi-colon (**;**) or hash (**#**) characters are not allowed.

3. Select **Auto register new computers** if it’s not already selected. Clearing this checkbox will disable the auto-registration feature.

4. Click **Save**

When this feature is enabled, new computers must be enrolled using the key that’s defined in the **Registration key** field. You can’t auto-register new computers if there is no registration key provided.

Once you’ve defined a registration key and enabled the auto-registration feature, you can auto-register new computers by passing the `--registration-key` argument into `landscape-config`. For example, the following code registers a new Landscape Client computer with a registration key. The `{LANDSCAPE_ACCOUNT_NAME}`, `{COMPUTER_TITLE}` and `{KEY}` placeholders must be changed to the appropriate values for your configuration.

```bash
sudo landscape-config --account-name={LANDSCAPE_ACCOUNT_NAME} --computer-title={COMPUTER_TITLE} --registration-key={KEY}
```

(howto-heading-client-enable-script-execution)=
## Enable script execution


> See also: [Landscape's scripts repository on GitHub](https://github.com/canonical/landscape-scripts)

An administrator can remotely execute scripts on any client machine if the appropriate plugin is enabled. This plugin is disabled by default. Any calls to the `ExecuteScript` API endpoint will result in failed activities if the client has the default configuration. For more information on API endpoints for stored scripts, visit {ref}`API Methods: Scripts <reference-legacy-api-scripts>`.

To use remote script execution on client machines, you must first enable it with the `landscape-config` command or by manually editing `/etc/landscape/client.conf`.

To enable this plugin with `landscape-config`, run:

```bash
sudo landscape-config --include-manager-plugins=ScriptExecution --script-users=root,landscape,nobody
```

Or, to enable this plugin by manually editing `/etc/landscape/client.conf`, add the following line to the `[client]` section of that file:

```bash
include_manager_plugins = ScriptExecution
script_users = root,landscape,nobody
```

After you’ve enabled script execution using one of these options, the system users listed in `script_users` can run scripts once you restart Landscape Client with:

```bash
sudo service landscape-client restart
```
Setting `script_users = ALL` (or passing `ALL` to the `--script-users` parameter of `landscape-config`) will allow any system user to run scripts. If `script_users` is not set, then scripts can only be run by the `nobody` user.

## Landscape clients with configuration management tools

If you want to manage `landscape-client` through a configuration management tool such as Puppet or Ansible, you can avoid getting duplicate computers by writing the `/etc/landscape/client.conf` and `/etc/default/landscape-client` files, and then restarting the `landscape-client` service.

In `/etc/landscape/client.conf`:
```
[client]
log_level = info 
url = https://landscape.canonical.com/message-system
ping_url = http://landscape.canonical.com/ping
data_path = /var/lib/landscape/client
registration_key = changeme
computer_title = my_machine
account_name = myaccount
include_manager_plugins = ScriptExecution
script_users = root,landscape,nobody
```
In `/etc/default/landscape-client`:
```
RUN=1
```
The advantage over calling `landscape-config` is that this will request a registration only if the client is not already registered against `landscape-server`. Be aware that some configuration options (namely `computer_title`, `tags`, `access_group`) are only sent to `landscape-server` on registration.

## Log rotation

Landscape Client implements automated log rotation to manage log file sizes and retention.

The log rotation configuration is located at `/etc/logrotate.d/landscape-client`. By default, the logs are rotated once per week and the four most recent log files are kept before the oldest ones are deleted.

Log rotation is automatically done through the system’s daily cron jobs, specifically via `/etc/cron.daily/logrotate`.

To manually trigger log rotation, run:

```bash
$ logrotate --force /etc/logrotate.d/landscape-client
```

