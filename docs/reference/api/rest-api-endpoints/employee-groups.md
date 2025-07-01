(reference-rest-api-employee-groups)=
# Employee groups

## POST `/employee_groups`

Imports selected staged OIDC groups from their OIDC provider.

Optional parameters:

- `import_all_from`: Pass the id of the staged OIDC group import session to import all staged OIDC groups from that session.
- `staged_oidc_group_ids`: A list IDs of the staged OIDC groups to import.

Note: exactly one of `import_all_from` and `staged_oidc_group_ids` should be included with the request.

Example requests:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/employee_groups" -H "Authorization: Bearer $JWT" -d '{"staged_oidc_group_ids": [1, 2, 3]}'
```

```bash
curl -X POST "https://landscape.canonical.com/api/v2/employee_groups" -H "Authorization: Bearer $JWT" -d '{"import_all": 7}'
```

Example response:

```bash
{
    "count": 1000
    "results": [
        1,
        2,
        3,
        ...
    ]
}
```