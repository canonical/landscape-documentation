(reference-service-conf)=

# The `service.conf` file

All Landscape service configurations are defined in the `service.conf` file. This file follows the `INI` file format. The default location for this file is `/etc/landscape/service.conf`. You can override that by setting the `LANDSCAPE_SERVICE_CONF` environment variable with the file path location of the `service.conf` file.

Changes to the `service.conf` file only take affect once you restart the relevant service(s).

Starting with Landscape 25.10, every entry in the `service.conf` file can be overridden by a corresponding environment variable. These variables have the following general structure: `LANDSCAPE_SECTION_NAME__KEY_NAME`.

The sections below contain information about the key-value pairs that can be set in each section, the corresponding environment variable, the default value (if any), and the purpose of the entry.

```{note}
The usage of the `-` character in section names and key names is deprecated in Landscape Server 25.10 in favor of the `_` character. Support for the `-` character will be removed in Landscape Server 26.04.

In addition, the names of some sections of the `service.conf` file are deprecated in Landscape Server 25.10. The new names are detailed below. Support for the deprecated names will be removed in Landscape Server 26.04.
```

## The `[system]` section

```{note}
The `[global]` section name is deprecated. The `[system]` section replaces the `[global]` section.
```

The `[system]` section contains configurations that apply across many or all of Landscape's services.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `analytics_id` | - | `LANDSCAPE_SYSTEM__ANALYTICS_ID` | `UA-1018242-60` | Google Analytics tracker ID for the deployment. |
| `apt_port` | - | `LANDSCAPE_SYSTEM__APT_PORT` | 8085 | The port the `landscape_apt` service should use. |
| `audit_retention_period` | `audit-retention-period` | `LANDSCAPE_SYSTEM__AUDIT_RETENTION_PERIOD` | `-1` | The time period in days to retain security profile audit records. A negative value means that records should be retained indefinitely. |
| `deployment_mode` | `deployment-mode` | `LANDSCAPE_SYSTEM__DEPLOYMENT_MODE` | `standalone` | Used only for development. The default value is appropriate for self-hosted Landscape. |
| `fqdn` | - | `LANDSCAPE_SYSTEM__FQDN` | `None` | Sets the root URL using the FQDN. |
| `gpg_home_dir` | - | `LANDSCAPE_SYSTEM__GPG_HOME_DIR` | `/var/lib/landscape-server/gnupg` | The directory containing GnuPG config files and the {spellexception}`keyrings`. |
| `license_file` | - | `LANDSCAPE_SYSTEM__LICENSE_FILE` | `/etc/landscape/license.txt` | The file path location of the license file. |
| {spellexception}`pidfile_directory` | {spellexception}`pidfile-directory` | {spellexception}`LANDSCAPE_SYSTEM__PIDFILE_DIRECTORY` | `/tmp/landscape` | Unused |
| `max_service_memory` | `max-service-memory` | `LANDSCAPE_SYSTEM__MAX_SERVICE_MEMORY` | `0` | An upper limit (in {spellexception}`mebibytes`) for the memory usage by a Landscape service. Services exceeding this limit will restart. A value of `0` means there is no limit. |
| `middleware` | - | `LANDSCAPE_SYSTEM__MIDDLEWARE` | `None` | The python dotted name to the middleware function or class to use. Multiple values can be provided by separating them with a comma. |
| `offline` | - | `LANDSCAPE_SYSTEM__OFFLINE` | `None` | Set `True` if Landscape is deployed in an air-gapped environment. |
| `oops_path` | `oops-path` | `LANDSCAPE_SYSTEM__OOPS_PATH` | `/var/lib/landscape/landscape-oops` | The directory where OOPS reports are stored. The `landscape` system user must have read/write access to the specified directory. |
| `root_url` | `root-url` | `LANDSCAPE_SYSTEM__ROOT_URL` | `http://localhost:8080` | Landscape Server's root URL path. |
| `syslog_address` | `syslog-address` | `LANDSCAPE_SYSTEM__SYSLOG_ADDRESS` | `/dev/log` | Path to the system's syslog logger. |

## The `[async_frontend]` section

```{note}
The `[async-frontend]` section name is deprecated. The `[async_frontend]` section replaces the `[async-frontend]` section.
```

The `[async_frontend]` section contains configurations that apply to the `landscape-async-frontend` service which handles AJAX requests from the Legacy UI. It has no settings beyond those shared by all services.

In practice, only the `base_port` setting needs to be configured for the service to operate correctly.

## The `[broker]` section

The `[broker]` section contains configurations that describe how services connect to our message queues.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `host` | - | `LANDSCAPE_BROKER__HOST` | `localhost` | The hostname or IP address of the message broker server. |
| `hostagent_command_status_queue` | - | `LANDSCAPE_BROKER__HOSTAGENT_COMMAND_STATUS_QUEUE` | `landscape-server-hostagent-command-status-queue` | Queue for sending command status updates from the hostagent server to the hostagent consumer. |
| `hostagent_ping_queue` | - | `LANDSCAPE_BROKER__HOSTAGENT_PING_QUEUE` | `landscape-server-hostagent-ping-queue` | Queue for sending pings from the hostagent server to the hostagent consumer. |
| `hostagent_task_queue` | - | `LANDSCAPE_BROKER__HOSTAGENT_TASK_QUEUE` | `landscape-server-hostagent-task-queue` | Queue for sending tasks from the hostagent consumer to the hostagent server. |
| `hostagent_virtual_host` | - | `LANDSCAPE_BROKER__HOSTAGENT_VIRTUAL_HOST` | `landscape-hostagent` | The virtual host of message queues for the hostagent message server and consumer. This provides support for Landscape integration with Ubuntu Pro for WSL. |
| `password` | - | `LANDSCAPE_BROKER__PASSWORD` | `guest` | Password used to authenticate with the message broker. |
| `port` | - | `LANDSCAPE_BROKER__PORT` | 5672 | Network port where message broker server is listening. |
| `user` | - | `LANDSCAPE_BROKER__USER` | `guest` | Username used to authenticate with the message broker. |
| `vhost` | - | `LANDSCAPE_BROKER__VHOST` | `landscape` | The virtual host namespace. |

