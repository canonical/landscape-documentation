---
myst:
  html_meta:
    description: "REST API endpoints for employee authentication and access to associated Landscape computers."
---

(reference-rest-api-employee-access)=
# Employee access

These endpoints provide employee authentication and access to data associated with the authenticated employee. They require the employee management feature to be enabled. See {ref}`reference-rest-api-employees` for employee administration endpoints.

```{note}
This feature is available from Landscape server `25.10` onwards, and only on self-hosted deployments. It is not intended for {ref}`Quickstart <how-to-quickstart-installation>` deployments.

To enable employee management features in self-hosted Landscape, add:

```ini
[features]
employee_management = true
```

## GET `/employee-access/auth/start`

Start the employee OIDC authorization code flow. The response contains the URL to which the user agent must be redirected for authentication.

Query parameters:

- `id`: The ID of the account OIDC configuration to use. If omitted, use standalone OIDC.
- `attach_code`: The attach code that binds the login attempt to an Ubuntu installer session.
- `return_to`: The path to return the employee to after authentication.
- `external`: Whether `return_to` is outside the new dashboard. Defaults to false.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/employee-access/auth/start?return_to=/employee-access/computers" \
  -H "Authorization: Bearer $JWT"
```

Example response (`200 OK`):

```json
{
  "location": "https://idp.example.com/authorize?client_id=landscape&redirect_uri=https%3A%2F%2Flandscape.canonical.com%2Fapi%2Fv2%2Femployee-access%2Fauth%2Fcallback&state=..."
}
```

## GET `/employee-access/login/methods`

Get the login methods available to employees for the current deployment and account.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/employee-access/login/methods
```

Example response (`200 OK`):

```json
{
  "oidc": {
    "available": true,
    "configurations": []
  },
  "standalone_oidc": {
    "available": true,
    "enabled": true
  },
  "ubuntu_one": {
    "available": false,
    "enabled": false
  },
  "password": {
    "available": false,
    "enabled": false
  },
  "pam": {
    "available": false,
    "enabled": false
  }
}
```

`available` indicates whether a login method is set by the deployment configuration. `enabled` indicates whether an available method may be used for the account.

## GET `/employee-access/me`

Get information about the currently authenticated employee. An unauthenticated request returns an empty object with `200 OK`.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/employee-access/me \
  -H "Authorization: Bearer $JWT"
```

Example response for an authenticated employee (`200 OK`):

```json
{
  "current_account": "onward",
  "email": "alex@example.com",
  "name": "Alex Example",
  "accounts": [
    {
      "default": true,
      "name": "onward",
      "title": "Onward, Inc.",
      "subdomain": "onward",
      "classic_dashboard_url": "https://landscape.canonical.com/account/onward"
    }
  ],
  "has_password": false,
  "token": "<employee-jwt>",
  "return_to": null,
  "attach_code": null,
  "invitation_id": null
}
```

## GET `/employee-access/computers`

List the computers associated with the authenticated employee.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/employee-access/computers \
  -H "Authorization: Bearer $JWT"
```

Example response (`200 OK`):

```json
{
  "count": 1,
  "results": [
    {
      "id": 23,
      "title": "Alex's workstation",
      "hostname": "workstation-23",
      "comment": "",
      "total_memory": 16777216,
      "total_swap": 8388608,
      "reboot_required_flag": false,
      "update_manager_prompt": "normal",
      "clone_id": null,
      "last_exchange_time": "2026-09-22T10:15:00Z",
      "last_ping_time": "2026-09-22T10:15:00Z",
      "tags": ["desktop"],
      "access_group": "global",
      "distribution": "24.04",
      "cloud_instance_metadata": {},
      "vm_info": null,
      "container_info": null,
      "default_child": null,
      "ubuntu_pro_info": null,
      "grouped_hardware": null,
      "provisioning_info": {
        "provisioned_at": "2026-09-22T10:15:00Z",
        "autoinstall": "default.yaml"
      }
    }
  ]
}
```

The list includes only computers associated with the authenticated employee. `provisioning_info` is `null` if the computer has not been provisioned through an autoinstall file.

## GET `/employee-access/computers/<int:computer_id>`

Get a computer associated with the authenticated employee.

Path parameters:

- `computer_id`: The ID of the computer associated with the employee.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/employee-access/computers/23 \
  -H "Authorization: Bearer $JWT"
```

Example response (`200 OK`):

```json
{
  "id": 23,
  "title": "Alex's workstation",
  "hostname": "workstation-23",
  "comment": "",
  "total_memory": 16777216,
  "total_swap": 8388608,
  "reboot_required_flag": false,
  "update_manager_prompt": "normal",
  "clone_id": null,
  "last_exchange_time": "2026-09-22T10:15:00Z",
  "tags": ["desktop"],
  "access_group": "global",
  "distribution": "24.04",
  "cloud_instance_metadata": {},
  "vm_info": null,
  "container_info": null,
  "default_child": null,
  "ubuntu_pro_info": null,
  "grouped_hardware": {
    "product": "Example workstation"
  },
  "provisioning_info": {
    "provisioned_at": "2026-09-22T10:15:00Z",
    "autoinstall": "default.yaml"
  }
}
```

The endpoint returns `404 Not Found` if the computer does not exist or is not associated with the authenticated employee.
