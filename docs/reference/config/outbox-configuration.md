---
myst:
  html_meta:
    description: "Technical reference for Landscape Outbox configuration including all environment variables, snap configuration keys, and defaults."
---

(reference-outbox-configuration)=
# Landscape Outbox configuration reference

The Landscape Outbox service is configured entirely through environment variables. There is no separate configuration file format; all settings are expressed as environment variables, which can be supplied directly or through the snap configuration system.

The outbox snap (`landscape-outbox`) provides two services:

- **`landscape-outbox.outbox`**: the main outbox daemon that reads pending entries from the database and publishes them to downstream systems.
- **`landscape-outbox.cleanup`**: a periodic cleanup job that purges old outbox entries from the database.

Each service has its own set of environment variables, described in the sections below.

## `service.conf` integration

The outbox needs to use the same database and broker systems that Landscape server uses. By default, the outbox will read all necessary database and broker configurations from `/etc/landscape/service.conf` and will populate the correspdonding environment variables. The path to the `service.conf` file can be overridden via the `LANDSCAPE_CONFIG_FILE` environment variable or equivalently the `landscape.service-conf-file` snap key.

This means that several environment variables marked as **required** in this reference do not need to be set directly and can instead be read from the `service.conf`. These configurations are marked with **`service.conf-supplied`: Yes**. It is recommended to use this integration instead of setting these environment variables directly.

The table below lists every environment variable that is populated. Note that all three databases share the same host, port, user, password, and SSL settings from the `[stores]` section.

| Environment variable | `service.conf` section | `service.conf` key |
|---|---|---|
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
| `LANDSCAPE_BROKER_HOST` | `[broker]` | `host` |
| `LANDSCAPE_BROKER_PORT` | `[broker]` | `port`, default `5672` |
| `LANDSCAPE_BROKER_USER` | `[broker]` | `user` |
| `LANDSCAPE_BROKER_PASSWORD` | `[broker]` | `password` (base64-decoded) |
| `LANDSCAPE_BROKER_VHOST` | `[broker]` | `vhost` |
| `LANDSCAPE_BROKER_SSL_CA_CERT` | `[broker]` | `ssl_client_ca_cert` |
| `LANDSCAPE_BROKER_SSL_CERT` | `[broker]` | `ssl_client_cert` |
| `LANDSCAPE_BROKER_SSL_KEY` | `[broker]` | `ssl_client_private_key` |

## `landscape-outbox.outbox` service

### Database settings

The outbox service connects to three PostgreSQL databases. Each database is configured with the same set of keys; replace `<DB>` below with `MAIN`, `ACCOUNT`, or `RESOURCE` when setting the environment variable. Replace `<db>` with `main`, `account`, or `resource` when setting the snap key. Note that environment variables and snap keys are case-sensitive.

#### `LANDSCAPE_DATABASE_<DB>_NAME`

- Purpose: The PostgreSQL database name to connect to.
- Snap key: `landscape.database.<db>.name`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_DATABASE_<DB>_HOST`

- Purpose: The hostname or IP address of the PostgreSQL server.
- Snap key: `landscape.database.<db>.host`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_DATABASE_<DB>_PORT`

- Purpose: The port on which the PostgreSQL server is listening.
- Snap key: `landscape.database.<db>.port`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_DATABASE_<DB>_USER`

- Purpose: The username used to authenticate with the PostgreSQL server.
- Snap key: `landscape.database.<db>.user`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_DATABASE_<DB>_PASSWORD`

- Purpose: The password used to authenticate with the PostgreSQL server. Required unless SSL client certificate authentication is configured (both `SSL_CERT` and `SSL_KEY` are set).
- Snap key: `landscape.database.<db>.password`
- Default: None
- Required: No
- `service.conf`-supplied: Yes

#### `LANDSCAPE_DATABASE_<DB>_SSL`

- Purpose: The SSL mode to use when connecting to PostgreSQL. Valid values are `disable`, `allow`, `prefer`, `require`, `verify-ca`, and `verify-full`.
- Snap key: `landscape.database.<db>.ssl`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_DATABASE_<DB>_SSL_ROOT_CERT`

- Purpose: Path to the root CA certificate file used to verify the server's certificate. Required when `SSL` is set to `verify-ca` or `verify-full`.
- Snap key: `landscape.database.<db>.ssl-root-cert`
- Default: None
- Required: No
- `service.conf`-supplied: Yes

#### `LANDSCAPE_DATABASE_<DB>_SSL_CERT`

- Purpose: Path to the client certificate file used for SSL client certificate authentication. Must be set together with `SSL_KEY`.
- Snap key: `landscape.database.<db>.ssl-cert`
- Default: None
- Required: No
- `service.conf`-supplied: Yes

#### `LANDSCAPE_DATABASE_<DB>_SSL_KEY`

- Purpose: Path to the private key file for the client certificate. Must be set together with `SSL_CERT`.
- Snap key: `landscape.database.<db>.ssl-key`
- Default: None
- Required: No
- `service.conf`-supplied: Yes

### Broker settings

#### `LANDSCAPE_BROKER_HOST`

- Purpose: The hostname or IP address of the AMQP broker (RabbitMQ).
- Snap key: `landscape.broker.host`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_BROKER_PORT`

