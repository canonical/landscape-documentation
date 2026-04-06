---
myst:
  html_meta:
    description: "Complete reference for Landscape profiles including package, reboot, removal, repository, script, security, upgrade, and WSL profile types."
---

(reference-terms-profiles)=
# Profiles

**Profiles** in Landscape are reusable sets of rules that define how Landscape should manage certain managed instances (machines and devices). Profiles are usually applied to groups of managed instances matching the tags and/or access group of the profile. Landscape automatically applies any relevant existing profiles to newly accepted managed instances. When an administrator modifies the tags or access group for a managed instance, Landscape automatically updates the set of profiles associated with that managed instance accordingly.

Once a profile is created, the access group associated with the profile cannot be edited.

Many profiles have a notion of **compliance**. When a managed instance becomes associated with a profile, Landscape will create activities to bring that managed instance into compliance with any profile associated with that managed instance.

Landscape has multiple types of profiles.

(reference-terms-package-profile)=
## Package profile

A **package profile**, or meta-package, comprises a set of one or more packages, including their dependencies and conflicts (generally called constraints), that you can manage as a group. Package profiles specify sets of packages that associated systems should always get, or never get. 

The constraints for package profiles can be specified in the following ways:
- From an existing instance's packages
- Imported from a CSV file
- Manually specified

Package profiles must be associated with an access group which determines the set of instances that the profile can act on. You can also associate zero or more managed instances with each package profile via tags. You can manage package profiles from the sidebar by navigating to **Profiles** > **Package Profiles**.

Package profiles are evaluated periodically, and can be used for ensuring compliance over time. If package profiles are used to install packages, it is important to ensure any prerequisite repository configurations have been applied so the package can be downloaded, otherwise the package profile will fail to install the package, and report the managed instance as non-compliant.

(reference-terms-reboot-profile)=
## Reboot profile

A **reboot profile** defines how and when Landscape executes system reboots on managed instances. Reboot profiles can automatically restart managed instances on select days of the week with a frequency of no more than once per week. Reboots can be staggered by configuring the delivery window. Reboot profiles are associated with managed instances using tags and an access group. You can manage reboot profiles from the **Profiles** page.

(reference-terms-removal-profile)=
## Removal profile

A **removal profile** defines a maximum number of days that a managed instance can go without sending a message to Landscape server before it is automatically removed. If more days pass than the profile's *Days without exchange*, that managed instance will automatically be removed and the license seat it held will be released. This helps Landscape keep license seats open and ensures Landscape is not tracking stale or retired instance data for long periods of time. Landscape considers any message sent from the client to be data exchanged. Note that pings do not count as data exchanged, except for Windows hosts.

Removal profiles must be associated with an access group which determines the set of instances that the profile can act on. You can also associate zero or more managed instances with each removal profile via tags. You can manage removal profiles from the sidebar by navigating to **Profiles** > **Removal Profiles**.

(reference-terms-repository-profile)=
## Repository profile

A **repository profile** defines a set of pockets and APT sources for managed instances to use to source packages. When a managed instance is associated with a repository profile, the repository configurations are applied one time. Repository profiles don't perform ongoing monitoring of repository configurations. You can associate zero or more managed instances with each repository profile via tags to ensure those managed instances are governed by this repository profile. You can also associate a repository profile with an access group, which limits its use to only managed instances within the specified access group. You can manage repository profiles from the sidebar by navigating to **Profiles** > **Repository Profiles**.

(reference-terms-script-profile)=
## Script profile

A **script profile** defines how and when a script is automatically executed on managed instances based on specific triggers. It specifies the script, the user account that executes the script, the time limit, and a trigger that determines when the script runs. A script profile also defines which managed instances the script applies to, either through tags or to all managed instances within an access group. You can manage script profiles from **Scripts** > **Profiles** page.

(reference-terms-security-profile)=
## Security profile

A **security profile** defines how Landscape should monitor and manage security compliance on managed instances using the [Ubuntu Security Guide (USG)](https://documentation.ubuntu.com/security/compliance/usg/). Security profiles evaluate managed instances against established security benchmarks, such as CIS and DISA-STIG, to collect compliance data on a scheduled basis. With additional configuration, security profiles can attempt to resolve detected compliance issues. Security profiles are associated with managed instances using tags and an access group. You can manage security profiles from the **Profiles** page.

(reference-terms-upgrade-profile)=
## Upgrade profile

An **upgrade profile** defines a schedule for the times when upgrades are to be automatically installed on the managed instances associated with a specific access group. You can also associate zero or more managed instances with each upgrade profile via tags.

Upgrade profiles run according to a configurable weekly schedule. You can set what days of the week you want upgrades to run, and at what times you want upgrades to run on those days. You can also randomize the delivery time of the updates across your estate. Upgrade profiles can be set to only apply security upgrades or to apply all upgrades.

You can manage upgrade profiles from the sidebar by navigating to **Profiles** > **Upgrade Profiles**.

(reference-terms-wsl-profile)=
## WSL profile

A **WSL profile** defines a single Ubuntu WSL instance that Landscape should install on Windows instances (host machines) in a given access group. You associate Windows instances with WSL profiles using tags. A profile can specify:

- Which Ubuntu distribution to install, either from the Microsoft store or from a custom image
- cloud-init configuration (optional)
- Compliance settings that specify how to interact with any WSL instances that were not created by Landscape

 Each Windows instance can be associated with zero or more WSL profiles.

WSL profiles are evaluated periodically for compliance. A Windows instance is considered **compliant** if the following are true:

- Landscape has installed a WSL instance on that Windows instance as specified by each of its associated WSL profiles, or the installation is in progress
- All Ubuntu WSL instances installed on that Windows instance were created through Landscape if any associated WSL profiles use this compliance settings

Landscape will alert you when a registered Windows instance is out of compliance with any of its WSL profiles. You can then take action to bring any non-compliant Windows instances into compliance with their WSL profiles.
