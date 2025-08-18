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

## The `[api]` section

The `[api]` section contains configurations for the Landscape API service, including service connection settings and database store configurations.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `allowed_interfaces` | - | `LANDSCAPE_API__ALLOWED_INTERFACES` | `None` | A list of allowed IP addresses or {spellexception}`hostnames` for the service. |
| `base_port` | `base-port` | `LANDSCAPE_API__BASE_PORT` | `8090` | Base port number for the service. |
| `cookie_encryption_key` | `cookie-encryption-key` | `LANDSCAPE_API__COOKIE_ENCRYPTION_KEY` | `None` | The key used to encrypt state and nonce cookies. |
| `cors_allow_all` | `cors-allow-all` | `LANDSCAPE_API__CORS_ALLOW_ALL` | `False` | Whether to allow CORS. |
| `enable_metrics` | `enable-metrics` | `LANDSCAPE_API__ENABLE_METRICS` | `False` | Whether to enable metrics collection for the service. |
| `gpg_home_path` | `gpg-home-path` | `LANDSCAPE_API__GPG_HOME_PATH` | `None` | Path to the GPG home directory. |
| `gpg_passphrase_path` | `gpg-passphrase-path` | `LANDSCAPE_API__GPG_PASSPHRASE_PATH` | `None` | Path to the GPG passphrase file. Required if `gpg_home_path` is set. |
| `mailer` | - | `LANDSCAPE_API__MAILER` | `None` | Mailer service configuration. |
| `mailer_path` | `mailer-path` | `LANDSCAPE_API__MAILER_PATH` | `None` | Path to the mailer executable. Required if `mailer` is set. |
| `oops_key` | `oops-key` | `LANDSCAPE_API__OOPS_KEY` | `None` | Key for OOPS error reporting system. |
| `root_url` | `root-url` | `LANDSCAPE_API__ROOT_URL` | `None` | The API URL to use. |
| `snap_store_api_url` | `snap-store-api-url` | `LANDSCAPE_API__SNAP_STORE_API_URL` | `https://api.snapcraft.io/v2` | The API for a Snap Store Proxy. By default, this is the Canonical Snap Store. |
| `soft_timeout` | `soft-timeout` | `LANDSCAPE_API__SOFT_TIMEOUT` | `None` | Soft timeout value in seconds for service operations. |
| `sslcert` | - | `LANDSCAPE_API__SSLCERT` | `None` | Path to the client certificate to use for SSL connection to Postgres (becomes `PGSSLCERT`). |
| `sslkey` | - | `LANDSCAPE_API__SSLKEY` | `None` | Path to the private key to use for SSL connection to Postgres (becomes `PGSSLKEY`). |
| `sslmode` | - | `LANDSCAPE_API__SSLMODE` | `None` | SSL mode when connecting to Postgres, for example `verify-full`. |
| `sslrootcert` | - | `LANDSCAPE_API__SSLROOTCERT` | `None` | Path to the root CA certificate to use for SSL connection to Postgres (becomes `PGSSLROOTCERT`). |
| `store_password` | - | `LANDSCAPE_API__STORE_PASSWORD` | `None` | Overrides the store password. |
| `store_user` | - | `LANDSCAPE_API__STORE_USER` | `None` | Overrides the store username. |
| `stores` | - | `LANDSCAPE_API__STORES` | `None` | The stores the service should use. |
| `threads` | - | `LANDSCAPE_API__THREADS` | `None` | Number of threads for the service. |
| `workers` | - | `LANDSCAPE_API__WORKERS` | `None` | Number of worker processes for the service. |

## The `[appserver]` section

```{note}
The `[landscape]` section name is deprecated. The `[appserver]` section replaces the `[landscape]` section.
```

