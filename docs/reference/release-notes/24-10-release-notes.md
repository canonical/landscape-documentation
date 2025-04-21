(reference-release-notes-24-10)=
# 24.10 release notes

> Landscape 24.10 runs on Ubuntu 24.04 LTS Noble Numbat or 22.04 LTS Jammy Jellyfish. Database schema changes are required to upgrade to Landscape Server 24.10.

You can now access Landscape 24.10 in our `latest-stable` rolling release PPA: `ppa:landscape/latest-stable`. 

Note that 24.10 is not an LTS release. For self-hosted production deployments, we recommend using an LTS release, such as [Landscape 24.04 LTS](/reference/release-notes/24-04-lts-release-notes), which come with 10 years of support.

## Highlights

* **Manage kernel versions and view Livepatch status information**: Upgrade (and downgrade) installed kernel versions on managed clients using Landscape’s web portal and view Livepatch status and kernel package information for Livepatch-enabled clients. For more information, see [how to manage Livepatch and kernel updates from the Landscape web portal](/how-to-guides/web-portal/web-portal-24-04-or-later/manage-livepatch-and-kernel-updates).

   ![Manage Landscape kernel versions](https://assets.ubuntu.com/v1/b0bb4263-manage_kernel_versions.png)

* **Okta login for select subdomain-hosted accounts**: Select customers may configure their own Okta server to authenticate their Landscape users.

    ![Okta login](https://assets.ubuntu.com/v1/7c2763c0-okta_login.png)

* **New login page**: SaaS and self-hosted accounts have the option to authenticate with SSO, and self-hosted also continues to have password authentication. You don’t need to make any changes to your service configuration to access the new login page.

* **New REST API endpoints and access for SaaS users**: The REST API is now available for SaaS users. A number of new endpoints have also been added to the REST API, including ones for managing package and repository profiles. For more information, see [how to make a REST API request](/how-to-guides/api/make-a-rest-api-request).

## Additional Updates

* **WSL management features**: WSL users now have the ability to provide a cloud-init YAML file to configure your WSL instances at creation time, and the choice to provide a custom root filesystem for the instances. Note that Ubuntu Pro for WSL is in beta, and is not generally available yet in the Microsoft Store.

    ![WSL management from the web portal](https://assets.ubuntu.com/v1/bc8cf059-wsl_management.png)

## Upgrade

For more information on upgrades, see [how to upgrade your Landscape server](/how-to-guides/upgrade/upgrade-landscape).

### Self-hosted

To upgrade to Landscape 24.10 from 24.04 LTS, you need to add `session session-autocommit` to `stores` under `[api]` in your `service.conf` file.

```bash
[api]
stores = main account-1 resource-1 package session session-autocommit
```

### Landscape Server charms

To use the `latest-stable` version of Landscape with the charms, you need charm revision 124 or above.

## Bug fixes

* [#2069746](https://bugs.launchpad.net/landscape/+bug/2069746): missing distribution information caused mis-identification of distros
* [#2076014](https://bugs.launchpad.net/landscape/+bug/2076014): improved resiliency against database disconnections
* [#2072985](https://bugs.launchpad.net/landscape/+bug/2072985): better errors when attempting to manage Snaps on unsupported instances
* [#2065095](https://bugs.launchpad.net/landscape/+bug/2065095): improved directory structure of mirrored repositories, serving the “ubuntu” directory as-needed
* Fixed “datetime” usage error in landscape-hostagent-messenger
* Database user no longer reset during upgrade with UPGRADE_SCHEMA enabled
* Updated available WSL instance types



