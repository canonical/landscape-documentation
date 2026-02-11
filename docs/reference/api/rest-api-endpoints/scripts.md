---
myst:
  html_meta:
    description: "REST API endpoints for managing scripts in Landscape. Retrieve and filter scripts by status, type, and version for automation."
---

# Scripts

The endpoints available here are related to the management of scripts. Creation, and modification of scripts must still
happen through the legacy API, this is subject to change in the future.

## GET `/scripts`

Get scripts associated with the current account.

Optional query parameters:

- `script_type`: the status of the script to filter by. Can be one of `v2`, `active`, `archived`, 
  `redacted`, `all`, and `v1` (deprecated). Defaults to `active`.
- `offset`: The offset inside the list of results, used for pagination.
- `limit`: The maximum number of results returned, defaults to 1000.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/scripts -H "Authorization: Bearer $JWT"
curl -X GET https://landscape.canonical.com/api/v2/scripts?script_type=v2&limit=2 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "results": [
    {
      "id": 37,
      "title": "Script 1",
      "version_number": 1,
      "created_by": {
        "id": 1,
        "name": "John Smith"
      },
      "created_at": "2025-04-16T21:09:19.872660",
      "last_edited_by": {
        "id": 1,
        "name": "John Smith"
      },
      "last_edited_at": "2025-04-16T21:09:19.872660",
      "script_profiles": [],
      "status": "REDACTED",
      "attachments": [],
      "code": "The code for this script has been redacted.",
      "interpreter": "/bin/false",
      "access_group": "server",
      "time_limit": 300,
      "username": "root",
      "is_redactable": true,
      "is_editable": true,
      "is_executable": true
    },
    {
      "id": 30,
      "title": "Script 2",
      "version_number": 1,
      "created_by": {
        "id": 1,
        "name": "John Smith"
      },
      "created_at": "2025-04-10T07:01:39.062323",
      "last_edited_by": {
        "id": 1,
        "name": "John Smith"
      },
      "last_edited_at": "2025-04-10T07:01:39.062323",
      "script_profiles": [
        {
          "title": "Script Profile 1",
          "id": 12
        }
      ],
      "status": "ACTIVE",
      "attachments": [],
      "code": "\nls /tmp",
      "interpreter": "/bin/bash",
      "access_group": "global",
      "time_limit": 300,
      "username": "landscape",
      "is_redactable": true,
      "is_editable": true,
      "is_executable": true
    }
  ],
  "count": 8,
  "next": "/api/v2/scripts?script_type=v2&limit=2&offset=2",
  "previous": null
}
```

## GET `/scripts/<id>`

Get a script defined by `id`.

Path parameters:

- `id`: The identification number of the script.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/scripts/40 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "id": 40,
  "title": "Script 3",
  "version_number": 1,
  "created_by": {
    "id": 1,
    "name": "John Smith"
  },
  "created_at": "2025-04-22T09:01:33.196083",
  "last_edited_by": {
    "id": 1,
    "name": "John Smith"
  },
  "last_edited_at": "2025-04-22T09:01:33.196083",
  "script_profiles": [],
  "status": "ACTIVE",
  "attachments": [
    {
      "filename": "test.py",
      "id": 18
    }
  ],
  "code": "print(\"test 2\")",
  "interpreter": "/bin/bash",
  "access_group": "global",
  "time_limit": 300,
  "username": "root",
  "is_redactable": true,
  "is_editable": true,
  "is_executable": true
}
```

## GET `/scripts/<id>/versions`

Get all versions associated with a script ordered by creation time.

Path parameters:

- `id`: The identification number of the script.
- `offset`: The offset inside the list of results, used for pagination.
- `limit`: The maximum number of results returned, defaults to 1000.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/scripts/34?limit=3 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "results": [
    {
      "id": 9,
      "created_by": {
        "name": "John Smith",
        "id": 1
      },
      "title": "Script 2",
      "version_number": 4,
      "code": "\nls /tmp\n# Version 4",
      "interpreter": "/bin/bash",
      "created_at": "2025-04-10T23:23:59.882443"
    },
    {
      "id": 8,
      "created_by": {
        "name": "John Smith",
        "id": 1
      },
      "title": "Script 2",
      "version_number": 3,
      "code": "\nls /tmp\n# Version 3",
      "interpreter": "/bin/bash",
      "created_at": "2025-04-10T23:23:39.784443"
    },
    {
      "id": 7,
      "created_by": {
        "name": "John Smith",
        "id": 1
      },
      "title": "Script 2",
      "version_number": 2,
      "code": "\nls /tmp\n# Version 2",
      "interpreter": "/bin/bash",
      "created_at": "2025-04-10T23:23:01.166583"
    }
  ],
  "count": 3,
  "next": "/api/v2/scripts/34/versions?limit=3&offset=3",
  "previous": null
}
```

## GET `/scripts/<id>/versions/<version_number>`

Get a specific version of a script.

Path parameters:

- `id`: The identification number of the script.
- `version_number`: The version number of the script.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/scripts/34/versions/3 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "id": 8,
  "created_by": {
    "name": "John Smith",
    "id": 1
  },
  "title": "Script 2",
  "version_number": 3,
  "code": "\nls /tmp\n# Version 3",
  "interpreter": "/bin/bash",
  "created_at": "2025-04-10T23:23:39.784443"
}
```

## GET `/scripts/<id>/attachments/<attachment_id>`

Get the attachment associated with a script.

Path parameters:

- `id`: The identification number of the script.
- `attachment_id`: The identification number of the attachment belonging to the script.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/scripts/40/attachments/18 -H "Authorization: Bearer $JWT"
```

Example response:

```text
#!/bin/bash
if test -f /var/run/reboot-required
then
  logger "Landscape triggered a reboot"
  reboot
else
  echo "reboot not required"
fi
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

## POST `/scripts/<id>:archive`

Archive a script, and any associated script profiles. This makes it inactive. 
Redacted scripts cannot be archived.

Path parameters:

- `id`: The identification number of the script to archive.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/scripts/176892:archive" -H "Authorization: Bearer $JWT"
```

## POST `/scripts/<id>:redact`

Redact a script, archive any associated script profiles, delete associated attachments, and redact script versions.
This deletes the code associated with the script and makes it inactive. If the script profile feature is not enabled, this endpoint behaves
similar to a `DELETE` instead.

Path parameters:

- `id`: The identification number of the script to redact.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/scripts/176892:redact" -H "Authorization: Bearer $JWT"
```
