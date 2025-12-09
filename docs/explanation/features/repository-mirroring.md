(explanation-repo-mirroring)=
# Repository mirroring

Landscape uses repository mirroring to internally distribute software in Debian packages over your local network and manage updates. This feature allows you to establish custom repositories from your local mirror, which provides an additional layer of control over the software versions available to your client machines. This can also reduce bandwidth usage by distributing updates to clients using your local network.

You can use the repository mirroring feature in Landscape to mirror several publicly accessible repositories owned by Ubuntu, repositories owned by third parties or your own private repositories for distributing internal software. 

Snaps can't be mirrored with Landscape. If you want to mirror snaps, use [Enterprise Store](https://documentation.ubuntu.com/enterprise-store/main/).

## Repository mirror hierarchy

When you mirror a repository, you create a local copy of the entire repository, which includes all its data and structural elements. Understanding the structure of Landscape repository mirrors and how you can restructure your repositories to create custom package bundles for specific machines is crucial to using this feature correctly.

To understand the repository mirroring hierarchy in Landscape, you should know the following terms:

- **Repository:** The repository is the highest level of the hierarchy. It can also be called the “distribution”. If you’re mirroring an Ubuntu repository, the repository would simply be “Ubuntu”.
- **Series:** Series are inside the repository; they are specific versions of your repository. For example, “Jammy 22.04” could be the series from the Ubuntu repository. When you download a series, you download every package locally that’s available from that particular series.
- **Pocket:** Pockets are inside the series. There are different pockets, or sections, of packages:
    - **Release pocket:** Contains all packages that were available at the moment of releasing that particular series. For example, the Jammy 22.04 release pocket contains all of the packages that were included with Jammy 22.04 at the time of its initial release.
    - **Updates pocket:** Contains all the updates, or newer versions, of the packages in the series that were added to the repository after its initial release. For example, the Jammy 22.04 updates pocket contains all package updates that have been added to Jammy 22.04 *after* its initial release. If the repository doesn’t have any updates, then there won’t be an updates pocket.
    - **Security pocket:** This is a subset of the updates pocket, and it contains all the newer versions of packages that were updated specifically to fix a security issue.
    - **Pull pocket (optional - user-defined):** Pull pockets are user-defined pockets that you can create to make specific packages and updates available to different groups of machines. Pull pockets are essentially a “staging” area for you to prepare packages from other pockets before they’re distributed to your systems. You can use allowlist and blocklist filters to control which packages are included or excluded from your user-defined pull pocket.
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

- **Profile:** A configuration that can be applied to managed machines. {ref}`Profiles <reference-terms-profiles>` are sometimes called “repository profiles” in the context of repository mirroring, and they enable you to enforce certain repository configurations on your machines. For example, you may have a `test` and `production` profile which you later distribute to various machines.
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

