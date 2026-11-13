---
myst:
  html_meta:
    description: "REST API endpoints for managing scripts in Landscape. Retrieve scripts for automation."
---

# Scripts

The endpoints available here are related to the management of scripts. Creation, and modification of scripts must still
happen through the legacy API, this is subject to change in the future.

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
      "script_profiles": [],
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
      "script_profiles": [
        {
          "title": "Script Profile 1",
          "id": 12
        }
      ],
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

## GET `/scripts/<id>/script-profiles`

Get all the script profiles associated with a script.

Path parameters:

- `id`: The identification number of the script.
- `offset`: The offset inside the list of results, used for pagination.
- `limit`: The maximum number of results returned, defaults to 1000.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/scripts/34/script-profiles -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "results": [
    {
      "id": 14,
      "title": "Script Profile 6",
      "script_id": 34,
      "access_group": "global",
      "created_by": {
        "name": "John Smith",
        "id": 1
      },
      "created_at": "2025-04-16T06:34:08.631937",
      "last_edited_at": "2025-04-16T21:48:12.933605",
      "trigger": {
        "trigger_type": "recurring",
        "interval": "0 0 5-10 */2 *",
        "start_after": "2025-04-17T12:00:00Z",
        "last_run": null,
        "next_run": "2025-04-17T12:00:00Z"
      },
      "all_computers": false,
      "tags": [
        "server",
        "laptop"
      ],
      "time_limit": 360,
      "username": "root",
      "computers": {
        "num_associated_computers": 10
      },
      "activities": {
        "last_activity": null
      },
      "archived": false
    }
  ],
  "count": 1,
  "next": null,
  "previous": null
}
```
