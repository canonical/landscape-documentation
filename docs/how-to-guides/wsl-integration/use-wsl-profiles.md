(how-to-use-wsl-profiles)=

# How to use WSL profiles

```{note}
This feature is currently in beta.
```

> See also: {ref}`reference-rest-api-child-instance-profiles` and {ref}`reference-rest-api-wsl`.

This guide describes how to use WSL profiles (also called child instance profiles) to provision WSL instances and manage them with Landscape.

## Create a WSL profile in the Landscape web portal

You can create a new WSL profile from the Landscape web portal. To do this:

1. Click **Profiles**
2. Click **WSL profiles**
3. Click **Add WSL profile**

In the WSL profile creation form, complete the following fields:

- **Title**: A title for the profile.
- **Description**: A human readable description for the profile.
- **Access group**: The access group the profile will apply to. Restricts which instances the profile can manage and which users can edit and execute the profile.
- **RootFS image**: The URL or file path for the RootFS image.
- **Cloud-init**: The contents of the cloud init to be supplied to the WSL instance. This can be uploaded as a file or inputted as text.
- **Association**:
  - **Associate to all instances**: The profile will affect all instances in the same access group as the profile
  - **Tag(s)**: Only instances having the specific tag(s), in the same access group as the profile will be affected

After you've created your WSL profile, activities will be created to install the specified WSL instance on the associated Windows host machines.
A Windows host machine is considered compliant with a WSL profile if it has the corresponding WSL instance that is created by Landscape.

You can view, edit, duplicate, or remove the profile using the dot menu under **Actions**. You can also see the number of associated parents and the number of compliant or non-compliant Windows host machines.

## Create a WSL profile using the Landscape API

You can create a WSL profile via Landscape's REST API.

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d '{"title": "JammyProfile", "description": "Jammy", "image_name": "Ubuntu-22.04", "all_computers": "true"}'
```

## Reapply a WSL profile using the Landscape API

Activities to install the corresponding WSL instance are automatically created when a Windows host machine is associated with a WSL profile.
If you want to fix any non-compliant Windows host machines, you can reapply a WSL profile via Landscape's REST API.

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles/JammyProfile:reapply -H "Authorization: Bearer $JWT"
```

## Apply all WSL profiles by Windows host machine in the Landscape web portal

You can apply all WSL profiles that are associated to a Windows host machine from the Landscape web portal. To do this:

1. Find the Windows machine that you want to apply WSL profiles. This can be found by clicking the link under **Associated parents** in the **WSL profiles** page or by going to the **Instances** page.
2. Click the name of the Windows machine that you want to make compliant.
3. Click on the **WSL** tab.
4. Click on **Make Compliant**
5. Type "make {the name of your Windows host machine} compliant"

This will create activities to provision WSL instances on specified Windows host machines for all associated WSL profiles.

```{note}
The **Make compliant** button will be hidden if the Windows machine has no associated WSL profiles.
```

## Apply all WSL profiles by Windows host machine using the Landscape API

You can reapply all WSL profiles on specified Windows host machines via Landscape's REST API.

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles/make-hosts-compliant -H "Authorization: Bearer $JWT" -d '{"host_computer_ids": [6, 15]}'
```
