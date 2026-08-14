---
myst:
  html_meta:
    description: "REST API endpoints for Landscape account management. Create and configure accounts with self-service organization setup."
---

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
curl -X POST https://landscape.canonical.com/api/v2/accounts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"title": "Onward, Inc."}'
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

## DELETE `/message-backlog-settings`

Clear the message backlog limit for the current account, restoring default behaviour.

Path parameters:

- None

Required parameters:

- None

Example request:

```bash
curl -X DELETE https://landscape.canonical.com/api/v2/message-backlog-settings \
  -H "Authorization: Bearer $JWT"
```

Example response: `204 No Content`

## GET `/message-backlog-settings`

Get the message backlog limit for the current account. Returns `404` if no limit has been set.

Path parameters:

- None

Required parameters:

- None

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/message-backlog-settings \
  -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
    "max_message_backlog": 100000
}
```

## PUT `/message-backlog-settings`

Set the message backlog limit for the current account.

Path parameters:

- None

Required parameters:

- `max_message_backlog`: Maximum number of messages to queue per computer (non-negative integer).

Example request:

```bash
curl -X PUT https://landscape.canonical.com/api/v2/message-backlog-settings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"max_message_backlog": 100000}'
```

Example response:

```json
{
    "max_message_backlog": 100000
}
```

## GET `/standalone-account`

An endpoint to indicate whether or not the standalone account has been created in a standalone deployment. This endpoint will always return a 404 in any deployment other than a standalone deployment (e.g. SaaS).

Path parameters:

- None

Required parameters:

- None

Example request:

```bash
curl -X GET https://landscape.example.com/api/v2/standalone-account
```

Example response:

```json
{"exists": true}
```

## POST `/standalone-account`

Create a standalone account with the first administrator. If this is not a standalone deployment or a standalone account already exists, the request will fail.

Path parameters:

- None

Required parameters:

- `email`: The email of the first administrator.
- `name`: The name of the first administrator.
- `password`: The password of the first administrator. Set {ref}`enforce_password_strength <service-conf-system-enforce-password-strength>` to `True` to enforce password strength requirements.

Example request:

```bash
curl -X POST https://landscape.example.com/api/v2/standalone-account \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"email": "john@example.com", "name": "John Doe", "password": "Passw0rd"}'
```

Example response:

```json
{
    "account": "standalone",
    "creation_time": "2025-09-15T22:52:11Z",
    "administrators": [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "openid": null,
        }
    ],
    "disabled": false,
    "disabled_reason": null,
    "computers": 0,
    "company": "Organization",
    "last_login_time": "2025-09-15T22:52:11Z",
    "licenses": [],
    "salesforce_account_key": null,
    "enabled_features": [],
    "subdomain": null
}
```
