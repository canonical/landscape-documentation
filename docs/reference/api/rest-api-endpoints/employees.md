---
myst:
  html_meta:
    description: "REST API endpoints for managing Landscape employees and their associated computers. Create, update, offboard, and retrieve employee records."
---

(reference-rest-api-employees)=
# Employees

The employee endpoints manage employee records and the computers associated with them. These endpoints require the employee management feature to be enabled.

```{note}
This feature is available from Landscape server `25.10` onwards, and only on self-hosted deployments. It is not intended for {ref}`Quickstart <how-to-quickstart-installation>` deployments.

To enable employee management features in self-hosted Landscape, add:

```ini
[features]
employee_management = true
```

The employee management feature is intended to be used with autoinstall provisioning. See {ref}`how-to-ubuntu-installer-configure-landscape-deployment` to configure the deployment and enable employee management and autoinstall provisioning.

## GET `/employees`

List employees in the account.

Query parameters:

- `limit`: The maximum number of employees to return.
- `offset`: The offset inside the list of employees.
- `search`: Return employees whose names match the search string.
- `is_active`: If true, return active employees. If false, return inactive employees.
- `issuer_ids`: A comma-separated list of OIDC issuer IDs. Return only employees associated with one of these issuers.
- `with_computers`: If true, include the computers associated with each employee. Defaults to false.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/employees?is_active=true&with_computers=true" \
  -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "count": 1,
  "results": [
    {
      "id": 12,
      "name": "Alex Example",
      "email": "alex@example.com",
      "issuer_id": 4,
      "subject": "alex-example",
      "is_active": true,
      "autoinstall_file": null,
      "computers": [
        {
          "access_group": "global",
          "archived": false,
          "clone_id": 0,
          "cloud_init": {},
          "cloud_instance_metadata": {},
          "comment": "",
          "container_info": "",
          "default_child": "",
          "distribution": "24.04",
          "distribution_info": {},
          "hostname": "workstation-23",
          "id": 23,
          "last_exchange_time": "2026-09-22T10:15:00Z",
          "last_ping_time": "2026-09-22T10:15:00Z",
          "livepatch_info": {},
          "num_child": 0,
          "reboot_required_flag": false,
          "tags": ["desktop"],
          "title": "Alex's workstation",
          "total_memory": 16777216,
          "total_swap": 8388608,
          "ubuntu_pro_info": {},
          "ubuntu_pro_reboot_required_info": {},
          "updated_manager_prompt": "",
          "vm_info": ""
        }
      ]
    }
  ],
  "next": null,
  "previous": null
}
```

Each object in `computers` contains the fields shown in the example. The field is `null` unless `with_computers` is true.

## POST `/employees`

Create an employee record. Employees are usually created automatically during authentication; use this endpoint when an employee record must be created explicitly.

Required request body parameters:

- `name`: The employee's name.
- `email`: The employee's email address.
- `issuer_id`: The ID of the configured OIDC issuer for the employee.
- `subject`: The employee's subject identifier from the OIDC issuer.

Optional request body parameters:

- `is_active`: Whether the employee is active. Defaults to true.

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/employees \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{
    "name": "Alex Example",
    "email": "alex@example.com",
    "issuer_id": 4,
    "subject": "alex-example"
  }'
```

Example response (`201 Created`):

```json
{
  "id": 12,
  "name": "Alex Example",
  "email": "alex@example.com",
  "issuer_id": 4,
  "subject": "alex-example",
  "is_active": true,
  "autoinstall_file": null,
  "computers": null
}
```

## GET `/employees/<int:id>`

Get an employee by ID.

Path parameters:

- `id`: The employee ID.

Query parameters:

- `with_computers`: If true, include the computers associated with the employee. Defaults to false.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/employees/12?with_computers=true" \
  -H "Authorization: Bearer $JWT"
```

Example response (`200 OK`):

```json
{
  "id": 12,
  "name": "Alex Example",
  "email": "alex@example.com",
  "issuer_id": 4,
  "subject": "alex-example",
  "is_active": true,
  "autoinstall_file": null,
  "computers": null
}
```

The response contains:

- `id`: The employee ID.
- `name`: The employee's name.
- `email`: The employee's email address.
- `issuer_id`: The ID of the employee's OIDC issuer.
- `subject`: The employee's subject identifier from the OIDC issuer.
- `is_active`: Whether the employee is active.
- `autoinstall_file`: Always `null`. This field is reserved for future use.
- `computers`: The associated computers, or `null` unless `with_computers` is true.

All employees currently receive the account's default autoinstall file. The API does not yet support different autoinstall files for individual employees, so `autoinstall_file` is always returned as `null` and is reserved for future use.

## PATCH `/employees/<int:id>`

Modify an employee record. Include only the fields to change. Sending an empty object, or setting fields to `null`, leaves those fields unchanged.

Path parameters:

- `id`: The employee ID.

Optional request body parameters:

- `name`: The employee's new name.
- `email`: The employee's new email address.
- `issuer_id`: The ID of the employee's new OIDC issuer.
- `subject`: The employee's new subject identifier from the OIDC issuer.
- `is_active`: Whether the employee is active.

Example request:

```bash
curl -X PATCH https://landscape.canonical.com/api/v2/employees/12 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"is_active": false}'
```

Example response (`200 OK`):

```json
{
  "id": 12,
  "name": "Alex Example",
  "email": "alex@example.com",
  "issuer_id": 4,
  "subject": "alex-example",
  "is_active": false,
  "autoinstall_file": null,
  "computers": null
}
```

## DELETE `/employees/<int:id>`

Delete an employee record.

Path parameters:

- `id`: The employee ID.

Example request:

```bash
curl -X DELETE https://landscape.canonical.com/api/v2/employees/12 \
  -H "Authorization: Bearer $JWT"
```

The endpoint returns `204 No Content`.

## POST `/employees/<int:id>/offboard`

Offboard an employee. This deactivates the employee and can optionally sanitize and/or remove the computers associated with the employee.

Path parameters:

- `id`: The employee ID.

Optional request body parameters:

- `sanitize_instances`: If true, sanitize all computers associated with the employee. Defaults to false.
- `remove_instances`: If true, remove all computers associated with the employee from Landscape. Defaults to false.

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/employees/12/offboard \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"sanitize_instances": true}'
```

Example response (`202 Accepted`):

```json
{
  "activity_status": "succeeded",
  "approval_time": null,
  "completion_time": null,
  "creation_time": "2026-09-22T10:15:00Z",
  "creator": {
    "email": "admin@example.com",
    "id": 1,
    "name": "Admin Example"
  },
  "deliver_delay_window": 0,
  "id": 115,
  "parent_id": null,
  "result_code": null,
  "result_text": null,
  "summary": "Offboarding employee",
  "type": "ActivityGroup"
}
```

## POST `/employees/<int:employee_id>/computers`

Associate an employee with a computer.

Path parameters:

- `employee_id`: The employee ID.

Required request body parameters:

- `computer_id`: The computer ID.

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/employees/12/computers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"computer_id": 23}'
```

Example response (`201 Created`):

```json
{
  "employee_id": 12,
  "computer_id": 23
}
```

## DELETE `/employees/<int:employee_id>/computers/<int:computer_id>`

Disassociate an employee from a computer.

Path parameters:

- `employee_id`: The employee ID.
- `computer_id`: The computer ID.

Example request:

```bash
curl -X DELETE https://landscape.canonical.com/api/v2/employees/12/computers/23 \
  -H "Authorization: Bearer $JWT"
```

The endpoint returns `204 No Content`.
