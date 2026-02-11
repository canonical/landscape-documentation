---
myst:
  html_meta:
    description: "REST API endpoints for repository management in Landscape. Retrieve and configure APT sources for package distribution."
---

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

## POST `/repository/series`

Create a series associated with a distribution in the account. Optionally create and associate pockets with this series.

Required parameters:

- `distribution`: The name of the distribution to create the series in.
- `name`: The name of the series. It must be unique within series within the distribution, start with an alphanumeric character and only contain lowercase letters, numbers, and `-` or `+` signs.

Optional parameters:

- `gpg_key`: The name of the GPG key to use to sign packages lists of the created pockets. This parameter is required if a pocket is specified.
- `include_udeb`: Whether the pocket should include selected components also for .udeb packages (debian-installer). It’s `false` by default.
- `mirror_gpg_key`: The name of the GPG key to use to verify the mirrored repositories for created pockets. If none is given, the stock Ubuntu archive one will be used.
- `mirror_series`: The remote series to mirror. If none is given, the name of the series will be used. If a pockets parameter also passed, each of the created pockets will mirror the relevant `dists/<mirror_series>-<pocket>` repository of the remote archive.
- `mirror_uri`: The URI to mirror for the created pockets. This parameter is required if a pocket is specified.
- `origin`: The origin of the pocket.
- `pockets`: An array of pocket objects. Each object defines a pocket to be created in the series. They will be in mirror mode by default. If this field is provided, each entry in the array must include:
  - `name`: The pocket name.
  - `components`: The list of components for this pocket.
  - `architectures`: The list of architectures for this pocket.

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/repository/series -H "Authorization: Bearer $JWT" -d '{"name": "oracular", "distribution": "ubuntu", "pockets": [{"name": "proposed", "components": ["main"], "architectures": ["amd64"]}], "mirror_uri": "http://archive.ubuntu.com", "gpg_key": "my-key"}'
```

Example output:

```json
{
  "name": "oracular",
  "creation_time": "2025-12-11T01:18:18Z",
  "pockets": [{
    "id": 35,
    "name": "proposed",
    "creation_time": "2025-12-11T01:18:18Z",
    "mode": "mirror",
    "gpg_key": {
      "id": 1,
      "name": "my-key",
      "key_id": "446733C2526084AB",
      "fingerprint": "cd4b:22a6:a06d:7fc8:bd39:0b7e:4467:33c2:5260:84ab",
      "has_secret": true
    },
    "components": ["main"],
    "architectures": ["amd64"],
    "include_udeb": false,
    "apt_source_line": "deb http://landscape.canonical.com/repository/myaccount/ubuntu oracular-proposed main",
    "series": {
      "name": "oracular",
      "creation_time": "2025-12-11T01:18:18Z"
    },
    "distribution": {
      "name": "ubuntu",
      "access_group": "global",
      "creation_time": "2025-12-10T00:59:43Z"
    },
    "package_count": 0,
    "mirror_uri": "http://archive.ubuntu.com",
    "mirror_suite": "oracular-proposed"
  }]
}
```
