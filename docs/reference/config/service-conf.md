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

### Moved Configuration Keys

The following keys have moved from the `[appserver]` section to the `[system]` section in Landscape 25.10:

- `enable-password-authentication` → `enable_password_authentication` in `[system]`
- `enable-subdomain-accounts` → `enable_subdomain_accounts` in `[system]`
- `enable-saas-metrics` → `enable_saas_metrics` in `[system]`
- `enable-tag-script-execution` → `enable_tag_script_execution` in `[system]`

These keys can still be used in their deprecated forms in `[appserver]`/`[landscape]` until Landscape 26.04, when support will be removed and they must be configured in the `[system]` section.

### Authentication providers

OpenID:

- Requires both `openid_provider_url` and `openid_logout_url` to be configured
- Defaults to using Ubuntu One

OIDC:

- Requires `oidc_issuer`, `oidc_client_id`, and `oidc_client_secret` to be configured

### `blob_storage_root`

- Purpose: Root directory for blob storage used for USG reports.
- Deprecated key name: `blob-storage-root`
- ENV name: `LANDSCAPE_APPSERVER__BLOB_STORAGE_ROOT`
- Default: `/var/lib/landscape/blobs`

### `display_consent_banner_at_each_login`

- Purpose: This setting should only be enabled in DISA STIG environments. Whether to display consent banner at each login.
- Deprecated key name: `display-consent-banner-at-each-login`
- ENV name: `LANDSCAPE_APPSERVER__DISPLAY_CONSENT_BANNER_AT_EACH_LOGIN`
- Default: `False`

### `known_proxies`

- Purpose: Comma-separated names of known proxies to consider when updating an administrator's last login host.
- Deprecated key name: `known-proxies`
- ENV name: `LANDSCAPE_APPSERVER__KNOWN_PROXIES`
- Default: `None`

### `oidc_client_id`

- Purpose: OIDC client identifier. Required along with `oidc_client_secret` and `oidc_issuer` when using OIDC authentication.
- Deprecated key name: `oidc-client-id`
- ENV name: `LANDSCAPE_APPSERVER__OIDC_CLIENT_ID`
- Default: `None`

### `oidc_client_secret`

- Purpose: OIDC client secret. Required along with `oidc_client_id` and `oidc_issuer` when using OIDC authentication.
- Deprecated key name: `oidc-client-secret`
- ENV name: `LANDSCAPE_APPSERVER__OIDC_CLIENT_SECRET`
- Default: `None`

### `oidc_issuer`

- Purpose: OIDC issuer URL. Required along with `oidc_client_secret` and `oidc_client_id` when using OIDC authentication.
- Deprecated key name: `oidc-issuer`
- ENV name: `LANDSCAPE_APPSERVER__OIDC_ISSUER`
- Default: `None`

### `oidc_provider`

- Purpose: The name of OIDC provider to use. Must be either `google`, `okta`, or `unspecified`.
- Deprecated key name: `oidc-provider`
- ENV name: `LANDSCAPE_APPSERVER__OIDC_PROVIDER`
- Default: `unspecified`

### `oidc_redirect_uri`

- Purpose: OIDC redirect URI for authentication callbacks.
- Deprecated key name: `oidc-redirect-uri`
- ENV name: `LANDSCAPE_APPSERVER__OIDC_REDIRECT_URI`
- Default: `None`

### `openid_logout_url`

- Purpose: OpenID logout URL. Required along with `openid_provider_url` when using OpenID authentication.
- Deprecated key name: `openid-logout-url`
- ENV name: `LANDSCAPE_APPSERVER__OPENID_LOGOUT_URL`
- Default: `None`

### `openid_provider_url`

- Purpose: OpenID logout URL. Required along with `openid_logout_url` when using OpenID authentication.
- Deprecated key name: `openid-provider-url`
- ENV name: `LANDSCAPE_APPSERVER__OPENID_PROVIDER_URL`
- Default: `None`

### `repository_path`

