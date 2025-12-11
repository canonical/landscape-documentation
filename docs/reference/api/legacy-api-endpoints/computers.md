(reference-legacy-api-computers)=
# Computers

The methods available here give the ability to retrieve computers and to do basic operations on them, such as tagging.

## GetComputers

Get a list of computers associated with the account.

- `query`: A query string with space-separated tokens used to filter the returned computers. Words provided as search parameters are treated as keywords, matching the hostname or the computer title. Selector prefixes can be used to further customize the search.
- `tag`: Search for computers with the specified tag.
- `distribution`: Search for computers running a specific Ubuntu release (can be code name like `jammy` or version number like `22.04`).
- `hostname`: Search for computers with the exact hostname.
- `title`: Search for computers with the exact title.
- `alert`: Search for computers with a named alert being active. Alerts can be one of the following: `package-upgrades`, `security-upgrades`, `package-profiles`, `package-reporter`, `computer-offline`, `computer-reboot`.
- `access-group`: Search for computers that belong to the access group with the specified name.
- `id`: Select the specified numeric computer ID.
- `mac`: Search for computers with the specified MAC address, which can be a substring of the full address.
- `ip`: Search for computers with the specified IP address, which can be a substring of the full address. No network classing is done.
- `search`: Select computers based on the result of the named search.
- `needs:reboot`: Search for computers that have the reboot required flag set. Note that with this particular criteria, the only possible value for it is the text `reboot`.
- `license-id`: Search for computers licensed to the specified `license-id`.
- `needs:license` OR `license-id:none`: Search for computers that do not have a Landscape license, and, as a result, are not managed.
- `annotation`: Search for computers which define the specified annotation key. Optionally specify `annotation:<key>:<string>` which will only return computers whose key matches and value also contains the `<string>` specified.
- `OR`: Search for computers matching term A or term B. `OR` must be in all-caps.
- `NOT`: search for computers not matching the next term. `NOT` must be in all-caps.

If values following a prefix contain spaces or non-ASCII characters, they must be in quotation marks.

These prefixes can be mixed and matched with keywords. For example, the following query would match computers with ‘appserver’ in their title or hostname, either with the tag "server" or running the "jammy" release of Ubuntu:

```text
appserver tag:server OR distribution:jammy
```

The `GetComputers` method also supports the following optional arguments:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.
- `with_network`: If true, include the details of all network devices attached to the computer.
- `with_hardware`: If true, include the details of all hardware information known.
- `with_annotations`: If true, include the details of all custom annotation information known.

For example, the following request searches for all computers with the tag "server", includes their network devices, and with a limit of 20 machines:

```text
?action=GetComputers&query=tag:server&limit=20&with_network=true
```

The method returns a JSON serialized list of computers:

```text
[{"access_group": "global",
  "comment": u"",
  "distribution": u"22.04",
  "hostname": u"a_comp.example.com",
  "id": 12345,
  "last_ping_time": None,
  "last_exchange_time": "2023-06-3017:59Z",
  "title": u"A Computer",
  "reboot_required_flag": False,
  "tags": ["server"],
  "total_memory": None,
  "total_swap": None,
  "network_devices": [{"broadcast_address": "192.168.1.255",
                       "interface": "eth0",
                       "ip_address": "192.168.1.2",
                       "mac_address": "00:1e:c9:6c:b8:de",
                       "netmask": "255.255.255.0"}]}]
```

The JSON equivalent of this output is:

```json
[
    {
        "access_group": "global",
        "comment": "",
        "distribution": "22.04",
        "hostname": "a_comp.example.com",
        "id": 12345,
        "last_ping_time": "None",
        "last_exchange_time": "2023-06-3017:59Z",
        "title": "A Computer",
        "reboot_required_flag": false,
        "tags": [
            "server"
        ],
        "total_memory": "None",
        "total_swap": "None",
        "network_devices": [
            {
                "broadcast_address": "192.168.1.255",
                "interface": "eth0",
                "ip_address": "192.168.1.2",
                "mac_address": "00:1e:c9:6c:b8:de",
                "netmask": "255.255.255.0"
            }
        ]
    }
]
```

## AddAnnotationToComputers

Add a custom annotation to a selection of computers.

Required arguments:

- `query`: A query string used to select the computers for which to add annotations. (See `query` under `GetComputers`, above, for additional details.)
- `key`: Annotation key to add to the selected computers.
- `value`: Annotation value associated with the provided key to add to the selected computers. (optional)

For example, the following request will add a custom annotation representing physical to all computers running Ubuntu 22.04 (Jammy):

