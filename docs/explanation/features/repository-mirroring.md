---
myst:
  html_meta:
    description: "Learn about repository mirroring in Landscape, including mirrors, pockets, publications, publication targets, profiles, and GPG key management."
---

(explanation-repo-mirroring)=
(explanation-repo-mirroring-2604)=
# Repository mirroring

Landscape uses repository mirroring to internally distribute software in Debian packages over your local network and manage updates. This feature allows you to establish custom repositories from your local mirror, which provides an additional layer of control over the software versions available to your client machines. This can also reduce bandwidth usage by distributing updates to clients using your local network.

Repository mirroring works differently in Landscape Server 26.04 LTS and later than it does in earlier releases..

**Select your Landscape Server version:**

`````{tab-set}

````{tab-item} Landscape Server 26.04 LTS and later

You can mirror publicly accessible Ubuntu repositories, third-party repositories, or create local repositories for distributing internal software.

Snaps can't be mirrored with Landscape. If you want to mirror snaps, use [Enterprise Store](https://documentation.ubuntu.com/enterprise-store/main/).

In Landscape 26.04 LTS and later, repository mirroring uses a publication-based model. You create or sync repository content in a mirror or local repository, then create a publication to publish that content to a publication target. Client machines are configured to pull from the publication target, which can serve the published repository content.

The service that provides this functionality is `landscape-debarchive`. You might see this name in installation instructions, configuration, logs, troubleshooting materials, or API references related to repository mirroring.

## Repository mirroring concepts

Repository mirroring in Landscape is built around four core entities: **mirrors**, **local repositories**, **publications**, and **publication targets**. Understanding these concepts and how they relate to each other is crucial to using this feature correctly.

Repository mirroring in Landscape is based on these main concepts:

- **{ref}`Mirrors <explanation-repo-mirroring-2604-mirrors>`:** Local copies of an upstream Debian repositories.
- **{ref}`Local repositories <explanation-repo-mirroring-2604-local-repositories>`:** Repositories that host your own `.deb` packages you provide.
- **{ref}`Publications <explanation-repo-mirroring-2604-publications>`:** Configurations that connect a mirror or local repository to a publication target, defining how the repository is made available to clients.
- **{ref}`Publication targets <explanation-repo-mirroring-2604-publication-targets>`:** Storage locations where published repositories are written.
- **{ref}`Repository profiles <explanation-repo-mirroring-2604-repository-profiles>`:** Configurations that can apply published repositories to client machines.

```{mermaid}
graph TD
    A[Mirror] -->|Source for| C[Publication]
    B[Local Repository] -->|Source for| C
    C -->|Publishes to| D[Publication Target]
    D -->|Serves repository to| E[Client Machines]
    F[Repository Profile] -->|Applies APT sources to| E
    D -.->|Repository URL used in profile| F
