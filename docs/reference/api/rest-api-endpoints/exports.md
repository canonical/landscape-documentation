---
myst:
  html_meta:
    description: "REST API endpoints for managing data exports in Landscape. Track, download, and delete TSV exports of systems and activity logs."
---

(reference-rest-api-exports)=

# TSV exports

```{note}
TSV exports are available starting in Landscape 26.10.
```

The endpoints available here are related to managing TSV exports. See {ref}`reference-computers-exports` to export computer data, or {ref}`reference-activities-exports` to export activity log history.

## GET `/exports`

Get export jobs associated with the current user.

Path parameters:

- None

Query parameters:

- `search`: Only export jobs with names matching the search term are returned.
- `limit`: The maximum number of results returned by the method. It defaults to 50.
- `offset`: The offset inside the list of results.
- `type`: Only export jobs of the specified type are returned. Can be `instance` or `activity`.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/exports?type=instance&limit=1" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "count": 3,
  "results": [
    {
      "id": 42,
      "name": "Weekly Computer Export",
      "status": "completed",
      "progress": 100,
      "type": "instance",
      "query": "tag:server",
      "creation_time": "2026-06-19T11:00:00Z",
      "retain_until": "2026-06-26T12:00:00Z",
      "filename": "export_42.tsv",
      "row_count": 13,
      "download_ready": true,
      "estimated_seconds_remaining": null
    }
  ],
  "next": "https://landscape.canonical.com/api/v2/exports?type=instance&limit=1&offset=1",
  "previous": null
}
```

## GET `/exports/<int:id>`

Get the export job associated with a specified ID.

Path parameters:

- `id`: The export job ID.

Query parameters:

- None

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/exports/42" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "id": 42,
  "name": "Weekly Computer Export",
  "status": "running",
  "progress": 45,
  "type": "instance",
  "query": "tag:server",
  "creation_time": "2026-06-19T11:00:00Z",
  "retain_until": "2026-06-26T12:00:00Z",
  "filename": null,
  "row_count": null,
  "download_ready": false,
  "estimated_seconds_remaining": 30
}
```

## POST `/exports/<int:id>/cancel`

Cancel an in-progress export job.

Path parameters:

- `id`: The export job ID.

Query parameters:

- None

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/exports/42/cancel" -H "Authorization: Bearer $JWT"
```

This endpoint returns an empty response.

## GET `/exports/<int:id>/download`

Download the generated TSV file.

```{note}
The export must have completed before the file can be downloaded. The file is deleted from storage once the download has finished.
```

Path parameters:

- `id`: The export job ID.

Query parameters:

- None

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/exports/42/download" \
  -H "Authorization: Bearer $JWT" \
  -o "export_results.tsv"
```

## DELETE `/exports/<int:id>`

Delete a finished, failed, or canceled export.

Path parameters:

- `id`: The export job ID.

Query parameters:

- None

Example request:

```bash
curl -X DELETE "https://landscape.canonical.com/api/v2/exports/42" -H "Authorization: Bearer $JWT"
```

This endpoint returns an empty response.

