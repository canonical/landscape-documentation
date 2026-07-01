---
myst:
  html_meta:
    description: "Set up repository mirroring with Landscape end-to-end, from a fresh deployment to installing a package on a client machine from your own mirror published to S3."
---

(how-to-set-up-repository-mirroring-end-to-end)=
# How to set up repository mirroring end-to-end (26.04 and later)

> See also: {ref}`explanation-repo-mirroring-2604`

```{note}
This document applies to **Landscape Server 26.04 LTS and later**. See the {ref}`reference-release-notes-26-04-lts` for details on our changes to repository management in 26.04.
```

This guide walks through repository mirroring in Landscape from end to end: mirroring part of the Ubuntu archive, publishing it to object storage, and configuring a client machine to install packages from your published copy. It puts the individual repository management tasks in order and in the context of a complete workflow.

It uses an opinionated setup with Amazon S3 as the publication target, but the steps generally apply to other configurations. For a broader set of repository management tasks, see {ref}`how-to-manage-repos-web-portal-2604`.

The workflow uses these repository management:

- A **mirror**: your copy of an upstream repository.
- A **publication target**: where the copy is stored.
- A **publication**: the configuration that connects a mirror to a target.
- A **repository profile**: the configuration that tells your clients to use the published repository.

## Background: repository signing

Client machines verify the repositories they install from using a signing key (a GPG key). When you publish a repository with Landscape, you can either preserve the upstream signing key or re-sign the repository with your own key.

This guide uses a re-signed publication, so you provide your own signing key. Landscape uses the private key to sign your published repository, and your client uses the matching public key to verify packages.

## Prerequisites

Before you start, make sure you have:

- A **Landscape Server 26.04 LTS (or later)** deployment with repository management set up. See {ref}`how-to-guides-landscape-installation-and-set-up-index` for installation, and {ref}`how-to-debarchive-repository-management` to set up repository management. If you're on a version earlier than 26.04, upgrade first by following {ref}`how-to-upgrade-to-26-04-lts`.
- At least one **registered client machine** running Ubuntu.
- An **S3-compatible object store** that you can write to, along with its region and a pair of access keys. This guide uses Amazon S3 as the example.
- The object store must allow your **client machine to read objects**. In this guide, the client fetches packages directly from the storage URL without credentials, so public object read must be enabled.

## Disk space requirements

```{include} /reuse/repository-disk-space.md
```

## Create a publication target

A publication target is the storage location where your mirrored repository is stored. Create it first so it's available when you publish.

1. From the sidebar, navigate to **Repositories** > **Publication targets**.
1. Click **Add publication target**.
1. Enter the name of the publication target. For example, `s3-target`.
1. In the **Type** dropdown menu, select **S3**.
1. Complete the S3 details for your bucket:
    - **Region**: the bucket's region. For example, `us-east-1`.
    - **Bucket**: the bucket's name.
    - **AWS access key ID**: your access key ID.
    - **AWS secret access key**: your secret access key.
1. Click **Add publication target**.

A publication target is defined independently of any repository, so you can reuse it for other publications.

## Create and sync a mirror

A mirror is Landscape's copy of an upstream Ubuntu repository. After you create it, sync it to download the packages from upstream.

1. From the sidebar, navigate to **Repositories** > **Mirrors**.
1. Click **Add mirror**.
1. Enter the name of the mirror. For example, `noble-backports-mirror`.
1. In the **Source type** dropdown menu, select **Ubuntu archive**.
1. Use the default **Source URL**, which points at the Ubuntu archive.
1. Leave the **Preserve upstream signing key** checkbox cleared. Landscape re-signs the mirror with your own key when you publish it.
1. Under **Mirror contents**, select what to mirror. For example:
    - **Distribution**: `noble-backports`
    - **Components**: `main`
    - **Architectures**: `amd64`
1. Click **Add mirror**.

To sync the mirror:

1. From the **Mirrors** list, select the mirror you created.
1. Click **Update** from the actions dropdown menu.

The sync downloads the upstream packages into Landscape so they're ready to publish. The time this takes depends on the size of the repository, from a few minutes for a small mirror to several hours for a large one. A single-component, single-architecture mirror such as `noble-backports main` for `amd64` is relatively small.

## Publish the mirror

A publication connects your mirror to your publication target and writes the repository into your object store.

First, generate a GPG key pair that Landscape uses to sign the published repository.

To create the publication:

1. From the sidebar, navigate to **Repositories** > **Publications**.
1. Click **Add publication**.
1. Enter the name of the publication. For example, `noble-backports-publication`.
1. In the **Source type** dropdown menu, select **Mirror**.
1. In the **Source** dropdown menu, select the mirror you created.
1. In the **Publication target** dropdown menu, select the publication target you created.
1. In the **Architectures** dropdown menu, select `amd64`.
1. In the **Signing GPG key** field, paste your private GPG signing key.
1. Click **Add publication**.

To publish the mirror:

1. From the Mirrors list, select the mirror you created.
1. Click **Publish** from the actions dropdown menu.
1. Select **Existing publication**.
1. In the **Publication** dropdown menu, select the publication you created.
1. Click **Publish Mirror**.

Landscape copies the packages and writes a complete APT repository into your object store, signed with your key. When the publish finishes, the repository is available for clients.

## Create a repository profile and associate client machines

A {ref}`repository profile <reference-terms-repository-profile>` applies an APT source to the client machines you associate with it. The configuration is applied one time when a machine is associated with the profile.

1. From the sidebar, navigate to **Repositories** > **Repository profiles**.
1. Click **Add repository profile**.
1. In the **Profile name** field, enter a name for this profile. For example, `noble-backports-profile`.
1. Click **Add source** to specify the Debian repository for this profile.
    1. In the **Source name** field, enter a name for the source.
    1. Add the `deb` line for your published repository, substituting your own bucket and region. For example:

        ```text
        deb https://my-bucket.s3.us-east-1.amazonaws.com/ noble-backports main
        ```

    1. In the **GPG key** field, paste your public GPG signing key. Your client uses this key to verify packages, since Landscape re-signed the repository with your key.
1. Use the **Access group** dropdown menu and **Association** section to associate this profile with an access group or tags.
1. Optionally fill out the **Description** field.
1. Save the profile.

Landscape creates activities to apply the new APT source to the associated client machines.

## Install a package from your mirror

On a client machine associated with the repository profile, refresh the package lists:

```bash
sudo apt update
```

If `apt update` completes without any signature warnings, the client has verified your published repository against your signing key.

To confirm your mirror is a source for a package it contains, check its policy, replacing `<package>` with a package that exists in your mirror:

```bash
apt-cache policy <package>
```

Your object store's address is listed among the sources for the package. Install it to confirm:

```bash
sudo apt install <package>
```

## See also

- {ref}`explanation-repo-mirroring-2604`
- {ref}`how-to-manage-repos-web-portal-2604`
- {ref}`how-to-debarchive-repository-management`