- Purpose: Path to the package repository directory. The `landscape` system user must have read and write privileges for that directory.
- Deprecated key name: `repository-path`
- ENV name: `LANDSCAPE_APPSERVER__REPOSITORY_PATH`
- Default: `/tmp/landscape-repository`

### `reprepro_binary`

- Purpose: Path to the reprepro binary executable. If unset the binary installed at `/usr/bin/reprepro` is used.
- Deprecated key name: `reprepro-binary`
- ENV name: `LANDSCAPE_APPSERVER__REPREPRO_BINARY`
- Default: `None`

### `sanitize_delay`

- Purpose: Delay in seconds before a sanitize activity is sent to a registered instance.
- Deprecated key name: `sanitize-delay`
- ENV name: `LANDSCAPE_APPSERVER__SANITIZE_DELAY`
- Default: `3600`

### `secret_token`

- Purpose: Secret token used as the secret key for symmetric encryption of JWTs.
- Deprecated key name: `secret-token`
- ENV name: `LANDSCAPE_APPSERVER__SECRET_TOKEN`
- Default: `None`

### `ubuntu_one_redirect_url`

- Purpose: Ubuntu One redirect URL for authentication.
- Deprecated key name: `ubuntu-one-redirect-url`
- ENV name: `LANDSCAPE_APPSERVER__UBUNTU_ONE_REDIRECT_URL`
- Default: `None`

## The `[async_frontend]` section

```{note}
The `[async-frontend]` section name is deprecated. The `[async_frontend]` section replaces the `[async-frontend]` section.
```

The `[async_frontend]` section contains configurations that apply to the `landscape-async-frontend` service which handles AJAX requests from the Legacy UI. It has no settings beyond the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

In practice, only the `base_port` setting needs to be configured for the service to operate correctly.

## The `[broker]` section

The `[broker]` section contains configurations that describe how services connect to our AMQP broker (RabbitMQ).

### `host`

- Purpose: The hostname or IP address of the AMQP broker server.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__HOST`
- Default: `localhost`

### `hostagent_command_status_queue`

- Purpose: Queue for sending command status updates from the hostagent server to the hostagent consumer.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__HOSTAGENT_COMMAND_STATUS_QUEUE`
- Default: `landscape-server-hostagent-command-status-queue`

### `hostagent_ping_queue`

- Purpose: Queue for pings from registered Windows instances.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__HOSTAGENT_PING_QUEUE`
- Default: `landscape-server-hostagent-ping-queue`

### `hostagent_task_queue`

- Purpose: Queue for messages received from registered Windows instances.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__HOSTAGENT_TASK_QUEUE`
- Default: `landscape-server-hostagent-task-queue`

### `hostagent_virtual_host`

- Purpose: The virtual host of message queues for the hostagent message server and consumer. This provides support for Landscape integration with Ubuntu Pro for WSL.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__HOSTAGENT_VIRTUAL_HOST`
- Default: `landscape-hostagent`

### `password`

- Purpose: Password used to authenticate with the AMQP broker.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__PASSWORD`
- Default: `guest`

### `port`

- Purpose: Network port where the AMQP broker is listening.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__PORT`
- Default: `5672`

### `ssl_client_cert`

- Purpose: Path to the client certificate to use for an SSL connection to the AMQP broker. Required along with `ssl_private_key` for mTLS connections.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__SSL_CLIENT_CERT`
- Default: `None`

### `ssl_private_key`

- Purpose: Path to the private key to use for an SSL connection to the AMQP broker. Required along with `ssl_client_cert` for mTLS connections.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__SSL_PRIVATE_KEY`
- Default: `None`

### `ssl_ca_cert`

- Purpose: Sets the path to the CA to use for mTLS. If set, both `ssl_private_key` and `ssl_server_cert` must also be set.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__SSL_CA_CERT`
- Default: `None`

### `user`

- Purpose: Username used to authenticate with the message broker.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__USER`
- Default: `guest`

### `vhost`

- Purpose: The virtual host namespace used by most of the Landscape services.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_BROKER__VHOST`
- Default: `landscape`

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

### `critical_load`