The `[appserver]` section contains configurations for the Landscape application server, including storage paths, authentication providers, and security settings.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `access_log` | `access-log` | `LANDSCAPE_APPSERVER__ACCESS_LOG` | `None` | Path to access log file for this service. |
| `allowed_interfaces` | | `LANDSCAPE_APPSERVER__ALLOWED_INTERFACES` | `None` | Network interfaces allowed for connections. |
| `base_port` | `base-port` | `LANDSCAPE_APPSERVER__BASE_PORT` | `8090` | Base port number for the service. |
| `blob_storage_root` | `blob-storage-root` | `LANDSCAPE_APPSERVER__BLOB_STORAGE_ROOT` | `/var/lib/landscape/blobs` | Root directory for blob storage. |
| `devmode` | | `LANDSCAPE_APPSERVER__DEVMODE` | `None` | Development mode settings. |
| `display_consent_banner_at_each_login` | `display-consent-banner-at-each-login` | `LANDSCAPE_APPSERVER__DISPLAY_CONSENT_BANNER_AT_EACH_LOGIN` | `False` | Whether to display consent banner at each login. |
| `enable_metrics` | `enable-metrics` | `LANDSCAPE_APPSERVER__ENABLE_METRICS` | `False` | Whether to enable metrics collection. |
| `gpg_home_path` | `gpg-home-path` | `LANDSCAPE_APPSERVER__GPG_HOME_PATH` | `None` | Path to GPG home directory. Must be used with `gpg_passphrase_path`. |
| `gpg_passphrase_path` | `gpg-passphrase-path` | `LANDSCAPE_APPSERVER__GPG_PASSPHRASE_PATH` | `None` | Path to GPG passphrase file. Required when `gpg_home_path` is set. |
| `juju_homes_path` | `juju-homes-path` | `LANDSCAPE_APPSERVER__JUJU_HOMES_PATH` | `/var/tmp/juju-homes` | Path to Juju home directories. |
| `known_proxies` | `known-proxies` | `LANDSCAPE_APPSERVER__KNOWN_PROXIES` | `None` | Comma-separated names of known proxies. |
| `mailer` | | `LANDSCAPE_APPSERVER__MAILER` | `None` | Mailer type specification. Must be used with `mailer_path`. |
| `mailer_path` | `mailer-path` | `LANDSCAPE_APPSERVER__MAILER_PATH` | `None` | Path to mailer executable. Required when `mailer` is set. |
| `oidc_client_id` | `oidc-client-id` | `LANDSCAPE_APPSERVER__OIDC_CLIENT_ID` | `None` | OIDC client identifier. Required when using OIDC authentication. |
| `oidc_client_secret` | `oidc-client-secret` | `LANDSCAPE_APPSERVER__OIDC_CLIENT_SECRET` | `None` | OIDC client secret. Required when using OIDC authentication. |
| `oidc_issuer` | `oidc-issuer` | `LANDSCAPE_APPSERVER__OIDC_ISSUER` | `None` | OIDC issuer URL. Required when using OIDC authentication. |
| `oidc_provider` | `oidc-provider` | `LANDSCAPE_APPSERVER__OIDC_PROVIDER` | `unspecified` | The name of OIDC provider to use. Must be either `google`, `okta`, or `unspecified`. |
| `oidc_redirect_uri` | `oidc-redirect-uri` | `LANDSCAPE_APPSERVER__OIDC_REDIRECT_URI` | `None` | OIDC redirect URI for authentication callbacks. |
| `oops_key` | `oops-key` | `LANDSCAPE_APPSERVER__OOPS_KEY` | `None` | Key for OOPS error reporting system. |
| `openid_logout_url` | `openid-logout-url` | `LANDSCAPE_APPSERVER__OPENID_LOGOUT_URL` | `None` | OpenID logout URL. Required when using OpenID authentication. |
| `openid_provider_url` | `openid-provider-url` | `LANDSCAPE_APPSERVER__OPENID_PROVIDER_URL` | `None` | OpenID provider URL. Required when using OpenID authentication. |
| `repository_path` | `repository-path` | `LANDSCAPE_APPSERVER__REPOSITORY_PATH` | `/tmp/landscape-repository` | Path to the package repository. |
| `reprepro_binary` | `reprepro-binary` | `LANDSCAPE_APPSERVER__REPREPRO_BINARY` | `None` | Path to the reprepro binary executable. |
| `sanitize_delay` | `sanitize-delay` | `LANDSCAPE_APPSERVER__SANITIZE_DELAY` | `3600` | Delay in seconds for data sanitization operations. |
| `secret_token` | `secret-token` | `LANDSCAPE_APPSERVER__SECRET_TOKEN` | `None` | Secret token for application security. |
| `soft_timeout` | `soft-timeout` | `LANDSCAPE_APPSERVER__SOFT_TIMEOUT` | `None` | Soft timeout value in seconds for service operations. |
| `threads` | | `LANDSCAPE_APPSERVER__THREADS` | `None` | Number of threads for the service. |
| `ubuntu_images_path` | `ubuntu-images-path` | `LANDSCAPE_APPSERVER__UBUNTU_IMAGES_PATH` | `/var/tmp/ubuntu-images` | Path to Ubuntu images directory. |
| `ubuntu_one_redirect_url` | `ubuntu-one-redirect-url` | `LANDSCAPE_APPSERVER__UBUNTU_ONE_REDIRECT_URL` | `None` | Ubuntu One redirect URL for authentication. |
| `workers` | | `LANDSCAPE_APPSERVER__WORKERS` | `None` | Number of worker processes for the service. |

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

