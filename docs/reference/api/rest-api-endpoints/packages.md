(reference-rest-api-packages)=
# Packages

## GET `/packages`

Get a list of packages that have been reported to this Landscape account.

Query parameters:

- `query`: A query string used to select computers to query packages on. 
- `search`: A string to restrict the search to (optional). All fields are searched, not just those returned. (e.g., description)
- `names`: Restrict the search to these package names. Multiple names can be specified by numbering the names with `names.1`, `names.2`, etc.
- `installed`: If true only packages in the installed state will be returned, if false only packages not installed will be returned. If not given both installed and not installed packages will be returned.
    - **Note:** setting `installed` to `false` will only return computers where the given package is `available` but not `installed`, and will not work for arbitrary package names that have not been reported by Landscape Client. For example, using a non-existent package name for `names` will not return all computers.
- `available`: If true only packages in the available state will be returned, if false only packages not available will be returned. If not given both available and not available packages will be returned.
- `upgrade`: If true, only installable packages that are upgrades for an installed one are returned. If false, only installable packages that are not upgrades are returned. If not given, packages will be returned regardless of whether they are upgrades or not.
- `held`: If true, only installed packages that are held on computers are returned. If false, only packages that are not held on computers are returned. If not given, packages will be returned regardless of the held state.
- `security`: If true, only packages in the security upgrade state will be returned. If false, only packages not in the security upgrade state will be returned. If omitted, packages in both states will be returned.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

A package is considered installed if dpkg reports it as installed on the system.

A package is considered available if it can be fetched from an APT source. Note that this means that it’s possible for an installed package to be not available.

A package is considered an upgrade if it’s available and if it has a version higher than a non-held installed package with the same name.

For example, the following request queries computers that are tagged with 'server' and returns up to 2 reported packages whose names include 'python':

```bash
curl -sk -X GET "https://localhost/api/v2/packages?query=tag:server&search=python&limit=2" -H "Authorization: Bearer $JWT"
```

The handler returns a JSON serialized list of packages, with the list of computer IDs on which they are available, installed, or upgradable:

```json
{
    "count": 2064,
    "next": "/api/v2/packages?query=tag%3Aserver&search=python&limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "computers": [
                {
                    "available_version": "2.5.1-1ubuntu2",
                    "current_version": "2.5.1-1ubuntu2",
                    "id": 1,
                    "status": "installed"
                },
                {
                    "available_version": "2.5.1-1ubuntu2",
                    "current_version": "2.5.1-1ubuntu2",
                    "id": 2,
                    "status": "installed"
                },
                {
                    "available_version": "2.5.1-1ubuntu2",
                    "current_version": "2.5.1-1ubuntu2",
                    "id": 3,
                    "status": "installed"
                }
            ],
            "id": 1143,
            "name": "python",
            "summary": "An interactive high-level object-oriented language (default version)"
        },
        {
            "computers": [
                {
                    "available_version": "0.1.9-2ubuntu1",
                    "current_version": null,
                    "id": 1,
                    "status": "available"
                },
                {
                    "available_version": "0.1.9-2ubuntu1",
                    "current_version": null,
                    "id": 2,
                    "status": "available"
                },
                {
                    "available_version": "0.1.9-2ubuntu1",
                    "current_version": null,
                    "id": 3,
                    "status": "available"
                }
            ],
            "id": 411,
            "name": "python-2play",
            "summary": "peer-to-peer network game engine"
        }
    ]
}
```


