(reference-api-rest-api-endpoints-beta-only)=
# Beta-only

```{note}
The following endpoints are only in beta.
```

## POST `/computers/<computer_id>/archive`

Archives the selected computer after it has been manually sanitized.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Required parameters:

- `computer_title`: Confirm the name of the computer to archive

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/29/archive" -H "Authorization: Bearer $JWT" -d '{"computer_title": "test computer"}'
```

Example output:

```json
{
 "id": 124,
 "activity_status": "succeeded",
 "approval_time": null,
 "completion_time": "2025-02-22T02:14:19Z",
 "creation_time": "2025-02-22T02:14:19Z",
 "creator": {
     "email": "john@example.com",
     "id": 1,
     "name": "John Smith"
 },
 "deliver_delay_window": 0,
 "parent_id": null,
 "result_code": null,
 "result_text": null,
 "summary": "Archive computer",
 "type": "ActivityGroup"
}
```

## POST `/computers/<computer_id>/delete-children`

Creates an activity to delete WSL instances on a Windows host. The WSL instance does not have to be managed in Landscape.

Required parameters:

- `computer_names`

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/computers/20/delete-children -H "Authorization: Bearer $JWT" -d '{"computer_names": ["Ubuntu-24.04", "Focal WSL"]}'
```

Example output:

```json
{
  "id": 119,
  "creation_time": "2025-02-22T02:03:26Z",
  "creator": {
    "email": "john@example.com",
    "id": 1,
    "name": "John Smith"
  },
  "summary": "Deleting child computer(s)",
  "type": "ActivityGroup",
  "deliver_delay_window": 0,
  "approval_time": null,
  "completion_time": null,
  "parent_id": null,
  "result_code": null,
  "result_text": null,
  "activity_status": "undelivered"
}
```

## POST `/computers/<computer_id>/sanitize`

[note type=information]
**Note:** **Please make sure you are sanitizing the correct computer. This action is irreversible.**
[/note]

Sanitizes the selected computer. This action will make the data on the selected computer permanently irrecoverable by erasing the keyslots of every encrypted volume. A configurable delay can be set in the service.conf file.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Required parameters:

- `computer_title`: Confirm the name of the computer to sanitize

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/29/sanitize" -H "Authorization: Bearer $JWT" -d '{"computer_title": "test computer"}'
```

Example output:

```json
{
 "id": 119,
 "activity_status": "scheduled",
 "approval_time": null,
 "completion_time": null,
 "creation_time": "2025-01-07T05:27:39Z",
 "creator": {
     "email": "john@example.com",
     "id": 1,
     "name": "John Smith"
 },
 "deliver_delay_window": 0,
 "parent_id": null,
 "result_code": null,
 "result_text": null,
 "summary": "Sanitizing computer",
 "type": "ActivityGroup"
}
```