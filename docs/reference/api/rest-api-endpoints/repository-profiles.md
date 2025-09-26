(reference-rest-api-repository-profiles)=
# Repository Profiles

## POST `/v2/repositoryprofiles`

Creates a new repository profile, including its associations, APT sources, and pockets.

Required parameters:

- `title`: Title of the repository profile.

Optional parameters:

- `description`: Description of the repository profile.
- `access_group`: Name of the access group in which to create the profile. Defaults to `"global"`.
- `tags`: Tags with which the profile will be associated.
- `all_computers`: If `true`, the profile is associated with all computers. Defaults to `false`.
- `apt_sources`: The IDs of the APT sources to add.
- `pockets`: The IDs of the pockets to add.

Example request:

```sh
curl -X POST "https://landscape.canonical.com/api/v2/repositoryprofiles" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Jammy Repo Profile",
    "description": "Repository profile for jammy instances",
    "tags": ["jammy"],
    "apt_sources": [1, 2],
    "pockets": [3]
}'
```

Example output:

```json
{
  "id": 6,
  "access_group": "global",
  "name": "jammy-repo-profile",
  "title": "Jammy Repo Profile",
  "description": "Repository profile for jammy instances",
  "all_computers": false,
  "tags": ["jammy"],
  "pockets": [
    {
      "id": 3,
      "name": "jammy-updates",
      "creation_time": "2025-09-24T23:10:47Z",
      "mode": "mirror",
      "gpg_key": null,
      "components": ["main"],
      "architectures": ["amd64"],
      "include_udeb": false,
      "apt_source_line": "deb http://10.1.77.207:8080/repository/onward/ubuntu jammy-updates main",
      "series": {
        "name": "jammy",
        "creation_time": "2025-09-24T23:10:47Z"
      },
      "distribution": {
        "name": "ubuntu",
        "access_group": "global",
        "creation_time": "2025-09-24T23:10:47Z"
      },
      "package_count": 0
    }
  ],
  "apt_sources": [],
  "pending_count": 0
}
```

---

## PUT `/v2/repositoryprofiles/<str:profile_name>`

Updates an existing repository profile.  

Path parameters:

- `profile_name`: The `name` of the repository profile to update.

Required parameters:

- `title`: Title of the repository profile.

Optional parameters:

- `description`: Description of the repository profile.
- `access_group`: Name of the access group in which the profile is stored.
- `tags`: Tags with which the profile will be associated.
- `all_computers`: If `true`, the profile is associated with all computers.
- `apt_sources`: The IDs of the APT sources to add.
- `pockets`: The IDs of the pockets to add.

Example request:

```bash
curl -X PUT "https://landscape.canonical.com/api/v2/repositoryprofiles/jammy-repo-profile" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Jammy Repo Profile",
    "description": "Updated description",
    "tags": ["jammy"],
    "apt_sources": [4],
    "pockets": [2]
}'
```

Example output:

```json
{
  "id": 6,
  "access_group": "global",
  "name": "jammy-repo-profile",
  "title": "Jammy Repo Profile",
  "description": "Updated description",
  "all_computers": false,
  "tags": ["jammy"],
  "pockets": [
    {
      "id": 2,
      "name": "jammy-security",
      "creation_time": "2025-09-24T23:10:47Z",
      "mode": "upload",
      "gpg_key": null,
      "components": ["main"],
      "architectures": ["amd64", "source"],
      "include_udeb": false,
      "apt_source_line": "deb http://10.1.77.207:8080/repository/onward/ubuntu jammy-security main",
      "series": {
        "name": "jammy",
        "creation_time": "2025-09-24T23:10:47Z"
      },
      "distribution": {
        "name": "ubuntu",
        "access_group": "global",
        "creation_time": "2025-09-24T23:10:47Z"
      },
      "package_count": 0,
      "upload_allow_unsigned": true,
      "upload_gpg_keys": []
    }
  ],
  "apt_sources": [],
  "pending_count": 1
}
```

---

## GET `/v2/repositoryprofiles`

Retrieves a list of repository profiles.

Optional parameters:

- `limit`: The maximum number of results returned. Defaults to 1000.
- `offset`: The number of items to skip before starting to collect the result set.
- `search`: Profile names to search for.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/repositoryprofiles?limit=2&search=jammy" -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "count": 2,
  "results": [
    {
      "id": 6,
      "access_group": "global",
      "name": "jammy-repo-profile",
      "title": "Jammy Repo Profile",
      "description": "Updated description",
      "all_computers": false,
      "tags": ["jammy"],
      "pockets": [
        {
          "id": 2,
          "name": "jammy-security",
          "creation_time": "2025-09-24T23:10:47Z",
          "mode": "upload",
          "gpg_key": null,
          "components": ["main"],
          "architectures": ["amd64", "source"],
          "include_udeb": false,
          "apt_source_line": "deb http://10.1.77.207:8080/repository/onward/ubuntu jammy-security main",
          "series": {
            "name": "jammy",
            "creation_time": "2025-09-24T23:10:47Z"
          },
          "distribution": {
            "name": "ubuntu",
            "access_group": "global",
            "creation_time": "2025-09-24T23:10:47Z"
          },
          "package_count": 0
        }
      ],
      "apt_sources": [],
      "pending_count": 1
    },
    {
      "id": 7,
      "access_group": "global",
      "name": "jammy-dev-profile",
      "title": "Jammy Development Profile",
      "description": "Repository profile for jammy development systems",
      "all_computers": false,
      "tags": ["jammy", "dev"],
      "pockets": [],
      "apt_sources": [],
      "pending_count": 1
    }
  ],
  "next": "/api/v2/repositoryprofiles?limit=2&search=jammy&offset=2",
  "previous": null
}
```
