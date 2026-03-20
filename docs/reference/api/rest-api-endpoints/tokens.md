---
myst:
  html_meta:
    description: "REST API endpoints for JWT token management in Landscape. Invalidate tokens for users and accounts for enhanced security."
---

(reference-rest-api-tokens)=
# Tokens

The endpoints available here are related to JSON web token (JWT) management.

## POST `/tokens/invalidate-account`

Invalidate all tokens for all users on the account associated with the JWT used to authenticate the request.

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/tokens/invalidate-account -H "Authorization: Bearer $JWT"
```

This endpoint returns an empty response.

## POST `/tokens/invalidate-me`

Invalidate all tokens associated with the user in the JWT used to authenticate the request.

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/tokens/invalidate-me -H "Authorization: Bearer $JWT"
```

This endpoint returns an empty response.

## POST `/tokens/invalidate-system`

Invalidate all tokens issued from the system. This includes all users across all accounts.

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/tokens/invalidate-system -H "Authorization: Bearer $JWT"
```

This endpoint returns an empty response.

## POST `/tokens/invalidate-system/account/<string:account_name>`

Invalidate all tokens for all users associated with the named account.

Path parameters:

- `account_name`: The name of the account that will have all outstanding tokens invalidated.

Query parameters:

- None

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/tokens/invalidate-account/account/my-account -H "Authorization: Bearer $JWT"
```

This endpoint returns an empty response.
