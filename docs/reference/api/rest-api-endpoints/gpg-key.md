(reference-rest-api-gpg-key)=
# GPG Key

The endpoint(s) here are for GPG key management.

## POST `/gpg-key`

Import a GPG key.

Required parameters:

- `name`: Name of the GPG key. It must be unique within the account, start with an alphanumeric character and only contain lowercase letters, numbers and the minus (-) or plus (+) signs.
- `material`: The text representation of the key.

Optional parameters:

- None

Example request:

```bash
curl -X POST -H "Authorization: Bearer $JWT" -d '{
"name": "gpg-mirror-key",
"material": "$(cat mirror-key.asc)"
}' https://landscape.canonical.com/api/v2/gpg-key
```

Example response:

```json
{
  "id": 10617,
  "name": "gpg-mirror-key",
  "key_id": "40V648A95FD69F40",
  "fingerprint": "b6a7:2bb0:2a06:be5a:0d05:0beb:49a6:33a9:5fa2:9f40",
  "has_secret": false
}
```
