(reference-terms-profiles)=
# Profiles

**Profiles** in Landscape are reusable sets of configuration rules that define how Landscape should manage certain instances (machines and devices). Profiles are usually applied to groups of instances.

Landscape has multiple types of profiles.

(reference-terms-package-profile)=
## Package profile

A **package profile**, or meta-package, comprises a set of one or more packages, including their dependencies and conflicts (generally called constraints), that you can manage as a group. Package profiles specify sets of packages that associated systems should always get, or never get. You can associate zero or more computers with each package profile via tags to install packages on those computers. You can also associate a package profile with an access group, which limits its use to only computers within the specified access group. You can manage package profiles from the **Profiles** tab in your organization's home page.

Package profiles are evaluated periodically, and can be used for ensuring compliance over time. If package profiles are used to install packages, it is important to ensure any prerequisite repository configurations have been applied so the package can be downloaded, otherwise the package profile will fail to install the package, and report the machine as non-compliant.

(reference-terms-removal-profile)=
## Removal profile

A **removal profile** defines a maximum number of days that a computer can go without exchanging data with the Landscape server before it is automatically removed. If more days pass than the profile’s “Days without exchange”, that computer will automatically be removed and the license seat it held will be released. This helps Landscape keep license seats open and ensure Landscape is not tracking stale or retired computer data for long periods of time. You can associate zero or more computers with each removal profile via tags to ensure those computers are governed by this removal profile. You can also associate a removal profile with an access group, which limits its use to only computers within the specified access group. You can manage removal profiles from the **Profiles** tab in your organization's home page.

(reference-terms-upgrade-profile)=
## Upgrade profile

An **upgrade profile** defines a schedule for the times when upgrades are to be automatically installed on the machines associated with a specific access group. You can associate zero or more computers with each upgrade profile via tags to install packages on those computers. You can also associate an upgrade profile with an access group, which limits its use to only computers within the specified access group. You can manage upgrade profiles from the **Profiles** tab in your organization's home page.