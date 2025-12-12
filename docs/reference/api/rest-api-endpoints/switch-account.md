(reference-rest-api-switch-account)=
# Switch Account

## POST `/switch-account`

Provides a new JWT for the selected account, assuming the user is entitled to access that account.

Required parameters:

- `account_name`: The name of the account to switch to.

Optional parameters:

- None

Example request:

```bash
curl -X POST -H "Authorization: Bearer $JWT" -d '{
  "account_name": "upside"
  }'   https://landscape.canonical.com/api/v2/switch-account
```

Example response:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIXzI1NiJ9.eyJleHAiOjE3MTI4NzqzNzMsImehdCI6MTcxMjc5MTk3My"
}
```
