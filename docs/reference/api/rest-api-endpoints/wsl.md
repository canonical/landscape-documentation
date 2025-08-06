(reference-rest-api-wsl)=

# WSL

```{note}
WSL features are in beta testing. The API endpoints below may not be available to all accounts.
```

To enable WSL features in self-hosted Landscape, add:

```bash
[features]
enable-wsl-child-instance-profiles = true
```

to the `service.conf` file.

## GET `/computers/<int:computer_id>/children`

Get information about the WSL instances associated with the computer.

Path parameters:

- `computer_id`: The ID assigned to a specific computer.

Query parameters:

- None

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/computers/23/children" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "children": [
      {
          "name": "WSL instance created via WSL profile, installed, registered",
          "computer_id": 5,
          "version_id": "Ubuntu 22.04",
          "compliance": "compliant",
          "profile": "WSL Profile 1",
          "is_running": true,
          "installed": true,
          "registered": true,
          "default": true,
      },
      {
          "name": "WSL instance associated with profile, not installed, installation in progress",
          "computer_id": null,
          "version_id": "Ubuntu 22.04",
          "compliance": "pending",
          "profile": "WSL Profile 2",
          "is_running": false,
          "installed": false,
          "registered": false,
          "default": null
      },
      {
          "name": "WSL instance associated with profile, installed, registration in progress",
          "computer_id": null,
          "version_id": "Ubuntu 22.04",
          "compliance": "unregistered",
          "profile": "WSL Profile 3",
          "is_running": false,
          "installed": true,
          "registered": false,
          "default": null
      },
      {
          "name": "WSL instance associated with profile, not installed, installation not in progress",
          "computer_id": null,
          "version_id": "Ubuntu 22.04",
          "compliance": "uninstalled",
          "profile": "WSL Profile 4",
          "is_running": false,
          "installed": false,
          "registered": false,
          "default": null
      },
      {
          "name": "WSL instance not created via Landscape, not conflicting with any profile",
          "computer_id": null,
          "version_id": "Ubuntu 22.04",
          "compliance": "compliant",
          "profile": null,
          "is_running": false,
          "installed": true,
          "registered": false,
          "default": false
      },
      {
          "name": "WSL instance not created via Landscape, conflicting with a profile",
          "computer_id": null,
          "version_id": "Ubuntu 22.04",
          "compliance": "noncompliant",
          "profile": "WSL Profile 2",
          "is_running": false,
          "installed": true,
          "registered": false,
          "default": false
      },
      {
          "name": "WSL instance created via Landscape without a WSL profile, registered, not conflicting with any profile",
          "computer_id": 6,
          "version_id": "Ubuntu 22.04",
          "compliance": "compliant",
          "profile": null,
          "is_running": false,
          "installed": true,
          "registered": true,
          "default": false
      },
      {
          "name": "WSL instance created via Landscape without a WSL profile, registered, conflicting with any profile",
          "computer_id": 7,
          "version_id": "Ubuntu 22.04",
          "compliance": "noncompliant",
          "profile": "WSL Profile 1",
          "is_running": false,
          "installed": true,
          "registered": true,
          "default": false
      }
  ]
}
```

## POST `/computers/<computer_id>/children`

Creates an activity to install a WSL instance on a Windows host. The WSL instance will be managed in Landscape.

Required parameters:

- `computer_name`

Optional parameters:

- `cloud_init`
- `data_id`
- `token`
- `rootfs_url`

Example requests:

```bash
curl -X POST https://landscape.canonical.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu-24.04"}'

curl -X POST https://landscape.canonical.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu-24.04", "data_id": "data-id", "token": "vault-token"}'

curl -X POST https://landscape.canonical.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d "{\"computer_name\": \"Ubuntu-24.04\", \"cloud_init\": \"$(base64 --wrap=0 < ~/cloud_init.yaml)\"}"
```

Example output:

```json
{
  "id": 118,
  "creation_time": "2024-08-05T16:38:52Z",
  "creator": {
    "name": "John Smith",
    "email": "john@example.com",
    "id": 1
  },
  "type": "ActivityGroup",
  "summary": "Create instance Ubuntu-24.04",
  "completion_time": null,
  "parent_id": null,
  "deliver_delay_window": 0,
  "result_text": null,
  "result_code": null,
  "activity_status": "delivered"
}
```

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Custom-WSL-Image", "cloud_init": "<b64 encoded cloud_init file contents>", "rootfs_url": "https://example.com/custom_wsl_image.tar.gz"}'
```

Example output:

```json
{
  "id": 118,
  "creation_time": "2024-08-05T16:38:52Z",
  "creator": {
    "name": "John Smith",
    "email": "john@example.com",
    "id": 1
  },
  "type": "ActivityGroup",
  "summary": "Create instance Custom-WSL-Image",
  "completion_time": null,
  "parent_id": null,
  "deliver_delay_window": 0,
  "result_text": null,
  "result_code": null,
  "activity_status": "delivered"
}
```

Notes:

1. Sending both `cloud_init` and `data_id` will produce a 400 response.
1. If `rootfs_url` is specified, then a 400 response is returned if the computer name matches any of the following case-insensitive patterns: `Ubuntu`, `Ubuntu-Preview`, `Ubuntu-XY.ZW`.

## POST `/computers/<computer_id>/delete-children`

Create activities to remove the specified child instances from the host.

Required parameters:

- `child_names`: A list of names of the child instances to remove.

Optional parameters:

- None

Example request:

