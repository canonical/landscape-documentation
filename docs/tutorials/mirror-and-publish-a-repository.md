---
myst:
  html_meta:
    description: "A hands-on tutorial that walks you through mirroring an Ubuntu repository with Landscape's Deb Archive service, publishing it to S3, and installing a package on a client."
---

(tutorial-deb-archive-mirror)=
# Mirror and publish a repository with Deb Archive

> See also: {ref}`explanation-repo-mirroring-2604`

In this tutorial, you'll use Landscape's Deb Archive service to mirror part of the Ubuntu archive, publish it to an Amazon S3 bucket, and configure a client machine to install packages from your published copy. Along the way, you'll see how the pieces of repository management in Landscape fit together: a *mirror* (your copy of an upstream repository), a *publication target* (where the copy is stored), a *publication* (which connects the two), and a *repository profile* (which tells your clients to use it).

You'll mirror with **signatures preserved**, meaning Landscape keeps the original Ubuntu signing information intact. This keeps the tutorial simple: because your client machine already trusts the Ubuntu archive's signing key, you won't need to manage any GPG keys yourself.

This tutorial creates a *learning* setup so you can see the full workflow end to end. When you're ready to manage repositories, see {ref}`how-to-manage-repos-web-portal-2604`.

Completing this tutorial should take approximately 30 minutes, plus time for the repository to publish.

## What you'll do

- Create an S3 publication target.
- Create a signature-preserving mirror of an Ubuntu repository.
- Publish the mirror to your target.
- Point a client machine at the published repository with a repository profile.
- Install a package on the client from your own mirror.

## Prerequisites

Before you start, make sure you have:

- A **Landscape Server 26.04 LTS (or later)** deployment with Deb Archive. If you don't have one yet, follow: {ref}`Getting started with Landscape <getting-started-with-landscape>` and {ref}`Set up Deb Archive <how-to-debarchive-repository-management>`.
- At least one **registered client machine** running Ubuntu.
- An **Amazon S3 bucket** that you can write to, along with its region and a pair of AWS access keys. Any S3-compatible object store (such as MinIO) also works.
- The bucket must allow your **client machine to read objects**. In this tutorial, the client fetches packages directly from the S3 URL without credentials, so enable public object read on the bucket.

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

## Step 2: Create a signature-preserving mirror

Next, you'll create a **mirror**: Landscape's own copy of an upstream Ubuntu repository. You'll preserve the upstream signatures so your client can verify packages against Ubuntu's existing signing key.

1. From the sidebar, navigate to **Repositories** > **Mirrors**.
1. Click **Add mirror**.
1. In the **Name** field, enter `tutorial-mirror`.
1. In the **Source type** dropdown menu, select **Ubuntu archive**.
1. Leave the **Source URL** at its default value. This points at the Ubuntu archive.
1. Select the **Preserve upstream signing key** checkbox. This is the setting that keeps Ubuntu's original signatures intact. Notice that, once you select it, package filtering is no longer offered: a signature-preserving mirror is a faithful pass-through of the upstream repository, so it can't be filtered.
1. Under **Mirror contents**, choose what to mirror:
    - **Distribution**: `noble`
    - **Components**: `main`
    - **Architectures**: `amd64`
1. Click **Add mirror** to create the mirror.

You've now defined a mirror, but it hasn't pulled any packages yet. For a signature-preserving mirror, Landscape fetches the upstream packages when you publish, which you'll do next.

## Step 3: Publish the mirror

A **publication** connects your mirror to your publication target and makes the repository available. Publishing it is what actually writes the repository into your S3 bucket.

1. From the sidebar, navigate to **Repositories** > **Publications**.
1. Click **Add publication**.
1. In the **Publication name** field, enter `tutorial-publication`.
1. In the **Source type** dropdown menu, select **Mirror**.
1. In the **Source** dropdown menu, select `tutorial-mirror`.
1. In the **Publication target** dropdown menu, select `tutorial-target`.
1. In the **Architectures** dropdown menu, select `amd64`.
1. Notice that there's no **Signing GPG key** field and that the distribution is fixed. Because you preserved the upstream signatures, Landscape doesn't re-sign anything, so there's nothing for you to configure here.
1. Click **Add publication** to create and publish.
1. From the **Publications** list, find `tutorial-publication`, click its actions menu, and select **Republish** to start the publishing process.

Landscape now copies the upstream packages and writes a complete APT repository into your S3 bucket. Mirroring `noble main` for `amd64` involves a fair amount of data, so this step takes some time and disk space. When it finishes, your repository is live in the bucket and ready for clients.

## Step 4: Point your client at the repository

Your repository exists, but your client doesn't know about it yet. You'll fix that with a **repository profile**, which applies an APT source to the client machines you associate with it.

1. From the sidebar, navigate to **Repositories** > **Repository profiles**.
1. Click **Add repository profile**.
1. In the **Profile name** field, enter `tutorial-clients`.
1. Click **Add source**, then fill in the source:
    1. In the **Source name** field, enter `tutorial-source`.
    1. In the `deb` line field, enter the address of your published repository, substituting your own bucket and region:

        ```text
        deb https://my-tutorial-bucket.s3.us-east-1.amazonaws.com/ noble main
        ```

    1. Leave the **GPG key** field empty. Because you preserved the upstream signatures, your client verifies packages against Ubuntu's archive key, which is already in its keyring.
1. Use the **Association** options to associate this profile with your registered client.
1. Save the profile.

Landscape applies the new APT source to your client. The configuration is applied once when the client is associated with the profile.

## Step 5: Install a package from your mirror

Now you'll confirm that your client is using your mirror and install a package from it.

On your client machine, refresh the package lists and install a package:

```bash
sudo apt update
sudo apt install hello
```

If `apt update` completes without any signature warnings, your client successfully verified your published repository against Ubuntu's signing key. To confirm the package came from your mirror rather than the public Ubuntu archive, check its source:

```bash
apt-cache policy hello
```

You should see your S3 bucket's address listed as the origin for the package. That means `hello` was installed from the repository you mirrored and published.

## Summary

Congratulations! You've mirrored part of the Ubuntu archive with Deb Archive, published it to an S3 bucket with the upstream signatures preserved, and installed a package on a client from your own copy of the repository. You've now seen how mirrors, publication targets, publications, and repository profiles work together to put you in control of the packages your machines receive.

From here, you have several options:

- **Learn the concepts in depth**: See {ref}`explanation-repo-mirroring-2604` to understand mirrors, local repositories, publications, targets, and profiles in detail.
- **Manage production repositories**: See {ref}`how-to-manage-repos-web-portal-2604` for the full set of repository management tasks, including local repositories, resigned mirrors, and other target types.