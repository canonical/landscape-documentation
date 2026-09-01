---
myst:
  html_meta:
    description: "REST API endpoints for managing Landscape access groups. Update access group titles by name."
---

(reference-rest-api-access-groups)=

# Access groups

## PATCH `/access-groups/<string:access_group_name>`

Update the title of an access group.

Path parameters:

- `access_group_name`: The name of the access group.

Required parameters:

- `title`: The new title for the access group. Must not be empty.

Optional parameters:

- None

Example request:

```bash
curl -X PATCH https://landscape.canonical.com/api/v2/access-groups/my-access-group \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"title": "New Access Group Title"}'
```

Example response:

```json
{
    "name":	"test",
    "title": "updated title",
    "parent": "global",
    "children":	"desktop,server-machines"
}
```
