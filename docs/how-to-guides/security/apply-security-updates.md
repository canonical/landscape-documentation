(how-to-apply-security-updates)=
# How to apply security patches and upgrades

You can use Landscape to apply security updates to your client machines. This includes Livepatch for kernel patches within Landscape’s web portal.

Landscape Server gets security update information from [Ubuntu Security Notices](https://ubuntu.com/security/notices) (USNs), many of which are based on [Common Vulnerabilities and Exposures](https://www.cve.org/) (CVE) reports. Landscape Client can also report security updates, but these updates come from a variety of sources because they’re reported from the package sources each client is configured to use.

## Apply security updates

You can apply security updates directly from the Landscape web portal, but the process differs slightly depending on which web portal you use.

You can also create [upgrade profiles](/reference/terms/profiles/upgrade-profile) to schedule security updates.

### Web portal (24.04 LTS and later)

There are two options to view the instances that have security upgrades available:

- **Overview**: From the **Overview** tab (home page), find the **Upgrades** section and click the instances link next to “Security”.
- **Instances**: From the **Instances** tab, select **Status** > **Security upgrades**.

You can update the security fixes on a per-instance basis. To do this, select the instance, and upgrade from the **Security issues** tab.

Or, you can update multiple instances at a time, but this would update all packages in those instances, not just the security updates. To do this, select the checkbox for the instances you want to fully update, then click **Upgrade**.

### Classic web portal

You can view security updates available and upgrade on a per-computer basis. To do this, select each computer in the classic web portal, and click **Packages**. In this tab, you can view and apply any reported security updates.

### Upgrade profiles

You can use [upgrade profiles](/reference/terms/profiles/upgrade-profile) to schedule any package updates, and you can choose to only upgrade security issues.

For more details, see [how to manage upgrade profiles](/how-to-guides/web-portal/classic-web-portal/manage-computers.md#manage-upgrade-profiles).

## Apply updates from Livepatch

> See also: [Livepatch documentation](https://ubuntu.com/security/livepatch/docs)

You can use Livepatch to schedule high and critical Linux kernel vulnerability patches, which removes the immediate need to reboot to upgrade the kernel on critical infrastructure.

For more information, see our documentation on [how to manage Livepatch and kernel updates from the Landscape web portal](/how-to-guides/web-portal/web-portal-24-04-or-later/manage-livepatch-and-kernel-updates.md) (24.04 and later).