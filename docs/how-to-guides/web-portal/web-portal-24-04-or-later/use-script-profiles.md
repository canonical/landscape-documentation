(how-to-web-portal-use-script-profiles)=
# How to use script profiles

Script profiles can be used to execute scripts based on a trigger.

```{note}
This feature is only available in **Landscape 25.04** and later.
```

## Creating a script profile

From the web portal:

1. Go to **Scripts**.
2. Click on **Profiles**.
3. Click on **Add profile**.

In the script profile creation form, fill out the following fields:

- **Name**: Name of the profile.
- **Script**: Name of a corresponding script (the same access group will be assigned to the profile).
- **Run as user**: The username to execute the script as on the client.
- **Time limit**: The time, in seconds, after which the script is considered defunct.
- **Trigger**:
    - **Post Enrollment**: Triggers after a computer is enrolled in an account.
    - **On a date**: A point in time the script profile should execute.
    - **Recurring**: A start date after which the profile will execute the specified [Cron](https://en.wikipedia.org/wiki/Cron) schedule.
- **Association**:
    - **All instances**: The profile will affect all instances in the same access group as the profile.
    - **Tag(s)**: Only instances having the specific tag(s), in the same access group as the profile will be affected.

## Managing a script profile

You can manage a script profile using the **Actions** menu:

- **Edit**: Modify the name, username, time limit or affected instances.
- **Archive**: Archive the profile, making it inactive.
               Note that archiving is irreversible.
