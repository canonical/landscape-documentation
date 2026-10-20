---
myst:
  html_meta:
    description: "REST API endpoints for managing Self-hosted Landscape license access."
---

# Self-hosted Landscape license

These endpoints manage legacy self-hosted license access for the current
account. The account is determined from the authenticated JWT. These endpoints
do not accept an account ID or account name.

## POST `/self-hosted/license-url:regenerate`

Regenerates the account's private token and invalidates the previous token. This
endpoint returns `404` when the account does not have a Self-hosted/LDS license.

Required permissions:

- `EditAccount`
- `ViewLicense`

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X POST \
  https://landscape.canonical.com/api/v2/self-hosted/license-url:regenerate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{}'
```

Example response:

```json
{
  "license_url": "https://<account>:<new-private-token>@<landscape-host>/license.txt"
}
```

## GET `/self-hosted/status`

Checks whether the current account is entitled to Self-hosted Landscape.

Required permissions:

- `ViewAccount`
- `ViewLicense`

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/self-hosted/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "enabled": true
}
```

## GET `/self-hosted/license-url`

Gets the license download URL for the current account. This endpoint returns
`404` when the account does not have a Self-hosted/LDS license.

Required permissions:

- `ViewAccount`
- `ViewLicense`

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/self-hosted/license-url \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "license_url": "https://<account>:<private-token>@<landscape-host>/license.txt"
}
```