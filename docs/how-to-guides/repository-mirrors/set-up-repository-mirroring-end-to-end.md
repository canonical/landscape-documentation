---
myst:
  html_meta:
    description: "Set up repository mirroring with Landscape end-to-end, from a fresh deployment to installing a package on a client machine from your own mirror published to S3 or a local filesystem."
---

(how-to-set-up-repository-mirroring-end-to-end)=
# How to set up repository mirroring end-to-end (26.04 and later)

> See also: {ref}`explanation-repo-mirroring`

```{note}
This document applies to **Landscape Server 26.04 LTS and later**. See the {ref}`reference-release-notes-26-04-lts` for details on our changes to repository management in 26.04.
```

This guide demonstrates how to mirror part of the Ubuntu archive, publish it to a publication target, and configure a client machine to install packages from the published repository. By the end of this guide, you'll have a repository mirror set up and a package on your client machine.

It covers two types of publication target: Amazon S3 and a local filesystem. Where the steps differ, select the tab for your publication target type. Landscape also supports OpenStack Swift publication targets, which this guide doesn't cover. For a broader set of repository management tasks, see {ref}`how-to-manage-repos-web-portal`.

The workflow uses these repository management components:

- A **mirror**: your copy of an upstream repository.
- A **publication target**: where the published repository is written, and where your clients download packages from.
- A **publication**: the configuration that connects a mirror to a target.
- A **repository profile**: the configuration that tells your clients to use the published repository.

## Background: repository storage and publication targets

```{include} /reuse/repository-storage-locations.md
```

This guide covers the following publication target types:

- **S3**: An Amazon S3 bucket or S3-compatible object store (such as MinIO). In this guide, clients download packages directly from the bucket.
- **Filesystem**: A directory on the local filesystem of the machine where Debarchive runs. Clients download packages from a web server, such as Apache or Nginx, that serves this directory. This guide uses the {ref}`example web server configurations <how-to-debarchive-filesystem-publications>` from the Debarchive setup guide.

For more information about choosing a publication target type, see {ref}`explanation-repo-mirroring-2604-publication-targets`.

## Background: repository signing

Client machines verify the repositories they install from using a signing key (a GPG key). When you publish a repository with Landscape, you can either preserve the upstream signing key or re-sign the repository with your own key.

This guide uses a re-signed publication, so you provide your own signing key. Landscape uses the private key to sign your published repository, and your client uses the matching public key to verify packages.

For more information about verification and signing keys, see {ref}`explanation-repo-mirroring-2604-gpg-keys`. For guidance on managing signing keys securely, see {ref}`how-to-harden-deployment-secure-gpg-keys`.

## Prerequisites

Before you start, make sure you have:

- A **Landscape Server 26.04 LTS (or later)** deployment with repository management set up. See {ref}`how-to-guides-landscape-installation-and-set-up-index` for installation. If you're on a version earlier than 26.04, upgrade first by following {ref}`how-to-upgrade-to-26-04-lts`.

    ```{include} /reuse/debarchive-setup-links.md
    ```

- At least one **registered client machine** running Ubuntu.

You also need the following, depending on your publication target type:

`````{tab-set}
:sync-group: publication-target

````{tab-item} S3
:sync: s3

- An **S3-compatible object store** that you can write to, along with its region and a pair of access keys. This guide uses Amazon S3 as the example.
- The object store must allow your **client machine to read objects**. In this guide, the client fetches packages directly from the storage URL without credentials, so public object read must be enabled.
````

````{tab-item} Filesystem
:sync: filesystem

- A **Quickstart or Manual installation** of Landscape Server. The filesystem steps in this guide use the published root and web server configuration from {ref}`how-to-debarchive-repository-management`, which covers Quickstart and Manual installations only.
- **Apache or Nginx** on the Debarchive machine, to serve the published repository directory. Quickstart installations already use Apache. {ref}`Step 4 <how-to-set-up-repository-mirroring-end-to-end-publish>` shows how to configure the web server. Your client machine must be able to reach it.
````

`````

## Disk space requirements

This guide uses the `main` component and `amd64` architecture in `noble-backports` to keep the example mirror small. Larger distributions with more components and architectures require more storage.

```{include} /reuse/filesystem-publication-target-disk-space.md
```

For disk space estimates, see {ref}`how-to-heading-disk-space-requirements-2604`.

## Step 1: Create a publication target

A publication target is the storage location where your published repository is written. Create it first so it's available when you publish.

