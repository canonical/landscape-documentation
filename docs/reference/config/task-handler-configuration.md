---
myst:
  html_meta:
    description: "Technical reference for Landscape Task Handler configuration including all environment variables, snap configuration keys, and defaults."
---

(reference-task-handler-configuration)=
# Landscape Task Handler configuration reference

The Landscape Task Handler service is configured entirely through environment variables. There is no separate configuration file format; all settings are expressed as environment variables, which can be supplied directly or through the snap configuration system.

The task handler snap (`landscape-task-handler`) provides four services:

- **`landscape-task-handler.server`**: the gRPC server other Landscape services can connect with to create a task.
- **`landscape-task-handler.worker`**: the service that performs queued tasks.
- **`landscape-task-handler.cert-renewer`**: a periodic job that automatically renews client and server mTLS certificates when they near their expiration dates.
- **`landscape-task-handler.cleanup`**: a periodic cleanup job that purges old task handler entries from the database.

## `service.conf` integration

To perform hard deletion tasks, the task handler needs to use the same databases that Landscape server uses. By default, the task handler will read database configurations from `/etc/landscape/service.conf` and will populate the corresponding environment variables. The path to the `service.conf` file can be overridden via the `LANDSCAPE_CONFIG_FILE` environment variable or equivalently the `landscape.service-conf-file` snap key.

This means that several environment variables marked as **required** in this reference do not need to be set directly and can instead be read from the `service.conf`. These configurations are marked with **`service.conf-supplied`: Yes**. It is recommended to use this integration instead of setting these environment variables directly. In cases where the task handler cannot use the same configuration value as the Landscape server, it is necessary to use the snap configuration. A snap configuration takes priority over the equivalent value in the `service.conf`.

The table below lists every environment variable that is populated from `service.conf`. Note that all three Landscape server databases share the same host, port, user, password, and SSL settings from the `[stores]` section. The task handler's own database (`LANDSCAPE_DATABASE_TASK_HANDLER_*`) is not populated from `service.conf` and must be configured directly.

| Environment variable | `service.conf` section | `service.conf` key |
| --- | --- | --- |
| `LANDSCAPE_DATABASE_MAIN_NAME` | `[stores]` | `main` |
| `LANDSCAPE_DATABASE_MAIN_HOST` | `[stores]` | `host` (hostname portion) |
| `LANDSCAPE_DATABASE_MAIN_PORT` | `[stores]` | `host` (port portion), default `5432` |
| `LANDSCAPE_DATABASE_MAIN_USER` | `[stores]` | `user` |
| `LANDSCAPE_DATABASE_MAIN_PASSWORD` | `[stores]` | `password` (base64-decoded) |
| `LANDSCAPE_DATABASE_MAIN_SSL` | `[stores]` | `sslmode`, default `prefer` |
| `LANDSCAPE_DATABASE_MAIN_SSL_ROOT_CERT` | `[stores]` | `sslrootcert` |
| `LANDSCAPE_DATABASE_MAIN_SSL_CERT` | `[stores]` | `sslcert` |
| `LANDSCAPE_DATABASE_MAIN_SSL_KEY` | `[stores]` | `sslkey` |
| `LANDSCAPE_DATABASE_ACCOUNT_NAME` | `[stores]` | `account_1` (or legacy `account-1`) |
| `LANDSCAPE_DATABASE_ACCOUNT_HOST` | `[stores]` | `host` (hostname portion) |
| `LANDSCAPE_DATABASE_ACCOUNT_PORT` | `[stores]` | `host` (port portion), default `5432` |
| `LANDSCAPE_DATABASE_ACCOUNT_USER` | `[stores]` | `user` |
| `LANDSCAPE_DATABASE_ACCOUNT_PASSWORD` | `[stores]` | `password` (base64-decoded) |
| `LANDSCAPE_DATABASE_ACCOUNT_SSL` | `[stores]` | `sslmode`, default `prefer` |
| `LANDSCAPE_DATABASE_ACCOUNT_SSL_ROOT_CERT` | `[stores]` | `sslrootcert` |
| `LANDSCAPE_DATABASE_ACCOUNT_SSL_CERT` | `[stores]` | `sslcert` |
| `LANDSCAPE_DATABASE_ACCOUNT_SSL_KEY` | `[stores]` | `sslkey` |
| `LANDSCAPE_DATABASE_RESOURCE_NAME` | `[stores]` | `resource_1` (or legacy `resource-1`) |
| `LANDSCAPE_DATABASE_RESOURCE_HOST` | `[stores]` | `host` (hostname portion) |
| `LANDSCAPE_DATABASE_RESOURCE_PORT` | `[stores]` | `host` (port portion), default `5432` |
| `LANDSCAPE_DATABASE_RESOURCE_USER` | `[stores]` | `user` |
| `LANDSCAPE_DATABASE_RESOURCE_PASSWORD` | `[stores]` | `password` (base64-decoded) |
| `LANDSCAPE_DATABASE_RESOURCE_SSL` | `[stores]` | `sslmode`, default `prefer` |
| `LANDSCAPE_DATABASE_RESOURCE_SSL_ROOT_CERT` | `[stores]` | `sslrootcert` |
| `LANDSCAPE_DATABASE_RESOURCE_SSL_CERT` | `[stores]` | `sslcert` |
| `LANDSCAPE_DATABASE_RESOURCE_SSL_KEY` | `[stores]` | `sslkey` |

