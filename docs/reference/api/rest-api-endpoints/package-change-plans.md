---
myst:
  html_meta:
    description: "REST API endpoints to create and manage package change plans in Landscape. Stage, inspect, and execute bulk package operations across a computer fleet."
---

(reference-rest-api-package-change-plans)=
# Package change plans

The following endpoints are for creating, viewing, and deleting package change plans. Package change plans let you stage and review a bulk package operation across a fleet of computers before executing it.

```{note}
TODO(srunde3): clarify point release version when finalized.

You must be running the latest point release of Landscape Server 26.04 or above to use the REST API for package management.

This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts.
```

## POST `/package-change-plans`

Create a new package change plan.

### Request body parameters

**Required:**

- `computer_query`: A query string that selects the target computers (uses the same syntax as the `query` parameter on {ref}`reference-rest-api-computers`).

**Required--exactly one action config:**

- `install_config`: Install packages. See [install_config](#install_config) below.
- `remove_config`: Remove packages. See [remove_config](#remove_config) below.
- `hold_config`: Hold packages at their current version. See [hold_config](#hold_config) below.
- `unhold_config`: Release held packages. See [unhold_config](#unhold_config) below.
- `upgrade_config`: Upgrade packages. See [upgrade_config](#upgrade_config) below.
- `change_version_config`: Change a package to a specific version. See [change_version_config](#change_version_config) below.

### Response fields

- `id`: UUID of the newly created plan.
- `state`: Lifecycle state of the plan. One of `created`, `started`, `completed`, `failed`.
- `action`: The package operation. One of `install`, `remove`, `hold`, `unhold`, `upgrade`, `change_version`.
- `created_at`: ISO 8601 timestamp of when the plan was created.
- `item_count`: Number of computer/package pairs targeted by the plan.

(install_config)=
### `install_config`

Installs packages on the target computers. Exactly one of `by_ids` or `latest_by_names` must be set.

- `by_ids.package_ids`: List of package IDs to install.
- `latest_by_names.package_names`: List of package names whose latest available versions will be installed.

Example request--install by name:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "install_config": {
      "latest_by_names": {
        "package_names": ["openssh-server", "curl"]
      }
    }
  }'
```

Example request--install by ID:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "install_config": {
      "by_ids": {
        "package_ids": [101, 102]
      }
    }
  }'
```

Example response (201 Created):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "created",
  "action": "install",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 50
}
```

(remove_config)=
### `remove_config`

Removes packages from the target computers. Exactly one of `by_ids` or `any_version_by_names` must be set.

- `by_ids.package_ids`: List of package IDs to remove.
- `any_version_by_names.package_names`: List of package names to remove (any installed version).

Example request--remove by name:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "remove_config": {
      "any_version_by_names": {
        "package_names": ["curl"]
      }
    }
  }'
```

Example response (201 Created):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "created",
  "action": "remove",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 12
}
```

(hold_config)=
### `hold_config`

Holds packages at their current version, preventing automatic upgrades.

- `package_ids` *(required)*: Non-empty list of package IDs to hold.

Example request:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "hold_config": {
      "package_ids": [101, 102]
    }
  }'
```

Example response (201 Created):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "created",
  "action": "hold",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 20
}
```

(unhold_config)=
### `unhold_config`

Releases held packages, allowing them to be upgraded again.

- `package_ids` *(required)*: Non-empty list of package IDs to unhold.

Example request:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "unhold_config": {
      "package_ids": [101, 102]
    }
  }'
```

Example response (201 Created):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "created",
  "action": "unhold",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 20
}
```

(upgrade_config)=
### `upgrade_config`

Upgrades packages on the target computers. Exactly one of `select_by_ids` or `select_by_category` must be set.

- `select_by_ids`: Upgrade specific packages by ID.
  - `package_ids` *(required)*: Non-empty list of package IDs to upgrade.
- `select_by_category`: Upgrade all packages in a given category, optionally excluding selected IDs.
  - `category` *(required)*: Which packages to upgrade. One of:
    - `all`: all upgradable packages, including security packages.
    - `all_security`: only upgradable security packages.
  - `excluded_package_ids`: Package IDs to exclude from the category (default: `[]`).

Example request--upgrade all security packages:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "upgrade_config": {
      "select_by_category": {
        "category": "all_security"
      }
    }
  }'
```

Example request--upgrade all security packages, excluding specific IDs:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "upgrade_config": {
      "select_by_category": {
        "category": "all_security",
        "excluded_package_ids": [99]
      }
    }
  }'
