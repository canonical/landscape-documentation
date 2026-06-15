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
  - `package_state_counts`: Counts of computers in each state for this package.
    - `available`: Number of computers where the package is available.
    - `held`: Number of computers where the package is held.
    - `upgrade_available`: Number of computers where an upgrade is available.
    - `installed`: Number of computers where the package is installed.
- `computer_selection_stats`: Aggregate stats for the computer selection.
  - `total_count`: Total number of computers matched by `computer_query`.
  - `no_results_count`: Number of matched computers that returned no packages.
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
      "package_state_counts": {
        "available": 50,
        "held": 2,
        "upgrade_available": 10,
        "installed": 48
      }
    }
  ],
  "computer_selection_stats": {
    "total_count": 50,
    "no_results_count": 2
  },
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

- `vulnerable_packages`: List of packages with known vulnerabilities.
  - `package`: Package details (same fields as in `/packages:search`).
  - `cve_ids`: List of CVE identifiers associated with this package (e.g. `CVE-2024-6387`).
  - `usn_ids`: List of Ubuntu Security Notice identifiers associated with this package (e.g. `USN-6859-1`).
- `computer_selection_stats`: Aggregate stats for the computer selection.
  - `total_count`: Total number of computers matched by `computer_query`.
  - `no_results_count`: Number of matched computers that returned no packages.
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
  "vulnerable_packages": [
    {
      "package": {
        "id": 1,
        "name": "openssh-server",
        "summary": "secure shell (SSH) server, for secure access from remote machines",
        "version": "1:9.6p1-3ubuntu13.5",
        "package_state_counts": {
          "available": 50,
          "held": 2,
          "upgrade_available": 10,
          "installed": 48
        }
      },
      "cve_ids": ["CVE-2024-6387", "CVE-2023-51385"],
      "usn_ids": ["USN-6859-1", "USN-6560-1"]
    },
    {
      "package": {
        "id": 3,
        "name": "curl",
        "summary": "command line tool for transferring data with URL syntax",
        "version": "8.5.0-2ubuntu10.6",
        "package_state_counts": {
          "available": 50,
          "held": 1,
          "upgrade_available": 3,
          "installed": 49
        }
      },
      "cve_ids": ["CVE-2024-2466"],
      "usn_ids": ["USN-6936-1"]
    }
  ],
  "computer_selection_stats": {
    "total_count": 50,
    "no_results_count": 2
  },
  "count": 2,
  "next": null,
  "prev": null
}
```
