(reference-rest-api-accounts)=

# Accounts

The endpoints available here are related to account management.

## POST `/accounts`

Create an account for the current user. If the user already has an account, or self-service account creation is disabled, the request will fail.

If successful, the current user will be an admin of the account.

Path parameters:

- None

Required parameters:

- `title`: The title of the organization.

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/accounts -H "Authorization: Bearer $JWT" -d '{"title": "Onward, Inc."}'
```

Example response:

```json
{
    "account": "8xag1afp",
    "creation_time": "2025-09-15T22:52:11Z",
    "administrators": [
        {
            "name": "Your Name",
            "email": "yourname@example.com",
            "openid": "youropenid"
        }
    ],
    "disabled": false,
    "disabled_reason": null,
    "computers": 0,
    "company": "Onward, Inc.",
    "last_login_time": "2025-09-15T22:52:11Z",
    "licenses": [],
    "salesforce_account_key": null,
    "enabled_features": [],
    "subdomain": null
}
```
