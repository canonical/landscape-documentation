---
myst:
  html_meta:
    description: "Install, refresh, remove, and hold snaps for managed computers using Landscape's 24.04+ portal Snaps tab."
---

(how-to-web-portal-manage-snaps)=
# How to manage snaps

You can manage snaps from the web portal for each managed computer in your Landscape account.

## View snap information from the **Snaps** tab

To view snap information for a specific computer:

1. Navigate to the **Instances** section from the sidebar
2. Click the computer name that you want to manage snaps on
3. Click the **Snaps** tab

This tab displays a list of installed snaps, including the name, channel, version, and whether the snap is held at a specific version.

You can search for specific snaps using the search bar.

## Install snaps for a specific computer

To install snaps for a specific computer, navigate to the **Snaps** tab and:

1. Click **Install**
2. Start typing the snap name. A drop-down list appears with matching snaps.
3. Click on the snap in the list you want to download and select the channel/revision and architecture you want to install
4. Click **Add**
5. (Optional) To add any additional snaps, repeat steps 2-4.
6. Click **Install snaps**

## Refresh (upgrade), remove or hold snaps for a specific computer

To manage snaps on a specific computer, navigate to the **Snaps** tab:

- To refresh (upgrade) a snap, select the checkboxes for each snap you want to refresh and click **Refresh**. Specify the delivery information then click **Refresh**.
- To remove a snap, select the checkboxes for each snap you want to remove and click **Uninstall**. Specify the delivery information then click **Uninstall**
- To hold a snap, select the checkboxes for each snap you want to hold and click **Hold**. Specify the delivery information then click **Hold**
  - Note: “Holding” a snap prevents the snap from upgrading in the background. It’ll stay locked to that version until you remove the hold, but you can still manually refresh (upgrade) the snap.
- To remove a hold, select the checkboxes for each snap you want to unhold and click **Unhold**. Specify the delivery information then click **Unhold**
