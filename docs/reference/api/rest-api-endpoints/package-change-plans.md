---
myst:
  html_meta:
    description: "REST API endpoints to create and manage package change plans in Landscape. Stage, inspect, and execute bulk package operations across a computer fleet."
---

(reference-rest-api-package-change-plans)=
# Package change plans

The following endpoints are for creating, viewing, and deleting package change plans. Package change plans let you stage and review a bulk package operation across a fleet of computers before executing it.

```{note}
You must be running  Landscape Server 26.10 or later to use the REST API for package management.

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
- `action`: The package operation. One of `install`, `remove`, `hold`, `unhold`, `upgrade`, `change_version`.
- `created_at`: ISO 8601 timestamp of when the plan was created.
- `item_count`: Number of computer/package pairs targeted by the plan.
- `executed_at`: ISO 8601 timestamp of when the plan was executed, or `null` if it has not been executed yet.
- `activity_id`: ID of the activity created by executing the plan, or `null` if it has not been executed yet.

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
  "action": "install",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 50,
  "executed_at": null,
  "activity_id": null
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
  "action": "remove",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 12,
  "executed_at": null,
  "activity_id": null
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
  "action": "hold",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 20,
  "executed_at": null,
  "activity_id": null
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
  "action": "unhold",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 20,
  "executed_at": null,
  "activity_id": null
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
  "action": "upgrade",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 85,
  "executed_at": null,
  "activity_id": null
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
  "action": "change_version",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 10,
  "executed_at": null,
  "activity_id": null
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
  "action": "install",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 50,
  "executed_at": null,
  "activity_id": null
}
```

Once the plan has been executed (see below), `executed_at` and `activity_id` will be populated:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "action": "install",
  "created_at": "2026-01-15T10:00:00+00:00",
  "item_count": 50,
  "executed_at": "2026-01-15T10:05:00+00:00",
  "activity_id": 42
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
- `computer_instance_name`: Filter by a computer's instance name (optional).
- `limit`: Maximum number of results to return (optional).
- `offset`: Offset into the result list (default: `0`).

**Action filters:** at most one of the following may be set. Each filter must match the plan's own `action`; using a filter for a different action returns a `400` error.

- `install`: A package ID. Restricts results to the item installing this package.
- `remove`: A package ID. Restricts results to the item removing this package.
- `hold`: A package ID. Restricts results to the item holding this package.
- `unhold`: A package ID. Restricts results to the item unholding this package.
- `upgrade`: A package ID (the target/new package). Restricts results to the item upgrading to this package.
- `change_version`: A JSON-encoded object with `from_package_id` and `to_package_id`, e.g. `{"from_package_id": 10, "to_package_id": 11}`. Restricts results to the item performing this version change.

Example request--filter by computer and action:

```bash
curl -s -X GET "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000/items?computer_ids=5,7&install=101" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

Example request--filter a `change_version` plan by the version change:

```bash
curl -s -G "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000/items" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  --data-urlencode 'change_version={"from_package_id": 10, "to_package_id": 11}'
```

Example response (200 OK)--`install` plan:

```json
{
  "action": "install",
  "items": [
    {
      "action": {
        "install": {
          "id": 101,
          "name": "openssh-server",
          "version": "1:9.6p1-3ubuntu13.5"
        }
      },
      "computer": {
        "id": 5,
        "name": "web-server-01"
      }
    },
    {
      "action": {
        "install": {
          "id": 102,
          "name": "curl",
          "version": "8.5.0-2ubuntu10.6"
        }
      },
      "computer": {
        "id": 7,
        "name": "db-server-01"
      }
    }
  ],
  "count": 2
}
```

Example response (200 OK)--`change_version` plan:

```json
{
  "action": "change_version",
  "items": [
    {
      "action": {
        "change_version": {
          "from_package": {
            "id": 10,
            "name": "vim",
            "version": "2:8.2"
          },
          "to_package": {
            "id": 11,
            "name": "vim",
            "version": "2:9.0"
          }
        }
      },
      "computer": {
        "id": 5,
        "name": "web-server-01"
      }
    }
  ],
  "count": 1
}
```

Response fields:

- `action`: The plan's package operation. One of `install`, `remove`, `hold`, `unhold`, `upgrade`, `change_version`.
- `items`: List of plan items.
  - `action`: An object with exactly one key--matching the plan's `action`--describing the package(s) involved in this item.
    - For `install`, `remove`, `hold`, `unhold`, and `upgrade`, the value is the package: `id`, `name`, and `version`.
    - For `change_version`, the value has `from_package` and `to_package`, each with `id`, `name`, and `version`.
  - `computer`: The computer targeted by this item.
    - `id`: ID of the computer.
    - `name`: Name of the computer.
- `count`: Total number of items returned.

## GET `/package-change-plans/<id>/summary`

Get an action-focused summary of a plan: the distinct package actions it will perform and how many computers each applies to, plus counts for computers that could not apply the action on a given package.

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

Example response (200 OK)--`install` plan:

```json
{
  "actions": [
    {
      "action": {
        "install": {
          "id": 101,
          "name": "openssh-server",
          "version": "1:9.6p1-3ubuntu13.5"
        }
      },
      "computer_count": 48
    }
  ],
  "exclusions": [
    {
      "package_name": "curl",
      "computer_count": 2
    }
  ]
}
```

Example response (200 OK)--`change_version` plan:

```json
{
  "actions": [
    {
      "action": {
        "change_version": {
          "from_package": {
            "id": 10,
            "name": "vim",
            "version": "2:8.2"
          },
          "to_package": {
            "id": 11,
            "name": "vim",
            "version": "2:9.0"
          }
        }
      },
      "computer_count": 12
    }
  ],
  "exclusions": []
}
```

Response fields:

- `actions`: One entry per distinct package action in the plan.
  - `action`: An object with exactly one key--matching the plan's `action`--describing the package(s) involved.
    - For `install`, `remove`, `hold`, `unhold`, and `upgrade`, the value is the package: `id`, `name`, and `version`.
    - For `change_version`, the value has `from_package` and `to_package`, each with `id`, `name`, and `version`.
  - `computer_count`: Number of selected computers this action applies to.
- `exclusions`: Packages that could not be resolved for some computers, grouped by package name.
  - `package_name`: Name of the excluded package. Exclusions are grouped by name (not ID), so multiple versions of the same package may be aggregated together.
  - `computer_count`: Number of selected computers excluded for this package.

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
