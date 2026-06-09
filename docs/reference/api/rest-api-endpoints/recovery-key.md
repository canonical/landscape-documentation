(reference-rest-api-recovery-key)=

# FDE Recovery Key

```{note}
These endpoints will only work with a computer with TPM-backed full disk encryption.
```

## GET `/computers/<int:computer_id>/recovery-key`

Gets the recovery key for a computer if one was created with Landscape. If an activity to generate the recovery key is in progress, additionally returns the state of the latest recovery key generation activity.

Path parameters:

- `computer_id`: The ID assigned to a specific computer.

Query parameters:

- None

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/computers/23/recovery-key" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
    "activity": {
        "activity_status": "undelivered",
        "approval_time": null,
        "completion_time": null,
        "creation_time": "2026-01-13T21:57:57Z",
        "creator": {
            "email": "john@example.com",
            "id": 1,
            "name": "John Smith"
        },
        "deliver_delay_window": 0,
        "id": 115,
        "parent_id": null,
        "result_code": null,
        "result_text": null,
        "summary": "Request computer 23 to generate a FDE recovery key.",
        "type": "ActivityGroup"
    },
    "fde_recovery_key": "12345-12345-12345-12345-12345-12345-12345-12345"
}
```

## POST `/computers/<int:computer_id>/recovery-key:generate`

Generates a recovery key for a computer. This will fail if an activity to generate a recovery key for the computer is in progress.

Path parameters:

- `computer_id`: The ID assigned to a specific computer.

Query parameters:

- `force`: If true, an activity will be created even if another activity to generate the recovery key is in progress.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/23/recovery-key:generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
    "activity_status": "undelivered",
    "approval_time": null,
    "completion_time": null,
    "creation_time": "2026-01-13T21:57:57Z",
    "creator": {
        "email": "john@example.com",
        "id": 1,
        "name": "John Smith"
    },
    "deliver_delay_window": 0,
    "id": 115,
    "parent_id": null,
    "result_code": null,
    "result_text": null,
    "summary": "Request computer 23 to generate a FDE recovery key.",
    "type": "ActivityGroup"
}
```