## The `[job_handler]` section

```{note}
The `[job-handler]` section name is deprecated. The `[job_handler]` section replaces the `[job-handler]` section.
```

The `[job_handler]` section contains configurations for the `landscape-job-handler` service which runs background jobs. It has no settings beyond those shared by all services.

In practice, only the `base_port` setting needs to be configured for the service to operate correctly.

## The `[message_server]` section

```{note}
The `[message-server]` section name is deprecated. The `[message_server]` section replaces the `[message-server]` section.
```

The `[message_server]` section contains configurations that apply to the `landscape-message-server` service that handles messages from instances running Landscape Client.

It has the following settings beyond those shared by all services.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `max_msg_size_bytes` | `max-msg-size-bytes` | `LANDSCAPE_MESSAGE_SERVER__MAX_MSG_SIZE_BYTES` | 30000000 (30 MB) | The maximum size, in bytes, of a message from Landscape Client that Landscape Server will accept. Messages larger than this size will be rejected. |
| `message_snippet_bytes` | `message-snippet-bytes` | `LANDSCAPE_MESSAGE_SERVER__MESSAGE_SNIPPET_BYTES` | 1000 | When Landscape Server receives a message larger than `max_msg_size_bytes`, it will log an error including the first `message_snippet_bytes` of the message. |
| `message_system_url` | - | `LANDSCAPE_MESSAGE_SERVER__MESSAGE_SYSTEM_URL` | `None` | The message system URL to use. |
| `ping_interval` | `ping-interval` | `LANDSCAPE_MESSAGE_SERVER__PING_INTERVAL` | `None` | Landscape Server will instruct Landscape Client to send a ping message every `ping_interval` seconds.  |

## The `[stores]` section

The `[stores]` section contains configurations for database store connections and SSL settings used across Landscape services.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `account_1` | `account-1` | `LANDSCAPE_STORES__ACCOUNT_1` | `landscape-standalone-account-1` | The first account database store name. |
| `account_2` | `account-2` | `LANDSCAPE_STORES__ACCOUNT_2` | `None` | The second account database store name. Optional. |
| `host` | - | `LANDSCAPE_STORES__HOST` | `localhost` | The hostname or IP address of the database server. |
| `knowledge` | - | `LANDSCAPE_STORES__KNOWLEDGE` | `landscape-standalone-knowledge` | The knowledge database name. |
| `main` | - | `LANDSCAPE_STORES__MAIN` | `landscape-standalone-main` | The main database name. |
| `package` | - | `LANDSCAPE_STORES__PACKAGE` | `landscape-standalone-package` | The package database name. |
| `password` | - | `LANDSCAPE_STORES__PASSWORD` | `None` | The password for database connections. |
| `resource_1` | `resource-1` | `LANDSCAPE_STORES__RESOURCE_1` | `landscape-standalone-resource-1` | The first resource database name. |
| `resource_2` | `resource-2` | `LANDSCAPE_STORES__RESOURCE_2` | `None` | The second resource database name. Optional and used for testing only. |
| `session` | - | `LANDSCAPE_STORES__SESSION` | `landscape-standalone-session` | The session database name. |
| `session_autocommit` | `session-autocommit` | `LANDSCAPE_STORES__SESSION_AUTOCOMMIT` | `landscape-standalone-session` | The name of the session database with {spellexception}`autocommit` isolation. |
| `sslcert` | - | `LANDSCAPE_STORES__SSLCERT` | `None` | Path to the client certificate to use for SSL connection to Postgres (becomes `PGSSLCERT`). |
| `sslkey` | - | `LANDSCAPE_STORES__SSLKEY` | `None` | Path to the private key to use for SSL connection to Postgres (becomes `PGSSLKEY`). |
| `sslmode` | - | `LANDSCAPE_STORES__SSLMODE` | `None` | SSL mode when connecting to Postgres, for example `verify-full`. |
| `sslrootcert` | - | `LANDSCAPE_STORES__SSLROOTCERT` | `None` | Path to the root CA certificate to use for SSL connection to Postgres (becomes `PGSSLROOTCERT`). |
| `store_password` | - | `LANDSCAPE_STORES__STORE_PASSWORD` | `None` | Overrides the store password. |
| `store_user` | - | `LANDSCAPE_STORES__STORE_USER` | `None` | Overrides the store username. |
| `stores` | - | `LANDSCAPE_STORES__STORES` | `None` | The stores the service should use. |
| `user` | - | `LANDSCAPE_STORES__USER` | `landscape` | The username for database connections. |
