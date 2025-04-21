(how-to-manage-repos-web-portal)=
# How to manage and mirror repositories from the web portal

> See also: [About repository mirroring](/explanation/repository-mirroring/repository-mirroring)

```{note}
Web-based repository mirroring is available in Landscape 24.04 LTS for self-hosted users.
```

The repository mirroring feature in Landscape enables you to mirror Ubuntu and third-party repositories locally, and to establish custom repositories from your local mirror. This provides an additional layer of control over the software versions available to your client machines. If you’re not familiar with repository mirroring in Landscape, we strongly encourage you to first read our [explanation of repository mirroring](/explanation/repository-mirroring/repository-mirroring).

The guide specifically demonstrates how to mirror an Ubuntu repository, but most of the information here also applies to mirroring third-party repositories.

## Disk space requirements

As of March 2024, these are the estimates for the amount of disk space needed to download the following Ubuntu distributions:

| Series | amd64 | i386  | Both |
| ------ | ----- | ----- | ----- |
| Noble | 150GB | 110GB | 180GB |
| Jammy  | 330GB | 120GB | 360GB |
| Focal  | 430GB | 105GB | 445GB |
| Bionic | 290GB | 155GB | 355GB |

Packages will be downloaded to `/var/lib/landscape/landscape-repository/standalone/`. These estimates are a breakdown of the total size of the pockets for the main, restricted, universe and multiverse components of the amd64 and i386 architectures (release, updates and security pockets). The last column provides an estimate for downloading both the amd64 and i386 architectures. It's not a total of the amd64 and i386 disk space requirements because it doesn't duplicate packages that are present in both architectures.

Note that this is only a subset, and it does not include arm and other architectures. Including these will use more disk space.

## (If needed) Generate API credentials

```{note}
You only need to generate API credentials if this is your first time using the newer web portal introduced in Landscape 24.04 LTS. If you've used this web portal before, you can skip this step.
```

If you're a first-time user of the 24.04 LTS web portal and web-based repository management, you'll need to generate API credentials from your account. To do this:

1. In the default web portal, click your account name from the header (near **Logout**), or go directly to `<landscape_url>/settings`.
1. Click **Generate API credentials**
    - Note: If you've already generated API credentials in the past, this button will instead read **Regenerate API credentials**. You don't need to regenerate API credentials, and you can proceed with the next step in this guide.

Now you can access web-based repository management and navigate to the newer web portal by clicking **Repositories** from the header. You may need to log out and back in again, but you only need to generate API credentials once.

## Create and import the GPG key

You need to create a secret GPG key in your terminal before importing it into the web portal. 

To create the GPG key:

1. Install and run `rngd` to improve the efficiency of generating the GPG key:
    
    ```bash
    sudo apt-get install rng-tools && sudo rngd -r /dev/urandom
    ```
    
2. Create the GPG key using one of the following commands. The `--gen-key` command creates a GPG key that sets a two year expiration date, and `--full-gen-key` creates a GPG key that does not expire.
    
    ```bash
    gpg --gen-key
    ```
    
    ```bash
    gpg --full-gen-key
    ```
    
3. If you’re prompted to provide information about the key, click **Enter** to choose the default options or make selections based on your system configuration. If you’re unsure what to select, the default options work for most configurations.
4. Enter **Y** when prompted with `Is this correct? (y/N)`
5. When you’re prompted with “Please confirm that you do not want to have any protection on your key,” choose **Yes, protection is not needed**. You’ll be prompted and need to confirm this twice.

Your GPG key should now be created. To import the GPG key into Landscape:

1. List the key in the command line:
    
    ```bash
    gpg -K
    ```
    
2. Copy the secret key ID from the output. It should look similar to `A1234B5678C9101112D12141516E17181920FGH0`.
3. Export the key to an `.asc` file:
    
    ```bash
    gpg -a --export-secret-keys {SECRET_KEY_ID} > mirror-key.asc
    ```
    
    Replacing `{SECRET_KEY_ID}` with your ID from the previous step. You can also change the `mirror-key.asc` file name and location if preferred, although that file will be deleted shortly.
    
4. In your Landscape web portal, navigate to the GPG Keys page (**Repositories** > **GPG Keys**).
5. Click **Import key**
6. In the **Name** field, provide a name for your key. For example, `mirror-key`.
7. In the **Material** field, copy and paste the contents of your `mirror-key.asc` file. Make sure you include the *entire contents* of the file, including the header and footer. If you paste the key incorrectly, your import will fail and you’ll get an error message.
8. Click **Import key**

If done successfully, your key will now be listed in the *GPG Keys* page. Once it’s imported, you can delete your `mirror-key.asc` file.

```{note}
If you intend to mirror a third-party repository, you'll also need to get their public GPG key and import it into Landscape.
```

## Create a new repository (distribution)

To create a new distribution:

1. From the sidebar, navigate to **Repositories** > **Mirrors**
2. Click **Add distribution**
3. Enter the name of the distribution you intend to mirror. For example, `ubuntu`.
    - Note: You can’t use the same name for multiple distributions, so you should make this name unique and descriptive of the repository. If you want to reuse a name later, you’ll have to delete the original distribution.
