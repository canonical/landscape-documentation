(reference-rest-api-child-instance-profiles)=

# Child Instance Profiles

```{note}
Child Instance Profiles are in beta testing. The API endpoints below may not be available to all accounts.
```

To enable WSL features in self-hosted Landscape, add:

```bash
[features]
enable-wsl-child-instance-profiles = true
```

to the `service.conf` file.

## GET `/child-instance-profile-types`

Returns a list of the child instance profile types supported by Landscape. Currently, only WSL Child Instance Profiles are supported.

Required parameters:

- None

Optional parameters:

- None

Example request:

```bash
curl -X GET -H "Authorization: Bearer $JWT" "https://landscape.canonical.com/api/v2/child-instance-profile-types"
```

Example output:

```json
{
  "results": [
    {
      "name": "wsl",
      "title": "WSL"
    }
  ]
}
```

## GET `/child-instance-profiles`

Gets a list of child instance profiles.

Required parameters:

- none

Optional parameters:

- `names`: A comma separated list of profile names. The profiles returned will exactly match one of these names.
- `search`: Only profiles with names or descriptions matching the search term are returned.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/child-instance-profiles?search=ubuntu -H "Authorization: Bearer $JWT"
```

Example output:

```json
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
- `only_landscape_created`: If true, this profile will delete WSL instances that were not created by Landscape from the associated Windows host machines; defaults to false.
- `access_group`: Name of the access group the profile applies to; defaults to Global Access.
- `tags`: A list of tag names to associate with the profile.
- `all_computers`: If true, this profile will be associated with all computers; defaults to false.

Example requests:

```bash
curl -X POST https://landscape.canonical.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d '{"title": "Stock Ubuntu 24.04", "description": "The image from the store", "image_name": "Ubuntu-24.04", "tags": ["windows_laptops", "windows_desktops"]}'

curl -X POST https://landscape.canonical.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d "{\"title\": \"Customized Ubuntu 24.04\", \"description\": \"The image from the store customized\", \"image_name\": \"Ubuntu-24.04\", \"cloud_init\": \"$(base64 --wrap=0 < cloud_init.yaml)\"}"

curl -X POST https://landscape.canonical.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d '{"title": "Custom Rootfs Image", "description": "My custom image", "image_name": "CustomUbuntu", "image_source": "https://example.com/myimage.tar.gz"}'
```

Example output:

```json
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

## DELETE `/child-instance-profiles/<string:profile_name>`

Delete the specified child instance profile.

Required parameters:

- none

Optional parameters:

- none

Example request:

```bash
curl -X DELETE https://landscape.canonical.com/api/v2/child-instance-profiles/stock-ubuntu-2404 -H "Authorization: Bearer $JWT"
```

Example output:

Empty response.

## GET `/child-instance-profiles/<string:profile_name>`

Get details of the specified child instance profile.

Required parameters:

- none

Optional parameters:

- none

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/child-instance-profiles/stock-ubuntu-2404 -H "Authorization: Bearer $JWT"
```

Example output:

```json
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
- `tags`: A list of tag names to associate with the profile.
- `all_computers`: Whether or not to associate this profile with all computers.

Example request:

```bash
curl -X PATCH https://landscape.canonical.com/api/v2/child-instance-profiles/stock-ubuntu-2404 -H "Authorization: Bearer $JWT" -d '{"description": "The stock image from the store", "tags": ["windows_laptops"]}'
```

Example output:

```json
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

## POST `/child-instance-profiles/<string:profile_name>:reapply`

Reapply a Child Instance Profile to host machines to make them compliant.

Required parameters:

- None

Optional parameters:

- `computer_ids`: A list of ids of the host instances to reapply the profile to. These instances must be associated with the profile. If the parameter is omitted, the profile will be reapplied to all non-compliant hosts.

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/child-instance-profiles/stock-ubuntu-2404:reapply -H "Authorization: Bearer $JWT" -d '{"computer_ids": [1,2,3]}'
```

Example response:

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
  "summary": "Reapply profile Stock Ubuntu 24.04",
  "completion_time": null,
  "parent_id": null,
  "deliver_delay_window": 0,
  "result_text": null,
  "result_code": null,
  "activity_status": "delivered"
}
```