```text
?action=AddAnnotationToComputers&query=distribution:22.04&key=location
    &value=BLDG3:FLR2:CAGE101A
```

## RemoveAnnotationFromComputers

Remove a custom annotation with the specified key from a selection of computers.

Required arguments:

- `query`: A query string used to select the computers to remove annotations from. (See `query` under `GetComputers`, above, for additional details.)
- `key`: The annotation key to remove.

For example, the following request removes the annotation key `location` from all computers tagged with "server":

```text
?action=RemoveAnnotationFromComputers&query=tag:server&key=location
```

## AddTagsToComputers

Add tags to a selection of computers.

Required arguments:

- `query`: A query string used to select the computers to add tags to. (See `query` under `GetComputers`, above, for additional details.)
- `tags`: Tag name to be applied, this can have more than one tag, by numbering the tags with `tags.1`, `tags.2`, `tags.3` etc.

For example, the following request will add the tags “server” and “jammy” to all computers running Ubuntu 22.04 (Jammy):

```text
?action=AddTagsToComputers&query=distribution:22.04&tags.1=server
    &tags.2=jammy
```

## RemoveTagsFromComputers

Remove tags from a selection of computers.

Required arguments:

- `query`: A query string used to select the computers to remove tags from. (See `query` under `GetComputers`, above, for additional details.)
- `tags`: Tag name to be remove, this can have more than one Tag, by numbering the tags with `tags.1`, `tags.2`, `tags.3` etc.

For example, the following request removes the tags “server” and “jammy” from all computers with tag server:

```text
?action=RemoveTagsFromComputers&query=tag:server&tags.1=server
    &tags.2=jammy
```

## ChangeComputersAccessGroup

Change the access group for a selection of computers.

Required arguments:

- `query`: A query string used to select the computers to change access group for. (See `query` under `GetComputers`, above, for additional details.)
- `access_group`: The name of the access group to assign selected computers to.

This is an example of a valid request:

```text
action=ChangeComputersAccessGroup&query=tag:new-servers
    &access_group=server
```

The method returns a JSON serialized list of computers in the selection which have successfully changed access group:

```text
[{"access_group": "server",
  "id": 12345,
  "title": u"A Computer",
  "comment": u"",
  "total_memory": None,
  "total_swap": None,
  "reboot_required_flag": False,
  "hostname": u"a_comp.example.com",
  "last_ping_time": None,
  "last_exchange_time": "2011-06-3017:59Z",
  "tags": ["server"],
  "network_devices": [{"broadcast_address": "192.168.1.255",
                       "interface": "eth0",
                       "ip_address": "192.168.1.2",
                       "mac_address": "00:1e:c9:6c:b8:de",
                       "netmask": "255.255.255.0"}]}]
```

The JSON equivalent of this output is:

```json
[
    {
        "access_group": "server",
        "id": 12345,
        "title": "A Computer",
        "comment": "",
        "total_memory": "None",
        "total_swap": "None",
        "reboot_required_flag": false,
        "hostname": "a_comp.example.com",
        "last_ping_time": "None",
        "last_exchange_time": "2011-06-3017:59Z",
        "tags": [
            "server"
        ],
        "network_devices": [
            {
                "broadcast_address": "192.168.1.255",
                "interface": "eth0",
                "ip_address": "192.168.1.2",
                "mac_address": "00:1e:c9:6c:b8:de",
                "netmask": "255.255.255.0"
            }
        ]
    }
]
```

The following errors may be raised:

- `InvalidQueryError`: If query format is invalid.

## RemoveComputers

Remove a list of computers by ID.

Required argument:

- `computer_ids`: A list of computer IDs to remove.

This is an example of a valid HTTP request:

```text
?action=RemoveComputers&computer_ids.1=30&computer_ids.2=43
```

The equivalent CLI command is:

```bash
landscape-api remove-computers 30,43
```

## GetPendingComputers

Get a list of pending computers associated with the account used for authentication:

```text
?action=GetPendingComputers
```

The method returns a JSON serialized list of pending computers:

```json
[
    {
        "id": 12345,
        "title": "My Server",
        "hostname": "server.london.company.com",
        "creation_time": "2011-06-3017:59Z",
        "vm_info": "xen",
        "client_tags": "['london'], ['server']"
    }
]
```

## AcceptPendingComputers

Accept a list of pending computers associated with the account used for authentication.

This method takes the following arguments:

- `computer_ids`: A list of pending computer IDs to accept.
- `access_group`: The name of the access group to accept the computers to. If not provided, they will be put into the global access group. (optional)

This is an example of a valid HTTP request:

```text
?action=AcceptPendingComputers?computer_ids.1=1&computer_ids.2=2
```

