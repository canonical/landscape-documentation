---
myst:
  html_meta:
    description: "REST API endpoints for managing user invitations in Landscape. Create, accept, revoke, and retrieve invitations for account access."
---

(reference-rest-api-invitations)=

# Invitations

## POST `/accept-invitation`

Accept an invitation for the current user.

Required parameters:

- `invitation_id`: The alphanumeric string used to identify the invitation.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/accept-invitation" -H "Authorization: Bearer $JWT" -d '{"invitation_id": "rqRmwFduPFTM1uy5cO0tOSovS4KNGG"}'
```

Example response:

```json
{
  "account_id": 4,
  "account_title": "My Account"
}
```

## GET `/invitations`

Get all invitations for the account that the principal is associated with.

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/invitations" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "secure_id": "EbXOD9yH4SCmIoTmO60AZkdFNVuMZ5",
      "account": "Onward, Inc.",
      "name": "Joe Wright",
      "email": "joe@example.com",
      "creation_time": "2024-03-20T14:49:25Z"
    },
    {
      "id": 2,
      "secure_id": "YE6XEiWr5V0HUBgMhZAwgyofwY5EKd",
      "account": "Onward, Inc.",
      "name": "Ted Support",
      "email": "ted@example.com",
      "creation_time": "2024-03-20T14:49:25Z"
    }
  ],
  "next": null,
  "previous": null
}
```

## POST `/invitations`

Create and send an invitation to a new administrator for your account. The default to the GlobalAdmin role if no role is specified.

Required parameters:

- `name`: The name of the person to invite.
- `email`: The email address where the administrator invitation will be sent.

Optional parameters:

- `roles`: If specified, a list of strings with the roles that the administrator will have in your account.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/invitations" -H "Authorization: Bearer $JWT" -d '{"name": "Bobby", "email": "bobby@ubuntu.com", "roles": ["Auditor", "SupportAnalyst"]}'
```

Example response:

```json
{
  "id": 4,
  "secure_id": "ozVPhiV41ZfgyP53QHvlwOP3syeKel"
}
```

## DELETE `/invitations/<int:id>`

Deletes an invitation request for a user to join Landscape.

Required parameters:

- `id`: The invitation ID

Optional parameters:

- None

Example request:

```bash
curl -X DELETE "https://landscape.canonical.com/api/v2/invitations/4" -H "Authorization: Bearer $JWT"
```

## GET `/invitations/<int:id>`

Gets the person's information in an invitation request to join Landscape.

Path parameters:

- `id`: The invitation ID

Query parameters:

- None

Example request:

```bash
curl -X GET  "https://landscape.canonical.com/api/v2/invitations/2" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "id": 2,
  "secure_id": "YE6XEiWr5T0HUBgMhXAwgyofwY5EKd",
  "account": "Onward, Inc.",
  "name": "Ted Support",
  "email": "ted@example.com",
  "creation_time": "2024-03-20T14:49:25Z"
}
```

## POST `/reject-invitation`

Reject an invitation. This will remove the invitation and an administrator will have to create a new invitation request.

Required parameters:

- `invitation_id`: The alphanumeric string used to identify the invitation.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/reject-invitation" -H "Authorization: Bearer $JWT" -d '{"invitation_id": "rqRmwFduPFTM1uy5cO0tOSovS4KNGG"}'
```