## `landscape-task-handler.server` and `landscape-task-handler.worker` services

### Database settings

The task handler service connects to four PostgreSQL databases. Three of these (`MAIN`, `ACCOUNT`, `RESOURCE`) are the Landscape server databases and can be populated from `service.conf`. The fourth (`TASK_HANDLER`) is the task handler's own database and must be configured directly.

Each database is configured with the same set of keys; replace `<DB>` below with `TASK_HANDLER`, `MAIN`, `ACCOUNT`, or `RESOURCE` when setting the environment variable. Replace `<db>` with `task-handler`, `main`, `account`, or `resource` when setting the snap key. Note that environment variables and snap keys are case-sensitive.

#### `LANDSCAPE_DATABASE_<DB>_NAME`

- Purpose: The PostgreSQL database name to connect to.
- Snap key: `landscape.database.<db>.name`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

#### `LANDSCAPE_DATABASE_<DB>_HOST`

- Purpose: The hostname or IP address of the PostgreSQL server.
- Snap key: `landscape.database.<db>.host`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

#### `LANDSCAPE_DATABASE_<DB>_PORT`

- Purpose: The port on which the PostgreSQL server is listening.
- Snap key: `landscape.database.<db>.port`
- Default: `5432`
- Required: Yes
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

#### `LANDSCAPE_DATABASE_<DB>_USER`

- Purpose: The username used to authenticate with the PostgreSQL server.
- Snap key: `landscape.database.<db>.user`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

#### `LANDSCAPE_DATABASE_<DB>_PASSWORD`

- Purpose: The password used to authenticate with the PostgreSQL server. Required unless SSL client certificate authentication is configured (both `SSL_CERT` and `SSL_KEY` are set).
- Snap key: `landscape.database.<db>.password`
- Default: None
- Required: No
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

#### `LANDSCAPE_DATABASE_<DB>_SSL`

- Purpose: The SSL mode to use when connecting to PostgreSQL. Valid values are `disable`, `allow`, `prefer`, `require`, `verify-ca`, and `verify-full`.
- Snap key: `landscape.database.<db>.ssl`
- Default: `prefer`
- Required: Yes
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

#### `LANDSCAPE_DATABASE_<DB>_SSL_ROOT_CERT`

- Purpose: Path to the root CA certificate file used to verify the server's certificate. Required when `SSL` is set to `verify-ca` or `verify-full`.
- Snap key: `landscape.database.<db>.ssl-root-cert`
- Default: None
- Required: No
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

#### `LANDSCAPE_DATABASE_<DB>_SSL_CERT`

- Purpose: Path to the client certificate file used for SSL client certificate authentication. Must be set together with `SSL_KEY`.
- Snap key: `landscape.database.<db>.ssl-cert`
- Default: None
- Required: No
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

#### `LANDSCAPE_DATABASE_<DB>_SSL_KEY`

- Purpose: Path to the private key file for the client certificate. Must be set together with `SSL_CERT`.
- Snap key: `landscape.database.<db>.ssl-key`
- Default: None
- Required: No
- `service.conf`-supplied: Yes (except `TASK_HANDLER`)

### Server settings

These settings apply to the `landscape-task-handler.server` service only.

#### `LANDSCAPE_TASK_HANDLER_SERVER_HOST`

- Purpose: The hostname or IP address the gRPC server binds to.
- Snap key: `landscape.task-handler.server.host`
- Default: None
- Required: Yes
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_SERVER_GRPC_PORT`

- Purpose: The port on which the gRPC server listens.
- Snap key: `landscape.task-handler.server.grpc-port`
- Default: `50051`
- Required: Yes
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_SERVER_DB_POOL_SIZE`

