# Script Profiles

The endpoints available here are related to the management of script profiles and are available only on self-hosted deployments.

## GET `/script-profiles`

Get script profiles associated with the current account, ordered by creation time.

Optional query parameters:

- `archived`: the status of the script profile to filter by. Can be one of `archived`, `active` or `all`. Defaults to `active`.
- `offset`: The offset inside the list of results, used for pagination.
- `limit`: The maximum number of results returned, defaults to 1000.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/script-profiles?archived=all -H "Authorization: Bearer $JWT"
curl -X GET https://landscape.canonical.com/api/v2/script-profiles -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "results": [
    {
      "id": 5,
      "title": "Recurring Script Profile",
      "script_id": 35,
      "access_group": "global",
      "created_by": {
        "name": "John Smith",
        "id": 1
      },
      "created_at": "2025-04-10T23:36:21.411941",
      "last_edited_at": "2025-04-10T23:36:21.411941",
      "trigger": {
        "trigger_type": "recurring",
        "interval": "0 8 * * *",
        "start_after": "2025-04-23T02:10:41Z",
        "last_run": null,
        "next_run": "2025-04-23T00:08:00Z"
      },
      "all_computers": true,
      "tags": [],
      "time_limit": 150,
      "username": "landscape",
      "computers": {
        "num_associated_computers": 20
      },
      "activities": {
        "last_activity": null
      },
      "archived": false
    },
    {
      "id": 4,
      "title": "Post Enrollment Script Profile",
      "script_id": 31,
      "access_group": "global",
      "created_by": {
        "name": "John Smith",
        "id": 1
      },
      "created_at": "2025-04-10T23:29:58.396345",
      "last_edited_at": "2025-04-10T23:29:58.396345",
      "trigger": {
        "trigger_type": "event",
        "event_type": "post_enrollment"
      },
      "all_computers": false,
      "tags": [
        "server",
        "laptop"
      ],
      "time_limit": 200,
      "username": "ubuntu",
      "computers": {
        "num_associated_computers": 0
      },
      "activities": {
        "last_activity": null
      },
      "archived": false
    },
    {
      "id": 1,
      "title": "One Time Script Profile",
      "script_id": 34,
      "access_group": "server",
      "created_by": {
        "name": "John Smith",
        "id": 1
      },
      "created_at": "2025-04-10T23:27:10.568080",
      "last_edited_at": "2025-04-10T23:27:10.568080",
      "trigger": {
        "trigger_type": "one_time",
        "timestamp": "2025-04-04T02:10:41Z",
        "is_finished": true,
        "next_run": null,
        "last_run": "2025-04-11T17:56:47Z"
      },
      "all_computers": true,
      "tags": [],
      "time_limit": 360,
      "username": "root",
      "computers": {
        "num_associated_computers": 20
      },
      "activities": {
        "last_activity": {
          "id": 2396,
          "creation_time": "2025-04-11T17:56:47Z",
          "creator": {
            "name": "John Smith",
            "email": "john@example.com",
            "id": 1
          },
          "type": "ActivityGroup",
          "summary": "Run script",
          "completion_time": null,
          "parent_id": null,
          "deliver_delay_window": 0,
          "result_text": null,
          "result_code": null,
          "activity_status": "undelivered"
        }
      },
      "archived": false
    }
  ],
  "count": 3,
  "next": null,
  "previous": null
}
```

## GET `/script-profiles/<id>`

Get a script profile by `id`.

Path parameters:

- `id`: The identification number of the profile.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/script-profiles/116782 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  {
    "id": 116782,
    "title": "Post Enrollment Script Profile",
    "script_id": 31,
    "access_group": "global",
    "created_by": {
      "name": "John Smith",
      "id": 1
    },
    "created_at": "2025-04-10T23:29:58.396345",
    "last_edited_at": "2025-04-10T23:29:58.396345",
    "trigger": {
      "trigger_type": "event",
      "event_type": "post_enrollment"
    },
    "all_computers": false,
    "tags": [
      "server",
      "laptop"
    ],
    "time_limit": 200,
    "username": "ubuntu",
    "computers": {
      "num_associated_computers": 0
    },
    "activities": {
      "last_activity": null
    },
    "archived": false
  },
}
```

## POST `/script-profiles`

Create a script profile.

Required parameters:

