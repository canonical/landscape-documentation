(how-to-classic-web-portal-manage-snaps)=
# How to manage snaps

You can manage snaps from the web portal for each managed computer in your Landscape account.

## View snap information from the **Snaps** tab

To view snap information for a specific computer:

1. Navigate to the **Computers** page in the header
2. Click the computer name that you want to manage snaps on
3. Click the **Snaps** tab

This tab displays the number of installed snaps and provides options for managing snaps.

To view installed snaps, click **Installed snaps** located after the table or click the number of installed snaps.

To view held snaps, click **Held snaps** located after the table.

## Install snaps for a specific computer

To install snaps for a specific computer, navigate to the **Snaps** tab and:

1. Click **Install snaps**
2. Enter the *exact* snap name
3. Enter the tracking channel and revision if not using the defaults. You can hover your cursor over these fields to view the defaults.
4. Select **Classic** if using classic confinement
5. Click **+** (plus sign) to add any additional snaps, repeating the previous steps
6. Specify the delivery information
7. Click **Submit**

## Refresh (upgrade), remove or hold snaps for a specific computer

To manage snaps on a specific computer:

- To refresh (upgrade) a snap, click the up arrow icon in the same row and column as the snap name.
- To remove a snap, click the minus sign icon in the same row and column as the snap name.
- To hold a snap, click the package icon directly next to the snap name in the same row and column as the snap name.
  - Note: “Holding” a snap prevents the snap from upgrading in the background. It’ll stay locked to that version until you remove the hold, but you can still manually refresh (upgrade) the snap.
- Specify the delivery information located after the table
- Click **Apply changes**

