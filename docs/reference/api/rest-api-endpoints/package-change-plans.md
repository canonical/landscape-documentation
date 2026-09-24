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
- `state`: Current plan state. Known values are `pending`, `generating`, `ready`, `executing`, `executed`, `failed`, `expired`.
- `created_at`: ISO 8601 timestamp of when the plan was created.
- `expires_at`: ISO 8601 timestamp when a `ready` plan expires, or `null` in other states.
- `item_count`: Number of computer/package pairs the plan targets, or `null` if content hasn't been generated.
- `executed_at`: ISO 8601 timestamp of execution, or `null` if the plan hasn't been executed.
- `activity_id`: ID of the activity created by execution, or `null` if the plan hasn't been executed.

The plan is created in the `pending` state and will become `ready` once the plan is fully generated. Use `GET /package-change-plans/<id>` to poll until the plan is ready.

### Limits

Landscape enforces limits on the number of selected computers and the number of distinct resolved target package IDs. Requests to create change plans that exceed either of these limits return a `too_many_instances` or `too_many_packages` error.

TODO: add specific limits

### Quotas

Landscape SaaS applies an account quota based on plan items created in the previous 24 hours. There is no quota on self-hosted deployments. Requests to create change plans that exceed the daily quota will return a `quota_exceeded` error.

TODO: add specific limit

### Creation errors

- `400 Bad Request`: `invalid_computer_query`, `too_many_instances`, `too_many_packages`, `quota_exceeded`, `unknown_packages`, or `invalid_version_change`.

Error responses use the standard API error response:

```json
{
  "error": "invalid_computer_query",
  "message": "The computer query is invalid.",
  "detail": null
}
```

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
  "state": "pending",
  "created_at": "2026-01-15T10:00:00+00:00",
  "expires_at": null,
  "item_count": null,
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
  "state": "pending",
  "created_at": "2026-01-15T10:00:00+00:00",
  "expires_at": null,
  "item_count": null,
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
  "state": "pending",
  "created_at": "2026-01-15T10:00:00+00:00",
  "expires_at": null,
  "item_count": null,
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
  "state": "pending",
  "created_at": "2026-01-15T10:00:00+00:00",
  "expires_at": null,
  "item_count": null,
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
  "state": "pending",
  "created_at": "2026-01-15T10:00:00+00:00",
  "expires_at": null,
  "item_count": null,
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

Instances are excluded from the operation if:

- `from_package_id` is not installed or is currently held.
- `to_package_id` is not available or is already installed.

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
  "state": "pending",
  "created_at": "2026-01-15T10:00:00+00:00",
  "expires_at": null,
  "item_count": null,
  "executed_at": null,
  "activity_id": null
}
```

## GET `/package-change-plans/<id>`

Retrieve a plan's status and metadata. Unknown IDs return `404`.

Clients should stop status polling on `ready`, `executed`, `failed`, or `expired`. Treat `pending`, `generating`, `executing`, and unrecognized states as still in progress.

`executed` means the activity was created. Use the activity status to track package execution.

A plan expires 24 hours after entering `ready`. Plans in `executed`, `failed`, or `expired` are removed 24 hours after entering that state.

Items, summaries, and exclusions are readable only while a plan is `ready`, `executing`, or `executed`. These endpoints return `409` with `invalid_plan_state` and the current `state` otherwise.

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
  "state": "executed",
  "created_at": "2026-01-15T10:00:00+00:00",
  "expires_at": null,
  "item_count": 50,
  "executed_at": "2026-01-15T10:05:00+00:00",
  "activity_id": 42
}
```

### Retrieval errors

Unknown plan IDs return `404 Not Found` with the standard error object.

## POST `/package-change-plans/<id>:execute`

Execute a plan, creating activities for every targeted computer.

Path parameters:

- `id`: The UUID of the plan.

Query parameters:

- None

Request body:

- None

This endpoint is idempotent: the second call returns the activity created by the first.

Only `ready` and `executed` plans can be executed. Other states return `409` with `invalid_plan_state`; a `ready` plan with no items returns `409` with `empty_plan`. If another operation changes the state concurrently, execution returns `409` with `transition_conflict`; retry the request to act on the current state. If the retained activity no longer exists, an `executed` plan returns `404` with `activity_not_found` without dispatching another activity.

A dispatch failure marks the plan `failed` and returns `500` with `dispatch_timeout` or `internal_error`.

### Execution errors

- `409 Conflict`: `invalid_plan_state` when the plan cannot be executed, or `empty_plan` when a ready plan has no items.
- `404 Not Found`: `activity_not_found` when an executed plan's retained activity no longer exists.
- `500 Internal Server Error`: `dispatch_timeout` or `internal_error` when dispatch fails.

Each error is returned as the standard error object. An `invalid_plan_state` response also includes the plan's current `state`:

```json
{
  "error": "invalid_plan_state",
  "message": "The plan cannot be executed in its current state.",
  "detail": {
    "state": "generating"
  }
}
```

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
- `install`, `remove`, `hold`, `unhold`: Package ID to match for the corresponding plan action.
- `upgrade`: Destination package ID to match for an upgrade plan.
- `change_version`: JSON object with `from_package_id` and `to_package_id` to match for a change-version plan.
- `limit`: Maximum number of items to return (default: `50`, maximum: `1000`).
- `offset`: Offset into the result list (default: `0`).

Set at most one action filter, and use the filter matching the plan's action. Invalid or mismatched action filters return `400` with `filter_mismatch`.

### Item-list errors

- `400 Bad Request`: `filter_mismatch` for invalid or mismatched action filters.
- `404 Not Found`: when the plan does not exist.
- `409 Conflict`: `invalid_plan_state` when plan contents are unavailable in the plan's current state.

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
  "count": 1,
  "next": null,
  "previous": null
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
  "count": 1,
  "next": null,
  "previous": null
}
```

Response fields:

- `action`: The plan's operation.
- `items`: The plan items.
  - `action`: A discriminated union keyed on `type`:
    - `install`, `remove`, `hold`, `unhold`: includes `package`, with `id`, `name`, and `version`.
    - `upgrade`: includes `to_package`, with `id`, `name`, and `version`.
    - `change_version`: includes `from_package` and `to_package`, each with `id`, `name`, and `version`.
  - `computer`: The targeted computer.
    - `id`: ID of the computer.
    - `name`: Instance name of the computer.
- `count`: Total number of items.
- `next`: The link to the next page.
- `previous`: The link to the previous page.

(package-change-plan-exclusions)=
## GET `/package-change-plans/<id>/exclusions`

List the packages that couldn't be applied to some computers while resolving the plan, with the number of affected computers per package. These are the same aggregations returned in the `exclusions` field of `/summary`.

This endpoint isn't paginated and takes no filters.

### Exclusion-list errors

- `404 Not Found`: when the plan does not exist.
- `409 Conflict`: `invalid_plan_state` when plan contents are unavailable in the plan's current state.

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

### Exclusion-detail errors

- `404 Not Found`: when the plan does not exist or `package_name` is not excluded by the plan.
- `409 Conflict`: `invalid_plan_state` when plan contents are unavailable in the plan's current state.

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

### Summary errors

- `404 Not Found`: when the plan does not exist.
- `409 Conflict`: `invalid_plan_state` when plan contents are unavailable in the plan's current state.

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

Delete a plan in any state.

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

Deleting an unknown or already-deleted plan also returns `204`.
