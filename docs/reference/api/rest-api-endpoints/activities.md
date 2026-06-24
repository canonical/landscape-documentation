---
myst:
  html_meta:
    description: "REST API endpoints to retrieve and monitor activities in Landscape. View activity history, creation time, and status for account operations."
---

(reference-rest-api-activities)=
# Activities

The endpoints available here are related to activity management.

## GET `/activities`

Get activities associated with the current account, ordered by creation time.

Path parameters:

- None

Query parameters:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/activities?limit=2 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "count": 89,
  "results": [
    {
      "id": 71666950,
      "creation_time": "2024-02-07T17:30:05Z",
      "creator": {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "id": 115669
      },
      "type": "ChangePackagesRequest",
      "summary": "Downgrade package apt-transport-https",
      "result_text": null,
      "computer_id": 365829,
      "approval_time": null,
      "delivery_time": null,
      "deliver_after_time": null,
      "deliver_before_time": null,
      "package_ids": [
        7085390,
        7915181
      ],
      "changes": [
        {
          "package": "apt-transport-https",
          "complemented": false,
          "type": "downgrade",
          "install_version": "1.0.1ubuntu2.19",
          "remove_version": "1.0.1ubuntu2.24"
        }
      ],
      "parent_id": 71666947,
      "modification_time": "2024-02-07T17:30:16Z",
      "completion_time": "2024-02-07T17:30:16Z",
      "schedule_before_time": null,
      "schedule_after_time": null,
      "result_code": null,
      "activity_status": "canceled",
      "children": []
    }
  ],
  "next": "https://landscape.canonical.com/api/v2/activities?limit=2&offset=2",
  "previous": null
}
```

## GET `/activities/<int:id>`

Get activities associated with a specified ID.

Path parameters:

- `id`: The activity ID.

Query parameters:

- None

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/activities/71666950 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "id": 71666950,
  "creation_time": "2024-02-07T17:30:05Z",
  "creator": {
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "id": 115669
  },
  "type": "ChangePackagesRequest",
  "summary": "Downgrade package apt-transport-https",
  "result_text": null,
  "computer_id": 365829,
  "approval_time": null,
  "delivery_time": null,
  "deliver_after_time": null,
  "deliver_before_time": null,
  "package_ids": [
  7085390,
  7915181
  ],
  "changes": [
  {
    "package": "apt-transport-https",
    "complemented": false,
    "type": "downgrade",
    "install_version": "1.0.1ubuntu2.19",
    "remove_version": "1.0.1ubuntu2.24"
  }
  ],
  "parent_id": 71666947,
  "modification_time": "2024-02-07T17:30:16Z",
  "completion_time": "2024-02-07T17:30:16Z",
  "schedule_before_time": null,
  "schedule_after_time": null,
  "result_code": null,
  "activity_status": "canceled",
  "children": []
}
```

## GET `/activities/parents`

Get activities with a specified parent ID.

Path parameters:

- None

Query parameters:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/activities/parents?limit=2 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "count": 87,
  "results": [
  {
    "id": 71666947,
    "creation_time": "2024-02-07T17:30:05Z",
    "creator": {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "id": 115669
    },
    "type": "ActivityGroup",
    "summary": "Downgrade package apt-transport-https",
    "completion_time": "2024-02-07T17:30:16Z",
    "parent_id": null,
    "deliver_delay_window": 0,
    "result_text": null,
    "result_code": null,
    "activity_status": "canceled",
    "children_count": 2,
    "children_statuses": {
      "good": 0,
      "warning": 0,
      "bad": 2
    },
    "computer_count": 2,
    "computer": null
  },
  {
    "id": 71666936,
    "creation_time": "2024-02-07T17:29:27Z",
    "creator": {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "id": 115669
    },
    "type": "ActivityGroup",
    "summary": "Downgrade package apt-transport-https",
    "completion_time": "2024-02-07T17:29:34Z",
    "parent_id": null,
    "deliver_delay_window": 0,
    "result_text": null,
    "result_code": null,
    "activity_status": "canceled",
    "children_count": 2,
    "children_statuses": {
      "good": 0,
      "warning": 0,
      "bad": 2
    },
    "computer_count": 2,
    "computer": null
  }
  ],
  "next": "https://landscape.canonical.com/api/v2/activities/parents?limit=2&offset=2",
  "previous": null
}
```

## POST `/activities/reapply`

Reapply the activities with the specified IDs, if possible.

Required parameters:

- `activity_ids`: A list of the specified ID(s) as integers for an activity.

Optional parameters:

- None

## POST `/activities/revert`

Revert the activities with the specified IDs, if possible.

Required parameters:

- `activity_ids`: A list of the specified ID(s) as integers for an activity.

Optional parameters:

- None

(reference-activities-exports)=
## POST `/activities/exports`

Initiates an asynchronous export of activity log history into Tab-Separated Value (TSV) format. See {ref}`reference-rest-api-exports` to manage and download export jobs.

Optional parameters:

- `name`: A name to identify the export job.
- `query`: A query string used to filter the activity history to export. Defaults to an empty string, which exports all activities.
- `selected_field_ids`: A list of field IDs to include in the exported TSV file.
- `retain_until`: An ISO 8601-formatted datestamp indicating how long to retain the export.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/activities/exports" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{
    "name": "Monthly Activity Export",
    "query": "activity_status:succeeded",
    "selected_field_ids": ["id", "creation_time", "summary", "type", "activity_status"],
    "retain_until": "2026-07-19T11:00:00Z"
  }'
```

Example response:

```json
{
  "id": 43,
  "name": "Monthly Activity Export",
  "status": "processing",
  "progress": 0,
  "type": "activity",
  "query": "activity_status:succeeded",
  "created_at": "2026-06-19T11:01:00Z",
  "retain_until": "2026-07-19T11:00:00Z",
  "filename": "",
  "row_count": 0,
  "download_ready": false,
  "estimated_seconds_remaining": null
}
```

```{note}
This endpoint is available starting in Landscape 26.10.
```
