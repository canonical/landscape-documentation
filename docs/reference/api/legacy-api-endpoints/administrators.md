---
myst:
  html_meta:
    description: "API reference for administrator management. Legacy API endpoints to invite, list, and disable administrators in your Landscape account."
---

(reference-legacy-api-administrators)=
# Administrators

The methods available here help you invite, list and disable administrators in your account.

## InviteAdministrator

Invite an administrator to your account.

- `name`: The name of the person to invite.
- `email`: The email address of the administrator, to which the invitation will be send.
- `roles`: If specified, the roles that the administrator is going to have in your account. Default to `GlobalAdmin`.

For example:

```text
?action=InviteAdministrator&name=John%2ODoe&email=john@example.com
```

## GetAdministrators

Retrieve the list of administrators in the account.

Here’s an example output:

```json
[
    {
        "email": "john@example.com",
        "id": 40042,
        "name": "John Doe",
        "role": "Owner"
    }
]
```

## DisableAdministrator

Disable an administrator of your account.

- `email`: The email address of the administrator to disable.

For example:

```text
?action=DisableAdministrator&email=john@example.com
```
