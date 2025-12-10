(reference-rest-api-repositories)=
# Repositories

These methods give access to repository management.

## GET `/repository/apt-source`

Gets a list of APT sources. Optionally filter by APT source name or id.

Optional query parameters:

- `ids`: A comma separated list of APT source ids. All of the APT sources returned will have one of these ids.
- `names`: A comma separated list of APT source names. All of the APT sources returned will have one of these names.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/repository/apt-source?ids=100,101" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
    "results": [
      {
        "id": 100,
        "name": "lucid-mirror",
        "access_group": "global",
        "line": "deb http://archive.ubuntu.com/ubuntu lucid main",
        "gpg_key": null,
        "profiles": ["myprofile"],
      },
      {
        "id": 101,
        "name": "bionic-mirror",
        "access_group": "global",
        "line": "deb http://archive.ubuntu.com/ubuntu bionic main",
        "gpg_key": null,
        "profiles": ["profile2"],
      }
    ],
}
```

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
