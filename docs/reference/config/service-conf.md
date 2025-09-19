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

(shared-service-settings)=

## Shared service settings

There are a set of generic settings that all services can set, where `SERVICE` in the ENV name matches the (uppercase) name of the service.

### `allowed_interfaces`

- Purpose: A list of allowed IP addresses or hostnames for the service.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SERVICE__ALLOWED_INTERFACES`
- Default: `None`

### `base_port`

- Purpose: Workers for the service will run on ports incrementing from this base port.
- Deprecated key name: `base-port`
- ENV name: `LANDSCAPE_SERVICE__BASE_PORT`
- Default: `8090`

### `devmode`

- Purpose: To control development mode configuration. This setting should not be configured in production environments.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SERVICE__DEVMODE`
- Default: `None`

### `enable_metrics`

- Purpose: Whether to enable metrics collection for the service.
- Deprecated key name: `enable-metrics`
- ENV name: `LANDSCAPE_SERVICE__ENABLE_METRICS`
- Default: `False`

### `gpg_home_path`

- Purpose: Sets the path to the GPG home directory.
- Deprecated key name: `gpg-home-path`
- ENV name: `LANDSCAPE_SERVICE__GPG_HOME_PATH`
- Default: `None`

### `gpg_passphrase_path`

- Purpose: Sets the path to the GPG passphrase file. Required if `gpg_home_path` is set.
- Deprecated key name: `gpg-passphrase-path`
- ENV name: `LANDSCAPE_SERVICE__GPG_PASSPHRASE_PATH`
- Default: `None`

### `mailer`

- Purpose: If set to `queue` the mailer will use the queue specified by the `mailer_path`. If set to `default` the queue will be at `/tmp/landscape-mail-queue`. If unset, no mailer will be configured for the service. Production deployments do not need to modify this setting.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SERVICE__MAILER`
- Default: `None`

### `mailer_path`

- Purpose: Path to the mail queue. Required if `mailer` is set.
- Deprecated key name: `mailer-path`
- ENV name: `LANDSCAPE_SERVICE__MAILER_PATH`
- Default: `None`

### `oops_key`

- Purpose: Key for OOPS error reporting system. Production deployments do not need to modify this setting.
- Deprecated key name: `oops-key`
- ENV name: `LANDSCAPE_SERVICE__OOPS_KEY`
- Default: `None`

### `root_url`

- Purpose: The URL for the service.
- Deprecated key name: `root-url`
- ENV name: `LANDSCAPE_SERVICE__ROOT_URL`
- Default: `None`

### `soft_timeout`

- Purpose: Soft timeout value in seconds for the OOPS reporter.
- Deprecated key name: `soft-timeout`
- ENV name: `LANDSCAPE_SERVICE__SOFT_TIMEOUT`
- Default: `None`

### `ssl_server_cert`

- Purpose: Sets the path to the certificate to use for mTLS. If set, `ssl_private_key` must also be set.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SERVICE__SSL_SERVER_CERT`
- Default: `None`

### `ssl_private_key`

- Purpose: Sets the path to the private key to use for mTLS. If set, `ssl_server_cert` must also be set.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SERVICE__SSL_PRIVATE_KEY`
- Default: `None`

### `ssl_ca_cert`

- Purpose: Sets the path to the CA to use for mTLS. If set, both `ssl_private_key` and `ssl_server_cert` must also be set.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SERVICE__SSL_CA_CERT`
- Default: `None`

### `threads`

- Purpose: Number of threads for the service to use. This setting only applies to Twisted services.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SERVICE__THREADS`
- Default: `None`

### `workers`

- Purpose: Number of worker processes for the service. If unset, the service will have a single worker.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SERVICE__WORKERS`
- Default: `None`

```{important}
The shared service settings are not mutually exclusive with the shared store settings; services can use both, if specified.
```

(shared-store-settings)=

## Shared store settings

There are a set of generic settings related to databases and SSL connections to Postgres that several sections can set, where `SECTION` in the ENV name matches the (uppercase) name of the section:

### `sslcert`

