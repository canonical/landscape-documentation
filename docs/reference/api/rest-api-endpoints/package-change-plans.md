---
myst:
  html_meta:
    description: "REST API endpoints to create and manage package change plans in Landscape. Stage, inspect, and execute bulk package operations across a computer fleet."
---

(reference-rest-api-package-change-plans)=
# Package Change Plans

A package change plan stages a bulk package operation over a computer selection. Creating a plan resolves the selection into concrete computer/package pairs.

```{note}
You must be running Landscape Server 26.10 or later to use the REST API for package management.

This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts.
```

## POST `/package-change-plans`

Create a plan.

### Request body parameters

**Required:**

- `computer_query`: Query string selecting the target computers (same syntax as the `query` parameter on {ref}`reference-rest-api-computers`).

**Required--exactly one action config:**

- `install_config`: Install packages. See [`install_config`](install_config).
- `remove_config`: Remove packages. See [`remove_config`](remove_config).
- `hold_config`: Hold packages at their current version. See [`hold_config`](hold_config).
- `unhold_config`: Release held packages. See [`unhold_config`](unhold_config).
- `upgrade_config`: Upgrade packages. See [`upgrade_config`](upgrade_config).
- `change_version_config`: Move packages between specific versions. See [`change_version_config`](change_version_config).

### Response fields

- `id`: UUID of the new plan.
- `action`: The package operation. One of `install`, `remove`, `hold`, `unhold`, `upgrade`, `change_version`.
- `created_at`: ISO 8601 timestamp of when the plan was created.
- `item_count`: Number of computer/package pairs the plan targets.
- `executed_at`: ISO 8601 timestamp of execution, or `null` if the plan hasn't been executed.
- `activity_id`: ID of the activity created by execution, or `null` if the plan hasn't been executed.

### Limits

Creation returns `400` if the query selects more than 10,000 computers, if the plan references more than 50 packages, or if the account has created more than 100,000 plan items in the last 24 hours. Referencing a package ID that doesn't exist also returns `400`.

(install_config)=
### `install_config`

Installs packages. Exactly one of `by_ids` or `latest_by_names` must be set.

- `by_ids.package_ids`: Non-empty list of package IDs to install.
- `latest_by_names.package_names`: Non-empty list of package names; the latest available version of each is installed.

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

Removes packages. Exactly one of `by_ids` or `any_version_by_names` must be set.

- `by_ids.package_ids`: Non-empty list of package IDs to remove.
- `any_version_by_names.package_names`: Non-empty list of package names to remove, whichever version is installed.

Example request:

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

Holds packages at their current version so they aren't upgraded.

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

Releases held packages.

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

Upgrades packages. Exactly one of `select_by_ids` or `select_by_category` must be set.

- `select_by_ids.package_ids` *(required)*: Non-empty list of package IDs to upgrade.
- `select_by_category`: Upgrade every package in a category.
  - `category` *(required)*: One of `all` (every upgradable package, security included) or `all_security` (security upgrades only).
  - `excluded_package_ids`: Package IDs to leave out of the category (default: `[]`).

Example request--all security upgrades, minus one package:

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

Example request--upgrade specific packages:

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

Moves a package from one specific version to another, in either direction.

- `version_changes` *(required)*: Non-empty list of version changes.
  - `from_package_id` *(required)*: The version currently installed.
  - `to_package_id` *(required)*: The version to install instead.

The two IDs must differ and must be two versions of the same package. Otherwise the request returns `400`.

Example request:

```bash
curl -s -X POST https://landscape.canonical.com/api/v2/package-change-plans \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "computer_query": "tag:production",
    "change_version_config": {
      "version_changes": [
        {"from_package_id": 10, "to_package_id": 11}
      ]
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

Retrieve a plan's status and metadata. Unknown IDs return `404`.

Path parameters:

- `id`: The UUID of the plan.

Query parameters:

- None

Example request:

```bash
curl -s -X GET "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer $JWT"
```

Example response (200 OK), for a plan that has been executed:

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

Execute a plan, creating activities for every targeted computer.

Path parameters:

- `id`: The UUID of the plan.

Query parameters:

- None

Request body:

- None

This endpoint is idempotent: the second call returns the activity created by the first.

Example request:

```bash
curl -s -X POST "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000:execute" \
  -H "Authorization: Bearer $JWT"
```

Example response (200 OK):

```json
{
  "id": 42,
  "summary": "Install, hold and/or remove packages",
  "type": "ActivityGroup",
  "deliver_delay_window": 0,
  "creator": {
    "id": 1,
    "name": "John Smith",
    "email": "john@example.com"
  },
  "activity_status": "undelivered"
}
```

The response is the parent activity tracking the whole execution. Child activities are created per computer.

## GET `/package-change-plans/<id>/items`

List the computer/package pairs in a plan.

Path parameters:

- `id`: The UUID of the plan.

Query parameters:

- `computer_ids`: Comma-separated computer IDs to filter by.
- `computer_instance_name`: Case-insensitive prefix match on a computer's instance name.
- `limit`: Maximum number of items to return.
- `offset`: Offset into the result list (default: `0`).

Example request:

```bash
curl -s -X GET "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000/items" \
  -H "Authorization: Bearer $JWT"
