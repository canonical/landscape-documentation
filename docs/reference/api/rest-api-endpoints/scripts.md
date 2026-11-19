---
myst:
  html_meta:
    description: "REST API endpoints for managing scripts in Landscape. Retrieve scripts for automation."
---

# Scripts

The endpoints available here are related to the management of scripts. Creation, and modification of scripts must still
happen through the legacy API.

## GET `/scripts`

Get scripts associated with the current account.

Optional query parameters:

- `offset`: The offset inside the list of results, used for pagination.
- `limit`: The maximum number of results returned, defaults to 1000.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/scripts -H "Authorization: Bearer $JWT"
curl -X GET https://landscape.canonical.com/api/v2/scripts?limit=2 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "results": [
    {
      "id": 37,
      "title": "Script 1",
      "creator": {
        "id": 1,
        "name": "John Smith",
        "email": "john@example.com"
      },
      "attachments": [],
      "access_group": "server",
      "time_limit": 300,
      "username": "root"
    },
    {
      "id": 30,
      "title": "Script 2",
      "creator": {
        "id": 1,
        "name": "John Smith",
        "email": "john@example.com"
      },
      "attachments": [],
      "access_group": "global",
      "time_limit": 300,
      "username": "landscape"
    }
  ],
  "count": 8,
  "next": "/api/v2/scripts?limit=2&offset=2",
  "previous": null
}
```