- Purpose: A float representing the database load threshold at which message processing time is reduced to zero. When load reaches this value, no time slice is allocated for processing.
- Deprecated key name: `critical-load`
- ENV name: `LANDSCAPE_LOAD_SHAPER__CRITICAL_LOAD`
- Default: `10.0`

### `good_duration`

- Purpose: A float representing the baseline time slice (in seconds) allocated for message processing when the database load is at the good load threshold. This duration is scaled up or down based on current load.
- Deprecated key name: `good-duration`
- ENV name: `LANDSCAPE_LOAD_SHAPER__GOOD_DURATION`
- Default: `60.0`

### `good_load`

- Purpose: A float representing the optimal database load threshold. When load is at this value, the full good duration time slice is allocated. Load below this increases the time slice, load above this decreases it.
- Deprecated key name: `good-load`
- ENV name: `LANDSCAPE_LOAD_SHAPER__GOOD_LOAD`
- Default: `3.0`

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

### `backoff_dir`

- Purpose: The directory to hold the `backoff.txt` file the server uses to indicate it should back off requests. If `None`, a `config` directory within the `landscape` directory will be used.
- Deprecated key name: `backoff-dirpath`
- ENV name: `LANDSCAPE_MESSAGE_SERVER__BACKOFF_DIR`
- Default: `None`

### `check_interval`

- Purpose: The interval in seconds at which to update knowledge of computers with outstanding messages from the database.
- Deprecated key name: `check-interval`
- ENV name: `LANDSCAPE_MESSAGE_SERVER__CHECK_INTERVAL`
- Default: `1200`

### `max_msg_size_bytes`

- Purpose: The maximum size, in bytes, of a message from Landscape Client that Landscape Server will accept. Messages larger than this size will be rejected.
- Deprecated key name: `max-msg-size-bytes`
- ENV name: `LANDSCAPE_MESSAGE_SERVER__MAX_MSG_SIZE_BYTES`
- Default: `30000000` (30MB)

### `message_snippet_bytes`

- Purpose: When Landscape Server receives a message larger than `max_msg_size_bytes`, it will log an error including the first `message_snippet_bytes` of the message.
- Deprecated key name: `message-snippet-bytes`
- ENV name: `LANDSCAPE_MESSAGE_SERVER__MESSAGE_SNIPPET_BYTES`
- Default: `1000`

### `message_system_url`

- Purpose: The message system URL to use. If not set, the system root url appended with `/message-system` is used.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_MESSAGE_SERVER__MESSAGE_SYSTEM_URL`
- Default: `None`

### `ping_interval`

- Purpose: Landscape Server will instruct Landscape Client to send a ping message every `ping_interval` seconds. If unset, each registered client will use the value set in its own Landscape Client configuration.
- Deprecated key name: `ping-interval`
- ENV name: `LANDSCAPE_MESSAGE_SERVER__PING_INTERVAL`
- Default: `None`

## The `[oops]` section

The `[oops]` section contains configurations for the OOPS error reporting and debugging system used for logging and traceback collection.

### `amqp_exchange`

- Purpose: AMQP exchange name for error reporting.
- Deprecated key name: `amqp-exchange`
- ENV name: `LANDSCAPE_OOPS__AMQP_EXCHANGE`
- Default: `""`

### `amqp_key`

- Purpose: AMQP routing key for error messages. Requires `amqp_exchange` to be set.
- Deprecated key name: `amqp-key`
- ENV name: `LANDSCAPE_OOPS__AMQP_KEY`
- Default: `landscape-oops`

### `path`

- Purpose: File path for local OOPS publishing. If set, overrides the value set by `LANDSCAPE_SYSTEM__OOPS_PATH`.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_OOPS__PATH`
- Default: `None`

## The `[schema]` section

The `[schema]` section contains configurations for updating the database schema. It has no settings beyond the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

## The `[package_upload]` section

```{note}
The `[package-upload]` section name is deprecated. The `[package_upload]` section replaces the `[package-upload]` section.
```

The `[package_upload]` section contains configurations for the package upload service, including service connection settings, database store configurations, and SSL options. In addition to the following, this section can use the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