```

Example response (200 OK)--`install` plan:

```json
{
  "action": "install",
  "items": [
    {
      "action": {
        "type": "install",
        "package": {
          "id": 101,
          "name": "openssh-server",
          "version": "1:9.6p1-3ubuntu13.5"
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

Example response (200 OK)--`change_version` plan:

```json
{
  "action": "change_version",
  "items": [
    {
      "action": {
        "type": "change_version",
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

- `action`: The plan's operation.
- `items`: The plan items.
  - `action`: A discriminated union keyed on `type`:
    - `install`, `remove`, `hold`, `unhold`: includes `package`, with `id`, `name`, and `version`.
    - `upgrade`, `change_version`: includes `from_package` and `to_package`, each with `id`, `name`, and `version`.
  - `computer`: The targeted computer.
    - `id`: ID of the computer.
    - `name`: Instance name of the computer.
- `count`: Total number of items.

(package-change-plan-exclusions)=
## GET `/package-change-plans/<id>/exclusions`

List the packages that couldn't be applied to some computers while resolving the plan, with the number of affected computers per package. These are the same aggregations returned in the `exclusions` field of `/summary`.

A plan references at most 50 packages, so this endpoint isn't paginated and takes no filters.

Path parameters:

- `id`: The UUID of the plan.

Query parameters:

- None

Example request:

```bash
curl -s -X GET "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000/exclusions" \
  -H "Authorization: Bearer $JWT"
```

Example response (200 OK):

```json
{
  "action": "upgrade",
  "exclusions": [
    {
      "package_name": "libthai0",
      "computer_count": 11
    },
    {
      "package_name": "nano",
      "computer_count": 11
    },
    {
      "package_name": "python-twisted-lore",
      "computer_count": 11
    }
  ]
}
```

Response fields:

- `action`: The plan's operation.
- `exclusions`: Excluded packages, sorted by name.
  - `package_name`: Name of the excluded package.
  - `computer_count`: Number of computers the package couldn't be applied to.

(package-change-plan-exclusion-detail)=
## GET `/package-change-plans/<id>/exclusions/<package_name>`

Get the computers a specific package couldn't be applied to.

Path parameters:

- `id`: The UUID of the plan.
- `package_name`: The excluded package name, exactly as returned by `/exclusions`.

Query parameters:

- `computer_ids`: Comma-separated computer IDs to filter by.
- `computer_instance_name`: Case-insensitive prefix match on a computer's instance name.

Example request--filter by instance name:

```bash
curl -s -G "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000/exclusions/nano" \
  -H "Authorization: Bearer $JWT" \
  --data-urlencode 'computer_instance_name=John'
```

Example response (200 OK):

```json
{
  "action": "upgrade",
  "package_name": "nano",
  "computers": [
    {
      "id": 4,
      "name": "John's Laptop"
    },
    {
      "id": 7,
      "name": "John's Windows Server"
    }
  ]
}
```

Response fields:

- `action`: The plan's operation.
- `package_name`: The excluded package name.
- `computers`: The computers the package couldn't be applied to, narrowed by the filters.
  - `id`: ID of the computer.
  - `name`: Instance name of the computer.

If the plan doesn't exist, or `package_name` isn't excluded by it, the endpoint returns `404`.

## GET `/package-change-plans/<id>/summary`

Get the distinct package actions in a plan, how many computers each applies to, and the packages that couldn't be resolved for some computers.

Path parameters:

- `id`: The UUID of the plan.

Query parameters:

- None

Example request:

```bash
curl -s -X GET "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000/summary" \
  -H "Authorization: Bearer $JWT"
```

Example response (200 OK):

```json
{
  "actions": [
    {
      "action": {
        "type": "install",
        "package": {
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

Response fields:

- `actions`: One entry per distinct package action in the plan.
  - `action`: The same discriminated union used by `/items`.
  - `computer_count`: Number of selected computers the action applies to.
- `exclusions`: Packages that couldn't be applied to some of the selected computers, aggregated by package name. Same data as [`/exclusions`](package-change-plan-exclusions).
  - `package_name`: Name of the excluded package.
  - `computer_count`: Number of selected computers excluded for that package.

## DELETE `/package-change-plans/<id>`

Delete a plan.

Path parameters:

- `id`: The UUID of the plan.

Query parameters:

- None

Request body:

- None

Example request:

```bash
curl -s -X DELETE "https://landscape.canonical.com/api/v2/package-change-plans/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer $JWT"
```

Response: `204 No Content` with an empty body.