## The `[maintenance]` section

The `[maintenance]` section contains configurations for running maintenance scripts.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `enable_metrics` | `enable-metrics` | `LANDSCAPE_MAINTENANCE__ENABLE_METRICS` | `False` | Whether to enable metrics collection for the service. |
| `gpg_home_path` | `gpg-home-path` | `LANDSCAPE_MAINTENANCE__GPG_HOME_PATH` | `None` | Path to the GPG home directory. |
| `gpg_passphrase_path` | `gpg-passphrase-path` | `LANDSCAPE_MAINTENANCE__GPG_PASSPHRASE_PATH` | `None` | Path to the GPG passphrase file. Required if `gpg_home_path` is set. |
| `mailer` | - | `LANDSCAPE_MAINTENANCE__MAILER` | `None` | Mailer service configuration. |
| `mailer_path` | `mailer-path` | `LANDSCAPE_MAINTENANCE__MAILER_PATH` | `None` | Path to the mailer executable. Required if `mailer` is set. |
| `oops_key` | `oops-key` | `LANDSCAPE_MAINTENANCE__OOPS_KEY` | `None` | Key for OOPS error reporting system. |
| `soft_timeout` | `soft-timeout` | `LANDSCAPE_MAINTENANCE__SOFT_TIMEOUT` | `None` | Soft timeout value in seconds for service operations. |
| `sslcert` | - | `LANDSCAPE_MAINTENANCE__SSLCERT` | `None` | Path to the client certificate to use for SSL connection to Postgres (becomes `PGSSLCERT`). |
| `sslkey` | - | `LANDSCAPE_MAINTENANCE__SSLKEY` | `None` | Path to the private key to use for SSL connection to Postgres (becomes `PGSSLKEY`). |
| `sslmode` | - | `LANDSCAPE_MAINTENANCE__SSLMODE` | `None` | SSL mode when connecting to Postgres, for example `verify-full`. |
| `sslrootcert` | - | `LANDSCAPE_MAINTENANCE__SSLROOTCERT` | `None` | Path to the root CA certificate to use for SSL connection to Postgres (becomes `PGSSLROOTCERT`). |
| `store_password` | - | `LANDSCAPE_MAINTENANCE__STORE_PASSWORD` | `None` | Overrides the store password. |
| `store_user` | - | `LANDSCAPE_MAINTENANCE__STORE_USER` | `None` | Overrides the store username. |
| `stores` | - | `LANDSCAPE_MAINTENANCE__STORES` | `None` | The stores the service should use. |
| `threads` | - | `LANDSCAPE_MAINTENANCE__THREADS` | `None` | Number of threads for the service. |
| `workers` | - | `LANDSCAPE_MAINTENANCE__WORKERS` | `None` | Number of worker processes for the service. |

## The `[message_server]` section

```{note}
The `[message-server]` section name is deprecated. The `[message_server]` section replaces the `[message-server]` section.
```

```{note}
The `[backoff]` section is deprecated. The settings have been moved to the `[message_server]` section.
```

The `[message_server]` section contains configurations that apply to the `landscape-message-server` service that handles messages from instances running Landscape Client.

It has the following settings beyond those shared by all services.

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

## The `[schema]` section

The `[schema]` section contains configurations for updating the database schema.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `sslcert` | - | `LANDSCAPE_SCHEMA__SSLCERT` | `None` | Path to the client certificate to use for SSL connection to Postgres (becomes `PGSSLCERT`). |
| `sslkey` | - | `LANDSCAPE_SCHEMA__SSLKEY` | `None` | Path to the private key to use for SSL connection to Postgres (becomes `PGSSLKEY`). |
| `sslmode` | - | `LANDSCAPE_SCHEMA__SSLMODE` | `None` | SSL mode when connecting to Postgres, for example `verify-full`. |
| `sslrootcert` | - | `LANDSCAPE_SCHEMA__SSLROOTCERT` | `None` | Path to the root CA certificate to use for SSL connection to Postgres (becomes `PGSSLROOTCERT`). |
| `store_password` | - | `LANDSCAPE_SCHEMA__STORE_PASSWORD` | `None` | Overrides the store password. |
| `store_user` | - | `LANDSCAPE_SCHEMA__STORE_USER` | `None` | Overrides the store username. |
| `stores` | - | `LANDSCAPE_SCHEMA__STORES` | `None` | The stores the service should use. |
| `threads` | - | `LANDSCAPE_SCHEMA__THREADS` | `None` | Number of threads for the service. |
| `workers` | - | `LANDSCAPE_SCHEMA__WORKERS` | `None` | Number of worker processes for the service. |

