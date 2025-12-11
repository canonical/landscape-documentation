(how-to-use-annotations-client-snap)=
# How to use annotations with the Landscape Client snap

Annotations in Landscape provide a mechanism for sending custom metadata from a client device to your Landscape server. These annotations can then be used to monitor, group and search for devices.

## Annotations file

Each annotation consists of a key-value pair. Annotations for the client snap are stored in the following directory:

```bash
/var/snap/landscape-client/common/var/lib/landscape/client/annotations.d`
```

You can also access the path from within the snap:

```bash
$SNAP_COMMON/var/lib/landscape/client/annotations.d
```

## Create an annotation

Inside this annotation folder, create a file. The file name should be the annotation key and the contents should be the annotation value(s).

Any annotations created in this folder will automatically be sent to the Landscape server and are visible in the web portal: **Computers** (Instances) > Select computer > **Info** tab.

**Note**: Updating an annotation on the client will automatically push it to the server; however, deleting a file from the folder will not delete the annotation with the last known value persisting.

## Edit annotations from a snap via the content interface

If you want to edit annotations from another snap, you can connect to the Landscape client annotations content interface. This allows you to read and write from the annotations folder.

To connect, you must first define a suitable plug in your `snapcraft.yaml` file:

```yaml
plugs:
 annotations:
   interface: content
   target: $SNAP_COMMON/annotations
```

After you've installed your snap, you'll need to connect the content interface:

```bash
snap connect <your-snap>:annotations landscape-client:annotations
```

You'll then be able to access the annotations directory from your own snap in the `$SNAP_COMMON/annotations` path. Any updates to this folder will be picked up by Landscape Client and sent to the server.

## Use annotations in the web portal

Once you've created annotations for devices, you can search for devices which either have a key or a specific value for a given key.

In the search bar, type:

```bash
annotation:<key>
```

Or

```bash
annotation:<key>:<value>
```

You can also save this search to re-use it and check for any changes.

Note that annotations and searching for keys and values are case-sensitive. Annotation search is a basic text search that doesn't consider word boundaries. For example, using the keys "attached" and "unattached" would be problematic because searching for "attached" will also return results labeled as "unattached".