```

(explanation-repo-mirroring-2604-mirrors)=
### Mirrors

A mirror is a local copy of an upstream Debian repository (for example, `archive.ubuntu.com`). When you create a mirror, you specify:

- **Archive root:** The upstream repository URL to mirror from (e.g. `http://archive.ubuntu.com/ubuntu/`)
- **Distribution:** The repository suite to mirror. This corresponds to what the Ubuntu archive calls a series and pocket combination. For example, `noble` (the release pocket of Ubuntu 24.04 LTS), `noble-updates` (the updates pocket), or `noble-security` (the security pocket). For more info, see the [Ubuntu project docs](https://documentation.ubuntu.com/project/release-team/ubuntu-releases/).
- **Components:** The categories of packages to include. Upstream Ubuntu repositories use `main`, `restricted`, `universe`, and `multiverse`. For more info, see [Ubuntu package archive](https://documentation.ubuntu.com/project/how-ubuntu-is-made/concepts/package-archive/).
- **Architectures:** The CPU architectures to mirror (e.g. `amd64`, `arm64`). For more info, see [Ubuntu supported architectures](https://documentation.ubuntu.com/project/how-ubuntu-is-made/concepts/supported-architectures/).
- **Filter (optional):** A package query expression to select a subset of packages from the upstream repository, optionally including their dependencies

After creating a mirror, you **sync** it to download packages from the upstream repository. You can sync a mirror repeatedly to pull in the latest packages from upstream.

#### Signature-preserving mirrors

A signature-preserving mirror is a special type of mirror that maintains the original GPG signatures from the upstream repository without re-signing. This allows clients to verify packages directly against the upstream repository's public key, rather than needing a separate key for the mirror. You can enable signature preservation when creating a mirror.

This mode has restrictions: you cannot apply filters to a signature-preserving mirror, and syncing does not occur until publication time. The mirror is treated as a direct pass-through of the upstream repository.

#### Filtered mirrors

Filtered mirrors include only a subset of packages from the upstream repository. The filter language lets you select which packages are included.

When you set a filter on a mirror, only packages matching the filter expression are downloaded during a sync. You can optionally enable **filter with dependencies**, which also includes any packages that the filtered packages depend on.

Filters are applied at sync time. If you need to distribute different subsets of packages to different groups of machines, you can create multiple filtered mirrors from the same upstream repository and publish each one separately.

```{note}
Filters cannot be used on signature-preserving mirrors, since filtering could invalidate the upstream repository's original GPG signatures.
```

(explanation-repo-mirroring-2604-local-repositories)=
### Local repositories

Local repositories let you host your own `.deb` packages that aren't sourced from an upstream mirror. You can use a local repository for distributing internally-built software or third-party packages that aren't available from an upstream repository you mirror. You add packages to the local repository, then publish the repository so that client machines can use it as an APT source.

Each local repository has a default distribution and component, which are used when packages are published.

(explanation-repo-mirroring-2604-publications)=
### Publications

Publications make a mirror or local repository available to client instances by publishing it to a publication target. A publication connects a **source** (a mirror or local repository) to a **publication target** (a storage backend). It defines *how* the repository is made available to clients by configuring:

- **Source:** The mirror or local repository to publish
- **{ref}`Publication target<explanation-repo-mirroring-2604-publication-targets>`:** Where to publish
- **Distribution:** The suite name clients will use in their APT configuration
- **Signing key:** A private GPG key used to sign the published repository metadata
- **Metadata options:**
  - The values of the `Label` and `Origin` fields in the published repository's `Release` file
  - Which architectures to include in the published repository
  - Whether to provide hash index files
  - Settings for the `ButAutomaticUpgrades` and `NotAutomatic` fields in the `Release` file
  - Settings for using compression and generating content index files

When you publish, Landscape creates a point-in-time snapshot of the source mirror or local repository and writes the resulting APT repository structure to the publication target. Client machines can then be configured to use that published repository.

You can create multiple publications from the same source, each going to a different target or using different settings. This lets you, for example, publish the same mirror to both a local filesystem for internal use and another target (such as an S3 bucket) for remote clients.

(explanation-repo-mirroring-2604-publication-targets)=
### Publication targets

A publication target is the storage location where Landscape writes a published repository. Landscape supports the following types of publication target:

- **Filesystem:** A directory on the local filesystem.
- **S3:** An Amazon S3 bucket or S3-compatible object store (such as MinIO).
- **Swift:** An OpenStack Swift container.

Publication targets are separate from mirrors and local repositories. You can define a target once and reuse it for multiple publications. The publication target must have enough storage available to hold the entire contents of the publication source.

If you are in a restricted environment (e.g. in an air-gapped environment, or with a manual Landscape deployment on a single machine, etc.), you may wish to use a filesystem publication target. Otherwise, we recommend using S3 or Swift publication targets.

Landscape itself does not serve filesystem publication targets. Instead, you must configure a web server to serve your packages from your filesystem.

(explanation-repo-mirroring-2604-repository-profiles)=
### Repository profiles

A repository profile is a configuration that can be applied to client machines to configure their APT sources. When you create a repository profile, you can specify the public URLs of your published repositories. This allows you to control which published repositories are used by which machines.

For example, if your publication target is a filesystem served over HTTP at `http://landscape-server/ubuntu/`, you would include that URL in the repository profile. When the profile is applied to client machines, they will be configured to pull packages from that URL. If your publication target is an S3 bucket configured for public HTTPS access, you could include the S3 URL (e.g. `https://my-bucket.s3.amazonaws.com/ubuntu/`) in the profile instead.

You can have different repository profiles for different groups of machines, allowing you to control which published repositories each group uses.

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

````

````{tab-item} Landscape Server 25.10 and earlier

You can use the repository mirroring feature in Landscape to mirror several publicly accessible repositories owned by Ubuntu, repositories owned by third parties or your own private repositories for distributing internal software.

Snaps can't be mirrored with Landscape. If you want to mirror snaps, use [Enterprise Store](https://documentation.ubuntu.com/enterprise-store/main/).

## Repository mirror hierarchy

When you mirror a repository, you create a local copy of the entire repository, which includes all its data and structural elements. Understanding the structure of Landscape repository mirrors and how you can restructure your repositories to create custom package bundles for specific machines is crucial to using this feature correctly.

To understand the repository mirroring hierarchy in Landscape, you should know the following terms:

- **Repository:** The repository is the highest level of the hierarchy. It can also be called the "distribution". If you’re mirroring an Ubuntu repository, the repository would simply be "Ubuntu".
- **Series:** Series are inside the repository; they are specific versions of your repository. For example, "noble" (for Ubuntu 24.04 LTS) could be the series from the Ubuntu repository. When you download a series, you download every package locally that’s available from that particular series.
- **Pocket:** Pockets are inside the series. They're system-defined sections of packages within a package repository. Pockets are a concept from the [Ubuntu package archive](https://documentation.ubuntu.com/project/how-ubuntu-is-made/concepts/package-archive/#). Landscape uses the following pockets:
  - **Release pocket:** Contains all packages that were available at the moment of releasing that particular series. For example, the Jammy 22.04 release pocket contains all of the packages that were included with Jammy 22.04 at the time of its initial release.
  - **Updates pocket:** Contains all the updates, or newer versions, of the packages in the series that were added to the repository after its initial release. For example, the Jammy 22.04 updates pocket contains all package updates that have been added to Jammy 22.04 *after* its initial release. If the repository doesn’t have any updates, then there won’t be an updates pocket.
  - **Security pocket:** This is a subset of the updates pocket, and it contains all the newer versions of packages that were updated specifically to fix a security issue.
  - **Pull pocket (optional - user-defined):** Pull pockets are user-defined pockets that you can create to make specific packages and updates available to different groups of machines. Pull pockets are essentially a "staging" area for you to prepare packages from other pockets before they’re distributed to your systems. You can use allowlist and blocklist filters to control which packages are included or excluded from your user-defined pull pocket.
- **Component:** Components are categories of packages in the system-defined pockets (release, updates, security). There are four possible components:
  - **Main:** Contains all packages that are directly maintained by the repository owner. For an Ubuntu repository, this would be all packages directly maintained by Canonical.
  - **Restricted:** Contains proprietary packages and drivers that aren’t fully open-source.
  - **Universe:** Contains packages that are maintained by the community, rather than the owner of the repository (Canonical, for Ubuntu repositories).
  - **Multiverse:** Contains packages that are maintained by the community, but these packages may have restrictions or other reasons to be separate from the universe component.

    All packages belong to a specific component (category), but not all pockets use all four components. For example, you may encounter a release pocket that only uses the main component, so all packages in that release pocket would be in the main component.

The following image demonstrates an example hierarchy of the previous terms, showing where the actual packages are located within the repository mirror.

**Repository mirror hierarchy**

![Repository mirror hierarchy](https://assets.ubuntu.com/v1/abfbe7d9-Landscape_RepoMirrorHierarchy_v4.png)

## An example repository mirroring process

The following diagram provides an example of how packages from the Ubuntu repository can get distributed to specific client machines. To understand the example, you should be familiar with these additional terms:

- **Profile:** A configuration that can be applied to managed machines. {ref}`Profiles <reference-terms-profiles>` are sometimes called "repository profiles" in the context of repository mirroring, and they enable you to enforce certain repository configurations on your machines. For example, you may have a `test` and `production` profile which you later distribute to various machines.
- **Tags:** Tags are labels you can apply to groups of machines, and they’re used with profiles when mirroring repositories. For example, if you had a repository profile named `test-profile`, you could associate it with a tag named `test-tag`, and the configuration in this profile would then be applied to all machines tagged with `test-tag`.

**Repository mirroring process**

![Repository mirror process](https://assets.ubuntu.com/v1/091b20af-Landscape_RepoMirroringProcess_Final.png)

Using this diagram as a reference, consider the following example scenario which illustrates how a user could use repository mirroring in Landscape:

1. From the Ubuntu repository, the user downloads all packages in the Jammy 22.04 series on their local server
2. They create two repository profiles for this local mirror: `test-profile` and `prod-profile`
3. They create two tags: `test-tag` and `prod-tag`. These tags are applied to the appropriate machines they use for test and production environments and associated with their corresponding profiles.
4. The user determines which packages from the `release`, `updates` and `security` pockets they want to install and update on their systems.
5. They add these packages to a pull pocket and name the pull pocket `dev-packages`
6. To test this configuration, the `dev-packages` pull pocket is applied to machines tagged with `test-tag` associated with the profile `test-profile`.
7. The user tests the new packages and updates to ensure they work as expected and don’t introduce new issues into the test environment.
8. Once testing is complete and the new packages and updates are approved, the user applies the `dev-packages` pull pocket to machines tagged with `prod-tag` associated with the profile `prod-profile`.
9. The user repeats steps #4-8 every time they want to distribute new packages to their client machines.

## GPG keys

GPG keys are used with repository mirroring in Landscape to establish trust in the mirror and verify the packages originated from a trusted source. When you mirror a repository with Landscape, you generate a mirror key-pair that includes the following two mirror keys:

- **Your private mirror key**

    When Landscape mirrors a repository, it copies all of the packages to your local server. After the packages are copied, Landscape needs to build its own metadata around the packages. These packages and metadata are what is signed by your private mirror key.

- **Your public mirror key**

    When you assign the packages of your local mirror to a client through a repository profile, the Landscape Client application downloads your public mirror key onto that client machine when it applies that repository profile. This tells the client machine that it can trust the metadata and packages signed by the private key on the Landscape server when getting packages from the local mirror.

Additionally, when Landscape downloads packages from a public repository, you also need the public GPG key for that public repository. For Ubuntu public repositories, all public GPG keys are known and are automatically included and pre-configured in Landscape.

If you’re mirroring a third-party repository that Landscape isn’t configured for, then you’ll need to:

1. Get the third party’s public GPG key
2. Download the GPG key
3. Ensure it’s in ASCII format 
4. Import it into your Landscape server
    - Note: The public GPG key doesn’t need to be accessible to the clients
5. Assign it to the repository that you want to mirror

````

`````
