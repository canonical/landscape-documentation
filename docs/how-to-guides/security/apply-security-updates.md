---
myst:
  html_meta:
    description: "Apply security patches and kernel updates using Landscape. Schedule security upgrades with Livepatch for high and critical vulnerabilities."
---

(how-to-apply-security-updates)=
# How to apply security patches and upgrades

You can use Landscape to apply security updates to your client machines. This includes Livepatch for kernel patches within Landscape’s web portal.

Landscape Server gets security update information from [Ubuntu Security Notices](https://ubuntu.com/security/notices) (USNs), many of which are based on [Common Vulnerabilities and Exposures](https://www.cve.org/) (CVE) reports. Landscape Client can also report security updates, but these updates come from a variety of sources because they’re reported from the package sources each client is configured to use.

## Apply security updates

You can apply security updates directly from the Landscape web portal, but the process differs slightly depending on which web portal you use.

You can also create an {ref}`reference-terms-upgrade-profile` to schedule security updates.

### Web portal (24.04 LTS and later)

There are two options to view the instances that have security upgrades available:

- **Overview**: From the **Overview** tab (home page), find the **Upgrades** section and click the instances link next to "Security".
- **Instances**: From the **Instances** tab, select **Status** > **Security upgrades**.

You can update the security fixes on a per-instance basis. To do this, select the instance, and upgrade from the **Security issues** tab.

Or, you can update multiple instances at a time, but this would update all packages in those instances, not just the security updates. To do this, select the checkbox for the instances you want to fully update, then click **Upgrade**.

#### Apply an individual CVE or USN fix

You can use remote script execution and Ubuntu Pro Client to apply an individual CVE or USN fix to selected managed instances in Landscape. This is useful if you want to test a specific security fix on a group of instances before applying it more broadly.

This process involves using Ubuntu Pro Client and the `pro fix` command. For more information, see their documentation: [Ubuntu Pro Client | How to resolve a specific CVE or USN](https://documentation.ubuntu.com/pro-client/en/latest/howtoguides/fix_how_to_resolve_given_cve/). Note that Ubuntu Pro Client must be installed on the target instances for this process to work.

From the web portal, add and run a script on the target instances (see {ref}`how-to-web-portal-use-remote-script-execution`) that uses `pro fix` and the CVE or USN ID(s) you want to fix.

For example, this script applies the fix for `CVE-YYYY-NNNN`:

```bash
#!/bin/bash
set -e

pro fix CVE-YYYY-NNNN
```

Landscape will create script execution activities for each selected instance. Use the **Activities** page or the instance’s **Activities** tab to review the status and output.

### Classic web portal

You can view security updates available and upgrade on a per-computer basis. To do this, select each computer in the classic web portal, and click **Packages**. In this tab, you can view and apply any reported security updates.

### Upgrade profiles

You can use an {ref}`reference-terms-upgrade-profile` to schedule any package updates, and you can choose to only upgrade security issues.

For more details, see [how to manage upgrade profiles](/how-to-guides/web-portal/classic-web-portal/manage-computers.md#manage-upgrade-profiles).

## Apply updates from Livepatch

> See also: [Livepatch documentation](https://ubuntu.com/security/livepatch/docs)

You can use Livepatch to schedule high and critical Linux kernel vulnerability patches, which removes the immediate need to reboot to upgrade the kernel on critical infrastructure.

For more information, see our documentation on {ref}`how-to-web-portal-manage-livepatch` (24.04 and later).
