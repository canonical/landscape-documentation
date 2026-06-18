---
myst:
  html_meta:
    description: "REST API endpoints to search packages and vulnerabilities across a computer fleet in Landscape."
---

(reference-rest-api-package-search)=
# Package search

These endpoints search for packages and vulnerabilities across a computer selection. Both accept the same core set of filters and return per-package state counts aggregated across the targeted computers.

```{note}
TODO(srunde3): clarify point release version when finalized.

You must be running the latest point release of Landscape Server 26.04 or above to use the REST API for package management.

This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts.
```

### Filter state values

Several parameters use a tri-state filter. Accepted values are:

- `true` -- include only items matching this condition.
- `false` -- exclude items matching this condition.
- `unspecified` *(default)* -- do not filter on this condition.

## POST `/packages:search`

Search for packages across a computer selection.

### Request body parameters

**Required:**

- `computer_query`: A query string that selects the target computers (uses the same syntax as the `query` parameter on {ref}`reference-rest-api-computers`).

**Optional:**

- `text`: Free-text search string. Matches against all package fields, including description.
- `names`: Comma-separated list of package names to restrict the search to.
- `installed`: Filter by installed state. See [filter state values](#filter-state-values) above.
- `available`: Filter by availability in an APT source. See [filter state values](#filter-state-values) above.
- `upgrade`: Filter by whether a newer version is available. See [filter state values](#filter-state-values) above.
- `held`: Filter by whether the package is held on computers. See [filter state values](#filter-state-values) above.
- `security`: Filter by security upgrade availability. See [filter state values](#filter-state-values) above.
- `limit`: Maximum number of packages to return.
- `offset`: Offset into the result list (default: `0`).

### Response fields

- `packages`: List of matched packages.
  - `id`: Package ID.
  - `name`: Package name.
  - `summary`: Short description of the package.
  - `version`: Package version string.
  - `computers`: Number of computers matching the query that have this package.
    - `count`: Count of matching computers.
  - `usn`: Associated Ubuntu Security Notice, if any.
    - `id`: USN identifier.
    - `summary`: Optional USN summary.
  - `cves`: Associated CVEs, if any.
    - `id`: CVE identifier.
- `count`: Total number of packages matching the query.
- `next`: URL for the next page of results, or `null` if there are no more results.
- `prev`: URL for the previous page of results, or `null` if on the first page.

### Example

Example request:

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
      }
    }
  ],
  "count": 1,
  "next": null,
  "prev": null
}
```

## POST `/packages:search-vulnerabilities`

Search for packages with known security vulnerabilities across a computer selection. Returns packages matching the query and their associated with CVEs or Ubuntu Security Notices (USNs), if any.

### Request body parameters

**Required:**

- `computer_query`: A query string that selects the target computers (uses the same syntax as the `query` parameter on {ref}`reference-rest-api-computers`).

**Optional:**

- `text`: Free-text search string. Matches against all package fields, including description.
- `names`: Comma-separated list of package names to restrict the search to.
- `installed`: Filter by installed state. See [filter state values](#filter-state-values) above.
- `available`: Filter by availability in an APT source. See [filter state values](#filter-state-values) above.
- `upgrade`: Filter by whether a newer version is available. See [filter state values](#filter-state-values) above.
- `held`: Filter by whether the package is held on computers. See [filter state values](#filter-state-values) above.
- `security`: Filter by security upgrade availability. See [filter state values](#filter-state-values) above.
- `limit`: Maximum number of packages to return.
- `offset`: Offset into the result list (default: `0`).

### Response fields

- `packages`: List of packages with known vulnerabilities.
  - `id`: Package ID.
  - `name`: Package name.
  - `summary`: Short description of the package.
  - `version`: Package version string.
  - `computers`: Number of computers matching the query that have this package.
    - `count`: Count of matching computers.
  - `usn`: Associated Ubuntu Security Notice, if any.
    - `id`: USN identifier.
    - `summary`: Optional USN summary.
  - `cves`: Associated CVEs, if any.
    - `id`: CVE identifier.
- `count`: Total number of vulnerable packages matching the query.
- `next`: URL for the next page of results, or `null` if there are no more results.
- `prev`: URL for the previous page of results, or `null` if on the first page.

### Example

Example request:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/packages:search-vulnerabilities \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "installed": "true"
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
      "cves": [
        {"id": "CVE-2024-6387"},
        {"id": "CVE-2023-51385"}
      ],
      "usn": {
        "id": "USN-6859-1",
        "summary": null
      }
    },
    {
      "id": 3,
      "name": "curl",
      "summary": "command line tool for transferring data with URL syntax",
      "version": "8.5.0-2ubuntu10.6",
      "computers": {
        "count": 50
      },
      "cves": [
        {"id": "CVE-2024-2466"}
      ],
      "usn": {
        "id": "USN-6936-1",
        "summary": null
      }
    }
  ],
  "count": 2,
  "next": null,
  "prev": null
}
```
