(scheduling-restarts-with-reboot-profiles)=
# Scheduling restarts for Landscape Client instances with reboot profiles

Reboot profiles in Landscape allow you to automatically restart specific Landscape Client instances on a scheduled interval.

This guide will show you how to create a reboot profile using Landscape Server to restart selected instances weekly.

```{note}
This feature is only available in **Landscape 25.04** and later.
```

## Use case

Imagine you're a system administrator at ACME Corp., a fictional media production studio. You manage several workstations using Landscape. Because of the memory-intensive workloads at your studio, you want to clear temporary files and caches by restarting machines at the end of each work week. Let’s walk through how to automate that with reboot profiles!

## Creating the profile

To start, determine which Landscape Client instances the reboot profile should target. You can select instances by tag or access group. In this case, we’ll apply the profile to all instances.

In the web app (`/new_dashboard`):

1. Expand the **Profiles** tab.
2. Click on **Reboot profiles**.
3. Click the green **Add reboot profile** button.

In the profile creation form:

- **Name**: Enter a name, e.g., `"Clear cache"`.
- **Access group**: Leave this as `"Global access"`.
- **Schedule**: Set the reboot to occur **every Saturday at 3:30 AM** by selecting the day and entering `3:30` in the time field.
- **Expires after**: Set this to **2 hours**—if a reboot fails, the request will be retried until this window closes.
- **Randomize delivery over a time window**: Choose `"No"` to execute the reboots without staggering them.
- **Associate to all instances**: Check this box to apply the profile to every machine.

Click **Add reboot profile** to save. You should now see the new profile listed, with its **next scheduled reboot** time clearly displayed.

## Managing reboot profiles

After creating a profile, you can manage it using the **Actions** menu (the three dots):

- **Edit**: Modify the schedule or settings. Changes apply to the next run.
- **Duplicate**: Create a new profile using the current one as a template.
- **Delete**: Permanently remove the profile.
