(how-to-web-portal-use-annotations)=
# How to use annotations

Annotations in Landscape provide a mechanism for sending custom metadata from a client device to your Landscape server. These annotations can then be used to monitor, group and search for devices.

The instructions provided here are specific to the Landscape Client debian package, although the information still generally applies to the snap. For information that's specific to the snap, see {ref}`how-to-use-annotations-client-snap`.

## Background information

Annotations are used to gather information from clients, and each annotation consists of a key-value pair. The key identifies the meaning or category of the information and the value is the data/information.

Annotations are similar to {ref}`reference-terms-tags`, which are also used to group clients. However, tags are a single value (not key-value pair). Tags are typically used to group clients for various purposes, such as upgrading a certain (tagged) group of machines, whereas annotations are used to store notes and information about your clients.

Annotations are configured on the Landscape client machines but can be viewed from the server.

## Annotations file

Annotations for the Landscape Client deb are stored in the following directory:

```bash
/var/lib/landscape/client/annotations.d
```

## Create an annotation

Inside the annotation folder, create a file. The file name should be the annotation key and the contents should be the annotation value(s).

Any annotations created in this folder will automatically be sent to the Landscape server and are visible in the web portal: **Computers** (**Instances**) > Select computer > **Info** tab.

Note that annotations and searching for keys and values are case-sensitive. Annotation search is a basic text search that doesn't consider word boundaries. For example, using the keys "attached" and "unattached" would be problematic because searching for "attached" will also return results labeled as "unattached".

## Use annotations in the web portal

Once you’ve created annotations for devices, you can search for devices which either have a key or a specific value for a given key.

In the search bar, type:

```bash
annotation:<key>
```

Or

```bash
annotation:<key>:<value>
```

For example:

```bash
annotation:timezone:est
```

You can also save this search to re-use it and check for any changes.

**Note**: Annotations and searching for keys and values are case-sensitive.

