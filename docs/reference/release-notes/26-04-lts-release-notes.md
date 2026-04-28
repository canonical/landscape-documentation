---
myst:
  html_meta:
    description: "Release notes for Landscape 26.04 LTS (April 2026). Features FDE recovery key management, Ubuntu release upgrades, saved searches, and a new Juju charm architecture."
---

(reference-release-notes-26-04-lts)=
# 26.04 LTS release notes

> See also: {ref}`how-to-migrate-to-26-04-charm`

**Note**: Landscape 26.04 LTS runs on Ubuntu 24.04 LTS Noble Numbat or 22.04 LTS Jammy Jellyfish.

**Note**: Database schema changes are required to upgrade to Landscape Server 26.04 LTS.

## Highlights

- **Full Disk Encryption (FDE) recovery key management**: Centrally request, store, and manage FDE recovery keys for compatible managed instances directly from Landscape Server. Recovery keys are stored securely in the Landscape Secrets Storage service. This feature is available for self-hosted Landscape 26.04 LTS and later. For more information, see {ref}`explanation-fde-recovery-key`.

- **Ubuntu release upgrades**: Upgrade managed instances to a newer Ubuntu release directly from Landscape. New REST API endpoints allow you to retrieve available upgrade targets and issue release upgrade requests to groups of instances. See the {ref}`REST API reference <reference-rest-api>` for details on the `/computers/release-upgrade-targets` and `/computers/release-upgrades` endpoints.

- **Saved searches in the web portal**: Save and reuse instance search queries in the Landscape web portal. Saved searches let you quickly filter instances by specific criteria without rebuilding queries each time. You can create, apply, edit, and delete saved searches from the **Instances** page.

- **New Juju charm architecture**: The 26.04 Landscape Server charm introduces a new deployment architecture. The charm now integrates directly with the external HAProxy charm (`2.8/edge`) using the `haproxy-route` interface, replacing the legacy `reverseproxy` interface. TLS is now managed by the HAProxy charm via the `tls-certificates` interface, enabling automated certificate management. PostgreSQL 16 and the modern `database` interface are recommended for new deployments. For migration instructions, see {ref}`how-to-migrate-to-26-04-charm`.

- **PgBouncer support for Juju deployments**: New support for [PgBouncer](https://charmhub.io/pgbouncer) as a connection pooler between Landscape Server and PostgreSQL in Juju deployments. PgBouncer improves database performance and scalability, and is recommended for production deployments with significant client loads. For more information, see {ref}`explanation-pgbouncer-integration`.

## Additional Updates

- **Secrets Service with HashiCorp Vault support**: The Landscape Secrets Service, which stores sensitive data such as FDE recovery keys, can now be configured to use [HashiCorp Vault](https://developer.hashicorp.com/vault) as a backend. TLS and mTLS connections to Vault are supported.
- **TLS and mTLS for internal services**: Landscape's internal services (including the broker, appserver, and async_frontend) can now be configured to use TLS or mTLS for their internal connections.
- **Test email REST API endpoint**: A new `POST /person:test-email` REST API endpoint allows administrators to verify their mail queue configuration by sending a test email.
- **Release upgrade search filter**: The `GET /computers` REST API endpoint now supports `release-upgrade:available` as a search query value and the `with_release_upgrades` parameter to include release upgrade availability in computer objects.
- **New pingserver configuration options**: Two new `[pingserver]` settings are available in `service.conf`: `batch_size` (controls ping write batch size, default `100`) and `statement_timeout_ms` (controls database write timeout in milliseconds, default `3000000`).
- **Access group title restrictions**: Access group titles now only accept `.` and `-` as special characters. Other special characters are stripped from the title.
- **Snap validation sets guidance**: New guidance on using snap validation sets to control snap updates across IoT and Ubuntu Core devices.
- Cron job scripts now use a PID file in `/run/landscape/` to prevent concurrent execution.
- The `sync_lds_releases.sh` and `report_anonymous_metrics.sh` maintenance scripts were removed in Landscape 25.10.

## Upgrade

### Self-hosted (deb archive)

There are no additional upgrade steps beyond the standard upgrade process for self-hosted deb archive installations. Follow the existing guide: {ref}`how-to-upgrade`.

### Juju charm deployments

The 26.04 Landscape Server charm introduces significant architectural changes. If you are upgrading from an existing Juju charm deployment, see {ref}`how-to-migrate-to-26-04-charm` for migration instructions.

For new Juju deployments, use the `26.04/beta` channel:

```bash
juju refresh landscape-server --channel 26.04/beta
```

## Bug fixes

- Fixed user enumeration vulnerability on the password reset page
- Fixed arbitrary file deletion vulnerability in package upload
- Enforced `application/json` content-type header check on `POST`, `PUT`, and `PATCH` requests
- Blocked cross-site request forgery via GET-based state modifications
- Fixed cross-site scripting vulnerability on the profile creation page
- Fixed cross-site scripting vulnerability on the activity result page
- Fixed hidden input fields when a validation error occurs
- Fixed issue with Ubuntu Pro free license handling
- Fixed HTML escaping of account title in invitation emails
- Forced download for all script attachments to prevent content injection
- Fixed Zope template security bugs
- Fixed pingserver reliability issues