### `base_port`

- Purpose: Workers for the service will run on ports incrementing from this base port.
- Deprecated key names: `port`, `base-port`
- ENV name: `LANDSCAPE_PACKAGE_UPLOAD__BASE_PORT`
- Default: `9100`

### `service_path`

- Purpose: The relative path portion to use for the service URL.
- Deprecated key name: `root-url`
- ENV name: `LANDSCAPE_PACKAGE_UPLOAD__SERVICE_PATH`
- Default: `/upload/`

## The `[scripts]` section

The `[scripts]` section contains configurations for scripts. The section contains only the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

## The `[secrets]` section

The `[secrets]` section contains configurations for the secrets service, such as vault connection settings. In addition to the following, this section can use the {ref}`shared service settings <shared-service-settings>` and the {ref}`shared store settings <shared-store-settings>`.

### `service_url`

- Purpose: The URL to use for the secrets service. Must include a port.
- Deprecated key name: `secrets-service-url`
- ENV name: `LANDSCAPE_SECRETS__SERVICE_URL`
- Default: `None`

### `vault_token`

- Purpose: The token to use for the vault instead of getting it from the secrets service.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SECRETS__VAULT_TOKEN`
- Default: `None`

### `vault_url`

- Purpose: The address of the vault to use for the secrets service.
- Deprecated key name: `secrets-url`
- ENV name: `LANDSCAPE_SECRETS__VAULT_URL`
- Default: `http://localhost:8200`

## The `[stores]` section

The `[stores]` section contains configurations for database store names and connections. In addition, the this section can use the {ref}`shared store settings <shared-store-settings>`.

### `account_1`

- Purpose: The account database store name.
- Deprecated key name: `account-1`
- ENV name: `LANDSCAPE_STORES__ACCOUNT_1`
- Default: `landscape-standalone-account-1`

### `account_2`

- Purpose: The second account database store name. In practice this settings should be left unset as it is used only by tests.
- Deprecated key name: `account-2`
- ENV name: `LANDSCAPE_STORES__ACCOUNT_2`
- Default: `None`

### `host`

- Purpose: The hostname or IP address of the database server.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_STORES__HOST`
- Default: `localhost`

### `knowledge`

- Purpose: The knowledge database name. The knowledge database is deprecated and will be dropped in a future release of Landscape Server.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_STORES__KNOWLEDGE`
- Default: `landscape-standalone-knowledge`

### `main`

- Purpose: The main database name.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_STORES__MAIN`
- Default: `landscape-standalone-main`

### `package`

- Purpose: The package database name.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_STORES__PACKAGE`
- Default: `landscape-standalone-package`

### `password`

- Purpose: The password for database connections by the configured `user`.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_STORES__PASSWORD`
- Default: `None`

### `resource_1`

- Purpose: The resource database name.
- Deprecated key name: `resource-1`
- ENV name: `LANDSCAPE_STORES__RESOURCE_1`
- Default: `landscape-standalone-resource-1`

### `resource_2`

- Purpose: The second resource database name. In practice this settings should be left unset as it is used only by tests.
- Deprecated key name: `resource-2`
- ENV name: `LANDSCAPE_STORES__RESOURCE_2`
- Default: `None`

### `session`

- Purpose: The session database name.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_STORES__SESSION`
- Default: `landscape-standalone-session`

### `session_autocommit`

- Purpose: The name of the session database with `autocommit` isolation.
- Deprecated key name: `session-autocommit`
- ENV name: `LANDSCAPE_STORES__SESSION_AUTOCOMMIT`
- Default: `landscape-standalone-session`

### `user`

- Purpose: The username for database connections.
- Deprecated key name: `session-autocommit`
- ENV name: `LANDSCAPE_STORES__USER`
- Default: `landscape`

## The `[system]` section

```{note}
The `[global]` section name is deprecated. The `[system]` section replaces the `[global]` section.
```

The `[system]` section contains configurations that apply across many or all of Landscape's services.

### `analytics_id`

