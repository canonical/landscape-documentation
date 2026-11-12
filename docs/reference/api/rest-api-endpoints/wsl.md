---
myst:
  html_meta:
    description: "REST API reference for WSL in Landscape. List WSL host computers and available WSL instance names."
---

(reference-rest-api-wsl)=
# WSL

## GET `/computers/wsl-hosts`

Gets a list of Windows computers that host at least one WSL instance that is registered in Landscape.

Optional query parameters:

- `query`: Filter the results using the computer search syntax described in {ref}`Computers <reference-rest-api-computers>`.
- `limit`: Maximum number of results to return.
- `offset`: Offset into the result list.

Example request:

```bash
curl -X GET -H "Authorization: ******" "https://landscape.canonical.com/api/v2/computers/wsl-hosts"
```

## GET `/wsl-instance-names`

Gets a listing of image names for the official Ubuntu WSL images available in the Windows Store.

Example request:

```bash
curl -X GET -H "Authorization: ******" "https://landscape.canonical.com/api/v2/wsl-instance-names"
```

Example response:

```json
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

The `name` value is used as the `computer_name` argument to the `CreateChildComputer` legacy API method.