## The `[scripts]` section

The `[scripts]` section contains configurations for the scripts service, including service operation settings, database store configurations, and SSL options.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `allowed_interfaces` | - | `LANDSCAPE_SCRIPTS__ALLOWED_INTERFACES` | `None` | A list of allowed IP addresses or {spellexception}`hostnames` for the service. |
| `base_port` | `base-port` | `LANDSCAPE_SCRIPTS__BASE_PORT` | `8090` | Base port number for the service. |
| `devmode` | - | `LANDSCAPE_SCRIPTS__DEVMODE` | `None` | Development mode configuration (ex. `on`). |
| `enable_metrics` | `enable-metrics` | `LANDSCAPE_SCRIPTS__ENABLE_METRICS` | `False` | Whether to enable metrics collection for the service. |
| `gpg_home_path` | `gpg-home-path` | `LANDSCAPE_SCRIPTS__GPG_HOME_PATH` | `None` | Path to the GPG home directory. |
| `gpg_passphrase_path` | `gpg-passphrase-path` | `LANDSCAPE_SCRIPTS__GPG_PASSPHRASE_PATH` | `None` | Path to the GPG passphrase file. Required if `gpg_home_path` is set. |
| `mailer` | - | `LANDSCAPE_SCRIPTS__MAILER` | `None` | Mailer service configuration. |
| `mailer_path` | `mailer-path` | `LANDSCAPE_SCRIPTS__MAILER_PATH` | `None` | Path to the mailer executable. Required if `mailer` is set. |
| `oops_key` | `oops-key` | `LANDSCAPE_SCRIPTS__OOPS_KEY` | `None` | Key for OOPS error reporting system. |
| `soft_timeout` | `soft-timeout` | `LANDSCAPE_SCRIPTS__SOFT_TIMEOUT` | `None` | Soft timeout value in seconds for service operations. |
| `sslcert` | - | `LANDSCAPE_SCRIPTS__SSLCERT` | `None` | Path to the client certificate to use for SSL connection to Postgres (becomes `PGSSLCERT`). |
| `sslkey` | - | `LANDSCAPE_SCRIPTS__SSLKEY` | `None` | Path to the private key to use for SSL connection to Postgres (becomes `PGSSLKEY`). |
| `sslmode` | - | `LANDSCAPE_SCRIPTS__SSLMODE` | `None` | SSL mode when connecting to Postgres, for example `verify-full`. |
| `sslrootcert` | - | `LANDSCAPE_SCRIPTS__SSLROOTCERT` | `None` | Path to the root CA certificate to use for SSL connection to Postgres (becomes `PGSSLROOTCERT`). |
| `store_password` | - | `LANDSCAPE_SCRIPTS__STORE_PASSWORD` | `None` | Overrides the store password. |
| `store_user` | - | `LANDSCAPE_SCRIPTS__STORE_USER` | `None` | Overrides the store username. |
| `stores` | - | `LANDSCAPE_SCRIPTS__STORES` | `None` | The stores the service should use. |
| `threads` | - | `LANDSCAPE_SCRIPTS__THREADS` | `None` | Number of threads for the service. |
| `workers` | - | `LANDSCAPE_SCRIPTS__WORKERS` | `None` | Number of worker processes for the service. |

## The `[secrets]` section

The `[secrets]` section contains configurations for the secrets service, including vault connection settings, service URLs, database store configurations, and SSL options.

