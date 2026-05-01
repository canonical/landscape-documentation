---
myst:
  html_meta:
    description: "Learn about repository mirroring in Landscape, including mirrors, local repositories, publications, publication targets, filters, and GPG key management."
---

(explanation-repo-mirroring)=
# Repository mirroring

```{note}
This document applies to **Landscape 25.10 and earlier**. <!-- TODO add when the release notes exist: See the {ref}`reference-release-notes-26-04-lts` for details on our changes to repository management in 26.04. -->
```

Landscape uses repository mirroring to internally distribute software in Debian packages over your local network and manage updates. This feature allows you to establish custom repositories from your local mirror, which provides an additional layer of control over the software versions available to your client machines. This can also reduce bandwidth usage by distributing updates to clients using your local network.

You can mirror publicly accessible Ubuntu repositories, third-party repositories, or create local repositories for distributing internal software.

Repository mirroring in Landscape is backed by the **landscape-debarchive** service, which must be installed alongside `landscape-server`. This service manages mirrors, local repositories, publications, and storage backends through an API that Landscape Server and the Landscape Server UI consume.

Snaps can't be mirrored with Landscape. If you want to mirror snaps, use [Enterprise Store](https://documentation.ubuntu.com/enterprise-store/main/).

## Core concepts

Repository mirroring in Landscape is built around four core entities: **mirrors**, **local repositories**, **publications**, and **publication targets**. Understanding these concepts and how they relate to each other is crucial to using this feature correctly.

### Mirrors

A mirror is a local copy of an upstream Debian repository (for example, `archive.ubuntu.com`). When you create a mirror, you specify:

- **Archive root:** The upstream URL to mirror from (e.g. `http://archive.ubuntu.com/ubuntu/`)
- **Distribution:** The repository suite to mirror. This corresponds to what the Ubuntu archive calls a series and pocket combination. For example, `noble` (the release pocket of Ubuntu 24.04 LTS), `noble-updates` (the updates pocket), or `noble-security` (the security pocket)
- **Components:** The categories of packages to include. Upstream Ubuntu repositories typically use `main`, `restricted`, `universe`, and `multiverse`
- **Architectures:** The CPU architectures to mirror (e.g. `amd64`, `arm64`)
- **Filter (optional):** A package query expression to select a subset of packages from the upstream repository, optionally including their dependencies

After creating a mirror, you **sync** it to download packages from the upstream repository. Syncing is a long-running operation that runs in the background. You can sync a mirror repeatedly to pull in the latest packages from upstream.

### Local repositories

Local repositories let you host your own `.deb` packages that aren't sourced from an upstream mirror. You can import packages into a local repository by providing a URL to a `.deb` file or archive of `.deb` files. This is useful for distributing internally-built software or third-party packages that aren't available in any upstream repository.

Each local repository has a default distribution and component, which are used when packages are published.

### Publications

A publication connects a **source** (a mirror or local repository) to a **publication target** (a storage backend). It defines *how* your repository is made available to clients by configuring:

- **Source:** Which mirror or local repository to publish
- **Publication target:** Where to publish (see below)
- **Distribution:** The suite name clients will use in their APT configuration
- **Signing key:** A private GPG key used to sign the published repository metadata
- **Metadata options:** Labels, origins, architectures, and compression settings

Publishing a publication is a long-running operation. When you publish, the service takes a point-in-time snapshot of the source mirror or local repository and writes the resulting APT repository structure to the publication target.

You can create multiple publications from the same source, each going to a different target or using different settings. This lets you, for example, publish the same mirror to both a local filesystem for internal use and an S3 bucket for remote clients.

### Publication targets

A publication target is a named storage destination where published repositories are written. Landscape supports three types of publication target:

- **Filesystem:** A directory on the local filesystem. You can configure whether files are hardlinked, symlinked, or copied.
- **S3:** An Amazon S3 bucket or S3-compatible object store (such as MinIO). Configuration includes access credentials, region, bucket name, prefix, and storage class.
- **Swift:** An OpenStack Swift container. Configuration includes authentication URL, credentials, container name, and prefix.

Publication targets are independent of the repositories themselves. You define them once and can reuse them across multiple publications.

## Mapping to Ubuntu archive terminology

If you're familiar with the [Ubuntu package archive](https://documentation.ubuntu.com/project/how-ubuntu-is-made/concepts/package-archive/#) structure and the pre-26.04 Landscape terminology, the following table maps those concepts to 26.04 Landscape's repository mirroring terminology:

