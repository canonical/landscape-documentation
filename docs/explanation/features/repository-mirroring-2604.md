---
myst:
  html_meta:
    description: "Learn about repository mirroring in Landscape, including mirrors, local repositories, publications, publication targets, filters, and GPG key management."
---

(explanation-repo-mirroring-2604)=
# Repository mirroring (26.04 LTS and later)

```{note}
This document applies to **Landscape 26.04 and later**. If you're using Landscape 25.10 or earlier, see {ref}`repository mirroring (25.10 and earlier)<explanation-repo-mirroring>` instead.
```

Landscape uses repository mirroring to internally distribute software in Debian packages over your local network and manage updates. This feature allows you to establish custom repositories from your local mirror, which provides an additional layer of control over the software versions available to your client machines. This can also reduce bandwidth usage by distributing updates to clients using your local network.

You can mirror publicly accessible Ubuntu repositories, third-party repositories, or create local repositories for distributing internal software.

Snaps can't be mirrored with Landscape. If you want to mirror snaps, use [Enterprise Store](https://documentation.ubuntu.com/enterprise-store/main/).

In Landscape 26.04 LTS and later, repository mirroring uses a publication-based model. You create or sync repository content in a mirror or local repository, then create a publication to publish that content to a publication target. Client machines are configured to pull from the publication target, which can serve the published repository content.

The service that provides this functionality is `landscape-debarchive`. You might see this name in installation instructions, configuration, logs, troubleshooting materials, or API references related to repository mirroring.

## Repository mirroring concepts

Repository mirroring in Landscape is built around four core entities: **mirrors**, **local repositories**, **publications**, and **publication targets**. Understanding these concepts and how they relate to each other is crucial to using this feature correctly.

Repository mirroring in Landscape is based on these main concepts:

- **Mirrors:** Local copies of an upstream Debian repositories.
- **Local repositories:** Repositories that host your own `.deb` packages you provide.
- **Publications:** Configurations that connect a mirror or local repository to a publication target, defining how the repository is made available to clients.
- **Publication targets:** Storage locations where published repositories are written.
- **Repository profiles:** Configurations that can apply published repositories to client machines.

```{mermaid}
graph TD
    A[Mirror] -->|Source for| C[Publication]
    B[Local Repository] -->|Source for| C[Publication]
    C[Publication] -->|Publishes to| D[Publication Target]
    D[Publication Target] -->|Serves repository to| E[Client Machines]
    F[Repository Profile] -->|Applies APT sources to| E[Client Machines]
```

### Mirrors

A mirror is a local copy of an upstream Debian repository (for example, `archive.ubuntu.com`). When you create a mirror, you specify:

- **Archive root:** The upstream repository URL to mirror from (e.g. `http://archive.ubuntu.com/ubuntu/`)
- **Distribution:** The repository suite to mirror. This corresponds to what the Ubuntu archive calls a series and pocket combination. For example, `noble` (the release pocket of Ubuntu 24.04 LTS), `noble-updates` (the updates pocket), or `noble-security` (the security pocket)
- **Components:** The categories of packages to include. Upstream Ubuntu repositories use `main`, `restricted`, `universe`, and `multiverse`
- **Architectures:** The CPU architectures to mirror (e.g. `amd64`, `arm64`)
- **Filter (optional):** A package query expression to select a subset of packages from the upstream repository, optionally including their dependencies

After creating a mirror, you **sync** it to download packages from the upstream repository. You can sync a mirror repeatedly to pull in the latest packages from upstream.

### Signature-preserving mirrors

A signature-preserving mirror is a special type of mirror that maintains the original GPG signatures from the upstream repository without re-signing. This allows clients to verify packages directly against the upstream repository's public key, rather than needing a separate key for the mirror. You can enable signature preservation when creating a mirror.

This mode has restrictions: you cannot apply filters to a signature-preserving mirror, and syncing does not occur until publication time. The mirror is treated as a direct pass-through of the upstream repository.

#### Filtered mirrors

Filtered mirrors include only a subset of packages from the upstream repository. The filter language lets you select which packages are included.

When you set a filter on a mirror, only packages matching the filter expression are downloaded during a sync. You can optionally enable **filter with dependencies**, which also includes any packages that the filtered packages depend on.

Filters are applied at sync time. If you need to distribute different subsets of packages to different groups of machines, you can create multiple filtered mirrors from the same upstream repository and publish each one separately.

```{note}
Filters cannot be used on signature-preserving mirrors, since filtering could invalidate the upstream repository's original GPG signatures.
```

### Local repositories

Local repositories let you host your own `.deb` packages that aren't sourced from an upstream mirror. You can use a local repository for distributing internally-built software or third-party packages that aren't available from an upstream repository you mirror. You add packages to the local repository, then publish the repository so that client machines can use it as an APT source.

Each local repository has a default distribution and component, which are used when packages are published.

### Publications

Publications make a mirror or local repository available to client instances by publishing it to a publication target. A publication connects a **source** (a mirror or local repository) to a **publication target** (a storage backend). It defines *how* the repository is made available to clients by configuring:

- **Source:** The mirror or local repository to publish
- **{ref}`Publication target<explanation-repo-mirroring-2604-publication-targets>`:** Where to publish
- **Distribution:** The suite name clients will use in their APT configuration
- **Signing key:** A private GPG key used to sign the published repository metadata
- **Metadata options:**
  - The values of the Label and Origin fields in the published repository's Release file
  - Which architectures to include in the published repository
  - Whether to provide hash index files
  - Settings for the ButAutomaticUpgrades and NotAutomatic fields in the Release file
  - Settings for using compression and generating content index files

When you publish, Landscape creates a point-in-time snapshot of the source mirror or local repository and writes the resulting APT repository structure to the publication target. Client machines can then be configured to use that published repository.

You can create multiple publications from the same source, each going to a different target or using different settings. This lets you, for example, publish the same mirror to both a local filesystem for internal use and another target (such as an S3 bucket) for remote clients.

(explanation-repo-mirroring-2604-publication-targets)=
### Publication targets

A publication target is the storage location where Landscape writes a published repository. Landscape supports the following types of publication target:

- **Filesystem:** A directory on the local filesystem.
- **S3:** An Amazon S3 bucket or S3-compatible object store (such as MinIO).
- **Swift:** An OpenStack Swift container.

Publication targets are separate from mirrors and local repositories. You can define a target once and reuse is for multiple publications.

## An example mirroring workflow

The following example illustrates how a Landscape administrator could use repository mirroring to manage package distribution. To understand the example, you should be familiar with these additional terms:

- **Profile:** A configuration that can be applied to managed machines. {ref}`Profiles <reference-terms-profiles>` are sometimes called "repository profiles" in the context of repository mirroring, and they enable you to enforce certain repository configurations on your machines. For example, you may have a `test` and `production` profile which you later distribute to various machines.
- **Tags:** Tags are labels you can apply to groups of machines, and they're used with profiles when mirroring repositories. For example, if you had a repository profile named `test-profile`, you could associate it with a tag named `test-tag`, and the configuration in this profile would then be applied to all machines tagged with `test-tag`.

**Repository mirroring process**

![Repository mirror process](/assets/images/repository-mirroring-2604.jpg)

Consider the following example scenario which illustrates how a user could use repository mirroring in Landscape:

1. The administrator creates two filesystem publication targets: `test-target` and `prod-target`. Each points to a separate directory on the Landscape server served over HTTP.
1. They create three mirrors of the Ubuntu archive for Resolute 26.04, using filters to select specific packages for each mirror, as-needed:
   - One for `resolute` (the release pocket) with components `main` and `universe`
   - One for `resolute-updates` (the updates pocket) with the same components
   - One for `resolute-security` (the security pocket) with the same components
1. They sync all three mirrors to download the matching packages from the upstream Ubuntu repository.
1. They create two repository profiles (`test-profile` and `prod-profile`) and two tags (`test-tag` and `prod-tag`). These tags are applied to the appropriate machines and associated with their corresponding profiles.
1. They create publications for each mirror targeting `test-target` and publish them. The `test-profile` is configured to point client machines at `test-target`, so machines tagged with `test-tag` begin pulling packages from the test publication.
1. The administrator tests the new packages and updates to ensure they work as expected and don't introduce issues into the test environment.
1. Once testing is complete and the packages are approved, the administrator creates publications for the same mirrors targeting `prod-target` and publishes them. The `prod-profile` is configured to point client machines at `prod-target`, so machines tagged with `prod-tag` now receive the approved packages. The decision of *when* to publish to `prod-target` is what controls the release to production.
1. The administrator repeats steps #3-7 every time they want to distribute new packages to their client machines. They can re-use the publications they created steps #5 and #7, since the publication configuration is the same each time. They just need to republish to update the content at the publication target.

## GPG keys

GPG keys are used with repository mirroring in Landscape to establish trust in the mirror and verify the packages originating from a trusted source. The GPG keys are used for two purposes:

- Verifying packages from upstream repositories
- Signing published repositories so clients can verify them

### Verification keys

When Landscape downloads packages from an upstream repository, it verifies that the repository's metadata is signed by a trusted key to ensure the packages are authentic and unmodified. This requires the **public GPG key** of the upstream repository.

For Ubuntu repositories, the public GPG keys are built into Landscape and configured automatically. No manual setup is required.

If you're mirroring a third-party repository, you need to provide its public GPG key when creating the mirror:

1. Obtain the third party's public GPG key
1. Ensure it's in ASCII-armored format
1. Provide it when creating the mirror in Landscape

### Signing keys

When Landscape publishes a mirror or local repository, the published repository metadata must be signed. Client machines use the corresponding public key to verify that the published repository is trustworthy.

The signing key has two parts:

- **Private key:** Used by Landscape to sign the published repository metadata.
- **Public key:** Distributed to client machines so they can verify the published repository.

When Landscape applies a repository configuration to a client via a repository profile, it distributes the attached public key so the client can authenticate packages from the published repository.