- Purpose: Path to the client certificate to use for SSL connection to Postgres. Landscape Server will set this as the `PGSSLCERT` environment variable for Postgres to consume.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SECTION__SSLCERT`
- Default: `None`

### `sslkey`

- Purpose: Path to the private key to use for SSL connection to Postgres. Landscape Server will set this as the `PGSSLKEY` environment variable for Postgres to consume.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SECTION__SSLKEY`
- Default: `None`

### `sslmode`

- Purpose: SSL mode to use when connecting to Postgres, for example `verify-full`.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SECTION__SSLMODE`
- Default: `None`

### `sslrootcert`

- Purpose: Path to the root CA certificate to use for SSL connection to Postgres. Landscape Server will set this as the `PGSSLROOTCERT` environment variable for Postgres to consume.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SECTION__SSLROOTCERT`
- Default: `None`

### `store_password`

- Purpose: Overrides the store password set in the `store` settings.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SECTION__STORE_PASSWORD`
- Default: `None`

### `store_user`

- Purpose: Overrides the store username set in the `store` settings.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SECTION__STORE_USER`
- Default: `None`

### `stores`

- Purpose: The stores the service should use.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SECTION__STORES`
- Default: `None`

```{important}
The shared store settings are not mutually exclusive with the shared service settings; services can use both, if specified.
```

## The `[api]` section

The `[api]` section contains configurations for the Landscape API service, including service connection settings and database store configurations. In addition to the following, this section can use the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

### `cookie_encryption_key`

- Purpose: The key used to encrypt state and nonce cookies. Must be 32 url-safe, base64-encoded bytes. If unset, Landscape will generate and set a key using the Fernet symmetric encryption algorithm. If the key is invalid, the `landscape-api` service will fail to start.
- Deprecated key name: `cookie-encryption-key`
- ENV name: `LANDSCAPE_API__COOKIE_ENCRYPTION_KEY`
- Default: `None`

### `cors_allow_all`

- Purpose: This setting should only be enabled in a development environment. If `True`, the following headers will be set in HTTP responses from the API service:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS`
  - `Access-Control-Allow-Credentials: true`
- Deprecated key name: `cors-allow-all`
- ENV name: `LANDSCAPE_API__CORS_ALLOW_ALL`
- Default: `False`

### `snap_store_api_url`

- Purpose: The API for a Snap Store Proxy. By default, this is the Canonical Snap Store.
- Deprecated key name: `snap-store-api-url`
- ENV name: `LANDSCAPE_API__SNAP_STORE_API_URL`
- Default: `https://api.snapcraft.io/v2`

## The `[appserver]` section

```{note}
The `[landscape]` section name is deprecated. The `[appserver]` section replaces the `[landscape]` section.
```