| Key name | Deprecated key name | ENV name | Default | Purpose |
| :------- | :------------------ | :------- | :------ | :------ |
| `allowed_interfaces` | - | `LANDSCAPE_SECRETS__ALLOWED_INTERFACES` | `None` | A list of allowed IP addresses or hostnames for the service. |
| `base_port` | `base-port` | `LANDSCAPE_SECRETS__BASE_PORT` | `8090` | Base port number for the service. |
| `devmode` | - | `LANDSCAPE_SECRETS__DEVMODE` | `None` | Development mode configuration (ex. `on`). |
| `enable_metrics` | `enable-metrics` | `LANDSCAPE_SECRETS__ENABLE_METRICS` | `False` | Whether to enable metrics collection for the service. |
| `gpg_home_path` | `gpg-home-path` | `LANDSCAPE_SECRETS__GPG_HOME_PATH` | `None` | Path to the GPG home directory. |
| `gpg_passphrase_path` | `gpg-passphrase-path` | `LANDSCAPE_SECRETS__GPG_PASSPHRASE_PATH` | `None` | Path to the GPG passphrase file. Required if `gpg_home_path` is set. |
| `mailer` | - | `LANDSCAPE_SECRETS__MAILER` | `None` | Mailer service configuration. |
| `mailer_path` | `mailer-path` | `LANDSCAPE_SECRETS__MAILER_PATH` | `None` | Path to the mailer executable. Required if `mailer` is set. |
| `oops_key` | `oops-key` | `LANDSCAPE_SECRETS__OOPS_KEY` | `None` | Key for OOPS error reporting system. |
| `service_url` | `secrets-service-url` | `LANDSCAPE_SECRETS__SERVICE_URL` | `None` | The URL to use for the secrets service. Must include a port. |
| `soft_timeout` | `soft-timeout` | `LANDSCAPE_SECRETS__SOFT_TIMEOUT` | `None` | Soft timeout value in seconds for service operations. |
| `sslcert` | - | `LANDSCAPE_SECRETS__SSLCERT` | `None` | Path to the client certificate to use for SSL connection to Postgres (becomes `PGSSLCERT`). |
| `sslkey` | - | `LANDSCAPE_SECRETS__SSLKEY` | `None` | Path to the private key to use for SSL connection to Postgres (becomes `PGSSLKEY`). |
| `sslmode` | - | `LANDSCAPE_SECRETS__SSLMODE` | `None` | SSL mode when connecting to Postgres, for example `verify-full`. |
| `sslrootcert` | - | `LANDSCAPE_SECRETS__SSLROOTCERT` | `None` | Path to the root CA certificate to use for SSL connection to Postgres (becomes `PGSSLROOTCERT`). |
| `store_password` | - | `LANDSCAPE_SECRETS__STORE_PASSWORD` | `None` | Overrides the store password. |
| `store_user` | - | `LANDSCAPE_SECRETS__STORE_USER` | `None` | Overrides the store username. |
| `stores` | - | `LANDSCAPE_SECRETS__STORES` | `None` | The stores the service should use. |
| `threads` | - | `LANDSCAPE_SECRETS__THREADS` | `None` | Number of threads for the service. |
| `vault_token` | - | `LANDSCAPE_SECRETS__VAULT_TOKEN` | `None` | The token to use for the vault instead of getting it from the secrets service. |
| `vault_url` | `secrets-url` | `LANDSCAPE_SECRETS__VAULT_URL` | `http://localhost:8200` | The address of the vault to use for the secrets service. |
| `workers` | - | `LANDSCAPE_SECRETS__WORKERS` | `None` | Number of worker processes for the service. |

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
| `session_autocommit` | `session-autocommit` | `LANDSCAPE_STORES__SESSION_AUTOCOMMIT` | `landscape-standalone-session` | The name of the session database with autocommit isolation. |
| `sslcert` | - | `LANDSCAPE_STORES__SSLCERT` | `None` | Path to the client certificate to use for SSL connection to Postgres (becomes `PGSSLCERT`). |
| `sslkey` | - | `LANDSCAPE_STORES__SSLKEY` | `None` | Path to the private key to use for SSL connection to Postgres (becomes `PGSSLKEY`). |
| `sslmode` | - | `LANDSCAPE_STORES__SSLMODE` | `None` | SSL mode when connecting to Postgres, for example `verify-full`. |
| `sslrootcert` | - | `LANDSCAPE_STORES__SSLROOTCERT` | `None` | Path to the root CA certificate to use for SSL connection to Postgres (becomes `PGSSLROOTCERT`). |
| `store_password` | - | `LANDSCAPE_STORES__STORE_PASSWORD` | `None` | Overrides the store password. |
| `store_user` | - | `LANDSCAPE_STORES__STORE_USER` | `None` | Overrides the store username. |
| `stores` | - | `LANDSCAPE_STORES__STORES` | `None` | The stores the service should use. |
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
