(how-to-guides-secure-removal-client-snap)=
# How to completely remove the Landscape Client snap and its data

This document provides guidance for thoroughly removing the Landscape Client snap and its associated data from a device.

## Snap lifecycle overview

While Landscape allows you to uninstall a snap in the web portal, a more comprehensive removal that includes all associated data and cached information requires additional steps and an understanding of how SnapD manages snap throughout their lifecycle.

**First install**

Upon the initial installation of a snap on a device, SnapD establishes the required structures and storage locations specific to that snap version.

**Upgrade**

During a snap upgrade, SnapD does not overwrite the existing version. Instead, it marks the preceding snap as "disabled" before installing the new version. This mechanism supports rollback functionality, allowing reversion to the previous version in the event of an error. Typically, SnapD retains only the current and immediately previous snap versions; older versions are automatically removed.

To view both active and disabled snaps within Landscape, use the following script:

```python
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.list_all()
```

**Uninstalling (basic)**

During a normal uninstall, the current version of the snap is removed along with a disabled previous version. However, SnapD will normally take a [snapshot](https://snapcraft.io/docs/snapshots) of the snap before it's deleted. This consists of user, system, and configuration data. Snapshots are not taken when upgrading a snap as it's already moved to and retained by the new version.

To view these snapshots for a device from Landscape using this example script.

```python
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.get_snapshots()
```

## Uninstall and purge a snap

If you wish to uninstall snap but not retain any of this data, you can do this by uninstalling the snap with the purge flag. Here's an example script demonstrating how to do this from Landscape.

```python
<missing-script>
```

## Manual snapshots

It's worth noting that the purge flag will only prevent the creation of a new snapshot during the uninstall. If there are already any previous snapshots on the system, either from previous uninstalls or manually created, there may still be data related to that snap on the device.

To verify this is not the case, you can check the snapshots and the snap data they contain using the script in the previous section.

If you then wish to remove that data, you can either forget the entire snapshot with the following script:

```python
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.forget_snapshot(id)
```

Or you can remove the data from that specific snap from a snapshot.

```python
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.forget_snapshot(id, snaps=[snaps])
```

## Perform a complete purge

This example script will terminate any running instances, uninstall a snap, prevent any snapshots being taken and scan all snapshots,  removing all traces of any data from that snap. 

```python
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.remove(snap, purge=True, terminate=True)
```

## Complete device wipe

While the above steps address individual snap data, for a more comprehensive approach to data removal, you may need to perform a complete device wipe. In the event that you wish to completely remove all data from a device, you'll need to use the “install recovery mode”. This should not be confused with a factory reset or remodeling as these processes will not necessarily clear system configuration data. 

With install mode, all existing user and system data on the device will be removed and the device will be initialized from the system version image specified. As such, the process should be treated with care if the device is not otherwise backed up. 

In order to perform this process, a device will require an onboard system image. These can be created on the device and also updated to include the latest releases of snaps that have been installed. To create a recovery image you can use this script:

```python
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.perform_system_action("create")
```

More information on recovery modes can be found in [Ubuntu Core's documentation](https://documentation.ubuntu.com/core/explanation/recovery-modes/index.html).

To initiate this mode, you can send the following script from Landscape Client. Note that depending on the default configuration of the device’s image, it may not be accessible from Landscape once the process has completed. 

```python
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.perform_system_action("do", "install")
```

## Secure data deletion

Note these mechanisms for wiping a device delete all data using the standard system calls. If a robust, secure data removal is required then additional tools will be required. You can't currently perform these tasks directly from Landscape without such tools. 