| Ubuntu archive/Pre-26.04 Landscape concept | 26.04 Landscape equivalent | Example |
|---|---|---|
| Repository / Archive | Archive root (upstream URL) | `http://archive.ubuntu.com/ubuntu/` |
| Series | Part of the distribution string | `noble` (Ubuntu 24.04 LTS) |
| Pocket (release, updates, security) | Part of the distribution string | `noble`, `noble-updates`, `noble-security` |
| Component (main, restricted, universe, multiverse) | Components list on a mirror | `["main", "universe"]` |
| Pull pocket (user-defined staging area) | Filtered mirror | A mirror with a package filter expression |

In the Ubuntu archive, the **series** and **pocket** are combined into a single **distribution** (dist) string. For example:

- `noble` — the release pocket of Ubuntu 24.04 LTS (all packages included at initial release)
- `noble-updates` — the updates pocket (newer versions of packages added after the initial release)
- `noble-security` — the security pocket (updates specifically addressing security issues)

If you need to mirror multiple pockets (for example, both `noble` and `noble-updates`), you create a separate mirror for each.

**Components** categorise packages within a distribution:

- **main:** Packages directly maintained by the repository owner (Canonical, for Ubuntu)
- **restricted:** Proprietary packages and drivers
- **universe:** Community-maintained packages
- **multiverse:** Community-maintained packages with additional restrictions

When you create a mirror, you select which components to include. A single mirror can include any combination of components.

## Filters

Mirrors support package-level filtering using a query expression language. Filters let you select a specific subset of packages from the upstream repository, replacing the role that pull pockets played in earlier versions of Landscape.

When you set a filter on a mirror, only packages matching the filter expression are downloaded during a sync. You can optionally enable **filter with dependencies**, which also includes any packages that the filtered packages depend on.

Filters are applied at sync time. If you need to distribute different subsets of packages to different groups of machines, you can create multiple filtered mirrors from the same upstream repository and publish each one separately.

```{note}
Filters cannot be used on signature-preserving mirrors, since filtering could invalidate the upstream repository's original GPG signatures.
```

## Signature-preserving mirrors

When you create a mirror, you can enable **signature preservation**. A signature-preserving mirror passes through the upstream repository's original GPG signatures without re-signing, which is useful when you want clients to verify packages directly against the upstream key.

This mode has restrictions: you cannot apply filters to a signature-preserving mirror, and syncing does not occur until publication time. The mirror is treated as a direct pass-through of the upstream repository.

## An example mirroring workflow

The following example illustrates how a Landscape administrator could use repository mirroring to manage package distribution:

1. **Create a publication target.** The administrator defines a filesystem publication target pointing to a directory on the Landscape server that will be served over HTTP.
1. **Create mirrors.** They create two mirrors of the Ubuntu archive for Noble 24.04:
   - One for `noble` (the release pocket) with components `main` and `universe`
   - One for `noble-security` (the security pocket) with the same components
1. **Sync the mirrors.** Both mirrors are synced to download all matching packages from the upstream repository.
1. **Create a filtered mirror for testing.** They create a third mirror of `noble-updates` with a filter that selects only packages relevant to their application stack.
1. **Publish.** They create publications for each mirror, all targeting the filesystem publication target, and publish them. Clients can now be configured to use a local server (e.g., Nginx or Apache Server) as their APT source.
1. **Iterate.** When new upstream updates are available, the administrator syncs the mirrors again and re-publishes to make the updated packages available.

## GPG keys

GPG keys serve two distinct purposes in Landscape repository mirroring: **verifying** upstream repositories and **signing** published repositories.

### Verification keys (mirrors)

When Landscape downloads packages from an upstream repository, it verifies the repository's GPG signatures to ensure the packages are authentic and unmodified. This requires the **public GPG key** of the upstream repository.

For Ubuntu repositories, the public GPG keys (Ubuntu Archive 2012 and 2018 signing keys) are built into the debarchive service and configured automatically. No manual setup is required.

If you're mirroring a third-party repository, you need to provide its public GPG key when creating the mirror:

1. Obtain the third party's public GPG key
1. Ensure it's in ASCII-armored format
1. Provide it when creating the mirror in Landscape

### Signing keys (publications)

When you publish a mirror or local repository, the debarchive service generates its own repository metadata (package indices, release files) for the published repository. A **private GPG key** is used to sign this metadata, so that client machines can verify the published repository is trustworthy.

You provide a private GPG key when creating a publication. This key is used to produce:

- **Detached signatures** (`Release.gpg`)
- **Clearsigned release files** (`InRelease`)

Client machines need the corresponding **public key** to verify these signatures. When Landscape applies a repository configuration to a client via a repository profile, it distributes the attached public key so the client can authenticate packages from the published repository.