The equivalent CLI command is:

```bash
landscape-api accept-pending-computers 1,2
```

The method returns a JSON serialized list of accepted computers:

```text
[{"id": 12345,
  "title": u"A Computer",
  "comment": u"",
  "hostname": u"a_comp.example.com",
  "last_exchange_time": "2011-06-3017:59Z"}]
```

The JSON equivalent of this output is:

```json
[
    {
        "id": 12345,
        "title": "A Computer",
        "comment": "",
        "hostname": "a_comp.example.com",
        "last_exchange_time": "2011-06-3017:59Z"
    }
]
```

To replace existing computers, map the pending IDs to the existing ones. For example, via HTTP request:

```text
?action=AcceptPendingComputers?computer_ids.1=1&computer_ids.2=2
    &existing_ids.2=3
```

The equivalent CLI command is:

```bash
landscape-api accept-pending-computers --existing-ids 1=1,2=2
```

The following errors may be raised:

- `InsufficientLicenses`: Insufficient licenses available to accept new computers.
- `UnknownComputer`: The provided computers are not known or have been already accepted or rejected.
- `UnknownAccessGroup`: The access group is not known or the person is not authorized to accept pending computers into the access group.

## RejectPendingComputers

Reject a list of pending computers associated with the account used for authentication.

This is an example of a valid HTTP request:

```text
?action=RejectPendingComputers?computer_ids.1=1&computer_ids.2=2
```

The equivalent CLI command is:

```bash
landscape-api reject-pending-computers 1,2
```

## CreateCloudOtps

```{warning}
CreateCloudOtps is no longer available from Landscape Server 25.04 onwards
```

Create one-time passwords used for registration of cloud instances:

```text
?action=CreateCloudOtps?count=3
```

The method returns a JSON serialized list of one-time passwords, one for each requested:

```json
["otp1", "otp2", "otp3"]
```

You can then use those OTPs in the client configuration, using cloud-init for example.

## RebootComputers

Reboot a list of computers.

Required argument:

- `computer_ids`: A list of computer IDs to reboot.

Optional argument:

- `deliver_after`: Reboot the computer after the specified time. The time format is `YYYY-MM-DDTHH:MM:SSZ`.

This is an example of a valid HTTP request:

```text
?action=RebootComputers&computer_ids.1=30&computer_ids.2=43
```

The equivalent CLI command is:

```bash
landscape-api reboot-computers 30,43
```

The method returns a JSON serialized activity:

```text
{u'computer_id': None,
 u'creation_time': u'2012-11-19T18:11:51Z',
 u'creator': {u'email': u'john@example.com', u'id': 3,
              u'name': u'John Smith'},
 u'id': 141,
 u'parent_id': None,
 u'summary': u'Restart computer',
 u'type': u'ActivityGroup'}
```

The JSON equivalent of this output is:

```json
{
    "computer_id": "None",
    "creation_time": "2012-11-19T18:11:51Z",
    "creator": {
        "email": "john@example.com",
        "id": 3,
        "name": "John Smith"
    },
    "id": 141,
    "parent_id": "None",
    "summary": "Restart computer",
    "type": "ActivityGroup"
}
```

## ShutdownComputers

Shut down a list of computers.

Required argument:

- `computer_ids`: A list of computer IDs to shut down.

Optional argument:

- `deliver_after`: Shutdown the computer after the specified time. The time format is `YYYY-MM-DDTHH:MM:SSZ`.

This is an example of a valid HTTP request:

```text
?action=ShutdownComputers&computer_ids.1=30&computer_ids.2=43
```

The equivalent CLI command is:

```bash
landscape-api shutdown-computers 30,43
```

The method returns a JSON serialized activity:

```text
{u'computer_id': None,
 u'creation_time': u'2012-11-19T18:14:19Z',
 u'creator': {u'email': u'john@example.com', u'id': 3,
              u'name': u'John Smith'},
 u'id': 147,
 u'parent_id': None,
 u'summary': u'Shutdown computer',
 u'type': u'ActivityGroup'}
```

The JSON equivalent of this output is:

```json
{
    "computer_id": "None",
    "creation_time": "2012-11-19T18:14:19Z",
    "creator": {
        "email": "john@example.com",
        "id": 3,
        "name": "John Smith"
    },
    "id": 147,
    "parent_id": "None",
    "summary": "Shutdown computer",
    "type": "ActivityGroup"
}
```

## RenameComputers

Rename a set of computers.

Required argument:

- `computer_titles`: A mapping of computer IDs to titles to set.

This is an example of a valid request:

```text
?action=RenameComputers&computer_titles.30:newname
```
