---
myst:
  html_meta:
    description: "A hands-on tutorial that walks you through mirroring an Ubuntu repository with Landscape, publishing it to S3, and installing a package on a client."
---

(tutorial-mirror-and-publish-a-repository)=
# Mirror and publish a repository

> See also: {ref}`explanation-repo-mirroring-2604`

In this tutorial, you'll use Landscape to mirror part of the Ubuntu archive, publish it to an Amazon S3 bucket, and configure a client machine to install packages from your published copy. Along the way, you'll see how the pieces of repository management in Landscape fit together: a *mirror* (your copy of an upstream repository), a *publication target* (where the copy is stored), a *publication* (which connects the two), and a *repository profile* (which tells your clients to use it).

Landscape will **re-sign** the mirrored repository with your own GPG key. You'll generate a signing key pair during the tutorial: Landscape uses the private key to sign your published repository, and your client uses the matching public key to verify packages.

This tutorial creates a *learning* setup so you can see the full workflow end to end. When you're ready to manage repositories, see {ref}`how-to-manage-repos-web-portal-2604`.

Completing this tutorial should take approximately 30 minutes, plus time for the mirror to sync and publish.

## What you'll do

- Create an S3 publication target.
- Create a mirror of an Ubuntu repository and sync it.
- Generate a signing key and publish the mirror to your target.
- Point a client machine at the published repository with a repository profile.
- Install a package on the client from your own mirror.

## Prerequisites

Before you start, make sure you have:

- A **Landscape Server 26.04 LTS (or later)** deployment with repository management available. If you don't have one yet, follow: {ref}`Getting started with Landscape <getting-started-with-landscape>` and {ref}`Set up Debarchive with Landscape <how-to-debarchive-repository-management>`.
- At least one **registered client machine** running Ubuntu.
- An **Amazon S3 bucket** that you can write to, along with its region and a pair of AWS access keys. Any S3-compatible object store (such as AIStor) also works.
- The bucket must allow your **client machine to read objects**. In this tutorial, the client fetches packages directly from the S3 URL without credentials, so enable public object read on the bucket.
- The `gpg` command on your workstation to generate a signing key. It's installed by default on Ubuntu.

When you sign in to the web portal, confirm that **Repositories** appears in the sidebar. This is where you'll spend the whole tutorial.

## Step 1: Create a publication target

First, you'll tell Landscape *where* your mirrored repository should be stored. This storage location is called a **publication target**. You're creating it first so it's ready when you publish later.

1. From the sidebar, navigate to **Repositories** > **Publication targets**.
1. Click **Add publication target**.
1. In the **Name** field, enter `tutorial-target`.
1. In the **Type** dropdown menu, select **S3**.
1. Fill in the S3 details for your bucket:
    - **Region**: your bucket's region, for example `us-east-1`.
    - **Bucket**: your bucket's name, for example `my-tutorial-bucket`.
    - **AWS access key ID**: your access key ID.
    - **AWS secret access key**: your secret access key.
1. Click **Add publication target**.

You now have a target named `tutorial-target`. Notice that it's defined independently of any repository, so you could reuse it for other publications later.

## Step 2: Create and sync a mirror

Next, you'll create a **mirror**: Landscape's own copy of an upstream Ubuntu repository. Then you'll sync it to download the packages from upstream.

1. From the sidebar, navigate to **Repositories** > **Mirrors**.
1. Click **Add mirror**.
1. In the **Name** field, enter `tutorial-mirror`.
1. In the **Source type** dropdown menu, select **Ubuntu archive**.
1. Leave the **Source URL** at its default value. This points at the Ubuntu archive.
1. Leave the **Preserve upstream signing key** checkbox cleared. Landscape will re-sign this mirror with your own key when you publish it.
1. Under **Mirror contents**, choose what to mirror:
    - **Distribution**: `noble-backports`
    - **Components**: `main`
    - **Architectures**: `amd64`
1. Click **Add mirror** to create the mirror.

