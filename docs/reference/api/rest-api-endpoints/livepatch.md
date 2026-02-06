(reference-rest-api-livepatch)=
# Livepatch

## GET /`computers/<computer_id>/livepatch/info`

Gets the Livepatch information reported by Landscape Client

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- None

Example request:

```
curl -X GET "https://landscape.canonical.com/api/v2/computers/29/livepatch/info" \
-H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "livepatch_info": {
      "humane": {
          "error": "",
          "output": {
              "kernel": "5.15.0-100.110-generic",
              "kernel state": "✓ kernel series 5.15 is covered by Livepatch",
              "machine id": "5a8061f3c51942ab906085377bb91634",
              "patch state": "✓ all applicable livepatch modules inserted",
              "patch version": 104.1,
              "server check-in": "succeeded",
              "tier": "updates (Free usage; This machine beta tests new patches.)"
          },
          "return_code": 0
      },
      "json": {
          "error": "",
          "output": {
              "Architecture": "amd64",
              "Boot-Time": "2024-08-19T02:14:28Z",
              "CPU-Model": "Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz",
              "Client-Version": "10.8.3",
              "Cloud-Enabled": {
                  "az": "",
                  "cloud": "lxd",
                  "cloud-enabled": true,
                  "region": ""
              },
              "Machine-Id": "5a8061f3c51942ab906085377bb91634",
              "Status": [
                  {
                      "Kernel": "5.15.0-100.110-generic",
                      "Livepatch": {
                          "CheckState": "checked",
                          "Fixes": [
                              {
                                  "Bug": "",
                                  "Description": "",
                                  "Name": "cve-2023-6270",
                                  "Patched": true
                              },
                              {
                                  "Bug": "",
                                  "Description": "",
                                  "Name": "cve-2024-1086",
                                  "Patched": true
                              },
                              {
                                  "Bug": "",
                                  "Description": "",
                                  "Name": "cve-2024-26581",
                                  "Patched": true
                              },
                              {
                                  "Bug": "",
                                  "Description": "",
                                  "Name": "cve-2024-26597",
                                  "Patched": true
                              }
                          ],
                          "State": "applied",
                          "Version": "104.1"
                      },
                      "Running": true,
                      "Supported": "supported",
                      "UpgradeRequiredDate": "2025-03-07"
                  }
              ],
              "tier": "updates"
          },
          "return_code": 0
      }
  },
  "ubuntu_pro_livepatch_service_info": {
      "available": "yes",
      "blocked_by": [],
      "description": "Canonical Livepatch service",
      "description_override": null,
      "entitled": "yes",
      "name": "livepatch",
      "status": "enabled",
      "status_details": "",
      "warning": null
  },
  "ubuntu_pro_reboot_required_info": {
      "error": "",
      "output": {
          "livepatch_enabled": true,
          "livepatch_enabled_and_kernel_patched": true,
          "livepatch_state": "applied",
          "livepatch_support": "supported",
          "reboot_required": "no",
          "reboot_required_packages": {
              "kernel_packages": null,
              "standard_packages": null
          }
      }
  }
}
```

## GET `computers/<computer_id>/livepatch/kernel`

Gets the kernel information from `apt` and the Livepatch status from Landscape

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- None

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/computers/29/livepatch/kernel" \
-H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "downgrades": [
      {
          "fixes": null,
          "id": 75473,
          "name": "linux-image-virtual",
          "version": "5.15.0.25.27",
          "version_rounded": "5.15.0.25"
      }
  ],
  "installed": {
      "fixes": null,
      "id": 239017,
      "name": "linux-image-virtual",
      "version": "5.15.0.100.97",
      "version_rounded": "5.15.0.100"
  },
  "message": "",
  "smart_status": "Kernel upgrade available",
  "upgrades": [
      {
          "fixes": {
          "cves": ["CVE-2023-52629", "CVE-2023-52760"],
          "name": "6974-1",
          "release_date": "2024-11-20",
          "summary": "Vulnerability of USN-6974-1",
      },
          "id": 229832,
          "name": "linux-image-virtual",
          "version": "5.15.0.118.118",
          "version_rounded": "5.15.0.118"
      }
  ]
}
```

## POST `/computers/<computer_id>/kernel/upgrade`

Upgrades the kernel package to the one requested

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- `kernel_package_id`: The package id to upgrade to. See the [`computers/<computer_id>/livepatch/kernel` endpoint](#get-computerscomputer_idlivepatchkernel).

Optional parameters:

- `reboot_after`: A boolean indicating whether to reboot (default value `False`)
- `deliver_after`: A time in the future to deliver the package activity
- `deliver_delay_window`: Randomize delivery within the given time frame (minutes)

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/29/kernel/upgrade" \
   -H "Authorization: Bearer $JWT" \
   -d "kernel_package_id=1122"
```

Example response:

```json
{
  "activity_status": null,
  "approval_time": null,
  "completion_time": null,
  "creation_time": "2024-11-21T23:36:04Z",
  "creator": {
      "email": "john@example.com",
      "id": 1,
      "name": "John Smith"
  },
  "deliver_delay_window": 0,
  "id": 2221,
  "parent_id": null,
  "result_code": null,
  "result_text": null,
  "summary": "Upgrade kernel package",
  "type": "ActivityGroup"
}
```

## POST `/computers/<computer_id>/kernel/downgrade`

Downgrades the kernel package to the one requested

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- `kernel_package_id`: The package id to downgrade to. See [`computers/<computer_id>/livepatch/kernel` endpoint](#get-computerscomputer_idlivepatchkernel).

Optional parameters:

- `reboot_after`: A boolean indicating whether to reboot (default value False)
- `deliver_after`: A time in the future to deliver the package activity
- `deliver_delay_window`: Randomize delivery within the given time frame (minutes)

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/29/kernel/downgrade" \
   -H "Authorization: Bearer $JWT" \
   -d "kernel_package_id=1122"
```

Example response:

```json
{
  "activity_status": null,
  "approval_time": null,
  "completion_time": null,
  "creation_time": "2024-11-21T23:36:04Z",
  "creator": {
      "email": "john@example.com",
      "id": 1,
      "name": "John Smith"
  },
  "deliver_delay_window": 0,
  "id": 2221,
  "parent_id": null,
  "result_code": null,
  "result_text": null,
  "summary": "Downgrade kernel package",
  "type": "ActivityGroup"
}
```