```bash
curl -X POST -H "Authorization: Bearer $JWT" "https://landscape.canonical.com/api/v2/computers/6/delete-children" -d '{"computer_names": ["child_one", "child_two"]}'
```

Example output:

```json
{
  "id": 115,
  "deliver_delay_window": 0,
  "summary": "Deleting child computer(s)",
  "type": "ActivityGroup",
  "creator": {
    "name": "John Smith",
    "email": "john@example.com",
    "id": 1
  },
  "activity_status": "undelivered",
  "parent_id": null,
  "creation_time": "2025-06-10T22:29:22Z",
  "approval_time": null,
  "completion_time": null,
  "result_text": null,
  "result_code": null
}
```

## GET `/computers/wsl-hosts`

Gets a list of Windows computers that host at least one WSL instance that is registered in Landscape.

Required parameters:

- None

Optional parameters:

- `query`: A query string with tokens used to filter the returned result objects. See {ref}`reference-rest-api-computers` for details.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET -H "Authorization: Bearer $JWT" "https://landscape.canonical.com/api/v2/computers/wsl-hosts"
```

Example output:

```json
{
  "count": 1,
  "results": [
    {
      "id": 6,
      "title": "Noel's Windows Laptop",
      "comment": "",
      "hostname": "noel",
      "total_memory": 1024,
      "total_swap": 1024,
      "reboot_required_flag": false,
      "update_manager_prompt": "normal",
      "clone_id": null,
      "secrets_name": null,
      "last_exchange_time": null,
      "last_ping_time": "2025-06-10T22:00:30Z",
      "tags": [
        "laptop",
        "windows"
      ],
      "access_group": "server",
      "distribution": "10 / 11",
      "distribution_info": {
        "description": "Windows 10 / Windows 11",
        "distributor": "Microsoft",
        "release": "10 / 11",
        "code_name": "windows"
      },
      "cloud_instance_metadata": {},
      "vm_info": null,
      "container_info": null,
      "default_child": null,
      "ubuntu_pro_info": null,
      "livepatch_info": null,
      "ubuntu_pro_reboot_required_info": null,
      "num_child": 2,
      "cloud_init": {},
      "archived": false,
      "employee_id": null,
      "is_wsl_instance": false,
      "children": [
        {
          "id": 7,
          "title": "Bionic WSL",
          "comment": "",
          "hostname": "bionic-wsl",
          "total_memory": 1024,
          "total_swap": 1024,
          "reboot_required_flag": false,
          "update_manager_prompt": "normal",
          "clone_id": null,
          "secrets_name": null,
          "last_exchange_time": null,
          "last_ping_time": "2025-06-10T21:59:30Z",
          "tags": [
            "bionic",
            "wsl"
          ],
          "access_group": "global",
          "distribution": "18.04",
          "distribution_info": {
            "description": "Ubuntu 18.04 LTS",
            "distributor": "Ubuntu",
            "release": "18.04",
            "code_name": "bionic"
          },
          "cloud_instance_metadata": {},
          "vm_info": null,
          "container_info": null,
          "default_child": null,
          "ubuntu_pro_info": null,
          "livepatch_info": null,
          "ubuntu_pro_reboot_required_info": null,
          "num_child": 0,
          "cloud_init": {},
          "archived": false,
          "employee_id": null,
          "is_wsl_instance": true,
          "is_default_child": null
        },
        {
          "id": 8,
          "title": "Focal WSL",
          "comment": "",
          "hostname": "focal-wsl",
          "total_memory": 1024,
          "total_swap": 1024,
          "reboot_required_flag": false,
          "update_manager_prompt": "normal",
          "clone_id": null,
          "secrets_name": null,
          "last_exchange_time": null,
          "last_ping_time": "2025-06-10T21:58:30Z",
          "tags": [
            "focal",
            "wsl"
          ],
          "access_group": "global",
          "distribution": "20.04",
          "distribution_info": {
            "description": "Ubuntu 20.04 LTS",
            "distributor": "Ubuntu",
            "release": "20.04",
            "code_name": "focal"
          },
          "cloud_instance_metadata": {},
          "vm_info": null,
          "container_info": null,
          "default_child": null,
          "ubuntu_pro_info": null,
          "livepatch_info": null,
          "ubuntu_pro_reboot_required_info": null,
          "num_child": 0,
          "cloud_init": {},
          "archived": false,
          "employee_id": null,
          "is_wsl_instance": true,
          "is_default_child": null
        }
      ],
      "is_default_child": null,
      "parent": null
    }
  ],
  "next": null,
  "previous": null
}
```

## GET `/wsl-feature-limits`

Get the limits for WSL related features for the account.

Path parameters:

- None

Required parameters:

- None

Optional parameters:

- None

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/wsl-feature-limits -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "max_windows_host_machines": 1000,
  "max_wsl_child_instances_per_host": 10,
  "max_wsl_child_instance_profiles": 100
}
```

## GET `/wsl-instance-names`

Gets a listing of image names for the official Ubuntu WSL images available in the Windows Store.

Required parameters:

- None

Optional parameters:

- None

Example request:

```bash
curl -X GET -H "Authorization: Bearer $JWT" "https://landscape.canonical.com/api/v2/wsl-instance-names"
```

Example output:

```json
[
  {
    "name": "Ubuntu",
    "label": "Ubuntu"
  },
  {
    "name": "Ubuntu-22.04",
    "label": "Ubuntu 22.04 LTS"
  },
  {
    "name": "Ubuntu-24.04",
    "label": "Ubuntu 24.04 LTS"
  }
]
```
