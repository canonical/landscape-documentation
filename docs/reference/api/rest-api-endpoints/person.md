---
myst:
  html_meta:
    description: "REST API endpoints to retrieve user information in Landscape. Access name, email, timezone, and login history for current user."
---

(reference-rest-api-person)=
# Person

## GET `/person`

Gets information about the currently logged-in user, such as name, email address, and timezone.

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X GET -I  -H "Authorization: Bearer $JWT" https://landscape.canonical.com/api/v2/person
```

Example response:

```json
{
  "allowable_emails": [
  "john@example.com",
  "klee123@yahoo.com",
  "klee123@hotmail.com"
  ],
  "name": "John Smith",
  "email": "john@example.com",
  "identity": "https://10.200.100.216:8080/id/john",
  "timezone": "UTC",
  "last_login_time": "2024-03-22T18:06:09Z",
  "last_login_host": "10.252.142.1",
  "preferred_account": null
}
```

## POST `/person`

Sets information for the currently logged-in user.

Required parameters:

- None

Optional parameters:

- `name`
- `email`
- `timezone`
- `preferred_account`

Example request:

```bash
curl -X POST -H "Authorization: Bearer $JWT"   -d '{
  "name": "John Allen Smith"
  }'   https://landscape.canonical.com/api/v2/person
```

Example response:

```json
{
  "allowable_emails": [
  "john@example.com",
  "klee123@yahoo.com",
  "klee123@hotmail.com"
  ],
  "name": "John Allen Smith",
  "email": "john@example.com",
  "identity": "https://10.200.100.216:8080/id/john",
  "timezone": "UTC",
  "last_login_time": "2024-03-22T18:06:09Z",
  "last_login_host": "10.252.142.1",
  "preferred_account": null
}
```
