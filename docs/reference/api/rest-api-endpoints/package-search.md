---
myst:
  html_meta:
    description: "REST API endpoints to search packages and upgrades across a computer fleet in Landscape."
---

(reference-rest-api-package-search)=
# Package search

These endpoints search for packages and available upgrades across a computer selection. Use them to find the package IDs you pass to {ref}`reference-rest-api-package-change-plans`.

```{note}
You must be running Landscape Server 26.10 or later to use the REST API for package management.

This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts. If it isn't enabled for your account, these endpoints return `404`.
```

Both endpoints are `POST` because the computer selection query is sent in the request body.

(package-search-filter-states)=
## Filter states

Some parameters are tri-state filters. Accepted values are:

- `true`: keep only packages matching the condition.
- `false`: keep only packages not matching the condition.
- `unspecified` *(default)*: don't filter on the condition.

## Pagination

Both endpoints page with `limit` and `offset`. `limit` defaults to `100` and cannot exceed `500`; a larger value returns `400`. `count` is the total number of matches, ignoring `limit` and `offset`. The `next` and `prev` fields are reserved for future use and are currently always `null`.

## POST `/packages:search`

Search packages across a computer selection.

### Request body parameters

**Required:**

- `computer_query`: Query string selecting the target computers (same syntax as the `query` parameter on {ref}`reference-rest-api-computers`).

**Optional:**

- `text`: Free-text search. Matches package names and descriptions.
- `names`: Comma-separated list of package names to restrict the search to.
- `installed`: Whether the package is installed on a selected computer. See [filter states](package-search-filter-states).
- `available`: Whether the package is available from an APT source. See [filter states](package-search-filter-states).
- `upgrade`: Whether a newer version is available. See [filter states](package-search-filter-states).
- `held`: Whether the package is held. See [filter states](package-search-filter-states).
- `security`: Whether the package comes from a security pocket. See [filter states](package-search-filter-states).
- `limit`: Maximum number of packages to return (default: `100`, maximum: `500`).
- `offset`: Offset into the result list (default: `0`).

### Response fields

- `packages`: Matched packages.
  - `id`: Package ID.
  - `name`: Package name.
  - `summary`: Short description.
  - `version`: Version string.
  - `computers.count`: Number of selected computers that have this package.
  - `usn`: Associated Ubuntu Security Notice, or `null`.
    - `id`: USN identifier.
    - `summary`: USN summary, if available.
  - `cves`: Associated CVEs.
    - `id`: CVE identifier.
- `count`: Total number of matching packages.
- `next`: Always `null`. Reserved.
- `prev`: Always `null`. Reserved.

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
      "usn": {
        "id": "USN-6859-1",
        "summary": null
      },
      "cves": [
        {"id": "CVE-2024-6387"}
      ]
    }
  ],
  "count": 1,
  "next": null,
  "prev": null
}
```

## POST `/packages:search-upgrades`

Search available package upgrades across a computer selection.

### Request body parameters

**Required:**

- `computer_query`: Query string selecting the target computers (same syntax as the `query` parameter on {ref}`reference-rest-api-computers`).

**Optional:**

- `text`: Free-text search. Matches package names and descriptions.
- `names`: Comma-separated list of package names to restrict the search to.
- `security`: Whether the upgrade comes from a security pocket. See [filter states](package-search-filter-states).
- `limit`: Maximum number of packages to return (default: `100`, maximum: `500`).
- `offset`: Offset into the result list (default: `0`).

### Response fields

Same shape as `/packages:search`, where each package is the upgrade candidate rather than the installed version. This endpoint doesn't return security metadata yet, so `usn` is always `null` and `cves` is always empty.

- `packages`: Upgradable packages.
  - `id`: Package ID of the new version.
  - `name`: Package name.
  - `summary`: Short description.
  - `version`: Version string of the new version.
  - `computers.count`: Number of selected computers that can take this upgrade.
- `count`: Total number of matching upgrades.
- `next`: Always `null`. Reserved.
- `prev`: Always `null`. Reserved.

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
      "usn": null,
      "cves": []
    },
    {
      "id": 4,
      "name": "curl",
      "summary": "command line tool for transferring data with URL syntax",
      "version": "8.5.0-2ubuntu10.6",
      "computers": {
        "count": 31
      },
      "usn": null,
      "cves": []
    }
  ],
  "count": 2,
  "next": null,
  "prev": null
}
```
