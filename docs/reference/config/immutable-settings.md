---
myst:
  html_meta:
    description: "Complete reference for Landscape immutable configuration settings in service.conf and environment variables including system and service options."
---

(reference-immutable-settings)=
# Immutable configuration settings

The following immutable configurations can be set in `service.conf` or through environment variables.

## `LANDSCAPE_CONFIG_FILE`

```{note}
This configuration can be set through environment variables only.
```

- Purpose: File path location of the `service.conf` file. The `landscape` user must have read/write privileges to the file.
- Default value: `/etc/landscape/service.conf`

## `LANDSCAPE_MESSAGE_SERVER__MESSAGE_URL`

- Purpose: The message system URL to use.
- Default value: The HTTP version of the root URL with `/message-system` appended.
- Section: `message_system`
- Key: `message_system_url`
- Deprecated ENV name: `LANDSCAPE_MESSAGE_URL`
- Deprecated section: N/A
- Deprecated key: N/A

## `LANDSCAPE_SYSTEM__ANALYTICS_ID`

- Purpose: The Google Analytics ID for the deployment.
- Default value: `UA-1018242-60`
- Section: `system`
- Key: `analytics_id`
- Deprecated ENV name: `LANDSCAPE_ANALYTICS_ID`
- Deprecated section: N/A
- Deprecated key: N/A

## `LANDSCAPE_SYSTEM__APT_PORT`

- Purpose: The port the `landscape_apt` service should use.
- Default value: 8085
- Section: `system`
- Key: `apt_port`
- Deprecated ENV name: `LANDSCAPE_APT_PORT`
- Deprecated section: N/A
- Deprecated key: N/A

## `LANDSCAPE_SYSTEM__ENABLE_PASSWORD_AUTHENTICATION`

- Purpose: Whether users are allowed to log in with email/password or not.
- Default value: `False`
- Section: `system`
- Key: `enable_password_authentication`
- Deprecated ENV name: `LANDSCAPE_ENABLE_PASSWORD_AUTHENTICATION`
- Deprecated section:  `landscape`
- Deprecated key: `enable-password-authentication`

## `LANDSCAPE_SYSTEM__ENABLE_SUBDOMAIN_ACCOUNTS`

- Purpose: Whether subdomain-based functionality is enabled or not.
- Default value: `False`
- Section: `system`
- Key: `enable_subdomain_accounts`
- Deprecated ENV name: `LANDSCAPE_ENABLE_SUBDOMAIN_ACCOUNTS`
- Deprecated section:  `landscape`
- Deprecated key: `enable-subdomain-accounts`

## `LANDSCAPE_SYSTEM__ENABLE_TAG_SCRIPT_EXECUTION`

- Purpose: Whether to enable tag-based script execution.
- Default value: `False`
- Section: `system`
- Key: `enable_tag_script_execution`
- Deprecated ENV name: `LANDSCAPE_ENABLE_TAG_SCRIPT_EXECUTION`
- Deprecated section:  `landscape`
- Deprecated key: `enable-tag-script-execution`

## `LANDSCAPE_SYSTEM__FQDN`

- Purpose: Sets the root URL using the FQDN.
- Default value: `None`
- Section: `system`
- Key: `fqdn`
- Deprecated ENV name: `LANDSCAPE_FQDN`
- Deprecated section: N/A
- Deprecated key: N/A

## `LANDSCAPE_SYSTEM__GPG_HOME_DIR`

- Purpose: The directory containing GnuPG config files and the keyrings. The `landscape` user must have read/write privileges to the directory.
- Default value: `/var/lib/landscape-server/gnupg`
- Section: `system`
- Key: `gpg_home_dir`
- Deprecated ENV name: `LANDSCAPE_GPG_HOME`
- Deprecated section: N/A
- Deprecated key: N/A

## `LANDSCAPE_SYSTEM__LICENSE_FILE`

- Purpose: The file path location of the legacy license file. The `landscape` user must have read/write privileges to the file.
- Default value: `/etc/landscape/license.txt`
- Section: `system`
- Key: `license_file`
- Deprecated ENV name: `LANDSCAPE_LICENSE_FILE`
- Deprecated section: N/A
- Deprecated key: N/A

## `LANDSCAPE_SYSTEM__OFFLINE`

- Purpose: Whether offline mode is set or not (only relevant for standalone setups).
- Default value: `None`
- Section: `system`
- Key: `offline`
- Deprecated ENV name: `LANDSCAPE_OFFLINE`
- Deprecated section: `global`
- Deprecated key: `offline`

## `LANDSCAPE_SYSTEM__ROOT_URL`

- Purpose: The Landscape Server’s root URL path. HTTP requests are expected to be made to this path.
- Default value: `None`
- Section: `system`
- Key: `root_url`
- Deprecated ENV name: `LANDSCAPE_ROOT_URL`
- Deprecated section: `global`
- Deprecated key: `root-url`

## `LANDSCAPE_SECRETS__VAULT_URL`

- Purpose: The address of the vault to use for the Secrets service.
- Default value: `http://localhost:8200`
- Section: `secrets`
- Key: `vault_url`
- Deprecated ENV name: `VAULT_ADDR`
- Deprecated section: N/A
- Deprecated key: `secrets-url`

## `LANDSCAPE_SECRETS__VAULT_TOKEN`

- Purpose: The token to use for the vault instead of getting it from the secrets service.
- Default value: `None`
- Section: `secrets`
- Key: `vault_token`
- Deprecated ENV name: `VAULT_TOKEN`
- Deprecated section: N/A
- Deprecated key: N/A