- `title`: The display name of the profile.
- `script_id`: The id of the script this profile is associated with, must be a `v2` script.
- `all_computers`: If `true`, the profile will be applied to all instances in the script's `access_group`, regardless of `tags`.
- `tags`: An array of tag strings. The profile will be applied only to instances with these tags in the script's `access_group`.
- `time_limit`: The time, in seconds, after which the script is considered defunct. The process will be killed, and the script execution will be marked as failed after this limit expires.
- `username`: The username to execute the script as on the client.
- `trigger`: Defined as a [trigger](#trigger) based on which the profile should execute.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/script-profiles" -H "Authorization: Bearer $JWT" -d '
{
  "title": "Optics and Design",
  "username": "root",
  "time_limit": 360,
  "script_id": 35,
  "tags": [],
  "all_computers": true,
  "trigger": {
    "trigger_type": "event",
    "event_type": "post_enrollment" 
  }
}'
```

Example response:

```json
{
  "id": 176892,
  "title": "Optics and Design",
  "script_id": 35,
  "access_group": "global",
  "created_by": {
    "name": "John Smith",
    "id": 1
  },
  "created_at": "2025-04-23T07:53:01.226040",
  "last_edited_at": "2025-04-23T07:53:01.226040",
  "trigger": {
    "trigger_type": "event",
    "event_type": "post_enrollment"
  },
  "all_computers": true,
  "tags": [],
  "time_limit": 360,
  "username": "root",
  "computers": {
    "num_associated_computers": 0
  },
  "activities": {
    "last_activity": null
  },
  "archived": false
}
```

### Trigger

Required parameters:

- `trigger_type`: Either of `event`, `one_time`, `recurring`.

Each `trigger_type` has corresponding required parameters.

#### Event

- `event_type`: Currently only the `post_enrollment` event is available, which triggers after a computer is enrolled in an account.

#### One Time

- `timestamp`: An ISO 8601-formatted datestamp that sets when the profile should execute. If it is in the past, the profile will start its first run immediately.

#### Recurring

- `start_after`: An ISO 8601-formatted datestamp that sets the earliest time after which the profile should be scheduled to execute.
- `interval`: A 5 digit, [Cron](https://en.wikipedia.org/wiki/Cron) string.

## PATCH `/script-profiles/<id>`

Update a script profile.

Path parameters:

- `id`: The identification number of the profile to update.

Optional parameters:

- `title`: The display name of the profile.
- `all_computers`: If `true`, the profile will be applied to all instances in the script's `access_group`, regardless of `tags`.
- `tags`: An array of tag strings. The profile will be applied only to instances with these tags in the script's `access_group`.
- `time_limit`: The time, in seconds, after which the script is considered defunct. The process will be killed, and the script execution will be marked as failed after this limit expires.
- `username`: The username to execute the script as on the client.
- `trigger`: Defined as a [trigger](#trigger) based on which the profile should execute.

Example request:

```bash
curl -X PATCH "https://landscape.canonical.com/api/v2/script-profiles/176892" -H "Authorization: Bearer $JWT" -d '
{
  "title": "Macrodata Refinement",
  "username": "landscape",
  "time_limit": 270,
  "tags": ["server"],
  "all_computers": false'
}'

```

Example response:

```json
{
  "id": 18,
  "title": "Macrodata Refinement",
  "script_id": 35,
  "access_group": "global",
  "created_by": {
    "name": "John Smith",
    "id": 1
  },
  "created_at": "2025-04-23T07:55:16.592280",
  "last_edited_at": "2025-04-23T08:07:53.838104",
  "trigger": {
    "trigger_type": "event",
    "event_type": "post_enrollment"
  },
  "all_computers": false,
  "tags": [
    "server"
  ],
  "time_limit": 270,
  "username": "landscape",
  "computers": {
    "num_associated_computers": 0
  },
  "activities": {
    "last_activity": null
  },
  "archived": false
}
```

## POST `/script-profiles/<id>:archive`

Archive a script profile. This makes it inactive.

Path parameters:

- `id`: The identification number of the profile to archive.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/script-profiles/176892:archive" -H "Authorization: Bearer $JWT"
```

## GET `/script-profiles/<id>/activities`

Get parent activities associated with a script profile ordered by creation time.

Path parameters:

- `id`: The identification number of the profile.
- `offset`: The offset inside the list of results, used for pagination.
- `limit`: The maximum number of results returned, defaults to 1000.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/script-profiles/176892/activities" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "results": [
    {
      "id": 2396,
      "creation_time": "2025-04-11T17:56:47Z",
      "creator": {
        "name": "John Smith",
        "email": "john@example.com",
        "id": 1
      },
      "type": "ActivityGroup",
      "summary": "Run script",
      "completion_time": null,
      "parent_id": null,
      "deliver_delay_window": 0,
      "result_text": null,
      "result_code": null,
      "activity_status": "undelivered"
    }
  ],
  "count": 1,
  "next": null,
  "previous": null
}
```

## GET `/script-profile-limits`

Get account wide limits associated with script profiles.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/script-profile-limits" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "max_num_computers": 5000,
  "max_num_profiles": 10,
  "min_interval": 360
}
```

- `min_interval`: The minimum time, in minutes, between execution of recurring script profiles that Landscape enforces.
