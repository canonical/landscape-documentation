---
myst:
  html_meta:
    description: "Reference guide for lsctl command line tool that manages Landscape systemd services including start, stop, enable, disable, and status."
---

(reference-lsctl)=
# `lsctl`

`lsctl` is a command line tool that simplifies managing Landscape systemd services. It allows you to apply `systemctl` commands to all of the services at once. It must be run with root privileges.

## Usage

```bash
lsctl <COMMAND>
```

Internally, this executes:

```bash
systemctl <COMMAND> landscape-server.target
```

## Common commands

Certain commands extend the basic `systemctl` behavior with extra functionality.

### `disable`

Prevents Landscape services from starting automatically at boot.

### `enable`

Configures Landscape services to start automatically at boot.

### `start`

Starts all Landscape services and also enables any Landscape cron jobs.

### `status`

Shows the status of all Landscape services. You can use this to determine which services are active or inactive for troubleshooting.

Equivalent `systemctl` command:

```bash
systemctl list-dependencies landscape-server.target
```

To check the status of an individual service, you can use:

```bash
systemctl status <SERVICE-NAME>
```

### `stop`

Stops all Landscape services cleanly, waiting for any batch scripts to complete. This also disables Landscape cron jobs.

(reference-lsctl-restart)=
### `restart`

Restart Landscape services. Currently, this {ref}`does not enable or disable Landscape cron jobs <reference-known-issues-lsctl-restart>`.
