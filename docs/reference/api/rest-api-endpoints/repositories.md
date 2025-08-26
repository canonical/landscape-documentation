(reference-rest-api-repositories)=
# Repositories

These methods give access to repository management.

## DELETE `/repository/apt-source/<id>`

Remove an APT source. Optionally remove associations from any repository profiles.

Path parameters:

- `id`: The identification number of the APT source.

Optional query parameters:

- `disassociate_profiles`: If true, remove associations to this APT source from repository profiles.

Example request:

```bash
curl -X DELETE https://landscape.canonical.com/api/v2/repository/apt-source/12 -H "Authorization: Bearer $JWT"
```