The `[appserver]` section contains configurations for the Landscape application server, including storage paths and authentication providers. In addition to the following, this section can use the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `blob_storage_root` | `blob-storage-root` | `LANDSCAPE_APPSERVER__BLOB_STORAGE_ROOT` | `/var/lib/landscape/blobs` | Root directory for blob storage. |
| `display_consent_banner_at_each_login` | `display-consent-banner-at-each-login` | `LANDSCAPE_APPSERVER__DISPLAY_CONSENT_BANNER_AT_EACH_LOGIN` | `False` | Whether to display consent banner at each login. |
| `juju_homes_path` | `juju-homes-path` | `LANDSCAPE_APPSERVER__JUJU_HOMES_PATH` | `/var/tmp/juju-homes` | Path to Juju home directories. |
| `known_proxies` | `known-proxies` | `LANDSCAPE_APPSERVER__KNOWN_PROXIES` | `None` | Comma-separated names of known proxies. |
| `oidc_client_id` | `oidc-client-id` | `LANDSCAPE_APPSERVER__OIDC_CLIENT_ID` | `None` | OIDC client identifier. Required when using OIDC authentication. |
| `oidc_client_secret` | `oidc-client-secret` | `LANDSCAPE_APPSERVER__OIDC_CLIENT_SECRET` | `None` | OIDC client secret. Required when using OIDC authentication. |
| `oidc_issuer` | `oidc-issuer` | `LANDSCAPE_APPSERVER__OIDC_ISSUER` | `None` | OIDC issuer URL. Required when using OIDC authentication. |
| `oidc_provider` | `oidc-provider` | `LANDSCAPE_APPSERVER__OIDC_PROVIDER` | `unspecified` | The name of OIDC provider to use. Must be either `google`, `okta`, or `unspecified`. |
| `oidc_redirect_uri` | `oidc-redirect-uri` | `LANDSCAPE_APPSERVER__OIDC_REDIRECT_URI` | `None` | OIDC redirect URI for authentication callbacks. |
| `openid_logout_url` | `openid-logout-url` | `LANDSCAPE_APPSERVER__OPENID_LOGOUT_URL` | `None` | OpenID logout URL. Required when using OpenID authentication. |
| `openid_provider_url` | `openid-provider-url` | `LANDSCAPE_APPSERVER__OPENID_PROVIDER_URL` | `None` | OpenID provider URL. Required when using OpenID authentication. |
| `repository_path` | `repository-path` | `LANDSCAPE_APPSERVER__REPOSITORY_PATH` | `/tmp/landscape-repository` | Path to the package repository. |
| `reprepro_binary` | `reprepro-binary` | `LANDSCAPE_APPSERVER__REPREPRO_BINARY` | `None` | Path to the reprepro binary executable. |
| `sanitize_delay` | `sanitize-delay` | `LANDSCAPE_APPSERVER__SANITIZE_DELAY` | `3600` | Delay in seconds for data sanitization operations. |
| `secret_token` | `secret-token` | `LANDSCAPE_APPSERVER__SECRET_TOKEN` | `None` | Secret token for application security. |
| `ubuntu_images_path` | `ubuntu-images-path` | `LANDSCAPE_APPSERVER__UBUNTU_IMAGES_PATH` | `/var/tmp/ubuntu-images` | Path to Ubuntu images directory. |
| `ubuntu_one_redirect_url` | `ubuntu-one-redirect-url` | `LANDSCAPE_APPSERVER__UBUNTU_ONE_REDIRECT_URL` | `None` | Ubuntu One redirect URL for authentication. |

### Authentication providers

OpenID:

- Requires both `openid_provider_url` and `openid_logout_url` to be configured
- Defaults to using Ubuntu One

OIDC:

- Requires `oidc_issuer`, `oidc_client_id`, and `oidc_client_secret` to be configured

### Moved Configuration Keys

The following keys have moved from the `[appserver]` section to the `[system]` section in Landscape 25.10:

- `enable-password-authentication` → `enable_password_authentication` in `[system]`
- `enable-subdomain-accounts` → `enable_subdomain_accounts` in `[system]`
- `enable-saas-metrics` → `enable_saas_metrics` in `[system]`
- `enable-tag-script-execution` → `enable_tag_script_execution` in `[system]`

These keys can still be used in their deprecated forms in `[appserver]`/`[landscape]` until Landscape 26.04, when support will be removed and they must be configured in the `[system]` section.

## The `[async_frontend]` section

```{note}
The `[async-frontend]` section name is deprecated. The `[async_frontend]` section replaces the `[async-frontend]` section.
```

The `[async_frontend]` section contains configurations that apply to the `landscape-async-frontend` service which handles AJAX requests from the Legacy UI. It has no settings beyond the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

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

The `[job_handler]` section contains configurations for the `landscape-job-handler` service which runs background jobs. It has no settings beyond the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

In practice, only the `base_port` setting needs to be configured for the service to operate correctly.

## The `[load_shaper]` section

```{note}
The `[load-shaper]` section name is deprecated. The `[load_shaper]` section replaces the `[load-shaper]` section.
```

The `[load_shaper]` section contains configurations for controlling how many messages are processed in each message exchange. It allots a time window for message processing based on the current database load.

