(how-to-web-portal-use-security-profiles)=
# How to use security profiles

You can use security profiles to automatically audit and fix your managed instances on a schedule using the [Ubuntu Security Guide (USG)](https://documentation.ubuntu.com/security/docs/compliance/usg/).

```{note}
This feature is only available in self-hosted **Landscape 25.04** and later.
```

## Create a security profile

On each instance you want to manage, follow the steps in [Install Ubuntu Security Guide](https://documentation.ubuntu.com/security/docs/compliance/usg/install-usg/), then:

1. Edit the client configuration file `/etc/landscape/client.conf`, add this line:

    ```
    include_manager_plugins = UsgManager
    ```

    If your `client.conf` already includes an `include_manager_plugins` line, then add `UsgManager` to it. For example:

    ```
    include_manager_plugins = ScriptExecution,UsgManager
    ```

2. Restart Landscape Client:

    ```
    sudo systemctl restart landscape-client
    ```

From the web portal:

1. Click **Profiles**
2. Click **Security Profiles**
3. Click **Add security profile**

In the security profile creation form, complete the following fields:

- **Profile name**: name of the profile
- **Access group**: the access group the profile will apply to
- **Base profile**: the security benchmark the profile will use
- **Mode**: the profile's mode – which actions it will perform on instances
- **Upload tailoring file**: a [benchmark customization file](https://documentation.ubuntu.com/security/docs/compliance/usg/cis-customize/). If provided, it supersedes the **Base profile**.
- **Schedule**:
  - **On a date**: a specific date and time at which the profile will execute once
  - **Recurring**: a start date and end date between which the profile will execute repeatedly, with the provided number of days between executions. The recurrence cannot be more frequent than once every seven days.
- **Association**:
  - **Associate to all instances**: The profile will affect all instances in the same access group as the profile
  - **Tag(s)**: Only instances having the specific tag(s), in the same access group as the profile will be affected
  
After you've created your security profile, you can view, edit, run, duplicate, or archive it from the **Security profiles** tag, under **Actions**.

## Download audit for a security profile

You can download the results of USG audits executed by your security profile for a specific date or for a range of dates.

From the web portal:

1. Click **Profiles**
2. Click **Security Profiles**
3. Click the menu dots under **Actions** for a profile
4. Click **Download audit**

In the download audit form, complete the following fields:

- **Audit timeframe**:
  - **Specific date**: a date on which the profile ran
  - **Date range**: a start date and end date between which all profile run results will be collected into a single report
- **Level of detail**:
  - **Summary only**: the report will only include the overall pass rate for each instance
  - **Detailed view**: the report will also include individual audit rules and their severity, references, description, and rationale

You report will be generated and you will see a notification "Your requested audit is ready". Click **Download audit** to download the report CSV file.
