Repository content is stored in two separate places:

- **Debarchive storage**: Repository files managed by the Debarchive service (`landscape-debarchive`), such as the packages that it downloads when you sync a mirror, are stored on the machine where Debarchive runs. The `landscape-debarchive` snap stores these files in `/var/snap/landscape-debarchive/common` by default. Clients don't install packages from this location.
- **The publication target**: When you publish, Landscape creates a point-in-time snapshot of the source mirror or local repository and writes the resulting APT repository structure to the publication target. Clients install packages from the published repository, so your clients must be able to reach it.