```{caution}
The default values have been chosen based on the underlying algorithm and typical workloads. Modifying these values is not advisable unless you have thoroughly tested the impact on your specific system, as changes can significantly affect performance and system stability.
```

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `critical_load` | `critical-load` | `LANDSCAPE_LOAD_SHAPER__CRITICAL_LOAD` | `10.0` | A float representing the database load threshold at which message processing time is reduced to zero. When load reaches this value, no time slice is allocated for processing. |
| `good_duration` | `good-duration` | `LANDSCAPE_LOAD_SHAPER__GOOD_DURATION` | `60.0` | A float representing the baseline time slice (in seconds) allocated for message processing when the database load is at the good load threshold. This duration is scaled up or down based on current load. |
| `good_load` | `good-load` | `LANDSCAPE_LOAD_SHAPER__GOOD_LOAD` | `3.0` | A float representing the optimal database load threshold. When load is at this value, the full good duration time slice is allocated. Load below this increases the time slice, load above this decreases it. |

## The `[maintenance]` section

The `[maintenance]` section contains configurations for running maintenance scripts. It has no settings beyond the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

## The `[message_server]` section

```{note}
The `[message-server]` section name is deprecated. The `[message_server]` section replaces the `[message-server]` section.
```

```{note}
The `[backoff]` section is deprecated. The settings have been moved to the `[message_server]` section.
```

The `[message_server]` section contains configurations that apply to the `landscape-message-server` service that handles messages from instances running Landscape Client. In addition to the following, this section can use the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `backoff_dir` | `backoff-dirpath` | `LANDSCAPE_MESSAGE_SERVER__BACKOFF_DIR` | `None` | The directory to hold the `backoff.txt` file the server uses to indicate it should back off requests. If `None`, a `config` directory within the `landscape` directory will be used. |
| `max_msg_size_bytes` | `max-msg-size-bytes` | `LANDSCAPE_MESSAGE_SERVER__MAX_MSG_SIZE_BYTES` | 30000000 (30 MB) | The maximum size, in bytes, of a message from Landscape Client that Landscape Server will accept. Messages larger than this size will be rejected. |
| `message_snippet_bytes` | `message-snippet-bytes` | `LANDSCAPE_MESSAGE_SERVER__MESSAGE_SNIPPET_BYTES` | 1000 | When Landscape Server receives a message larger than `max_msg_size_bytes`, it will log an error including the first `message_snippet_bytes` of the message. |
| `message_system_url` | - | `LANDSCAPE_MESSAGE_SERVER__MESSAGE_SYSTEM_URL` | `None` | The message system URL to use. |
| `ping_interval` | `ping-interval` | `LANDSCAPE_MESSAGE_SERVER__PING_INTERVAL` | `None` | Landscape Server will instruct Landscape Client to send a ping message every `ping_interval` seconds.  |

## The `[oops]` section

The `[oops]` section contains configurations for the OOPS error reporting and debugging system used for logging and traceback collection.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `amqp_exchange` | `amqp-exchange` | `LANDSCAPE_OOPS__AMQP_EXCHANGE` | `None` | AMQP exchange name for error reporting. |
| `amqp_key` | `amqp-key` | `LANDSCAPE_OOPS__AMQP_KEY` | `None` | AMQP routing key for error messages. Requires `amqp_exchange` to be set. |
| `directory` | - | `LANDSCAPE_OOPS__DIRECTORY` | `None` | Directory path for OOPS error report storage. |
| `path` | - | `LANDSCAPE_OOPS__PATH` | `None` | File path for OOPS configuration. |
| `reporter` | - | `LANDSCAPE_OOPS__REPORTER` | `None` | Error reporter configuration. |

The `[schema]` section contains configurations for updating the database schema. It has no settings beyond the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

## The `[package_upload]` section

```{note}
The `[package-upload]` section name is deprecated. The `[package_upload]` section replaces the `[package-upload]` section.
```

The `[package_upload]` section contains configurations for the package upload service, including service connection settings, database store configurations, and SSL options. In addition to the following, this section can use the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `port` | - | `LANDSCAPE_PACKAGE_UPLOAD__PORT` | `None` | The port the service will use. This field is required. |
| `service_path` | `root-url` | `LANDSCAPE_PACKAGE_UPLOAD__SERVICE_PATH` | `/upload/` | The relative path portion to use for the service URL. |

