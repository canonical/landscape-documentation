(reference-release-notes-24-04-lts)=
# 24.04 LTS release notes

> See also: {ref}`how-to-upgrade-to-24-04-lts`

**Note**: Landscape 24.04 LTS runs on Ubuntu 24.04 LTS Noble Numbat or 22.04 LTS Jammy Jellyfish.

**Note**: Database schema changes are required to upgrade to Landscape Server 24.04 LTS.

## Highlights

- **New web portal:** Use Landscape’s new, early-access web portal built with Canonical’s [Vanilla Framework](https://vanillaframework.io). 
    
    ![Landscape 24.04 LTS new web portal](https://assets.ubuntu.com/v1/ef0d70d5-24.04LandscapeWebPortal.png)

    This portal is available to self-hosted Landscape users. To access it, click **Try the new UI** from the header of the default web portal. The first time you use the portal, you may need to generate new API credentials to access the portal. For more information, see {ref}`how to generate API credentials <howto-heading-manage-repos-web-portal-generate-api-credentials>`.
    
- **Web-based repository management**: Manage and mirror your repositories locally with Landscape’s new web-based repository management. For more information, see {ref}`how-to-manage-repos-web-portal` and an {ref}`explanation-repo-mirroring`.

- **REST API for self-hosted users**: Use the new REST API that supports JSON Web Tokens for authentication. For more information, see {ref}`how-to-rest-api-request` and the available REST API endpoints.

- **Snap management:** Manage snaps directly from the Landscape web portal.

- **Landscape Client - new features for Ubuntu Core users**: The Landscape Client snap now includes additional features for Ubuntu Core users, such as remote script execution for snaps, user management on Core, and more. For more information, see the {ref}`how-to-guides-iot-for-devices-index`.

## Additional updates

- WSL: Update apache2 config template for Landscape Quickstart installations to use SSL/TLS on gRPC calls
- Quickstart installation configures PostgreSQL `max_connections` and `max_prepared_transactions`

## Bug fixes

- [#2055348](https://bugs.launchpad.net/ubuntu/+source/landscape-client/+bug/2055348): Potential arbitrary execution in `expandvars`
- [#2057976](https://bugs.launchpad.net/ubuntu/+source/landscape-client/+bug/2057976): Ubuntu Pro info is not sent on registration
- [#2043035](https://bugs.launchpad.net/landscape/+bug/2043035): Landscape UI lag
- [#2062561](https://bugs.launchpad.net/ubuntu/+source/landscape-client/+bug/2062561): There are no APT sources configured in `/etc/apt/sources.list` or `/etc/apt/sources.list.d`.
- In the legacy API, add `access_group` parameter to `EditUpgradeProfile`
- Fix with OIDC login not working, not producing any errors
- Fixed the database object crossing thread boundaries in gRPC activities
- Fix with `bpickle` to guard against negative string/bytestring lengths
- Fixed errors on Ubuntu Pro tab for Windows machines
- Fixed startup errors when Pro Licenses are the only Licenses
- Memory-usage improvements for `landscape-appserver` service
- Extra prevention against invitation hijacking
- Language improvements around allowlists and blocklists
- WSL instances are deleted when hosts stop reporting them
- Distribution information is provided for pending Windows machines

## Patch Notices

### Landscape Server

- 24.04.9 published 4 November 2024

  * fix: attempt to recover disconnected db connections on reuse (LP: [#2076014](https://launchpad.net/bugs/2076014))

- 24.04.8 published 3 October 2024

  * build: re-build to unblock Launchpad PPA publication

- 24.04.7 published 2 October 2024

  * fix: reprepro list/sync race condition (LP: [#2081056](https://launchpad.net/bugs/2081056))

- 24.04.6 published 9 September 2024

  * feat: PAM-mediated LDAP/AD auth in REST API login (LP: [#2077763](https://launchpad.net/bugs/2077763))

- 24.04.5 published 14 June 2024

  * fix(hostagent-messenger): remove hostagent_api submodule and use grpcio-tools to generate stubs instead.
  * fixes broken release 24.04.4

- 24.04.4 published 13 June 2024

  * fix(package-search): include sslmode parameter in config for connections to Postgres. Previously hardcoded to 'disable' (LP: [#2064756](https://launchpad.net/bugs/2064756))

- 24.04.3 published on 6 June 2024

  - fix: correct new dashboard login page API URL.
  - fix: persist session from old dashboard to new dashboard (LP: [#2066944](https://launchpad.net/bugs/2066944))

## Landscape 24.04.10 Point Release

We published the 24.04.10 point release on 27 February 2025.

 - fix: change access group API bug
 - fix: API permissions check
 - fix: make use of MD5 hash FIPS-compliant
 - fix: bug in v2 API eventlog endpoint
 - fix: make logfile create perms CIS-compliant; proper signal to rsyslogd
 - fix: prevent epoll race conditions when writing API responses
 - fix: reset passphrase oops backport (LP: [#2094844](https://bugs.launchpad.net/landscape/+bug/2094844))
 - fix: 500 error when logging out in standalone