```

Example request--upgrade specific packages by ID:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "upgrade_config": {
      "select_by_ids": {
        "package_ids": [101, 102]
      }
    }
  }'
```

Example response (201 Created):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "created",
  "action": "upgrade",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 85
}
```

(change_version_config)=
### `change_version_config`

Changes targeted computers to a specific version of a package.

- `package_ids` *(required)*: Non-empty list of package IDs whose version should be changed.

Example request:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "change_version_config": {
      "package_ids": [101]
    }
  }'
```

Example response (201 Created):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "created",
  "action": "change_version",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 10
}
```

## GET `/package-change-plans/<id>`

Retrieve the status and metadata of a specific plan.

Path parameters:

- `id`: The UUID of the package change plan.

Query parameters:

- None

Example request:

```bash
curl -s -X GET "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

Example response (200 OK):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "created",
  "action": "install",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 50
}
```

## POST `/package-change-plans/<id>:execute`

Execute a package change plan, creating activities for every targeted computer.

Path parameters:

- `id`: The UUID of the package change plan.

Query parameters:

- None

Request body:

- None

Example request:

```bash
curl -s -X POST "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000:execute" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

Example response (200 OK):

```json
{
  "id": 42,
  "summary": "Install packages on selected computers",
  "type": "PackageChangePlanActivity",
  "deliver_delay_window": 0,
  "creator": {
    "id": 1,
    "name": "John Smith",
    "email": "john@example.com"
  },
  "activity_status": "pending"
}
```

The response is a parent activity that tracks the overall execution. Child activities are created for each targeted computer.

## GET `/package-change-plans/<id>/items`

List the individual computer/package pairs within a plan.

Path parameters:

- `id`: The UUID of the package change plan.

Query parameters:

- `computer_ids`: Comma-separated list of computer IDs to filter by (optional).
- `package_ids`: Comma-separated list of package IDs to filter by (optional).
- `computer_instance_name`: Filter by a computer's instance name (optional).
- `limit`: Maximum number of results to return (optional).
- `offset`: Offset into the result list (default: `0`).

Example request:

```bash
curl -s -X GET "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000/items?limit=2" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

Example response (200 OK):

```json
{
  "items": [
    {
      "package_id": 101,
      "computer": {
        "id": 5,
        "name": "web-server-01"
      },
      "action": "install"
    },
    {
      "package_id": 102,
      "computer": {
        "id": 7,
        "name": "db-server-01"
      },
      "action": "install"
    }
  ],
  "count": 2
}
```

Response fields:

- `items`: List of plan items.
  - `package_id`: ID of the package targeted by this item.
  - `computer`: The computer targeted by this item.
    - `id`: ID of the computer.
    - `name`: Name of the computer.
  - `action`: The package operation for this item.
- `count`: Total number of items returned.

## GET `/package-change-plans/<id>/summary`

Get a per-package summary of applicable and non-applicable target states across the computer selection.

Path parameters:

- `id`: The UUID of the package change plan.

Query parameters:

- None

Example request:

```bash
curl -s -X GET "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000/summary" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

Example response (200 OK):

```json
{
  "summary_items": [
    {
      "package_id": 1,
      "package_name": "openssh-server",
      "package_version": "1:9.6p1-3ubuntu13.5",
      "package_state_counts": [
        {
          "state": "applicable",
          "count": 48
        },
        {
          "state": "not_applicable",
          "count": 2
        }
      ]
    }
  ]
}
```

Response fields:

- `summary_items`: One entry per package included in the plan.
  - `package_id`: ID of the package.
  - `package_name`: Name of the package.
  - `package_version`: Version string of the package.
  - `package_state_counts`: List of state/count pairs describing the distribution of target states across the selected computers.
    - `state`: Either `applicable` or `not_applicable`.
    - `count`: Number of computers in this state.

`applicable` means the operation will be performed on that computer. `not_applicable` means the operation will not.

## DELETE `/package-change-plans/<id>`

Delete a package change plan.

Path parameters:

- `id`: The UUID of the package change plan.

Query parameters:

- None

Request body:

- None

Example request:

```bash
curl -s -X DELETE "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

Response: 204 No Content (empty body).