## The `[scripts]` section

The `[scripts]` section contains configurations for scripts. The section contains only the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

## The `[secrets]` section

The `[secrets]` section contains configurations for the secrets service, such as vault connection settings. In addition to the following, this section can use the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `service_url` | `secrets-service-url` | `LANDSCAPE_SECRETS__SERVICE_URL` | `None` | The URL to use for the secrets service. Must include a port. |
| `vault_token` | - | `LANDSCAPE_SECRETS__VAULT_TOKEN` | `None` | The token to use for the vault instead of getting it from the secrets service. |
| `vault_url` | `secrets-url` | `LANDSCAPE_SECRETS__VAULT_URL` | `http://localhost:8200` | The address of the vault to use for the secrets service. |

## The `[stores]` section

The `[stores]` section contains configurations for database store names and connections. In addition, the this section can use the {ref}`shared store settings <shared-store-settings>`.

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
| `user` | - | `LANDSCAPE_STORES__USER` | `landscape` | The username for database connections. |

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
| `enable_password_authentication` | - | `LANDSCAPE_SYSTEM__ENABLE_PASSWORD_AUTHENTICATION` | `False` | Whether to enable password-based authentication or not. |
| `enable_query_debug` | - | `LANDSCAPE_SYSTEM__ENABLE_QUERY_DEBUG` | `False` | Whether to enable query introspection and debugging middleware or not. |
| `enable_saas_metrics` | - | `LANDSCAPE_SYSTEM__ENABLE_SAAS_METRICS` | `False` | Whether to enable metrics on SaaS or not. |
| `enable_subdomain_accounts` | - | `LANDSCAPE_SYSTEM__ENABLE_SUBDOMAIN_ACCOUNTS` | `False` | Whether to enable subdomain accounts or not. |
| `enable_tag_script_execution` | - | `LANDSCAPE_SYSTEM__ENABLE_TAG_SCRIPT_EXECUTION` | `False` | Whether to enable tag-based script execution or not. |
| `fqdn` | - | `LANDSCAPE_SYSTEM__FQDN` | `None` | Sets the root URL using the FQDN. |
| `gpg_home_dir` | - | `LANDSCAPE_SYSTEM__GPG_HOME_DIR` | `/var/lib/landscape-server/gnupg` | The directory containing GnuPG config files and the keyrings. |
| `license_file` | - | `LANDSCAPE_SYSTEM__LICENSE_FILE` | `/etc/landscape/license.txt` | The file path location of the license file. |
| {spellexception}`pidfile_directory` | {spellexception}`pidfile-directory` | {spellexception}`LANDSCAPE_SYSTEM__PIDFILE_DIRECTORY` | `/tmp/landscape` | Unused |
| `max_service_memory` | `max-service-memory` | `LANDSCAPE_SYSTEM__MAX_SERVICE_MEMORY` | `0` | An upper limit (in {spellexception}`mebibytes`) for the memory usage by a Landscape service. Services exceeding this limit will restart. A value of `0` means there is no limit. |
| `middleware` | - | `LANDSCAPE_SYSTEM__MIDDLEWARE` | `None` | The python dotted name to the middleware function or class to use. Multiple values can be provided by separating them with a comma. |
| `offline` | - | `LANDSCAPE_SYSTEM__OFFLINE` | `None` | Set `True` if Landscape is deployed in an air-gapped environment. |
| `oops_path` | `oops-path` | `LANDSCAPE_SYSTEM__OOPS_PATH` | `/var/lib/landscape/landscape-oops` | The directory where OOPS reports are stored. The `landscape` system user must have read/write access to the specified directory. |
| `root_url` | `root-url` | `LANDSCAPE_SYSTEM__ROOT_URL` | `http://localhost:8080` | Landscape Server's root URL path. |
| `syslog_address` | `syslog-address` | `LANDSCAPE_SYSTEM__SYSLOG_ADDRESS` | `/dev/log` | Path to the system's syslog logger. |