- Purpose: The maximum number of database connections the server maintains in its connection pool.
- Snap key: `landscape.task-handler.server.db-pool-size`
- Default: `20`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_SERVER_CONN_MAX_LIFETIME`

- Purpose: The maximum length of time a database connection in the server pool may be reused. Accepts Go duration strings.
- Snap key: `landscape.task-handler.server.conn-max-lifetime`
- Default: `5m`
- Required: No
- `service.conf`-supplied: No

(landscape-task-handler-grpc-certs-dir)=
#### `LANDSCAPE_TASK_HANDLER_GRPC_CERTS_DIR`

- Purpose: Path to the directory containing the gRPC mTLS certificates. When unset, defaults to the auto-generated location under `$SNAP_COMMON/certs/active`.
- Snap key: `landscape.task-handler.grpc.certs-dir`
- Default: `$SNAP_COMMON/certs/active`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_GRPC_ALLOWED_CLIENT_CNS`

- Purpose: Comma-separated list of client certificate common names (CNs) that are permitted to connect to the gRPC server.
- Snap key: `landscape.task-handler.grpc.allowed-client-cns`
- Default: `landscape-outbox`
- Required: No
- `service.conf`-supplied: No

### Worker settings

These settings apply to the `landscape-task-handler.worker` service only.

#### `LANDSCAPE_TASK_HANDLER_WORKER_BATCH_SIZE`

- Purpose: The maximum number of task entries to dequeue and process in a single iteration of the worker loop.
- Snap key: `landscape.task-handler.worker.batch-size`
- Default: `10`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_WORKER_SLEEP`

- Purpose: A fixed delay introduced between every worker loop iteration, regardless of whether entries were found. Accepts Go duration strings (for example `500ms`, `1s`).
- Snap key: `landscape.task-handler.worker.sleep`
- Default: `5s`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_WORKER_MAX_RETRIES`

- Purpose: The maximum number of times the worker will retry a failed task before marking it as permanently failed. When unset, retries are unlimited.
- Snap key: `landscape.task-handler.worker.max-retries`
- Default: None (unlimited)
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_WORKER_LEASE_DURATION`

- Purpose: How long a claimed task is leased to this worker before it can be reclaimed by another worker. Accepts Go duration strings.
- Snap key: `landscape.task-handler.worker.lease-duration`
- Default: `2m`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_WORKER_LEASE_RESET_INTERVAL`

- Purpose: How often the worker scans for tasks with expired leases and makes them available for reprocessing. Accepts Go duration strings.
- Snap key: `landscape.task-handler.worker.lease-reset-interval`
- Default: `5m`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_WORKER_CONCURRENCY`

- Purpose: The number of tasks the worker processes concurrently.
- Snap key: `landscape.task-handler.worker.concurrency`
- Default: `4`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TASK_HANDLER_WORKER_CONN_MAX_LIFETIME`

- Purpose: The maximum length of time a database connection in the worker pool may be reused. Accepts Go duration strings.
- Snap key: `landscape.task-handler.worker.conn-max-lifetime`
- Default: `5m`
- Required: No
- `service.conf`-supplied: No

### Logging settings

#### `LANDSCAPE_LOGGING_LEVEL`

- Purpose: The minimum log level for the service. Valid values are `trace`, `debug`, `info`, `warn`, `error`, and `fatal`.
- Snap key: `landscape.logging.level`
- Default: `info`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_LOGGING_HUMAN_READABLE`

- Purpose: When `true`, log output is formatted for human readability. When `false`, logs are emitted as structured JSON.
- Snap key: `landscape.logging.human-readable`
- Default: `false`
- Required: No
- `service.conf`-supplied: No

### Service identity settings

These settings identify the service instance to telemetry and observability systems. They are optional; if unset, the corresponding fields are omitted from telemetry data.

#### `LANDSCAPE_SERVICE_NAME`

- Purpose: The name reported by this service instance to the telemetry backend.
- Snap key: `landscape.service.name`
- Default: None
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_SERVICE_VERSION`

- Purpose: The version string reported by this service instance to the telemetry backend.
- Snap key: None (set automatically by the snap)
- Default: None
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_SERVICE_NAMESPACE`

- Purpose: The namespace reported by this service instance to the telemetry backend.
- Snap key: `landscape.service.namespace`
- Default: None
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_SERVICE_ENVIRONMENT`

- Purpose: The environment name (for example `production` or `staging`) reported by this service instance to the telemetry backend.
- Snap key: `landscape.service.environment`
- Default: None
- Required: No
- `service.conf`-supplied: No

### Telemetry settings

#### `LANDSCAPE_TELEMETRY_ENDPOINT`