`````{tab-set}
:sync-group: publication-target

````{tab-item} S3
:sync: s3

1. From the sidebar, navigate to **Repositories** > **Publication targets**.
1. Click **Add publication target**.
1. Enter the name of the publication target. For example, `s3-target`.
1. In the **Type** dropdown menu, select **S3**.
1. Complete the S3 details for your bucket:
    - **Region**: the bucket's region. For example, `us-east-1`.
    - **Bucket name**: the bucket's name.
    - **AWS access key ID**: your access key ID.
    - **AWS secret access key**: your secret access key.
    - **Endpoint** (optional): leave this empty for Amazon S3. For other S3-compatible object stores, enter the object store's hostname. If you set an endpoint, the region is ignored.
    - **Prefix** (optional): a path in the bucket to publish under. This guide leaves it empty, so the repository is published at the root of the bucket.
1. Click **Add publication target**.
````

````{tab-item} Filesystem
:sync: filesystem

1. From the sidebar, navigate to **Repositories** > **Publication targets**.
1. Click **Add publication target**.
1. Enter the name of the publication target. For example, `filesystem-target`.
1. In the **Type** dropdown menu, select **Filesystem**.
1. In the **Path** field, enter the directory to publish to. For example, `/noble-backports`.
1. Leave **Link method** set to the default, **Hardlink**.
1. Click **Add publication target**.

```{include} /reuse/filesystem-publication-target-path.md
```

Landscape doesn't serve filesystem publication targets. {ref}`Step 4 <how-to-set-up-repository-mirroring-end-to-end-publish>` shows how to serve this repository with Apache or Nginx. To change the published root, see {ref}`how-to-debarchive-filesystem-publications`.
````

`````

A publication target is defined independently of any repository, so you can reuse it for other publications.

## Step 2: Create and sync a mirror

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

## Step 3: Create a GPG key pair

Create a GPG key pair to sign the published repository:

```bash
gpg --full-generate-key
```

When prompted, do not set a passphrase on the key. Landscape needs direct access to the private key material for signing during publication.

Use this key pair in the next steps: paste the private key in the publication and the public key in the repository profile.

(how-to-set-up-repository-mirroring-end-to-end-publish)=
## Step 4: Publish the mirror

A publication connects your mirror to your publication target and writes the repository there.

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

Landscape copies the packages and writes a complete APT repository to your publication target, signed with your key.

``````{tab-set}
:sync-group: publication-target

`````{tab-item} S3
:sync: s3

When the publish finishes, the repository is available for clients from your bucket.
`````

`````{tab-item} Filesystem
:sync: filesystem

When the publish finishes, the repository is written to the publication directory on the Debarchive machine. For example, `/var/snap/landscape-debarchive/common/publications/noble-backports`.

Landscape doesn't serve this directory. Serve it to your clients with Apache or Nginx, using the full publication directory as the document root. The example configurations below listen on port 8000. For more detail, including how to change the published root, see {ref}`how-to-debarchive-filesystem-publications`.

````{dropdown} Example Apache and Nginx web server configurations
```{include} /reuse/filesystem-web-server-config.md
```
````
`````

``````

## Step 5: Create a repository profile and associate client machines

A {ref}`repository profile <reference-terms-repository-profile>` applies an APT source to the client machines you associate with it. The configuration is applied one time when a machine is associated with the profile.

The `deb` line in the profile points your client at the published repository. Its URL depends on your publication target type:

`````{tab-set}
:sync-group: publication-target

````{tab-item} S3
:sync: s3

Use your bucket's URL, substituting your own bucket and region. For example:

```text
deb https://my-bucket.s3.us-east-1.amazonaws.com/ noble-backports main
```

If you set a **Prefix** on the publication target, add the prefix to the end of the URL. If you use an S3-compatible object store other than Amazon S3, use the URL that your object store provides for public reads from the bucket.
````

````{tab-item} Filesystem
:sync: filesystem

Use the URL of your web server, replacing `<WEB_SERVER_FQDN>` with the fully qualified domain name of the web server that serves the publication directory. For example:

```text
deb http://<WEB_SERVER_FQDN>:8000/ noble-backports main
```

This example assumes that the web server's document root is the full publication directory, and that it listens on port 8000, as in the example configurations in {ref}`Step 4 <how-to-set-up-repository-mirroring-end-to-end-publish>`.
````

`````

To create the repository profile:

1. From the sidebar, navigate to **Repositories** > **Repository profiles**.
1. Click **Add repository profile**.
1. In the **Profile name** field, enter a name for this profile. For example, `noble-backports-profile`.
1. Click **Add source** to specify the Debian repository for this profile.
    1. In the **Source name** field, enter a name for the source.
    1. Add the `deb` line for your published repository.
    1. In the **GPG key** field, paste your public GPG signing key. Your client uses this key to verify packages, since Landscape re-signed the repository with your key.
1. Use the **Access group** dropdown menu and **Association** section to associate this profile with an access group or tags.
1. Optionally fill out the **Description** field.
1. Save the profile.

Landscape creates activities to apply the new APT source to the associated client machines.

## Step 6: Install a package from your mirror to the client machine

On a client machine associated with the repository profile, refresh the package lists:

```bash
sudo apt update
```

If `apt update` completes without any signature warnings, the client has verified your published repository against your signing key.

To confirm your mirror is a source for a package it contains, check its policy, replacing `<PACKAGE>` with a package that exists in your mirror:

```bash
apt-cache policy <PACKAGE>
```

The URL of your published repository is listed among the sources for the package. Install it to confirm:

```bash
sudo apt install <PACKAGE>
```

## See also

- {ref}`explanation-repo-mirroring`
- {ref}`how-to-manage-repos-web-portal`
- {ref}`how-to-debarchive-repository-management`
- {ref}`reference-api-debarchive`
