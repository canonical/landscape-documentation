---
myst:
  html_meta:
    description: "Manage repository mirrors from Landscape 24.04 LTS web portal. Configure Ubuntu repositories, generate GPG keys, and create profiles."
---

(how-to-manage-repos-web-portal)=
# How to manage and mirror repositories from the web portal

> See also: {ref}`explanation-repo-mirroring`

```{note}
This document applies to **Landscape 25.10 and earlier**. See the {ref}`reference-release-notes-26-04-lts` for details on our changes to repository management in 26.04.

Web-based repository mirroring is available starting in Landscape 24.04 LTS for self-hosted users.
```

The repository mirroring feature in Landscape lets you mirror Ubuntu and third-party repositories locally, and to establish custom repositories from your local mirror. This adds an extra layer of control over the software versions available to your client machines. If you're not familiar with repository mirroring in Landscape, read our explanation before continuing through this how-to guide {ref}`explanation-repo-mirroring`.

This guide demonstrates how to mirror an Ubuntu repository, but most of the information here also applies to mirroring third-party repositories.

(how-to-heading-disk-space-requirements)=
## Disk space requirements

```{include} /reuse/repository-disk-space.md
```

(how-to-heading-create-import-gpg-key)=
## Create and import the GPG key

You need to create a secret GPG key in your terminal before importing it into the web portal.

To create a new GPG key:

1. Install and run `rngd` to improve the efficiency of generating the GPG key:

    ```bash
    sudo apt-get install rng-tools && sudo rngd -r /dev/urandom
    ```

1. Create the GPG key using one of the following commands. The `--gen-key` command creates a GPG key that sets a two-year expiration date, and `--full-gen-key` creates a GPG key that does not expire.

    ```bash
    gpg --gen-key
    ```

    ```bash
    gpg --full-gen-key
    ```

1. If you're prompted to provide information about the key, press **Enter** to choose the default options or make selections based on your system configuration. If you're unsure what to select, the default options work for most configurations.
1. Enter **Y** when prompted with `Is this correct? (y/N)`.
1. When you're prompted with "Please confirm that you do not want to have any protection on your key," choose **Yes, protection is not needed**. You'll be prompted and need to confirm this twice.

Your GPG key should now be created. To import the GPG key into Landscape:

1. List the key in the command line:

    ```bash
    gpg -K
    ```

1. Copy the secret key ID from the output. It should look similar to `A1234B5678C9101112D12141516E17181920FGH0`.
1. Export the key to an `.asc` file:

    ```bash
    gpg -a --export-secret-keys <SECRET_KEY_ID> > mirror-key.asc
    ```

    Replace `<SECRET_KEY_ID>` with your ID from the previous step. You can also change the `mirror-key.asc` file name and location if preferred, although that file will be deleted shortly.

1. In your Landscape web portal, navigate to the GPG Keys page (**Repositories** > **GPG Keys**).
1. Click **Import key**
1. In the **Name** field, provide a name for your key. For example, `mirror-key`.
1. In the **Material** field, copy and paste the contents of your `mirror-key.asc` file. Make sure you include the *entire contents* of the file, including the header and footer. If you paste the key incorrectly, your import will fail and you'll get an error message.
1. Click **Import key**

If done successfully, your key will now be listed in the *GPG Keys* page. Once it's imported, you can delete your local `mirror-key.asc` file.

```{note}
If you intend to mirror a third-party repository, you'll also need to get their public GPG key and import it into Landscape.
```

(how-to-heading-create-new-repo)=
## Create a new repository (distribution)

To create a new distribution:

1. From the sidebar, navigate to **Repositories** > **Mirrors**
1. Click **Add distribution**
1. Enter the name of the distribution you intend to mirror. For example, `ubuntu`.
    - Note: You can't use the same name for multiple distributions, so you should make this name unique and descriptive of the repository. If you want to reuse a name later, you'll have to delete the original distribution.
1. Select the appropriate access group(s) for this distribution > **Add distribution**

(how-to-heading-manage-repos-create-mirror)=
## Create a mirror

To create a mirror using the distribution you previously made:

1. On the same page where you created your repository (**Repositories** > **Mirrors**), click **Add mirror**
1. Select the type of mirror from the **Type** dropdown menu. For example, select **Ubuntu Archive** if you’re mirroring Noble 24.04 or another Ubuntu repository.
1. In the **Mirror URI** field, use the default Mirror URI if you’re mirroring Noble 24.04 or another Ubuntu repository
1. In the **Mirror series** dropdown menu, select the series you’re mirroring. For example, **Ubuntu Noble 24.04**.
1. In the **Series name** field, enter a name for your series. For example, "noble".
1. In the **Mirror GPG key** dropdown menu, you can leave this blank if mirroring an Ubuntu repository. The Ubuntu public mirror GPG key is already configured in Landscape.
1. In the **GPG key** dropdown menu, select your private key which you previously generated.
1. Review the selections under **Pockets**, **Components** and **Architectures**. Either use the defaults or change the options as needed to customize your mirror.
1. Click **Add mirror**