4. Select the appropriate access group(s) for this distribution
5. Click **Add distribution**

## Create a mirror

To create a mirror using the distribution you previously made:

1. On the same page where you created your repository (**Repositories** > **Mirrors**), click **Add mirror**
1. Select the type of mirror from the **Type** dropdown menu. For example, select **Ubuntu Archive** if you’re mirroring Jammy 22.04 or another Ubuntu repository.
1. In the **Mirror URI** field, use the default Mirror URI if you’re mirroring Jammy 22.04 or anther Ubuntu repository
1. In the **Mirror series** dropdown menu, select the series you’re mirroring. For example, **Ubuntu Jammy 22.04**.
1. In the **Series name** field, enter a name for your series. For example, “jammy”.
1. In the **Mirror GPG key** dropdown menu, you can leave this blank if mirroring an Ubuntu repository. The Ubuntu public mirror GPG key is already configured in Landscape.
1. In the **GPG key** dropdown menu, select your private key which you previously generated.
1. Review the selections under **Pockets**, **Components** and **Architectures**. Either use the defaults or change the options as needed to customize your mirror. 
1. Click **Add mirror**

## Sync pockets

```{note}
If you’re using Landscape on Jammy 22.04 or later, you may need to change the default timeout of 30 minutes in RabbitMQ before syncing your pocket. For more information, see [how to configure RabbitMQ for Jammy 22.04 or later](/how-to-guides/landscape-installation-and-set-up/configure-rabbitmq).
```

Syncing pockets involves downloading all packages from that pocket locally. For large pockets, such as those in the Ubuntu repositories, this step can take a few hours or even longer depending on the size of the pocket and your download speed. We have some estimates of the [amount of disk space required](#disk-space-requirements) for the Ubuntu repositories; however, these repositories change frequently and may be larger than the provided estimates. If you attempt to sync a pocket but don’t have enough disk space available, the sync pocket activity will fail and you’ll receive an error message before any packages are downloaded.

To sync a pocket from the web portal:

1. On the same page where you created your mirror (**Repositories** > **Mirrors**), locate the pocket you intend to sync. For example, the “release” pocket in Jammy 22.04.
2. In the same row, click the <img src="https://assets.ubuntu.com/v1/e8b73774-sync.png" alt="two arrows creating a circle" width="32"/> arrow to sync your pocket
    - If you hover your cursor over the icon, it says **Sync** for mirrored pockets and **Pull** for pull pockets

**NOTE:** Only one pocket can be synchronized, at a time. This will change in the future.

The Landscape web portal has a progress bar, and you can also make an API call to check on the progress. To do this via the command line API package, run:

```bash
landscape-api get-activities --query type:SyncPocketRequest --limit 1
```

The output of this returns a `progress` field that provides an estimate of the percent complete of your pocket sync. You can also add `watch --`  before the previous command to get an update every two seconds.

## Create a repository profile and associate computers to the profile

A repository profile in Landscape is useful for updating repository configurations. When a machine is associated with a repository profile, the repository configurations are applied one time. Repository profiles don't perform ongoing monitoring of repository configurations.

To create a profile:

1. From the sidebar, navigate to **Repositories** > **Profiles**
2. Click **Add Profile**
3. In the **Title** field, enter a name for this profile. For example, “jammy-test”.
4. (Optional) Add a description of this profile in the **Description** field
5. (Optional) Use the **Access group** dropdown menu and **Association** category to associate this profile with an access group or specific computers (tags)
6. (Optional) Use the **Pockets** and **Apt Sources** tabs to associate this profile with certain pockets or apt sources
7. Click **Add profile**

Note that you may want to create multiple repository profiles for different groups of computers.

## Create and manage pull pockets

To create a new pull pocket:

1. On the same page where you created your mirror (**Repositories** > **Mirrors**), locate the series with the pocket you intend to pull from. For example, “jammy”.
2. In that section, click **New pocket**.
3. In the **Type** dropdown menu, select the type. For example, **Ubuntu**.
4. In the **Mode** dropdown menu, select **Pull**.
5. In the **Name** field, enter a name for your pull pocket. For example, “jammy-release-pull”.
6. In the **Pull from** dropdown menu, select the pocket you intend to pull from.
7. In the **GPG Key** dropdown menu, select the same private key you previously generated.
8. (Optional) If you want to use filters in your pull pocket, select the type in the **Filter type** dropdown menu.
9. Change any selections in **Components** and **Architectures** as necessary for your configuration.
10. Click **Create**

To update your pull pocket:

1. On the same page where you created your mirror (**Repositories** > **Mirrors**), locate your pull pocket
2. In the same row, click the <img src="https://assets.ubuntu.com/v1/e8b73774-sync.png" alt="two arrows creating a circle" width="32"/> arrow to update your pocket. This activity may take awhile to complete.
    - If you hover your cursor over the icon, it says **Sync** for mirrored pockets and **Pull** for pull pockets.

