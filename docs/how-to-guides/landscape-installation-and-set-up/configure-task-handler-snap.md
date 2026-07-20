---
myst:
  html_meta:
    description: "Configure the Landscape Task Handler snap for Landscape 26.04.1 LTS and later manual deployments."
---

(how-to-configure-task-handler-snap)=
# How to configure the Landscape Task Handler snap

The Landscape Task Handler snap (`landscape-task-handler`) is required for Landscape Server 26.04.1 LTS and later.

The task handler snap runs sandboxed as `root` and connects to both its own task database and the shared Landscape Server databases. By default, the task handler reads the shared database configuration from `/etc/landscape/service.conf`. The task handler's own database must always be configured directly, as it is not provided by `service.conf`.

## Identify whether additional configuration is needed

After the initial installation (covered in {ref}`the manual installation guide <how-to-manual-installation>`), the task handler needs at minimum its own database connection configured. Additional configuration is usually needed only when one or more of these are true:

- The task handler must read from a non-default `service.conf` path.
- The task handler needs to connect to its database or the shared databases with different settings than those in `service.conf`.
- You need to tune worker, cleanup, or logging behavior beyond the defaults.

For all available keys and environment variable mappings, see {ref}`reference-task-handler-configuration`.

## Apply configuration

Use `snap set landscape-task-handler ...` to set values. For example, to configure the task handler database connection:

```bash
sudo snap set landscape-task-handler \
  landscape.database.task-handler.host=<DB-HOST> \
  landscape.database.task-handler.port=<DB-PORT> \
  landscape.database.task-handler.user=landscape \
  landscape.database.task-handler.password=<DB-PASSWORD> \
  landscape.database.task-handler.name=landscape-standalone-task-handler \
  landscape.database.task-handler.ssl=disable
```

Values set through snap configuration will override equivalent values from `service.conf`. For example, to configure the task handler to use a different SSL mode for the shared databases than what Landscape Server uses:

```bash
sudo snap set landscape-task-handler landscape.database.main.ssl=verify-full
```

## Verify configuration changes

The services restart automatically when configuration changes are applied. Verify the services are running and check the logs for errors:

```bash
sudo snap services landscape-task-handler
sudo snap logs landscape-task-handler -n 50
```

If there are no errors, the configuration is valid.
