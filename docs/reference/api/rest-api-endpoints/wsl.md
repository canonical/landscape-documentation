(reference-rest-api-wsl)=

# WSL

```{note}
WSL features are in beta testing. The API endpoints below may not be available to all accounts.
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
curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu-24.04"}'

curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu-24.04", "data_id": "data-id", "token": "vault-token"}'

curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d "{\"computer_name\": \"Ubuntu-24.04\", \"cloud_init\": \"$(base64 --wrap=0 < ~/cloud_init.yaml)\"}"
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
curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Custom-WSL-Image", "cloud_init": "<b64 encoded cloud_init file contents>", "rootfs_url": "https://example.com/custom_wsl_image.tar.gz"}'
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

- `query`: A query string with tokens used to filter the returned result objects.
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
