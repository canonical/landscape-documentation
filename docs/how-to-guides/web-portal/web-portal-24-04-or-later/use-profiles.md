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

> Reference: {ref}`reference-terms-package-profile`

Package profiles let you define rules for how packages should exist on certain client instances. For example, you could use a package profile to prevent certain packages from being installed together on the same client instances.

To create a package profile, go to **Profiles** from the sidebar > **Package profiles**. Then **Add package profile** and complete the form. You'll need to specify what package constraints you want to enforce on the package profile in this form, and which access group and (optional) tags to apply the profile to.

Once you've created your profile, you can edit, remove, and more using the dot menu under **Actions** for each profile.

(how-to-web-portal-use-reboot-profiles)=
## Reboot profiles

```{note}
This feature is only available in **Landscape 25.04** and later.

Reference: {ref}`reference-terms-reboot-profile`
```

You can use reboot profiles to automatically restart specific Landscape Client instances on a scheduled basis.

To create a reboot profile, go to **Profiles** from the sidebar > **Reboot profiles**. Then **Add reboot profile** and complete the form. The following fields appear in the form:

   - **Name**: Name of the profile.
   - **Access group**: The access group the profile will apply to.
   - **Schedule**:

     - **Days**: The day(s) the reboot will occur
     - **Time**: The time (in 24-hour format) when the reboot will occur. The scheduled time is interpreted in UTC.
     - **Expires after**: A time window for retrying the reboot if it fails. The request will be retried until this window closes.

   - **Randomize delivery over a time window**: Select **Yes** if you want to stagger the delivery of reboots to the selected instances. This avoids rebooting them all simultaneously.
   - **Association**:

     - **All instances**: The profile will affect all instances in the same access group as the profile
     - **Tag(s)**: Only instances having the specific tag(s) will be affected

After you've created your reboot profile, you'll see the new profile listed along with its next scheduled reboot time. You can manage existing profiles using the dot menu under **Actions**.

## Removal profiles

> Reference: {ref}`reference-terms-removal-profile`

Removal profiles let you automatically remove client instances from Landscape that haven't communicated with the Landscape server in a specified number of days.

To create a removal profile, go to **Profiles** from the sidebar > **Removal profiles**. Then **Add removal profile** and complete the form. You'll need to specify the removal timeframe (in days), and which access group and (optional) tags to apply the profile to.

Once you've created your profile, you can edit, remove, and more using the dot menu under **Actions** for each profile.

## Repository profiles

> Reference: {ref}`reference-terms-repository-profile`

To create or manage a repository profile, see {ref}`how-to-heading-manage-repos-create-repo-profile`. Note that repository mirroring is only available for self-hosted Landscape users.

(how-to-web-portal-use-script-profiles)=
## Script profiles

```{note}
This feature is only available in self-hosted **Landscape 25.04** and later.

Reference: {ref}`reference-terms-script-profile`
```

You can use script profiles to execute scripts based on certain triggers. The possible triggers are: post-enrollment, date, and a recurring schedule.

To create a reboot profile, go to **Profiles** from the sidebar > **Script profiles**. Then **Add script profile** and complete the form. The following fields appear in the form:

   - **Name**: Name of the profile.
   - **Script**: Name of a corresponding script.
The same access group of this script will be assigned to the new profile.
   - **Run as user**: The username to execute the script as on the client.
   - **Time limit**: The time, in seconds, after which the script is considered defunct.
   - **Trigger**:

     - **Post Enrollment**: Triggers after a computer is enrolled in an account.
     - **On a date**: A UTC time at which the script profile should execute.
     - **Recurring**: A start date after which the profile will execute the specified [Cron](https://en.wikipedia.org/wiki/Cron) schedule.

   - **Association**:

     - **All instances**: The profile will affect all instances in the same access group as the profile.
     - **Tag(s)**: Only instances having the specific tag(s), in the same access group as the profile will be affected.

Once you've created your profile, you can edit, remove, and more using the dot menu under **Actions** for each profile.

## USG profiles

> Reference: {ref}`reference-terms-usg-profile`

To create or manage USG profiles, see {ref}`how-to-security-use-usg-profiles`.

## Upgrade profiles

> Reference: {ref}`reference-terms-upgrade-profile`

Upgrade profiles let you schedule and control when package updates are applied to client instances. This allows you to automate upgrades across groups of machines.

To create an upgrade profile, go to **Profiles** from the sidebar > **Upgrade profiles**. Then **Add upgrade profile** and complete the form. You'll need to specify the type of upgrades (e.g., security-only upgrades), the schedule of upgrades, and which access group and (optional) tags to apply the profile to.

Once you've created your profile, you can edit or remove it using the dot menu under **Actions** for each profile.

## WSL profiles

> Reference: {ref}`reference-terms-wsl-profile`

To create or manage a WSL profile, see {ref}`how-to-use-wsl-profiles`.
