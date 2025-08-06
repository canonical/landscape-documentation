(reference-immutable-settings)=

# Immutable configuration settings

The following immutable configurations can be set in `service.conf` or through environment variables:

| Deprecated ENV name | New ENV name | Deprecated section of `service.conf` | Section of `service.conf` | Deprecated key name in `service.conf` | Key name in `service.conf`  | Default value | Purpose |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| `LANDSCAPE_OFFLINE` | `LANDSCAPE_FEATURES__ENABLE_OFFLINE` | `global` | `features` | `offline` | `enable_offline` | `False` | Whether offline mode is set or not (only relevant for standalone setups). |
| `LANDSCAPE_ROOT_URL` | `LANDSCAPE_GLOBAL__ROOT_URL` | `global` | `global` | `root-url` | `root_url` | `None` | The Landscape Server’s root URL path. HTTP requests are expected to be made to this path. |
| `LANDSCAPE_LICENSE_FILE` | `LANDSCAPE_GLOBAL__LICENSE_FILE` | `N/A` | `global` | `N/A` | `license_file` | `/etc/landscape/license.txt` | The file path location of the license file. |
| `LANDSCAPE_ENABLE_PASSWORD_AUTHENTICATION` | `LANDSCAPE_FEATURES__ENABLE_PASSWORD_AUTHENTICATION` | `landscape` | `features` | `enable-password-authentication` | `enable_password_authentication` | `False` | Whether users are allowed to log in with email/password or not.  |
| `LANDSCAPE_ENABLE_SUBDOMAIN_ACCOUNTS` | `LANDSCAPE_FEATURES__ENABLE_SUBDOMAIN_ACCOUNTS` | `landscape` | `features` | `enable-subdomain-accounts` | `enable_subdomain_accounts` | `False` | Whether subdomain-based functionality is enabled or not. |
| `LANDSCAPE_QUERY_DEBUG` | `LANDSCAPE_OOPS__QUERY_DEBUG` | `N/A` | `oops` | `N/A` | `enable_query_debug` | `False` | Whether to enable query introspection and debugging middleware for Landscape or not. |
| `LANDSCAPE_MESSAGE_URL` | `LANDSCAPE_GLOBAL__MESSAGE_URL` | `N/A` | `message_system` | `N/A` | `message_system_url` | The HTTP version of the root URL with `/message-system` appended.  | The message system URL to use |
| `LANDSCAPE_GPG_HOME` | `LANDSCAPE_GLOBAL__GPG_HOME_DIR` | `N/A` | `global` | `N/A` | `gpg_home_dir` | `/var/lib/landscape-server/gnupg` | The directory containing GnuPG config files and the {spellexception}`keyrings`.  |
| `LANDSCAPE_FQDN` | `LANDSCAPE_GLOBAL__FQDN` | `N/A` | `global` | `N/A` | `fqdn` | `None` | Sets the root URL using the FQDN. |
| `LANDSCAPE_MIDDLEWARE` | `LANDSCAPE_GLOBAL__MIDDLEWARE` | `N/A` | `global` | `N/A` | `middleware` | `None` | The python dotted name to the middleware function or class to use. Multiple values can be provided by separating them with a comma. |
| `LANDSCAPE_ANALYTICS_ID` | `LANDSCAPE_GLOBAL__ANALYTICS_ID` | `N/A` | `global` | `N/A` | `google_analytics_id` | `UA-1018242-60` | Google Analytics tracker ID for the deployment. |
| `LANDSCAPE_APT_PORT` | `LANDSCAPE_GLOBAL__APT_PORT` | `N/A` | `global` | `N/A` | `apt_port` | 8085 | The port the `landscape_apt` service should use. |
| `VAULT_TOKEN` | `LANDSCAPE_SECRETS__VAULT_TOKEN` | `secrets` | `secrets` | `secrets-service-url` | `secrets_service_url` | `None` | If provided through an environment variable, it’s expected to be the token itself. If set in `service.conf` it’s expected to be the URL of the secrets service to get the token from. |
| `VAULT_ADDR` | `LANDSCAPE_SECRETS__VAULT_URL` | `secrets` | `secrets` | `secrets-url` | `vault_url` | `None` | The URL to use for the secrets service. |
| `LANDSCAPE_ENABLE_TAG_SCRIPT_EXECUTION` | `LANDSCAPE_FEATURES__ENABLE_TAG_SCRIPT_EXECUTION` | `landscape` | `features` | `enable-tag-script-execution` | `enable_tag_script_execution` | `False` | Whether to enable tag-based script execution. |
| `LANDSCAPE_TEST_RUNNER` | `LANDSCAPE_TESTING__TEST_RUNNER` | `N/A` | `testing` | `N/A` | `test_runner` | `trial` | The `twisted` test runner to use for the `trial` script in `/dev`. |
| `LANDSCAPE_TESTRUN` | `LANDSCAPE_TESTING__TESTRUN` | `N/A` | `testing` | `N/A` | `test_run` | `False` | If true, do not replace the importer with the import guardian to speed up the tests. |