(how-to-heading-manage-repos-sync-pockets)=
## Sync pockets

```{note}
If you're using Landscape on Jammy 22.04 or later, you may need to change the default timeout of 30 minutes in RabbitMQ before syncing your pocket. For more information, see {ref}`how-to-configure-rabbitmq`.
```

Syncing pockets involves downloading all packages from that pocket locally. For large pockets, such as those in the Ubuntu repositories, this step can take a few hours or even longer depending on the size of the pocket and your download speed. We have some estimates of the {ref}`amount of disk space required <how-to-heading-disk-space-requirements>` for the Ubuntu repositories; however, these repositories change frequently and may be larger than the provided estimates. If you attempt to sync a pocket but don't have enough disk space available, the sync pocket activity will fail and you'll receive an error message before any packages are downloaded.

To sync a pocket from the web portal:

1. On the same page where you created your mirror (**Repositories** > **Mirrors**), locate the pocket you intend to sync. For example, the "release" pocket in Noble 24.04.
1. In the same row, click the arrow icon to sync your pocket
    - If you hover your cursor over the icon, it says **Sync** for mirrored pockets and **Pull** for pull pockets

**NOTE:** Only one pocket can be synchronized at a time.

The Landscape web portal has a progress bar, but you can also make a (legacy) API call to check on the progress. To do this via the command line API package, run:

```bash
landscape-api get-activities --query type:SyncPocketRequest --limit 1
```

The output of this returns a `progress` field that provides an estimate of the percent complete of your pocket sync. You can also add `watch --`  before the previous command to get an update every two seconds.

(how-to-heading-manage-repos-create-repo-profile)=
## Create a repository profile and associate client machines to the profile

A {ref}`repository profile <reference-terms-repository-profile>` in Landscape is useful for updating repository configurations. When a machine (instance) is associated with a repository profile, the repository configurations are applied one time. Repository profiles don't perform ongoing monitoring of repository configurations.

To create a profile:

1. From the sidebar, go to **Profiles** > **Repository profiles** > **Add repository profile**
1. In the **Title** field, enter a name for this profile. For example, "noble-test".
1. Complete the rest of the form to match your desired repository profile configurations. The remaining fields are **optional**:
   - Add a description of this profile in the **Description** field
   - Use the **Access group** dropdown menu and **Association** category to associate this profile with an access group or specific instances/computers (tags)
   - Use the **Pockets** and **APT sources** tabs to associate this profile with certain pockets or apt sources
1. Click **Add profile**

Note that you may want to create multiple repository profiles for different groups of managed instances.

## Create and manage pull pockets

A pull pocket is a user-defined pocket that acts as a staging area for selected packages and updates from another pocket, so you can control what gets distributed to different groups of machines.

To create a new pull pocket:

1. On the same page where you created your mirror (**Repositories** > **Mirrors**), locate the series with the pocket you intend to pull from. For example, "noble".
1. In that section, click **New pocket**.
1. In the **Type** dropdown menu, select the type. For example, **Ubuntu**.
1. In the **Mode** dropdown menu, select **Pull**.
1. In the **Name** field, enter a name for your pull pocket. For example, "noble-release-pull".
1. In the **Pull from** dropdown menu, select the pocket you intend to pull from.
1. In the **GPG Key** dropdown menu, select the same private key you previously generated.
1. (Optional) If you want to use filters in your pull pocket, select the type in the **Filter type** dropdown menu.
1. Change any selections in **Components** and **Architectures** as necessary for your configuration.
1. Click **Create**

To update your pull pocket:

1. On the same page where you created your mirror (**Repositories** > **Mirrors**), locate your pull pocket
1. In the same row, click the arrow icon to update your pocket. This activity may take a while to complete.
    - If you hover your cursor over the icon, it says **Sync** for mirrored pockets and **Pull** for pull pockets.

### Derive series

If you're making multiple pull pockets, you can also use the **Derive series** feature, which creates a "snapshot" of the source series. The new series will contain the same packages and versions as the source at the time it was created, but it won't automatically track future changes. This process allows you to promote packages through separate environments without the packages changing unexpectedly.

For example, you could define the following pull pockets by deriving the series:

- `dev`
- `test` (derived from `dev`)
- `prod` (derived from `test`)

In this example, updates flow from `dev` > `test` > `prod`, with each stage using a fixed set of package versions.

When deriving series to make cascading pull pockets, we recommend you include the date in the series name. For example, `noble-2026-03-29`.

## Use repository snapshots

[Snapshots](https://snapshot.ubuntu.com/) are another source you can use to mirror packages. They allow Landscape to mirror packages from the Ubuntu archive at a specific point in time.

To use a snapshot, follow the same process as you would to {ref}`how-to-heading-manage-repos-create-mirror`, but change the type to **Ubuntu Snapshot**, and choose a snapshot date.

