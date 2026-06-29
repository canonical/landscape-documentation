---
myst:
  html_meta:
    description: "Install, upgrade, remove, and hold packages and snaps for managed instances using Landscape's 24.04+ web portal."
---

(how-to-web-portal-manage-snaps)=
# How to manage packages and snaps

You can manage packages (Debian) and snaps from the web portal for each managed instance in your Landscape account. You can also use package profiles and remote script execution to apply package management policies across multiple instances.

## Packages

### View package information

To view package information for a specific client instance, go to **Instances** > click the instance you want to manage > **Packages** tab. Note that packages can sometimes take awhile to load.

This tab displays a list of installed packages, including the name, status, and version.

You can also search for specific packages using the search bar.

### Manage packages: Install, hold, upgrade, and more

You can perform different actions with packages from an instance's **Packages** tab, either in bulk or on a single package. From the **Packages** tab, you can:

- Install/uninstall
- Hold/unhold
   - "Holding" a package prevents the package from upgrading in the background. It’ll stay locked to that version until you remove the hold, but you can still manually upgrade the package.
- Upgrade/Downgrade
   - You can only downgrade an individual package, not multiple packages at once.

All actions will ask you to complete a form or confirm before Landscape sends an activity to perform the action. You can check the status of activities in the **Activities** page from the sidebar.

### Prevent a package from being installed

You can prevent a Debian package from being installed on groups of managed instances by combining remote script execution with a package profile.

This workflow is for APT-managed Debian packages on instances using the Landscape Client deb package. If you're using the Landscape Client snap (with Ubuntu Core), remote script execution is still available, but APT-based package blocking isn't.

1. Add and run a script on the target instances (see {ref}`how-to-web-portal-use-remote-script-execution`) that creates `/etc/apt/preferences.d/<PACKAGE>.pref` with `Pin-Priority` set below `0`.
   For example, to block `audacity`, the preferences file content should be:

   ```text
   Package: audacity
   Pin: release *
   Pin-Priority: -1
   ```

1. Create a package profile with a manual `Conflicts with` constraint for that package, then associate it with the target access group or tags (see {ref}`how-to-web-portal-use-profiles`).

APT preferences prevent future installation, but they don't remove a package that's already installed. The package profile is what enforces removal if the package appears on associated instances.

To allow the package again later, remove the APT preferences file from target instances, then remove or update the related package profile constraint.

## Snaps

### View snap information

To view snap information for a specific client instance, go to **Instances** > click the instance you want to manage > **Snaps** tab.

This tab displays a list of installed snaps, including the name, channel, version, and whether the snap is held at a specific version.

You can also search for specific snaps using the search bar.

### Manage snaps: Install, refresh, hold, and more

You can perform different actions with snaps from an instance's **Snaps** tab, either in bulk or on a single snap. From the **Snaps** tab, you can:

- Install/uninstall (remove)
- Refresh (upgrade)
- Hold/unhold
   - "Holding" a snap prevents the snap from upgrading in the background. It’ll stay locked to that version until you remove the hold, but you can still manually refresh (upgrade) the snap.
- Switch channels
   - You can only switch channels on individual snap, not multiple snaps at once.

All actions will ask you to complete a form or confirm before Landscape sends an activity to perform the action. You can check the status of activities in the **Activities** page from the sidebar.
