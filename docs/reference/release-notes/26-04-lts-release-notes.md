---
myst:
  html_meta:
    description: "Release notes for Landscape 26.04 LTS (April 2026). Introduces security event logging, FDE recovery key management, release upgrade REST API, the new debarchive repository service, and multiple security fixes."
---

(reference-release-notes-26-04-lts)=
# 26.04 LTS release notes

> See also: {ref}`how-to-upgrade-to-26-04-lts`

```{note}
- Landscape Server 26.04 LTS runs on Ubuntu 26.04 LTS Resolute Raccoon, 24.04 LTS Noble Numbat, or 22.04 LTS Jammy Jellyfish.
- Database schema changes are required to upgrade to Landscape Server 26.04 LTS.
- Landscape Server 26.04 LTS requires the `landscape-outbox` snap.
- The updated Landscape Server Charm will not be released until the Landscape Server 26.04.1 LTS point release in August 2026.
```

## Highlights

- **Security event logging**: Security-relevant actions are now recorded in the {ref}`reference-logs`, including:

  - Authentication success and failure events
  - Password reset events
  - JWT issuance, validation, and expiry events
  - User, employee, and admin profile updates
  - Role and permission changes
  - Authorization failures

- **FDE recovery key management**: The server now provides REST API endpoints for Full Disk Encryption (FDE) recovery key management, enabling automated storage and retrieval of recovery keys for enrolled machines. A new client plugin (fde-recovery-key-manager) enables the client to securely report FDE recovery keys to the server.

- **Soft deletion of computers**: Computer deletion now happens asynchronously, allowing for a smoother user workflow.

- **Release upgrade REST API**: New REST API endpoints for managing OS release upgrades have been added, providing improved control and status reporting compared to the legacy endpoints.

- **Repository management improvements**:

  - Introduces the new `debarchive` service for repository management.
  - Repository profiles have been updated with improved workflows.
  - A feature flag has been added for repository mirroring, with a safeguard that prevents upgrading from a version with existing repository mirrors until the feature is re-enabled.
  - The quickstart installer now includes `debarchive` for local archive support.
  - The legacy API endpoints for repository management have been removed; the new archive management system replaces them.

- **Ubuntu Installer attach service**: The Ubuntu Installer attach service is now included in the quickstart installation by default, allowing machines to be attached to Landscape during the Ubuntu installation process.

- **TLS support for RabbitMQ**: Standard TLS connections are now supported for RabbitMQ.

- **REST API strict content-type enforcement**: HTTP `POST`, `PUT`, and `PATCH` requests to the v2 REST API now require the `Content-Type: application/json` request header. Requests that omit this header will receive a 415 Unsupported Media Type response.

- **Python version and dependency updates**:

  - Landscape Server now vendors its Python dependencies into a virtual environment and requires Python 3.12.
  - Dependencies on `netaddr`, `python3-bs4`, `python3-oops-amqp`, `python3-stripe`, `simplejson`, and `wkhtmltopdf` have been removed.
  - The build system has migrated from `setup.py/requirements.txt` to `pyproject.toml` with `uv`.

- **Landscape Client - Configurable apt update timeout**: A new configuration option allows administrators to set a custom timeout for apt update operations, addressing issues with slow or unreliable package mirrors.

## Breaking changes

- **Legacy API repository management endpoints removed**: Users relying on these endpoints should migrate to the new repository management API.

- **Secrets management**: The legacy v1 secrets functionality and secrets UI have been removed. The modern secrets service replaces them.

## Bug fixes

- Fixed package changer not honouring the configured proxy when downloading packages.
- Fixed WSL profiles incorrectly adding non-Windows computers.
- Fixed Landscape Client snap builds and installation issues.
- Fixed socket leak when connectors encountered errors.
- Fixed `--url` and related options in the snap to be consistent with `landscape-config`.
- Fixed an issue where the Ubuntu release upgrader log used incorrect string formatting.
- Fixed a memory leak in the `pingserver` service.
- REST API requests authenticated with a JWT belonging to a disabled account now return HTTP 403 instead of a generic error.

## Security fixes

Multiple security fixes are included in this release:

- Fixed user enumeration on the password reset page.
- Fixed a stored cross-site scripting (XSS) vulnerability on the activity result page.
- Fixed a stored XSS vulnerability in the profile creation page.
- Fixed HTML escaping in Legacy UI page templates.
- Fixed sanitization of access group titles and descriptions (both in the UI and Legacy API).
- Fixed an arbitrary file deletion vulnerability in the package upload handler.
- Fixed a cross-site request forgery (CSRF) vector via GET-based state-modifying requests.
- Fixed a JavaScript execution (XSS) vulnerability.
- Replaced `xml.etree` with `defusedxml` throughout the codebase.
- Fixed a Landscape Client issue where data file permissions were too permissive. [LP: #2121558](https://bugs.launchpad.net/landscape-client/+bug/2121558)
- Fixed content-type header validation for REST API endpoints.

## Supported third-party services

| Service | Compatible versions |
| ------- | ------------------- |
| PostgreSQL | 14, 16, 18 |
| HAProxy | 2.4, 2.8, 3.2 |
| RabbitMQ | 3.9, 3.12 |
