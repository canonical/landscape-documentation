---
myst:
  html_meta:
    description: "API reference for WSL management. Legacy API endpoints to create, configure, and manage Windows Subsystem for Linux instances in Landscape."
---

(reference-legacy-api-wsl)=
# WSL

The methods available here are for managing Windows Subsystem for Linux (WSL) clients registered with Landscape.

```{note}
WSL features are available starting in Landscape 25.10.
```

To enable WSL features in self-hosted Landscape, add:

```ini
[features]
wsl_management = true
```

to the `service.conf` file.

## CreateChildComputer

Create child computer instances on a parent host machine.

Required arguments:

- `parent_id`: The ID of the parent computer.
- `computer_name`: The name of the child computer to create.

Optional arguments:

- `cloud_init`: The b64 encoded cloud-init file contents.

If `cloud_init` is provided, the new instance will be created according to the cloud-init file specified.

Example calls:

```bash
?action=CreateChildComputer&parent_id=20&computer_name=Ubuntu
```

```bash
?action=CreateChildComputer&parent_id=20&computer_name=Ubuntu&cloud_init=<b64 encoded cloud_init file>
```

Example response:

```json
{
    "activity_status": "delivered",
    "completion_time": null,
    "creation_time": "2023-10-25T18:55:42Z",
    "creator": {
        "email": "john@example.com",
        "id": 1,
        "name": "John Smith"
    },
    "deliver_delay_window": 0,
    "id": 114,
    "parent_id": null,
    "result_code": null,
    "result_text": null,
    "summary": "Create instance Ubuntu",
    "type": "ActivityGroup"
}
```

(reference-legacy-api-wsl-delete-child-computer)=
## DeleteChildComputers

Delete a list of child computers by ID.

Required argument:

- `computer_id`: A list of child computer IDs to delete.

Example calls:

```bash
?action=DeleteChildComputers&computer_id.1=21
```

```bash
?action=DeleteChildComputers&computer_id.1=21&computer_id.2=22
```

Example outputs:

```json
{
    "activity_status": "delivered",
    "completion_time": null,
    "creation_time": "2023-10-25T19:08:38Z",
    "creator": {
        "email": "john@example.com",
        "id": 1,
        "name": "John Smith"
    },
    "deliver_delay_window": 0,
    "id": 131,
    "parent_id": null,
    "result_code": null,
    "result_text": null,
    "summary": "Delete instance Ubuntu",
    "type": "ActivityGroup"
}
```

```json
{
    "activity_status": "delivered",
    "completion_time": null,
    "creation_time": "2023-10-25T19:08:52Z",
    "creator": {
        "email": "john@example.com",
        "id": 1,
        "name": "John Smith"
    },
    "deliver_delay_window": 0,
    "id": 133,
    "parent_id": null,
    "result_code": null,
    "result_text": null,
    "summary": "Deleting child computer(s)",
    "type": "ActivityGroup"
}
```

## GetWSLHosts

Gets a list of Windows computers that host at least one WSL instance that is registered in Landscape.

Optional arguments:

- `query`: A query string with tokens used to filter the returned result objects.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

This method doesn't return a list of WSL instances or WSL hosts that don't have a child WSL instance registered in Landscape. If you want to view those computers, you can use the `GetComputers` method from {ref}`reference-legacy-api-computers`, or visit {ref}`how to view WSL host machines and child computers in the Landscape web portal <howto-heading-wsl-view-computers>`.

Example calls:

```bash
?action=GetWSLHosts
```

```bash
?action=GetWSLHosts&limit=10
```

```bash
?action=GetWSLHosts&offset=30
```

```bash
?action=GetWSLHosts&limit=10&offset=30
```

```bash
?action=GetWSLHosts&query=title:Machine12345
```

Example outputs:

```json
[
    {
        "access_group": "server",
        "clone_id": null,
        "cloud_instance_metadata": {},
        "comment": "",
        "container_info": null,
        "distribution": "10 / 11",
        "hostname": "noel",
        "id": 6,
        "last_exchange_time": null,
        "last_ping_time": "2023-10-25T18:45:37Z",
        "reboot_required_flag": false,
        "tags": [
            "laptop",
            "windows"
        ],
        "title": "Noel's Windows Laptop",
        "total_memory": 1024,
        "total_swap": 1024,
        "update_manager_prompt": "normal",
        "vm_info": null
    },
    {
        "access_group": "desktop",
        "clone_id": null,
        "cloud_instance_metadata": {},
        "comment": "",
        "container_info": null,
        "distribution": "10 / 11",
        "hostname": "Machine12345",
        "id": 20,
        "last_exchange_time": "2023-10-25T18:54:26Z",
        "last_ping_time": "2023-10-25T20:21:43Z",
        "reboot_required_flag": false,
        "tags": [],
        "title": "Machine12345",
        "total_memory": null,
        "total_swap": null,
        "update_manager_prompt": "normal",
        "vm_info": null
    }
]
```

```json
[
    {
        "access_group": "desktop",
        "clone_id": null,
        "cloud_instance_metadata": {},
        "comment": "",
        "container_info": null,
        "distribution": "10 / 11",
        "hostname": "Machine12345",
        "id": 20,
        "last_exchange_time": "2023-10-25T18:54:26Z",
        "last_ping_time": "2023-10-25T20:22:30Z",
        "reboot_required_flag": false,
        "tags": [],
        "title": "Machine12345",
        "total_memory": null,
        "total_swap": null,
        "update_manager_prompt": "normal",
        "vm_info": null
    }
]
```

(reference-legacy-api-wsl-set-default-child-computer)=
## SetDefaultChildComputer

Set the child computer instance with the provided ID as the default instance for the host parent. This is the default instance you log into if you run `wsl` in PowerShell from the Windows host.

Required arguments:

- `parent_id`: The ID of the parent host computer.
- `child_id`: The ID of the child computer to set as default.

Example call:

```bash
?action=SetDefaultChildComputer&parent_id=30&child_id=32
```

Example response:

```json
{
    "activity_status": "delivered",
    "completion_time": null,
    "creation_time": "2023-10-25T19:04:45Z",
    "creator": {
        "email": "john@example.com",
        "id": 1,
        "name": "John Smith"
    },
    "deliver_delay_window": 0,
    "id": 124,
    "parent_id": null,
    "result_code": null,
    "result_text": null,
    "summary": "Set instance Ubuntu as default",
    "type": "ActivityGroup"
}
```
