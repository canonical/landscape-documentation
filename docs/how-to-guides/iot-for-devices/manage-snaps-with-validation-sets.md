(howto-manage-snaps-with-validation-sets)=
# How to manage snaps in Landscape with validation sets

Managing software updates for a large fleet of IoT devices presents significant challenges, especially for organizations using their own [Dedicated Snap Stores](https://documentation.ubuntu.com/dedicated-snap-store/). While individual device snap updates can be managed manually in Landscape's web portal or via scripting interfaces, a more robust and scalable solution is often required. You can use validation sets to manage snaps for large fleets.

## Background information

**Validation sets** offer a powerful way to control, enforce and standardize the snap environment on your device across an entire fleet. These sets enable precise control over which snaps are installed, which are blocked, and even specific revisions that must be present. Key benefits of using validation sets include:

* **Controlled snap environments:** Define exactly which snaps and their revisions are permitted on devices.
* **Seamless transitions:** Sequence updates to ensure smooth, automated transitions between defined states, with SnapD managing the conformity process.
* **Preventing undesired changes:** Automatically block any changes to snaps that violate the rules established in the applied validation sets, especially for snaps from other publishers (e.g. Canonical, community, etc.).

While validation sets enforce conformity, the automatic removal of snaps as part of a validation set update is not handled by SnapD and must be performed separately.

Working with validation sets involves two primary stages: their creation and editing are handled via your Snap Store, while their application and enforcement across devices can be managed through Landscape.

## Create a validation set

Validation sets belong to the account listed in the assertion that owns the key used to sign it. This could be a Brand account or an individual developer account. 

To create and sign a validation set, follow the steps in [Snapcraft's documentation on managing validation sets](https://snapcraft.io/docs/manage-validation-sets).

Having created your validation set in the store, you can apply it to a device (or fleet of devices) from Landscape.

```{note}
Validation set functionality is currently not supported when using an Enterprise store in a non-proxy mode. 
```

## Apply a validation set to a device

With your validation set in your store, you can apply it to a device using a script that leverages the [`snap_http` library](https://github.com/canonical/snap-http) included with Landscape to interact directly with SnapD. You have the option to either monitor the device’s state, allowing you to determine if, in fact, the device conforms to the requirements of a validation set, or enforce it in which any attempt to break compliance with the set will be rejected by SnapD. 

For more information on validation sets, see [Snapcraft's documentation](https://snapcraft.io/docs/manage-validation-sets).

## Check device state against a validation set

You can find out what validation sets are enabled on a device using:

```bash
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.get_validation_sets()
```

Next, you may want to determine if the device is already in a conformant state for a given validation set. The following script will return a result that includes whether the set is “valid” - meaning the device meets the requirements of the set.

```bash
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.monitor_validation_sets("<ACCOUNT_ID>", "<VALIDATION_SET_NAME>")
```

## Enforce validation set across your fleet

It's recommended that you try to enforce a validation set when a device is first being imaged - then increment the validation set sequence number to change the state. You can do this by specifying a list of validation sets in your model assertion when building your custom image. More information on this process can be found in [Ubuntu Core's documentation](https://documentation.ubuntu.com/core/reference/assertions/model/).

Applying a validation state to an existing device may require you to manually ensure conformity before enforcement can be enabled. This could involve manually installing or removing snaps to match the validation set's requirements.

However, if you have a device and you have ensured it's already compliant with the validation set as described in the previous section, you can tell that device to enforce that validation set going forward. This ensures that it will remain in compliance.

```bash
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.enforce_validation_set("<ACCOUNT_ID>", "<VALIDATION_SET_NAME>", <VALIDATION_SET_SEQUENCE>)
```

The validation set sequence parameter is optional. Specifying it will pin the device to that sequence. If this is omitted, the device will update to the latest sequence when they are made available. 

You can change the sequence you're pinned to by re-applying the command with the new sequence number. 

## Update the validation set on a new snap release

After you've enforced your validation set across your fleet of devices, you now have a new release of a snap that you want to upgrade your fleet to. If you haven't specified a specific revision in your validation sets, a simple refresh of the snap will update the device to the latest version. 

If, however, you've specified the revision - you'll need to update the validation set in your store. 

Editing a validation set is exactly the same sequence as creating a new one, but in this instance, Snapcraft will present you with the existing validation set for you to edit. 

In the spawned text editor, perform the following tasks:

* Increment the validation set sequence number
* Update the snap revision for the snaps you want to update.

On saving and exiting the text editor, Snapcraft will sign and upload the updated validation set to your store. 

**Note**: Ensuring sensible incrementation of sequence number of your validation set is strongly recommended because it allows for much cleaner and easier roll backs to previous device states in the event an attempted refresh to a new sequence fails.

## Refresh a validation set 

When snapd performs a refresh, any validation sets which have not been pinned to a specific sequence are updated before any snap updates are attempted. This is actually standard snapd behavior during refresh; assertions are updated before snaps.

This process occurs automatically if the refresh timer is still enabled, although it's advised that this timer is disabled on Ubuntu Core to allow specific control over update scheduling. If the device is in “managed mode”, which disables the automatic refresh, it'll be necessary to tell your devices to refresh. 

You can do this with the following script: 

```bash
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.refresh_validation_set("<ACCOUNT_ID>", "<VALIDATION_SET_NAME>", <VALIDATION_SET_SEQUENCE>)
```

The sequence parameter is optional. If omitted, the device will update to the latest sequence, otherwise the device will be pinned to the specified sequence going forward.  

This script will download the latest revision of the validation set and attempt to update the device to remain in compliance. However, this command will not attempt to remove any snaps. Accordingly, if you change a snap from being *required* to *invalid*, the process will fail as the command does not have the authority to uninstall a snap.

In order to remove a snap completely from a device you would need to update the validation set to remove the enforcement of its installation before then manually attempting to uninstall the snap.

```bash
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.forget_validation_set("<ACCOUNT_ID>","<VALIDATION_SET_NAME>")
snap_http.remove("<SNAP_NAME>")
snap_http.refresh_validation_set("<ACCOUNT_ID>","<VALIDATION_SET_NAME>", <VALIDATION_SET_SEQUENCE>)
```

## Remove a validation set 

All validation sets on a device that have not been specifically defined in your model assertion, or have been defined with the “prefer-enforce” setting, may be forgotten if the snap restrictions are no longer required. Forgetting a validation set will remove all restrictions on installing, updating, or removing snaps that were previously enforced by that validation.

To remove a validation set from a device, use the following script:

```bash
#!/usr/bin/env python3

from landscape.client import snap_http

snap_http.forget_validation_set("<ACCOUNT_ID>","<VALIDATION_SET_NAME>")
```

```{important}
As the device will likely remain in managed mode, removing the validation set alone will not result in any immediate changes to installed snaps. Additional manual intervention (e.g., explicitly asking the device to refresh all snaps or install/remove specific snaps) may be required to achieve the desired state.
```

## Multiple validation sets and consistency

You can apply multiple validation sets to a device if you wish to manage and control sets of snaps independently. For example, you could have a validation set for the core OS components, one for the application components and a further one for a third-party snap. 

The only restriction on multiple validation sets is that they are coherent. Trying to enforce a validation set that would conflict with an existing one will result in an error being returned.

## Summary

Validation sets give more control over the state of your devices and can be used across a fleet. As the sets are distributed by a store, all devices can access them and you can ensure they are all using the same version. 

By using multiple validation sets, you can manage any update process, using one set to update core OS components, another to update application snaps, and another to update third-party snaps. This allows for independent updates of different components without affecting others, and provided sequence numbers are incremented sensibly, can simplify rollbacks for specific parts of the system in the event of an update failure. 

With Landscape, you can instruct groups of devices to refresh their validation sets automatically when the set is updated or via the scripting interface. This means that you can update your entire fleet with one action. 
