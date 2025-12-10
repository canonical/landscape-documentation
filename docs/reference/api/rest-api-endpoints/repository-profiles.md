(reference-rest-api-repository-profiles)=
# Repository Profiles

## POST `/v2/repositoryprofiles`

Creates a new repository profile, including its associations, APT sources, and pockets.

Required parameters:

- `title`: Title of the repository profile.

Optional parameters:

- `description`: Description of the repository profile.
- `access_group`: Name of the access group in which to create the profile. Defaults to `"global"`.
- `tags`: Tags the profile will be associated with.
- `all_computers`: If `true`, the profile is associated with all computers. Defaults to `false`.
- `apt_sources`: The IDs of the APT sources to add.
- `pockets`: The IDs of the pockets to add.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/repositoryprofiles" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Noble Repo Profile",
    "description": "Repository profile for noble instances",
    "tags": ["noble"],
    "apt_sources": [1, 2],
    "pockets": [3]
}'
```

Example response:

```json
{
  "id": 6,
  "access_group": "global",
  "name": "noble-repo-profile",
  "title": "Noble Repo Profile",
  "description": "Repository profile for noble instances",
  "all_computers": false,
  "tags": ["noble"],
  "pockets": [
    {
      "id": 3,
      "name": "noble-updates",
      "creation_time": "2025-09-24T23:10:47Z",
      "mode": "mirror",
      "gpg_key": null,
      "components": ["main"],
      "architectures": ["amd64"],
      "include_udeb": false,
      "apt_source_line": "deb http://10.1.77.207:8080/repository/onward/ubuntu noble-updates main",
      "series": {
        "name": "noble",
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

- `profile_name`: The URL-safe identifier (`name`) for the repository profile.

Required parameters:

- `title`: Title of the repository profile.

Optional parameters:

- `description`: Description of the repository profile.
- `access_group`: Name of the access group in which the profile is stored.
- `tags`: Tags with which the profile will be associated.
- `all_computers`: If `true`, the profile is associated with all computers. Defaults to `false`.
- `apt_sources`: The IDs of the APT sources to add.
- `pockets`: The IDs of the pockets to add.

Example request:

```bash
curl -X PUT "https://landscape.canonical.com/api/v2/repositoryprofiles/noble-repo-profile" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Noble Repo Profile",
    "description": "Updated description",
    "tags": ["noble"],
    "apt_sources": [4],
    "pockets": [2]
}'
```

Example response:

```json
{
  "id": 6,
  "access_group": "global",
  "name": "noble-repo-profile",
  "title": "Noble Repo Profile",
  "description": "Updated description",
  "all_computers": false,
  "tags": ["noble"],
  "pockets": [
    {
      "id": 2,
      "name": "noble-security",
      "creation_time": "2025-09-24T23:10:47Z",
      "mode": "upload",
      "gpg_key": null,
      "components": ["main"],
      "architectures": ["amd64", "source"],
      "include_udeb": false,
      "apt_source_line": "deb http://10.1.77.207:8080/repository/onward/ubuntu noble-security main",
      "series": {
        "name": "noble",
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
curl -X GET "https://landscape.canonical.com/api/v2/repositoryprofiles?limit=2&search=noble" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "count": 2,
  "results": [
    {
      "id": 6,
      "access_group": "global",
      "name": "noble-repo-profile",
      "title": "Noble Repo Profile",
      "description": "Updated description",
      "all_computers": false,
      "tags": ["noble"],
      "pockets": [
        {
          "id": 2,
          "name": "noble-security",
          "creation_time": "2025-09-24T23:10:47Z",
          "mode": "upload",
          "gpg_key": null,
          "components": ["main"],
          "architectures": ["amd64", "source"],
          "include_udeb": false,
          "apt_source_line": "deb http://10.1.77.207:8080/repository/onward/ubuntu noble-security main",
          "series": {
            "name": "noble",
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
      "name": "noble-dev-profile",
      "title": "Noble Development Profile",
      "description": "Repository profile for noble development systems",
      "all_computers": false,
      "tags": ["noble", "dev"],
      "pockets": [],
      "apt_sources": [],
      "pending_count": 1
    }
  ],
  "next": "/api/v2/repositoryprofiles?limit=2&search=noble&offset=2",
  "previous": null
}
```
