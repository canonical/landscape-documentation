(reference-rest-api-preferences)=
# Preferences
The endpoint(s) here are for account preferences.

## PATCH `/preferences`

Updates account preferences using [JSON Merge Patch](https://datatracker.ietf.org/doc/html/rfc7386) semantics. This endpoint allows you to modify specific fields while leaving others unchanged.

Required parameters:

- None

Optional parameters:

- `audit_retention_period`: The time period in days to retain security profile audit records. A negative value means that records should be retained indefinitely.
- `auto_register_new_computers`: Toggle to automatically register new computers.
- `registration_password`: Registration key for auto-registering computers. A valid input is a non-empty string (3-50 chars, single line). To clear the value, explicitly set to `null`.`auto_register_new_computers` must be false in order to clear the registration key (null).
- `title`: The title of organization name.
- `ubuntu_one`: Enable or disable Ubuntu One as an identity provider.

```{note}
- If you don't provide a value for any field in the request, the current value is unchanged.
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
