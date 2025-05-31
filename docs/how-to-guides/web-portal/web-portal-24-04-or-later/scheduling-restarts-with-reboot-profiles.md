# Scheduling restarts for Landscape Client instances with reboot profiles

Reboot profiles in Landscape allow you to automatically restart specific Landscape Client instances on a scheduled basis. This guide will walk you through creating a reboot profile that restarts selected instances at regular intervals every week.

```{note}
This feature is only available in **Landscape 25.04** and later.
```

## Creating the profile

In the web app (`/new_dashboard`):

1. Expand the **Profiles** tab.
2. Click on **Reboot profiles**.
3. Click the green **Add reboot profile** button.

In the profile creation form, fill out the following fields:

- **Name**: Enter the name of the profile.
- **Access group**: Select the access group associated with this profile.
- **Schedule**: Choose the day(s) of the week and the time (in 24-hour format) when the reboot will occur.
- **Expires after**: Specify a time window for retrying the reboot if it fails. The request will be retried until this window closes.
- **Randomize delivery over a time window**: Select this option if you want to stagger the delivery of reboots to the selected instances to avoid rebooting them all simultaneously.
- **Association**: Set which instances this profile will affect using one of the following options:
  - **All instances**: Check this box if you want the profile to affect all Landscape Client instances.
  - **Tag(s)**: Only instances with the specified tag(s) will be affected by this profile.

Once you have completed the fields, click **Add reboot profile** to create the profile. You should now see the new profile listed along with its next scheduled reboot time.

## Managing reboot profiles

After creating a profile, you can manage it using the **Actions** menu (the three dots at the end of each row):

- **Edit**: Modify the schedule or settings. Changes will apply to the next run.
- **Duplicate**: Create a new profile using the current one as a template.
- **Delete**: Permanently remove the profile.