- Purpose: The port on which the AMQP broker is listening.
- Snap key: `landscape.broker.port`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_BROKER_USER`

- Purpose: The username used to authenticate with the AMQP broker.
- Snap key: `landscape.broker.user`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_BROKER_PASSWORD`

- Purpose: The password used to authenticate with the AMQP broker. Required unless SSL client certificate authentication is configured (both `SSL_CERT` and `SSL_KEY` are set).
- Snap key: `landscape.broker.password`
- Default: None
- Required: No
- `service.conf`-supplied: Yes

#### `LANDSCAPE_BROKER_VHOST`

- Purpose: The virtual host namespace to use on the AMQP broker.
- Snap key: `landscape.broker.vhost`
- Default: None
- Required: Yes
- `service.conf`-supplied: Yes

#### `LANDSCAPE_BROKER_SSL_CA_CERT`

- Purpose: Path to the CA certificate file used to verify the broker's TLS certificate. When any SSL variable is set, the connection uses the `amqps` scheme.
- Snap key: `landscape.broker.ssl-ca-cert`
- Default: None
- Required: No
- `service.conf`-supplied: Yes

#### `LANDSCAPE_BROKER_SSL_CERT`

- Purpose: Path to the client certificate file used for mTLS authentication with the broker. Must be set together with `SSL_KEY`.
- Snap key: `landscape.broker.ssl-cert`
- Default: None
- Required: No
- `service.conf`-supplied: Yes

#### `LANDSCAPE_BROKER_SSL_KEY`

- Purpose: Path to the private key file for the broker client certificate. Must be set together with `SSL_CERT`.
- Snap key: `landscape.broker.ssl-key`
- Default: None
- Required: No
- `service.conf`-supplied: Yes

### Worker settings

#### `LANDSCAPE_WORKER_BATCH_SIZE`

- Purpose: The maximum number of outbox entries to read and publish in a single iteration of the worker loop.
- Snap key: `landscape.worker.batch-size`
- Default: `50`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_WORKER_SLEEP`

- Purpose: A fixed delay introduced between every worker loop iteration, regardless of whether entries were found. Accepts Go duration strings (for example `500ms`, `1s`).
- Snap key: `landscape.worker.sleep`
- Default: `0s`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_WORKER_IDLE_SLEEP`

- Purpose: The duration the worker sleeps between iterations when no outbox entries were found in the previous iteration. Accepts Go duration strings.
- Snap key: `landscape.worker.idle-sleep`
- Default: `1s`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_WORKER_QUEUE_SLEEP`

- Purpose: The duration the worker sleeps between iterations when the broker's publish queue is full. Accepts Go duration strings.
- Snap key: `landscape.worker.queue-sleep`
- Default: `1s`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_WORKER_MAX_RETRIES`

- Purpose: The maximum number of times the worker will retry publishing a single outbox entry before marking it as failed.
- Snap key: `landscape.worker.max-retries`
- Default: `3`
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
- Snap key: `landscape.service.version`
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

## `landscape-outbox.cleanup` service

The cleanup service purges old outbox entries from the database on a periodic schedule. It shares the database and logging configuration with the main outbox service but does not connect to the broker.

### Database settings

The cleanup service connects to two PostgreSQL databases: `main` and `account`. The configuration keys are identical to those described in the [outbox service database settings](#database-settings) above, using `LANDSCAPE_DATABASE_MAIN_*` and `LANDSCAPE_DATABASE_ACCOUNT_*`.

The cleanup service does not use the resource database.

### Logging settings

The cleanup service uses the same `LANDSCAPE_LOGGING_LEVEL` and `LANDSCAPE_LOGGING_HUMAN_READABLE` environment variables described in [logging settings](#logging-settings) above.

### Cleanup settings

#### `LANDSCAPE_CLEANUP_SENT_RETENTION_DURATION`

- Purpose: How long to retain successfully sent outbox entries before they are eligible for deletion. Accepts Go duration strings.
- Snap key: `landscape.cleanup.sent-retention-duration`
- Default: `24h`
- Required: No
- `service.conf`-supplied: No

#### `LANDSCAPE_CLEANUP_FAILED_RETENTION_DURATION`

- Purpose: How long to retain failed outbox entries before they are eligible for deletion. Accepts Go duration strings.
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