- Purpose: Google Analytics tracker ID for the deployment.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__ANALYTICS_ID`
- Default: `UA-1018242-60`

### `apt_port`

- Purpose: The port the `landscape_apt` service should use.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__APT_PORT`
- Default: `8085`

### `audit_retention_period`

- Purpose: The time period in days to retain security profile audit records. A negative value means that records should be retained indefinitely.
- Deprecated key name: `audit-retention-period`
- ENV name: `LANDSCAPE_SYSTEM__AUDIT_RETENTION_PERIOD`
- Default: `-1`

### `deployment_mode`

- Purpose: Used only for development. The default value is appropriate for self-hosted Landscape Server.
- Deprecated key name: `deployment-mode`
- ENV name: `LANDSCAPE_SYSTEM__DEPLOYMENT_MODE`
- Default: `standalone`

### `enable_password_authentication`

- Purpose: Whether to enable password-based authentication or not.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__ENABLE_PASSWORD_AUTHENTICATION`
- Default: `False`

### `enable_query_debug`

- Purpose: Whether to enable query introspection and debugging middleware or not. The default value is appropriate for self-hosted Landscape Server.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__ENABLE_QUERY_DEBUG`
- Default: `False`

### `enable_saas_metrics`

- Purpose: Whether to enable metrics on SaaS or not. The default value is appropriate for self-hosted Landscape Server.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__ENABLE_SAAS_METRICS`
- Default: `False`

### `enable_subdomain_accounts`

- Purpose: Whether to enable subdomain accounts or not. The default value is appropriate for self-hosted Landscape Server.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__ENABLE_SUBDOMAIN_ACCOUNTS`
- Default: `False`

### `enable_tag_script_execution`

- Purpose: Whether to enable tag-based script execution or not.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__ENABLE_TAG_SCRIPT_EXECUTION`
- Default: `False`

### `gpg_home_dir`

- Purpose: The directory containing GnuPG config files and the keyrings.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__GPG_HOME_DIR`
- Default: `/var/lib/landscape-server/gnupg`

### `license_file`

- Purpose: The file path location of the license file. The `landscape` system user must be able to read this file.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__LICENSE_FILE`
- Default: `/etc/landscape/license.txt`

### `max_service_memory`

- Purpose: An upper limit (in `mebibytes`) for the memory usage by a Landscape service. Services exceeding this limit will restart. A value of `0` means there is no limit.
- Deprecated key name: `max-service-memory`
- ENV name: `LANDSCAPE_SYSTEM__MAX_SERVICE_MEMORY`
- Default: `0`

### `middleware`

- Purpose: The python dotted name to the middleware function or class to use. Multiple values can be provided by separating them with a comma. This setting should remain unset in production environments.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__MIDDLEWARE`
- Default: `None`

### `offline`

- Purpose: Set `True` if Landscape is deployed in an air-gapped environment.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__OFFLINE`
- Default: `None`

### `oops_path`

- Purpose: The directory where OOPS reports are stored. The `landscape` system user must have read/write access to the specified directory.
- Deprecated key name: `oops-path`
- ENV name: `LANDSCAPE_SYSTEM__OOPS_PATH`
- Default: `/var/lib/landscape/landscape-oops`

### `root_url`

- Purpose: Landscape Server's root URL path.
- Deprecated key name: `root-url`
- ENV name: `LANDSCAPE_SYSTEM__ROOT_URL`
- Default: `http://localhost:8080`

### `syslog_address`

- Purpose: Path to the system's syslog logger.
- Deprecated key name: `syslog-address`
- ENV name: `LANDSCAPE_SYSTEM__SYSLOG_ADDRESS`
- Default: `/dev/log`

<!-- This setting is technically available, but the relevant feature is not yet implemented.
### `ubuntu_pro_contract_server_url`

- Purpose: The URL of the Ubuntu Pro contract server, used to verify Ubuntu Pro tokens.
- Deprecated key name: N/A
- ENV name: `LANDSCAPE_SYSTEM__UBUNTU_PRO_CONTRACT_SERVER_URL`
- Default: `https://contracts.canonical.com/`
-->
