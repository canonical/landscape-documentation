---
myst:
  html_meta:
    description: "Manage repository mirrors from the Landscape Server 26.04 LTS web portal. Configure Debian repositories and create repository profiles."
---

(how-to-manage-repos-web-portal-2604)=
# How to manage and mirror repositories from the web portal (26.04 and later)

> See also: {ref}`explanation-repo-mirroring-2604`

```{note}
This document applies to **Landscape Server 26.04 LTS and later**. See the {ref}`reference-release-notes-26-04-lts` for details on our changes to repository management in 26.04.
```

The repository mirroring feature in Landscape lets you mirror Ubuntu and third-party repositories, create local repositories for personal packages, and publish repositories to different targets. This adds an extra layer of control over the software versions available to your client machines. If you're not familiar with repository mirroring in Landscape, read our explanation before continuing through this how-to guide: {ref}`explanation-repo-mirroring-2604`.

This guide demonstrates how to mirror a Debian repository.

(how-to-heading-create-new-mirror)=
## Create a new mirror

To create a new mirror:

1. From the sidebar, navigate to **Repositories** > **Mirrors**
1. Click **Add mirror**
1. Enter the name of the mirror. For example, `noble-backports-mirror`.
    - Note: You can't use the same name for multiple mirrors, so you should make this name unique and descriptive of the repository. If you want to reuse a name later, you'll have to delete the original mirror.
1. Select the type of mirror from the **Source Type** dropdown menu. For example, select **Ubuntu archive** if you're mirroring an Ubuntu repository.
1. In the **Source URL** field, use the default mirror URL if you're mirroring an Ubuntu repository. Otherwise, enter the URL for the Debian repository you want to mirror. For example, `https://deb.debian.org/debian/`.
    - Note: If you're mirroring an **Ubuntu Pro** repository, enter your Ubuntu Pro token in the token field.
1. To preserve signatures from the upstream source, select the **Preserve upstream signing key** checkbox.
1. Enter the distribution you want to mirror. If you're mirroring an Ubuntu repository, select the distribution from the dropdown menu. Otherwise, enter the distribution name. For example, `bookworm`.
1. Select the components you want to mirror. If you're mirroring an Ubuntu repository, select the components from the dropdown menu. Otherwise, enter a comma-separated list of components. For example, `non-free-firmware, main`.
1. Select the architectures you want to mirror. If you're mirroring an Ubuntu repository, select the architectures from the dropdown menu. Otherwise, enter a comma-separated list of architectures. For example, `amd64, arm64`.
1. To filter which packages are retrieved instead of mirroring the entire selected component, use the **Filter** text box. The filtering language is documented in the web portal when you click on the help icon.
1. If you're not preserving the upstream signing key, provide the ASCII-armored GPG key for the mirror in the **Verification GPG key** text box.

(how-to-heading-create-new-local)=
## Create a new local repository

To create a new local repository:

1. From the sidebar, navigate to **Repositories** > **Local repositories**
1. Click **Add local repository**
1. Enter the name of the local repository. For example, `my-local-repo`.
    - Note: You can't use the same name for multiple local repositories, so you should make this name unique and descriptive. If you want to reuse a name later, you'll have to delete the original local repository.
1. Enter a description of your local repository.
1. Enter the distribution name to display for your local Debian repository.
1. Enter the component name to display for your local Debian repository.

(how-to-heading-create-new-publication-target)=
## Create a new publication target

To create a new publication target:

1. From the sidebar, navigate to **Repositories** > **Publication targets**
1. Click **Add publication target**
1. Enter the name of the publication target. For example, `s3-target-1`.
1. In the **Type** dropdown menu, select the type of publication target you want to create.
1. Enter the required information for your publication target.

(how-to-heading-create-new-publication)=
## Create a new publication

To create a new publication:

1. From the sidebar, navigate to **Repositories** > **Publications**
1. Click **Add publication**
1. Enter the name of the publication. For example, `noble-backports-publication`.
1. In the **Source type** dropdown menu, select whether you want to publish a local repository or mirror.
    - In the **Source** dropdown menu, select the mirror or local repository you want to publish.
1. In the **Publication target** dropdown menu, select the publication target you want to publish to.
1. To resign packages in your publication target, enter the ASCII-armored GPG key you want to use in the **Signing GPG key** text box.

(how-to-create-repo-profile)=
## Create a repository profile and associate client machines to the profile

A {ref}`repository profile <reference-terms-repository-profile>` in Landscape is useful for updating repository configurations. When a machine (instance) is associated with a repository profile, the repository configurations are applied one time. Repository profiles don't perform ongoing monitoring of repository configurations.

To create a profile:

1. From the sidebar, go to **Profiles** > **Repository profiles**
1. Click **Add repository profile**
1. In the **Title** field, enter a name for this profile. For example, `noble-test`.
1. Select **Add source** to specify a Debian repository for this repository profile.
    1. In the **Source name** field, enter a name for the source.
    1. Add the `deb` line for the Debian repository. For example, `deb [trusted=yes] https://debarchive-test-bucket.s3.us-west-1.amazonaws.com/ devel main`.
    1. If the repository's GPG verification key isn't already in the client machine's keyring, provide the verification key in the **GPG key** field.
1. Use the **Access group** dropdown menu and **Association** category to associate this profile with an access group or specific instances/computers (tags).
1. Optionally fill out the **Description** field.

Note that you may want to create multiple repository profiles for different groups of managed instances.

(how-to-manage-created-repositories-publishing)=
## Managing existing repositories

To publish a mirror:

1. If the mirror doesn't preserve upstream signatures, sync the mirror:
    1. From the sidebar, navigate to **Repositories** > **Mirrors**.
    1. Select the mirror you want to publish.
    1. Select the **Update** option on the mirror.
1. Select the publication with the mirror and publication target you want to publish, then select **Republish**.

To publish a local repository:

1. Make sure the local repository contains the packages you want to publish:
    1. From the sidebar, navigate to **Repositories** > **Local repositories**.
    1. Select the local repository you want to publish.
    1. Select **Import packages** and provide the URI for the packages you want to import into the local repository.
1. Select the publication with the local repository and publication target you want to publish, then select **Republish**.
