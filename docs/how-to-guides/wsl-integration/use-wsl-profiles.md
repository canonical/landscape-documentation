(how-to-use-wsl-profiles)=

# How to use WSL profiles

> See also: {ref}`reference-rest-api-child-instance-profiles` and {ref}`reference-rest-api-wsl` REST API endpoints.

```{note}
This feature is currently in beta.
```

This guide describes how to use {ref}`WSL profiles <reference-terms-wsl-profile>` to provision WSL instances and manage them with Landscape.

To use WSL profiles, your Windows host **must not** have any WSL child instances that aren't registered with Landscape. If you want to use WSL profiles but you have WSL instances that aren't managed by Landscape, you need to remove them from your Windows host, or re-register a new Windows host with only the Landscape-managed WSL instances.

## Create a WSL profile

### Web portal

To create a new WSL profile from the Landscape web portal, go to **Profiles** > **WSL profiles** > **Add WSL profile**.

Then complete the relevant fields:

- **Title**: A title for the profile. For example, "Web Developer workspace".
- **Description**: A summary of what the profile configures. For example, "Install NodeJS and NPM".
- **Access group**: The access group the profile will apply to. Restricts which instances the profile can manage and which users can edit and execute the profile.
- **rootfs image**: The rootfs image to be installed. These correspond to the available WSL Ubuntu releases on the Microsoft Store. The Ubuntu image corresponds to the latest release available on the store and will give the WSL instance the ability to upgrade to the next release when it's available. If you have a custom rootfs image, you can provide the URL instead by selecting **From URL**. If you want multiple copies of the same rootfs image, you must use the **From URL** selection and provide a unique name.
  - **Image name**: The name of the rootfs image that will be installed on the WSL instance.
  - **rootfs image URL**: The URL of the rootfs image that will be installed on the WSL instance. This URL must be reachable by the Windows host machine. Organizations can also host their own custom rootfs images and reference them here. If your environment uses a WSL `manifest.json` file to define which distributions are available for `wsl --install`, you can point Windows to your own manifest URL. This is optional and independent of Landscape, but it allows administrators to present a controlled list of distributions to end users. For example (using a beta manifest URL):

    ```powershell
    $distributionListUrl = "https://raw.githubusercontent.com/wiki/canonical/ubuntu-pro-for-wsl/beta/manifest.json"
    Set-ItemProperty -Path "HKLM:SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss" -Name DistributionListUrl -Value "$distributionListUrl" -Type String -Force
    ```

- **cloud-init** (optional): The contents of the cloud-init to be supplied to the WSL instance. This can be uploaded as a file or inputted as text. If you don't include a cloud-init file, the rootfs image will be applied without any additional configuration.
- **Compliance settings** : Whether or not the associated Windows instances should only have WSL instances that were created through Landscape.
- **Association** (optional):
  - **Associate to all instances**: The profile will affect all instances in the same access group as the profile.
  - **Tag(s)**: Only instances having the specific tag(s), in the same access group as the profile will be affected. Leaving tags blank, and not selecting **Associate to all instances** will result in zero machines being associated with the WSL Profile.

After you've added your WSL profile, activities will be created to install the specified WSL instance on the associated Windows host machines.

You can edit or remove the profile using the dot menu under **Actions**. You can also see the number of associated parents and the number of compliant or non-compliant Windows host machines.

### REST API

To create a WSL profile via Landscape's REST API, see {ref}`reference-rest-api-child-instance-profiles`.

## Reapply a WSL profile to the Windows host

Activities to install the corresponding WSL instance are automatically created when a Windows host machine is associated with a WSL profile. If you want to fix any non-compliant Windows host machines, you can reapply a WSL profile via Landscape's REST API. See {ref}`reference-rest-api-child-instance-profiles`.

## Apply all WSL profiles per Windows host

### Web portal

You can apply all WSL profiles that are associated to a Windows host machine from the Landscape web portal. To do this:

1. Find the Windows machine that you want to apply WSL profiles. To find this, click the link under **Associated parents** in the **WSL profiles** page, or find your instance from the **Instances** page.
1. Click the Windows machine that you want to make compliant > **WSL** tab > **Make compliant**
1. Complete the prompt

This will create activities to provision WSL instances on specified Windows host machines for all associated WSL profiles.

```{note}
The **Make compliant** button is hidden for Windows machines that have no associated WSL profiles.
```

### REST API

To apply all WSL profiles on specified Windows host machines via Landscape's REST API, see {ref}`reference-rest-api-child-instance-profiles`.
