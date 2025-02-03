(how-to-guides-web-portal-web-portal-24-04-or-later-manage-livepatch-and-kernel-updates)=
# How to manage Livepatch and kernel updates from the Landscape web portal

You can view and manage kernel and Livepatch information from the **Kernel** tab. To access this tab, go to **Instances** > Select your instance > **Kernel**.

**Current kernel version** shows the kernel version installed on your instance, and you can upgrade/downgrade with **Upgrade kernel** or **Downgrade kernel**.  

Note that if you upgrade or downgrade to a new version of the kernel, you’ll need to restart your instance for the new version to be used. You can restart your instance from the web portal with **Restart instance.**

**Status** shows the statuses that can be reported by Livepatch. Your instance can have more than one status, and Landscape only reports the most relevant status. The possible statuses are:

* **Livepatch disabled**: Displayed when Landscape detects that Livepatch is disabled.
* **Restart required**: A new kernel has been installed, and a restart is required to load it.
* **End of life**: The current kernel is no longer supported by Livepatch.
* **Kernel upgrade available**: A new kernel is available to be installed from the Ubuntu archive.
* **Fully patched**: All Livepatches have been applied.
* **Waiting for status**: Livepatch information has not yet been received by Landscape.

**Livepatch coverage** shows the date until the current kernel is supported or indicates if it has expired. Sometimes the kernel expiration date won’t be known or has not yet been reported by the Landscape client.

The **Patches discovered since last restart** table lists the patches applied by Livepatch to the current running kernel and their status.

