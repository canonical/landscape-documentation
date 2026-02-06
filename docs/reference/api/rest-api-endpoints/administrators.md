(reference-rest-api-administrators)=
# Administrators

The endpoint(s) available here are for managing administrators in your account.

## PUT `/administrators/<int:person_id>`

Assign administrators to certain roles by their ID.

Path parameters:

- `person_id`: The ID for the administrator.

Required parameters:

- `roles`: A list of the role(s) the administrator should have as strings.

Optional parameters:

- None

Example request:

```bash
curl -X PUT https://landscape.canonical.com/api/v2/administrators/6 -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" -d '{"roles": ["ServerAdmin", "DesktopAdmin"]}'
```

Example response:

```json
{
  "email": "robert@example.com",
  "id": 6,
  "name": "Robert Frost",
  "roles": [
  "DesktopAdmin",
  "ServerAdmin"
  ]
}
```
