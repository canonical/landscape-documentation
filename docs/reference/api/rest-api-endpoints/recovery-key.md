(reference-rest-api-recovery-key)=

# FDE Recovery Key

```{note}
These endpoints will only work with a computer that has hardware-backed full disk encryption enabled.
```

## DELETE `/computers/<int:computer_id>/recovery-key`

Deletes the recovery key from Landscape Server if one was created with Landscape. The computer will retain the recovery key keyslot so the previous recovery key can still be used.

Path parameters:

- `computer_id`: The ID assigned to a specific computer.

Query parameters:

- None

Example request:

```bash
curl -X DELETE "https://landscape.canonical.com/api/v2/computers/23/recovery-key" -H "Authorization: Bearer $JWT"
```

## GET `/computers/<int:computer_id>/recovery-key`

Gets the recovery key for a computer if one was created with Landscape.

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
    "contents": "12345-12345-12345-12345-12345-12345-12345-12345"
}
```
