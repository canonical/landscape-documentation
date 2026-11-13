---
myst:
  html_meta:
    description: "Reference for lsctl in Landscape Server 24.04 LTS, including starting, stopping, restarting, and checking enabled services."
---

(reference-lsctl)=
# `lsctl`

`lsctl` is a command line tool that manages Landscape services. It must be run with root privileges.

It reads `/etc/default/landscape-server` and applies the requested command to services enabled by `RUN_ALL` or their individual `RUN_*` settings. Services that are not enabled are skipped.

## Usage

```bash
sudo lsctl <COMMAND>
```

The available commands are `start`, `stop`, `restart`, and `status`.

## Commands

### `start`

Starts the enabled Landscape services.

### `status`

Shows the status of the enabled Landscape services.

### `stop`

Stops the enabled Landscape services in reverse startup order.

(reference-lsctl-restart)=
### `restart`

Restarts the enabled Landscape services. This {ref}`does not enable or disable Landscape cron jobs <reference-known-issues-lsctl-restart>`.

## Cron jobs

For charmed deployments, when cron jobs are enabled through `RUN_ALL` or `RUN_CRON`, `lsctl stop` prevents new jobs from starting and waits for running batch scripts to complete. `lsctl start` re-enables cron jobs.

For Quickstart and manual deployments, `lsctl` does not enable or disable cron jobs. To control them separately, see {ref}`reference-known-issues-lsctl-restart`.
