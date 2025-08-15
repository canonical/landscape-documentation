(reference-immutable-settings)=

# Immutable configuration settings

The following immutable configurations can be set in `service.conf` or through environment variables:

| Deprecated ENV name | New ENV name | Deprecated section of `service.conf` | Section of `service.conf` | Deprecated key name in `service.conf` | Key name in `service.conf`  | Default value | Purpose |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| `LANDSCAPE_ANALYTICS_ID` | `LANDSCAPE_SYSTEM__ANALYTICS_ID` | `N/A` | `system` | `N/A` | `analytics_id` | `UA-1018242-60` | Google Analytics tracker ID for the deployment. |
| `LANDSCAPE_APT_PORT` | `LANDSCAPE_SYSTEM__APT_PORT` | `N/A` | `system` | `N/A` | `apt_port` | 8085 | The port the `landscape_apt` service should use. |
| `LANDSCAPE_ENABLE_PASSWORD_AUTHENTICATION` | `LANDSCAPE_SYSTEM__ENABLE_PASSWORD_AUTHENTICATION` | `landscape` | `system` | `enable-password-authentication` | `enable_password_authentication` | `False` | Whether users are allowed to log in with email/password or not.  |
| `LANDSCAPE_ENABLE_SUBDOMAIN_ACCOUNTS` | `LANDSCAPE_SYSTEM__ENABLE_SUBDOMAIN_ACCOUNTS` | `landscape` | `system` | `enable-subdomain-accounts` | `enable_subdomain_accounts` | `False` | Whether subdomain-based functionality is enabled or not. |
| `LANDSCAPE_ENABLE_TAG_SCRIPT_EXECUTION` | `LANDSCAPE_SYSTEM__ENABLE_TAG_SCRIPT_EXECUTION` | `landscape` | `system` | `enable-tag-script-execution` | `enable_tag_script_execution` | `False` | Whether to enable tag-based script execution. |
| `LANDSCAPE_FQDN` | `LANDSCAPE_SYSTEM__FQDN` | `N/A` | `system` | `N/A` | `fqdn` | `None` | Sets the root URL using the FQDN. |
| `LANDSCAPE_GPG_HOME` | `LANDSCAPE_SYSTEM__GPG_HOME_DIR` | `N/A` | `system` | `N/A` | `gpg_home_dir` | `/var/lib/landscape-server/gnupg` | The directory containing GnuPG config files and the {spellexception}`keyrings`. |
| `LANDSCAPE_LICENSE_FILE` | `LANDSCAPE_SYSTEM__LICENSE_FILE` | `N/A` | `system` | `N/A` | `license_file` | `/etc/landscape/license.txt` | The file path location of the license file. |
| `LANDSCAPE_MESSAGE_URL` | `LANDSCAPE_MESSAGE_SERVER__MESSAGE_URL` | `N/A` | `message_system` | `N/A` | `message_system_url` | The HTTP version of the root URL with `/message-system` appended.  | The message system URL to use. |
| `LANDSCAPE_MIDDLEWARE` | `LANDSCAPE_SYSTEM__MIDDLEWARE` | `N/A` | `system` | `N/A` | `middleware` | `None` | The python dotted name to the middleware function or class to use. Multiple values can be provided by separating them with a comma. |
| `LANDSCAPE_OFFLINE` | `LANDSCAPE_SYSTEM__OFFLINE` | `global` | `system` | `offline` | `offline` | `None` | Whether offline mode is set or not (only relevant for standalone setups). |
| `LANDSCAPE_QUERY_DEBUG` | `LANDSCAPE_SYSTEM__ENABLE_QUERY_DEBUG` | `N/A` | `system` | `N/A` | `enable_query_debug` | `False` | Whether to enable query introspection and debugging middleware for Landscape or not. |
| `LANDSCAPE_ROOT_URL` | `LANDSCAPE_SYSTEM__ROOT_URL` | `global` | `system` | `root-url` | `root_url` | `None` | The Landscape Server’s root URL path. HTTP requests are expected to be made to this path. |
| `LANDSCAPE_TESTRUN` | `LANDSCAPE_TESTING__TESTRUN` | `N/A` | `testing` | `N/A` | `test_run` | `False` | If true, do not replace the importer with the import guardian to speed up the tests. |
| `LANDSCAPE_TEST_RUNNER` | `LANDSCAPE_TESTING__TEST_RUNNER` | `N/A` | `testing` | `N/A` | `test_runner` | `trial` | The `twisted` test runner to use for the `trial` script in `/dev`. |
| `VAULT_ADDR` | `LANDSCAPE_SECRETS__VAULT_URL` | `secrets` | `secrets` | `secrets-url` | `vault_url` | `http://localhost:8200` | The address of the vault to use for the secrets service. |
| `VAULT_TOKEN` | `LANDSCAPE_SECRETS__VAULT_TOKEN` | `N/A` | `secrets` | `N/A` | `vault_token` | `None` | The token to use for the vault instead of getting it from the secrets service. |

The following immutable configurations can be set through environment variables only:

| ENV name | Default value | Purpose |
| :---- | :---- | :---- |
| `LANDSCAPE_CONFIG_FILE` | `/etc/landscape/service.conf` | File path location of the `service.conf` file. |
