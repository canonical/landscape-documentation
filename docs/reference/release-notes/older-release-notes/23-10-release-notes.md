---
myst:
  html_meta:
    description: "Release notes for Landscape version 23.10 (October 2023). Introduces WSL integration, JWT authentication, repository management dashboard, and auto-registration features."
---

(reference-release-notes-23-10)=
# 23.10 release notes

```{note}
Support for Landscape 23.10 ended in April 2024. 
```

Landscape 23.10 is an interim release and is **not recommended for production use**. Interim releases provide access to upcoming features, but these releases are only supported for 6 months, until the next release is published. Production deployments should only use LTS releases, which come with 10 years of support.

## Highlights

- **Windows Subsystem for Linux (WSL)**: Use Landscape with WSL and Ubuntu Pro for Windows
- **Repository management dashboard**: Preview the new repository management dashboard for self-hosted Landscape users.
- **JWT-Authentication for all API endpoints**: Introduced JWT-authentication as an option for all API endpoints. This feature is only available for users who don’t authenticate using SSO or OIDC at this time.
- **Auto-registration toggle:** Automatically register new computers when they’re registered using a registration key.
- **New `--method` parameter for `landscape-api`:** Use the new `--method` parameter to specify the HTTP method when making API calls.
- **Landscape Client - `landscape-config` changes:** The `landscape-config` command can now start the `landscape-client` systemd service.
- **Landscape Client - updated ping protocol:** Clients now use HTTPS (instead of HTTP) when pinging the message server for updates.

## Bugfixes

- [#2027613](https://bugs.launchpad.net/ubuntu/+source/landscape-client/+bug/2027613): Avoid stopping services on upgrade
- [#2043035](https://bugs.launchpad.net/landscape/+bug/2043035): Landscape UI lag

## Patch Notices

### Landscape Server

- 23.10+10 published on 6 June 2024
  - fix: persist session from old dashboard to new dashboard (LP: [#2066944](https://launchpad.net/bugs/2066944))

- 23.10+9 published on 8 May 2024
  - Schema changes required with new version of postgres on noble
  - API:
    - Add: Endpoints for account preferences management
    - Add: Endpoints to manage package profiles
    - Update: Computer packages split security upgrades from upgrades
    - Add: Add search for event log
    - Add: Search as optional kwarg to paginated endpoints
    - Fix: In legacy api add `access_group` parameter to `EditUpgradeProfile`
    - Update: Use `List` type for old API profile tags instead of `Array` type
    - Add: Alerts to computer object
    - Add: `/info` to snap endpoints (forwarded from snap store)
  - Add: Free accounts for SAAS users
  - Fix: Move onus of polling to front-end to old UI (LP: [#2043035](https://launchpad.net/bugs/2043035))
  - Fix: Actually use proxy settings for appserver process
  - Fix: Database object crossing thread boundaries in GRPC activities
  - Update: Hashids config for noble
  - Update: Allow server to run on Noble
  - Fix: Revert most of "batch pingserver update queries…"
  - Update: gRPC max connection age defaults to 30 days

- 23.10+3 published on 17 April 2024

   - Fix: reduce number of handing /ajax polls

- 23.10+2 published on 14 December 2023
    - Schema changes to support future Person-Computer relationships
    - Add activity ID to API responses with SyncPocket activities
    - Move repository dashboard to `/new_dashboard` from `/dashboard` to avoid clash
    with older pages
    - Use default account when no account provided during JWT API authentication
    - Add secrets dashboard to list, create, and remove secrets, if Vault
    integration is enabled
    - UI changes to support management of WSL instances belonging to registered
    Windows hosts

