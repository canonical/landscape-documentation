(reference-rest-api-oidc)=
# OIDC

## POST `/oidc/groups/import_session`

Creates a new OIDC group import session. The groups will be staged in a background task.

Required parameters:

- `issuer_id`: The id of the issuer.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/oidc/groups/import_session" -H "Authorization: Bearer $JWT" -d '{"issuer_id": 123}'
```

Example output:

```bash
{
   "id": 1,
   "account_id": 312,
   "status": "IN_PROGRESS",
   "issuer_id": 123,
   "synced_at": "2024-02-07T17:30:16Z"
}
```

## GET `/oidc/groups/import_session/<id>`

Gets information about an OIDC group import session. Used as a polling endpoint while the group import completes.

Path parameters:

- `id`: ID of the OIDC groups import session.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/oidc/groups/import_session/1" -H "Authorization: Bearer $JWT"
```

Example output:

```bash
{
   "id": 1,
   "account_id": 312,
   "status": "IN_PROGRESS",
   "issuer_id": 123,
   "synced_at": "2024-02-07T17:30:16Z"
}
```

## GET `/oidc/groups/staged`

Lists all staged OIDC groups.

Required query parameters:

- `import_session_id`: The ID of the OIDC group import session.

Optional query parameters:

- `include_imported`: Whether or not to include OIDC groups that have already been imported. Defaults to `false`.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/oidc/groups/staged" -H "Authorization: Bearer $JWT"
```

Example output:

```bash
{
   "count": 500,
   "results": [
       {
           "id": 1,
           "account_id": 312,
           "issuer_id": 123,
           "group_id": "1239fzxv39fvzcz3fcwp",
           "name": "Marketing",
           "import_session_id": 3
       },
       {
           "id": 2,
           "account_id": 312,
           "issuer_id": 123,
           "group_id": "ij9v3490vjxczl209jxc",
           "name": "Engineering",
           "import_session_id": 3
       },
       ...
   ]
}
```
