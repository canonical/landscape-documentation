(reference-rest-api-wsl)=
# WSL

## GET `/child-instance-profiles`

Gets a list of child instance profiles.

Required parameters:

- none

Optional parameters:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET https://your-landscape.domain.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT"
```

Example output:

```text
{
    "count": 1,
    "results": [
        {
        "id": 2,
        "name": "stock-ubuntu-2404",
        "title": "Stock Ubuntu 24.04",
        "instance_type": "WSL",
        "description": "The image from the store",
        "image_name": "Ubuntu-24.04",
        "image_source": null,
        "cloud_init_contents": null,
        "cloud_init_secret_name": null,
        "tags": [
            "windows_desktops",
            "windows_laptops"
        ],
        "all_computers": false,
        "access_group": "global",
        "computers": {
          "constrained": [2, 3, 4, 5],
          "non-compliant": [3, 5],
          "pending": [4]
        }
      }
    ],
    "next": null,
    "previous": null
}
```

## POST `/child-instance-profiles`

Creates a child instance profile.

Required parameters:

- `title`: A title for the profile.
- `description`: A human readable description for the profile.
- `image_name`: The name of the WSL image to use (e.g. `Ubuntu-24.04`).

Optional parameters:

- `image_source`: The URL or file path for the rootfs image.
- `cloud_init_contents`: The base64-encoded cloud init file contents.
- `access_group`: Optional name of the access group to create the profile under; defaults to Global Access.
- `tags`: A comma separated string of tag names to associate with the profile.
- `all_computers`: If true, this profile will be associated with all computers; defaults to false.

Example requests:

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d '{"title": "Stock Ubuntu 24.04", "description": "The image from the store", "image_name": "Ubuntu-24.04", "tags": "windows_laptops,windows_desktops"}'

curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d "{\"title\": \"Customized Ubuntu 24.04\", \"description\": \"The image from the store customized\", \"image_name\": \"Ubuntu-24.04\", \"cloud_init\": \"$(base64 --wrap=0 < cloud_init.yaml)\"}"

curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d '{"title": "Custom Rootfs Image", "description": "My custom image", "image_name": "CustomUbuntu", "image_source": "https://example.com/myimage.tar.gz"}'
```

Example output:

```text
{
    "id": 2,
    "name": "customized-ubuntu-2404",
    "title": "Customized Ubuntu 24.04",
    "instance_type": "WSL",
    "description": "The image from the store customized",
    "image_name": "Ubuntu-24.04",
    "image_source": null,
    "cloud_init_contents": "********",
    "cloud_init_secret_name": null,
    "tags": [
        "windows_desktops",
        "windows_laptops"
    ],
    "all_computers": false,
    "access_group": "global",
    "computers": {
      "constrained": [2, 3, 4, 5],
      "non-compliant": [],
      "pending": [2, 3, 4, 5]
    }
}
```

## DELETE `/child-instance-profiles/<str:profile_name>`

Delete the specified child instance profile.

Required parameters:

- none

Optional parameters:

- none

Example request:

```bash
curl -X DELETE https://your-landscape.domain.com/api/v2/child-instance-profiles/stock-ubuntu-2404 -H "Authorization: Bearer $JWT"
```

Example output:

Empty response.

## GET `/child-instance-profiles/<str:profile_name>`

Get details of the specified child instance profile.

Required parameters:

- none

Optional parameters:

- none

Example request:

```bash
curl -X GET https://your-landscape.domain.com/api/v2/child-instance-profiles/stock-ubuntu-2404 -H "Authorization: Bearer $JWT"
```

Example output:

```text
{
  "id": 2,
  "name": "stock-ubuntu-2404",
  "title": "Stock Ubuntu 24.04",
  "instance_type": "WSL",
  "description": "The image from the store",
  "image_name": "Ubuntu-24.04",
  "image_source": null,
  "cloud_init_contents": null,
  "cloud_init_secret_name": null,
  "tags": [
    "windows_desktops",
    "windows_laptops"
  ],
  "all_computers": false,
  "access_group": "global",
  "computers": {
    "constrained": [2, 3, 4, 5],
    "non-compliant": [3, 5],
    "pending": [4]
  }
}
```

## PATCH `/child-instance-profiles/<str:profile_name>`

Edit a child instance profile.

Required parameters:

- None.

Optional parameters:

- `title`: A title for the profile.
- `description`: A human readable description for the profile.
- `access_group`: Name of the access group for the profile under.
- `tags`: A comma separated string of tag names to associate with the profile.
- `all_computers`: Whether or not to associate this profile with all computers.

Example requests:

```bash
curl -X PATCH https://your-landscape.domain.com/api/v2/child-instance-profiles/stock-ubuntu-2404 -H "Authorization: Bearer $JWT" -d '{"description": "The stock image from the store", "tags": "windows_laptops"}'
```

Example output:

```text
{
  "id": 2,
  "name": "stock-ubuntu-2404",
  "title": "Stock Ubuntu 24.04",
  "instance_type": "WSL",
  "description": "The stock image from the store",
  "image_name": "Ubuntu-24.04",
  "image_source": null,
  "cloud_init_contents": null,
  "cloud_init_secret_name": null,
  "tags": [
    "windows_laptops"
  ],
  "all_computers": false,
  "access_group": "global",
  "computers": {
    "constrained": [2, 3, 4, 5],
    "non-compliant": [3, 5],
    "pending": [4]
  }
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
curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu-24.04"}'

curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu-24.04", "data_id": "data-id", "token": "vault-token"}'

curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d "{\"computer_name\": \"Ubuntu-24.04\", \"cloud_init\": \"$(base64 --wrap=0 < ~/cloud_init.yaml)\"}"
```

Example output:
```text
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
```text
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

## GET `/wsl-instance-names`

Gets a listing of valid WSL image names.

Required parameters:

- None

Optional parameters:

- None

Example request:

```bash
curl -X GET -H "Authorization: Bearer $JWT" "https://landscape.canonical.com/api/v2/wsl-instance-names"
```

Example output:
```bash
[
  {
	"name": "Ubuntu",
	"label": "Ubuntu"
  },
  {
	"name": "Ubuntu-22.04",
	"label": "Ubuntu 22.04"
  }
]
```

