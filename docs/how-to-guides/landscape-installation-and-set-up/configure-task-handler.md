---
myst:
  html_meta:
    description: "Configure the Landscape Task Handler snap for Landscape 26.04.1 LTS and later manual deployments."
---

(how-to-configure-task-handler)=
# How to configure Task Handler

Task handler is required for Landscape 26.04.1 LTS and later. It performs hard deletion tasks (for example, permanently deleting a computer) as a saga that spans the main, account, and resource databases, tracking each task through its stages so that a transient failure can be retried instead of leaving the deletion partially applied.

The Landscape Task Handler snap (`landscape-task-handler`) runs sandboxed as `root` and connects to both its own task database and the shared Landscape Server databases. By default, the task handler reads the shared database configuration from `/etc/landscape/service.conf`. The task handler's own database must always be configured directly, as it is not provided by `service.conf`.

After the initial installation (covered in {ref}`the manual installation guide <how-to-manual-installation>`), the task handler needs at minimum its own database connection configured. Additional configuration is usually needed only when one or more of these are true:

- The task handler must read from a non-default `service.conf` path.
- The task handler needs to connect to its database or the shared databases with different settings than those in `service.conf`.
- You need to tune worker, cleanup, or logging behavior beyond the defaults.

For all available keys and environment variable mappings, see {ref}`reference-task-handler-configuration`.

## Apply database configuration

The task handler's own database connection is required and does not come from `service.conf`. Use `snap set landscape-task-handler ...` to configure it:

```bash
sudo snap set landscape-task-handler \
  landscape.database.task-handler.host=<DB-HOST> \
  landscape.database.task-handler.port=<DB-PORT> \
  landscape.database.task-handler.user=landscape \
  landscape.database.task-handler.password=<DB-PASSWORD> \
  landscape.database.task-handler.name=landscape-standalone-task-handler \
  landscape.database.task-handler.ssl=disable
```

```{seealso}
See [Configuring SSL/TLS for PostgreSQL connections](#task-handler-ssl-tls) if you need to enable SSL/TLS instead of `ssl=disable`.
```

## Apply additional configuration

The rest of the task handler's settings are optional and only need to be set if your deployment requires something other than the defaults. Values set through snap configuration override the equivalent value from `service.conf`.

For example, to configure the task handler to use a different SSL mode for the shared databases than what Landscape Server uses:

```bash
sudo snap set landscape-task-handler landscape.database.main.ssl=verify-full
```

Or to tune worker concurrency:

```bash
sudo snap set landscape-task-handler landscape.task-handler.worker.max-retries=5
```

## Verify configuration changes

The services restart automatically when configuration changes are applied. Verify the services are running and check the logs for errors:

```bash
sudo snap services landscape-task-handler
sudo snap logs landscape-task-handler -n 50
```

If there are no errors, the configuration is valid.

(task-handler-ssl-tls)=
## Configuring SSL/TLS for PostgreSQL connections

By default, the examples in the installation guides use `ssl=disable` for simplicity. If your PostgreSQL connection requires SSL, enable SSL/TLS instead.

The task handler's own database connection and the shared database connections each have their own SSL settings. Set the SSL mode with `landscape.database.<db>.ssl`, where `<db>` is `task-handler`, `main`, `account`, or `resource`. Valid modes are `disable`, `allow`, `prefer`, `require`, `verify-ca`, and `verify-full`.

```bash
sudo snap set landscape-task-handler \
  landscape.database.task-handler.ssl=verify-full \
  landscape.database.task-handler.ssl-root-cert=/etc/landscape/task-handler-certs/root.crt
```

If your PostgreSQL server requires client certificate authentication instead of, or in addition to, a password, also set `landscape.database.<db>.ssl-cert` and `landscape.database.<db>.ssl-key`.

For the shared databases (`main`, `account`, `resource`), the SSL mode and certificate paths are normally read automatically from `/etc/landscape/service.conf`, matching what Landscape Server itself uses. Only set these snap keys directly if the task handler needs different SSL settings than Landscape Server for the shared databases.

For the full list of SSL-related settings and their defaults, see {ref}`reference-task-handler-configuration`.
