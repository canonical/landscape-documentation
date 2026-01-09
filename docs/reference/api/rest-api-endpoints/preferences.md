(reference-rest-api-preferences)=
# Preferences

## PATCH `/preferences`

Updates account preferences using [JSON Merge Patch](https://datatracker.ietf.org/doc/html/rfc7386) semantics. This endpoint allows you to modify specific fields while leaving others unchanged.

Path parameters:

- None

Query parameters:

- None

Required parameters:

- None

Optional parameters:

- `audit_retention_period`: Audit log retention period in days.
- `auto_register_new_computers`: Whether to automatically register new computers.
- `registration_password`: Registration key for auto-registering computers. 
- `title`: The title of organization name.
- `ubuntu_one`: Enable or disable Ubuntu One as an identity provider.

```{note}
- `registration_password` has three states: omitted (no change), a non-empty valid string (set), or null (clear/unset).
- If the `auto_register_new_computers` is `true` and registration key is `null`, the request returns an error (HTTP 400).
```

Example request:

```bash
curl -X PATCH "https://landscape.canonical.com/api/v2/preferences"  \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "auto_register_new_computers": false,
    "registration_password": null,
    "title": "changed_title"
  }'
```

Example response:

```json
{
    "audit_retention_period": -1,
    "auto_register_new_computers": false,
    "registration_password": null,
    "title": "changed_title",
    "ubuntu_one": true
}
```
