(how-to-use-wsl-profiles)=

# How to use WSL profiles

> See also: {ref}`reference-rest-api-child-instance-profiles` and {ref}`reference-rest-api-wsl` REST API endpoints.

```{note}
This feature is currently in beta.
```

This guide describes how to use WSL profiles to provision WSL instances and manage them with Landscape.

## Background information

In Landscape, a child instance profile is a configuration that defines the virtual instances, such as containers or VMs, that run on a machine registered with Landscape. Currently, WSL profiles are the only type of child instance profile supported.

WSL profiles specify the WSL instance to be provisioned on a Windows host machine. Each WSL profile corresponds to a single WSL instance with a unique rootfs image name. You also have the option to configure your WSL instance with a cloud-init file.

A Windows host machine is considered **compliant** with a WSL profile if it meets one of these criteria:
  - It has an installed WSL instance that's registered with Landscape and matches the profile, or
  - It has an activity to provision and register the corresponding WSL instance.
  
A Windows machine that doesn't meet either of these criteria is considered **non-compliant** with the WSL profile.

## Create a WSL profile in the Landscape web portal

To create a new WSL profile from the Landscape web portal, go to **Profiles** > **WSL profiles** > **Add WSL profile**.

Then complete the relevant fields:

- **Title**: A title for the profile. For example, "Ubuntu 24.04"
- **Description**: A description for the profile. For example, "Install 24.04 LTS WSL instance"
- **Access group**: The access group the profile will apply to. Restricts which instances the profile can manage and which users can edit and execute the profile.
- **Rootfs image**: The rootfs image to be installed. These correspond to the available WSL Ubuntu releases on the Microsoft Store. The Ubuntu image corresponds to the latest release available on the store and will give the WSL instance the ability to upgrade to the next release when it's available. If you have a custom rootfs image, you can provide the URL instead by selecting **From URL**. If you want multiple copies of the same rootfs image, you must use the **From URL** selection and provide a unique name.
  - **Image name**: The name of the rootfs image that will be installed on the WSL instance.
  - **Rootfs image URL**: The URL of the rootfs image that will be installed on the WSL instance. This URL must be reachable by the affected WSL instances. For instructions on ensuring the WSL instance can reach the provided rootfs image URL, see {ref}`how-to-wsl-use-specific-image-source`.
- **Cloud-init** (optional): The contents of the cloud-init to be supplied to the WSL instance. This can be uploaded as a file or inputted as text.
- **Association** (optional):
  - **Associate to all instances**: The profile will affect all instances in the same access group as the profile.
  - **Tag(s)**: Only instances having the specific tag(s), in the same access group as the profile will be affected.

After you've added your WSL profile, activities will be created to install the specified WSL instance on the associated Windows host machines.

You can edit or remove the profile using the dot menu under **Actions**. You can also see the number of associated parents and the number of compliant or non-compliant Windows host machines.

## Create a WSL profile using the Landscape API

To create a WSL profile via Landscape's REST API, see the following example command:

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d '{"title": "NobleProfile", "description": "Noble", "image_name": "Ubuntu-24.04", "all_computers": "true"}'
```

## Reapply a WSL profile using the Landscape API

Activities to install the corresponding WSL instance are automatically created when a Windows host machine is associated with a WSL profile. If you want to fix any non-compliant Windows host machines, you can reapply a WSL profile via Landscape's REST API. See the following example command:

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles/NobleProfile:reapply -H "Authorization: Bearer $JWT"
```

## Apply all WSL profiles by Windows host machine in the Landscape web portal

You can apply all WSL profiles that are associated to a Windows host machine from the Landscape web portal. To do this:

1. Find the Windows machine that you want to apply WSL profiles. To find this, click the link under **Associated parents** in the **WSL profiles** page, or by go to the **Instances** page.
2. Click the name of the Windows machine that you want to make compliant.
3. Click on the **WSL** tab.
4. Click **Make compliant** and complete the prompt.

This will create activities to provision WSL instances on specified Windows host machines for all associated WSL profiles.

```{note}
The **Make compliant** button is hidden for Windows machines that have no associated WSL profiles.
```

## Apply all WSL profiles by Windows host machine using the Landscape API

To reapply all WSL profiles on specified Windows host machines via Landscape's REST API, see the following example command:

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles/make-hosts-compliant -H "Authorization: Bearer $JWT" -d '{"host_computer_ids": [6, 15]}'
```
