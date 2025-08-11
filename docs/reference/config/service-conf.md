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

The `[async_frontend]` section contains configurations that apply to the `landscape-async-frontend` service which handles AJAX requests from the Legacy UI. It has no settings beyond those shared by all services.

In practice, only the `base_port` setting needs to be configured for the service to operate correctly.
