---
myst:
  html_meta:
    description: "REST API endpoints to search packages and upgrades across a computer fleet in Landscape."
---

(reference-rest-api-package-search)=
# Package Search

These endpoints search for packages and available upgrades across a computer selection.

```{note}
You must be running Landscape Server 26.10 or later to use the REST API for package management.

This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts.
```

(package-search-filter-states)=
## Filter states

Some parameters are tri-state filters. Accepted values are:

- `"true"`: keep only packages matching the condition.
- `"false"`: keep only packages not matching the condition.
- `"unspecified"` *(default)*: don't filter on it.

## POST `/packages:search`

Search packages across a computer selection.

### Request body parameters

**Required:**

- `computer_query`: Query string selecting the target computers (same syntax as the `query` parameter on {ref}`reference-rest-api-computers`).

**Optional:**

- `text`: Matches against package name, summary, and description.
- `names`: Package names as one comma-separated string, such as `"curl,nginx"`. Each name takes an optional version constraint using `=`, `>>`, `<<`, `>=`, or `<=`, such as `"curl>=8.5"`.
- `installed`: Whether the package is installed on a selected computer. See [filter states](package-search-filter-states).
- `available`: Whether the package is available from an APT source.
- `upgrade`: Whether a newer version is available.
- `held`: Whether the package is held.
- `security`: Whether the package comes from a security pocket.
- `limit`: Maximum number of packages to return (default: `100`).
- `offset`: Offset into the result list (default: `0`).

### Response fields

- `packages`: Matched packages.
  - `id`: Package ID.
  - `name`: Package name.
  - `summary`: Short description.
  - `version`: Version string.
  - `computers.count`: Number of selected computers that have this package.
- `count`: Total number of matching packages.
- `next`: The link to the next page.
- `prev`: The link to the previous page.


### Example

Example request--installed packages matching "ssh":

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/packages:search \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "text": "ssh",
    "installed": "true",
    "limit": 2
  }'
```

Example response (200 OK):

```json
{
  "packages": [
    {
      "id": 1,
      "name": "openssh-server",
      "summary": "secure shell (SSH) server, for secure access from remote machines",
      "version": "1:9.6p1-3ubuntu13.5",
      "computers": {
        "count": 50
      },
    }
  ],
  "count": 1,
  "next": null,
  "prev": null,
}
```

## POST `/packages:search-upgrades`

Search available (latest) package upgrades across a computer selection.

### Request body parameters

**Required:**

- `computer_query`: Query string selecting the target computers (same syntax as the `query` parameter on {ref}`reference-rest-api-computers`).

**Optional:**

- `text`: Matches against package name, summary, and description.
- `names`: Package names as one comma-separated string, such as `"curl,nginx"`. Each name takes an optional version constraint using `=`, `>>`, `<<`, `>=`, or `<=`, such as `"curl>=8.5"`.
- `security`: Whether the upgrade comes from a security pocket. See [filter states](package-search-filter-states).
- `limit`: Maximum number of packages to return (default: `100`).
- `offset`: Offset into the result list (default: `0`).

### Response fields

Same shape as `/packages:search`, where each package is the upgrade candidate rather than the installed version.

- `packages`: Upgradable packages.
  - `id`: Package ID of the new version.
  - `name`: Package name.
  - `summary`: Short description.
  - `version`: Version string of the new version.
  - `computers.count`: Number of selected computers that can take this upgrade.
- `count`: Total number of matching upgrades.
- `next`: The link to the next page.
- `prev`: The link to the previous page.

### Example

Example request--security upgrades only:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/packages:search-upgrades \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "security": "true"
  }'
```

Example response (200 OK):

```json
{
  "packages": [
    {
      "id": 2,
      "name": "openssh-server",
      "summary": "secure shell (SSH) server, for secure access from remote machines",
      "version": "1:9.6p1-3ubuntu13.9",
      "computers": {
        "count": 50
      },
    },
    {
      "id": 4,
      "name": "curl",
      "summary": "command line tool for transferring data with URL syntax",
      "version": "8.5.0-2ubuntu10.6",
      "computers": {
        "count": 31
      },
    }
  ],
  "count": 2,
  "next": null,
  "prev": null,
}
```
