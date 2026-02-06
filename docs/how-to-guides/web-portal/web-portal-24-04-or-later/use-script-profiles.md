(how-to-web-portal-use-script-profiles)=
# How to use script profiles

You can use script profiles to execute scripts based on certain triggers.
The possible triggers are: post-enrollment, date, and a recurring schedule.

```{note}
This feature is only available in self-hosted **Landscape 25.04** and later.
```

## Create a script profile

From the web portal:

1. Go to **Scripts**.
2. Click **Profiles**.
3. Click **Add profile**.

In the script profile creation form, complete the following fields:

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

After you've created your script profile, you can view, edit, or archive it from the **Profiles** tab, under *Actions*.
