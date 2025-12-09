(how-to-web-portal-use-reboot-profiles)=
# How to use reboot profiles

You can use reboot profiles to automatically restart specific Landscape Client instances on a scheduled basis.

```{note}
This feature is only available in **Landscape 25.04** and later.
```

## Create the profile

To create a new reboot profile from the web portal:

1. Click **Profiles**
2. Click **Reboot profiles**
3. Click **Add reboot profile**

In the profile creation form, complete the following fields:

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

After you've created your reboot profile, you'll see the new profile listed along with its next scheduled reboot time. 

You can manage existing profiles using the dot menu under **Actions**.