The mirror now exists, but it hasn't pulled any packages yet. Sync it to download packages from upstream:

1. From the **Mirrors** list, select `tutorial-mirror`.
1. Click **Update** to start the sync.

Wait for the sync to finish before continuing. Syncing downloads the upstream packages into Landscape so they're ready to publish.

## Step 3: Publish the mirror

A **publication** connects your mirror to your publication target and makes the repository available. Publishing it is what actually writes the repository into your S3 bucket.

First, generate a GPG key pair that Landscape will use to sign the published repository. On your workstation, run:

```bash
gpg --quick-generate-key "Tutorial Signing Key" default default never
gpg --armor --export-secret-keys "Tutorial Signing Key" > signing-private.asc
gpg --armor --export "Tutorial Signing Key" > signing-public.asc
```

The first command creates the key pair. The next two export the private key (which Landscape signs with) and the public key (which your client verifies with) as ASCII-armored text files.

Now create the publication:

1. From the sidebar, navigate to **Repositories** > **Publications**.
1. Click **Add publication**.
1. In the **Publication name** field, enter `tutorial-publication`.
1. In the **Source type** dropdown menu, select **Mirror**.
1. In the **Source** dropdown menu, select `tutorial-mirror`.
1. In the **Publication target** dropdown menu, select `tutorial-target`.
1. In the **Architectures** dropdown menu, select `amd64`.
1. In the **Signing GPG key** field, paste the contents of `signing-private.asc`. Landscape uses this key to sign your published repository.
1. Click **Add publication** to create and publish.
1. From the **Publications** list, find `tutorial-publication`, click its actions menu, and select **Republish** to start the publishing process.

Landscape now copies the packages and writes a complete APT repository into your S3 bucket, signed with your key. Mirroring `noble-backports main` for `amd64` takes some time and disk space. When it finishes, your repository is live in the bucket and ready for clients.

## Step 4: Point your client at the repository

Your repository exists, but your client doesn't know about it yet. You'll fix that with a **repository profile**, which applies an APT source to the client machines you associate with it.

1. From the sidebar, navigate to **Repositories** > **Repository profiles**.
1. Click **Add repository profile**.
1. In the **Profile name** field, enter `tutorial-clients`.
1. Click **Add source**, then fill in the source:
    1. In the **Source name** field, enter `tutorial-source`.
    1. In the `deb` line field, enter the address of your published repository, substituting your own bucket and region:

        ```text
        deb https://my-tutorial-bucket.s3.us-east-1.amazonaws.com/ noble-backports main
        ```

    1. In the **GPG key** field, paste the contents of `signing-public.asc`. Your client uses this key to verify packages, since Landscape re-signed the repository with your key rather than Ubuntu's.
1. Use the **Association** options to associate this profile with your registered client.
1. Save the profile.

Landscape applies the new APT source to your client. The configuration is applied once when the client is associated with the profile.

## Step 5: Install a package from your mirror

Now you'll confirm that your client can install a package from your mirror.

On your client machine, refresh the package lists:

```bash
sudo apt update
```

If `apt update` completes without any signature warnings, your client successfully verified your published repository against your signing key.

Next, check that your mirror is a source for a package it contains. Replace `<package>` with a package that exists in `noble-backports`:

```bash
apt-cache policy <package>
```

You should see your S3 bucket's address listed among the sources for the package. Install it to confirm:

```bash
sudo apt install <package>
```

## Summary

Congratulations! You've mirrored part of the Ubuntu archive, re-signed it with your own key, published it to an S3 bucket, and installed a package on a client from your own copy of the repository. You've now seen how mirrors, publication targets, publications, and repository profiles work together to put you in control of the packages your machines receive.

From here, you have several options:

- **Learn the concepts in depth**: See {ref}`explanation-repo-mirroring-2604` to understand mirrors, local repositories, publications, targets, and profiles in detail.
- **Manage production repositories**: See {ref}`how-to-manage-repos-web-portal-2604` for the full set of repository management tasks, including local repositories, resigned mirrors, and other target types.