- Purpose: The OTLP endpoint URL to which the service sends telemetry data (traces and metrics). When unset, telemetry is disabled.
- Snap key: `landscape.telemetry.endpoint`
- Default: None
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_TELEMETRY_METRICS_INTERVAL`

- Purpose: How often the service reports metrics to the telemetry backend. Accepts Go duration strings.
- Snap key: `landscape.telemetry.metrics-interval`
- Default: `30s`
- Required: No
- `service.conf`-supplied: No

## mTLS certificate management

The task handler gRPC server and its clients (such as the outbox) communicate over mutual TLS (mTLS). The snap manages the certificate material under `$SNAP_COMMON` (typically `/var/snap/landscape-task-handler/common`).

### Auto-generated certificates

By default, the `landscape-task-handler.cert-renewer` service automatically generates a self-signed CA, a server certificate, and a client certificate. These are written to the active directory:

```text
$SNAP_COMMON/certs/active/
    ca.crt          # CA certificate (server-side trust anchor)
    server.crt      # gRPC server certificate
    server.key      # gRPC server private key
    client/
        ca.crt      # CA certificate (client-side trust anchor, exposed to outbox)
        client.crt  # gRPC client certificate (exposed to outbox)
        client.key  # gRPC client private key (exposed to outbox)
```

Auto-generated certificates have a 90-day lifetime and are rotated automatically when fewer than 30 days remain. The `landscape-task-handler.cert-renewer` timer runs once per day to check for rotation.

The `$SNAP_COMMON/certs/active/client/` directory is exposed to the outbox snap via the `grpc-client-certs` snap content slot, so the outbox can read the client certificates without any manual copying.

### Operator-provided certificates

To use your own certificates instead of the auto-generated ones, place all five of the following files in `$SNAP_COMMON/custom-certs/`:

| File | Contents |
| --- | --- |
| `ca.crt` | CA certificate (PEM) |
| `server.crt` | Server certificate (PEM), must chain to `ca.crt` |
| `server.key` | Server private key (PEM) |
| `client.crt` | Client certificate (PEM), must chain to `ca.crt` |
| `client.key` | Client private key (PEM) |

All five files must be present; a partial set is ignored. On the next cert-manager run (which happens on every service start, snap refresh, and daily rotation), the certificates are validated, copied into the active directory, and a `.custom-managed` sentinel file is written.

```{important}
Once the `.custom-managed` sentinel is present, removing the files from `custom-certs/` will cause the cert-manager to error rather than fall back to auto-generated certificates. To revert to auto-generated certificates, remove both the `custom-certs/` files and the `.custom-managed` sentinel from `$SNAP_COMMON/certs/active/`.
```

There are no snap keys for providing certificate content directly; operator certificates must be placed on the filesystem as described above.

### Overriding the active certificate directory

If you manage certificate placement outside of the snap's cert-manager (for example, via a secrets management system), you can tell the server where to find the active certificates using the `LANDSCAPE_TASK_HANDLER_GRPC_CERTS_DIR` environment variable or its snap key equivalent. See [`LANDSCAPE_TASK_HANDLER_GRPC_CERTS_DIR`](#landscape-task-handler-grpc-certs-dir) in the server settings above.

Because `landscape-task-handler` is strictly confined, the snap can only read files from paths it has been granted access to. The snap ships with no `system-files` plug beyond `etc-landscape` (scoped to `/etc/landscape`), so any override path must be within `$SNAP_COMMON` or a subdirectory of `/etc/landscape`. The practical options are to write certificates directly to `$SNAP_COMMON/certs/active/`, use the `custom-certs/` mechanism described above, or place certificates under `/etc/landscape/` (for example `/etc/landscape/task-handler-certs/`).

## `landscape-task-handler.cleanup` service

The cleanup service purges old task handler entries from the database on a periodic schedule. It shares logging configuration with the main task handler services but uses only the task handler's own database.

### Database settings

The cleanup service connects only to the task handler database (`LANDSCAPE_DATABASE_TASK_HANDLER_*`). The configuration keys are identical to those described in the [server and worker database settings](#database-settings) above.

The cleanup service does not use the main, account, or resource databases.

### Logging settings

The cleanup service uses the same `LANDSCAPE_LOGGING_LEVEL` and `LANDSCAPE_LOGGING_HUMAN_READABLE` environment variables described in [logging settings](#logging-settings) above.

### Cleanup settings

#### `LANDSCAPE_CLEANUP_FAILED_RETENTION_DURATION`

- Purpose: How long to retain failed task handler entries before they are eligible for deletion. Accepts Go duration strings.
- Snap key: `landscape.cleanup.failed-retention-duration`
- Default: `720h` (30 days)
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_CLEANUP_BATCH_SIZE`

- Purpose: The maximum number of entries to delete in a single database operation.
- Snap key: `landscape.cleanup.batch-size`
- Default: `50`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_CLEANUP_BATCH_SLEEP`

- Purpose: The duration the cleanup job sleeps between successive delete batches. Accepts Go duration strings.
- Snap key: `landscape.cleanup.batch-sleep`
- Default: `50ms`
- Required: No
- `service.conf`-supplied: No
