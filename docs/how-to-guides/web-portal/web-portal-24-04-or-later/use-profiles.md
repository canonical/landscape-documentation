---
myst:
  html_meta:
    description: "Create and manage profiles in Landscape's 24.04+ portal including package, reboot, removal, script, security, and upgrade profiles."
---

(how-to-web-portal-use-profiles)=
# How to use profiles

Profiles in Landscape are reusable sets of rules that define how Landscape should manage specified instances. You can use profiles for different types of tasks, such as applying automatic upgrades on groups of client instances, or manage packages and their dependencies as a group, This guide describes how to create and manage different types of profiles in the web portal.

For a full list and description of each profile type, see {ref}`reference-terms-profiles`. Profiles are often managed using {ref}`tags <reference-terms-tags>` and/or {ref}`access groups <reference-terms-access-groups>`.

## Basic tasks for all profiles

To access different types profiles, go to **Profiles** from the sidebar > select the type of profile you're working on. 

To create a new profile, click **Add [profile type]**, and complete the form. The information on this form differs depending on the type of profile you're creating.

Once you've created your profile, you can edit, remove, and more using the dot menu under **Actions** for each profile.

## Package profiles

> See also: {ref}`reference-terms-package-profile`

Package profiles let you define rules for how packages should exist on certain client instances. For example, you could use a package profile to prevent certain packages from being installed together on the same client instances.

To create a package profile, go to **Profiles** from the sidebar > **Package profiles**. Then **Add package profile** and complete the form. You'll need to specify what package constraints you want to enforce on the package profile in this form, and which tags and/or access groups to apply the profile to.

Once you've created your profile, you can edit, remove, and more using the dot menu under **Actions** for each profile.

## Upgrade profiles

> See also: {ref}`reference-terms-upgrade-profile`

Upgrade profiles let you schedule and control when package updates are applied to client instances. This allows you to automate upgrades across groups of machines.

To create an upgrade profile, go to **Profiles** from the sidebar > **Upgrade profiles**. Then **Add upgrade profile** and complete the form. You'll need to specify the type of upgrades (e.g., security-only upgrades), the schedule of upgrades, and which tags and/or access groups to apply the profile to.

Once you've created your profile, you can edit or remove it using the dot menu under **Actions** for each profile.

### <CONTINUE> ###
