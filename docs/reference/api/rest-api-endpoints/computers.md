(reference-rest-api-computers)=

# Computers

## GET `/computers`

Get information on a list of computers associated with the account.

Path parameters:

- None

Query parameters:

- `query`: A query string with space-separated tokens used to filter the returned computers. Words provided as search parameters are treated as keywords, matching the hostname or the computer title. Selector prefixes can be used to further customize the search:
  - `tag`: Search for computers with the specified tag.
  - `distribution`: Search for computers running a specific Ubuntu release (can be code name like -`jammy` or version number like `22.04`).
  - `hostname`: Search for computers with the exact hostname.
  - `title`: Search for computers with the exact title.
  - `alert`: Search for computers with a named alert being active. Alerts can be one of the following: `package-upgrades`, `security-upgrades`, `package-profiles`, `package-reporter`, `computer-offline`, `computer-reboot`.
  - `access-group`: Search for computers that belong to the access group with the specified name.
  - `id`: Select the specified numeric computer ID.
  - `mac`: Search for computers with the specified MAC address, which can be a substring of the full address.
  - `ip`: Search for computers with the specified IP address, which can be a substring of the full address. No network classing is done.
  - `search`: Select computers based on the result of the named search.
  - `needs:reboot`: Search for computers that have the reboot required flag set. Note that with this particular criteria, the only possible value for it is the text `reboot`.
  - `license-id`: Search for computers licensed to the specified `license-id`.
  - `needs:license` OR `license-id:none`: Search for computers that do not have a Landscape license, and, as a result, are not managed.
  - `annotation`: Search for computers which define the specified annotation key. Optionally specify `annotation:<key>:<string>` which will only return computers whose key matches and value also contains the `<string>` specified.
  - `profile:<profile-type>:<profile-id>`: Instances associated with the specified profile. The `<profile-type>` must be one of `security`, `script`, `repository`, `package`, `upgrade`, `reboot`, `removal`, or `wsl`. The `<profile-id>` is the database id of the profile.
  - `profile:security:<profile-id>:<status>`: Instances associated with the specified USG security profile with the indicated last audit result. The `<profile-id>` is the database id of the profile. The `<status>` must be one of `pass`, `fail`, or `in-progress`.
  - `profile:wsl:<profile-id>:<status>`: Instances associated with the specified WSL Child Instance Profile. The `<profile-id>` is the database id of the profile. The `<status>` must either be `compliant` or `noncompliant`.
  - `OR`: Search for computers matching term A or term B. `OR` must be in all-caps.
  - `NOT`: search for computers not matching the next term. `NOT` must be in all-caps.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.
- `with_network`: If true, include the details of all network devices attached to the computer.
- `with_hardware`: If true, include the details of all hardware information known.
- `with_annotations`: If true, include the details of all custom annotation information known.
- `with_wsl_profiles`: If true, include WSL profiles associated with Windows computers. Defaults to false.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/computers?limit=1 -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "count": 13,
  "results": [
    {
      "id": 1,
      "title": "Application Server 1",
      "comment": "",
      "hostname": "appserv1",
      "total_memory": 1024,
      "total_swap": 1024,
      "reboot_required_flag": false,
      "update_manager_prompt": "normal",
      "clone_id": null,
      "secrets_name": null,
      "last_exchange_time": null,
      "last_ping_time": "2024-02-07T21:21:41Z",
      "tags": [
        "lucid",
        "server",
        "webfarm"
      ],
      "access_group": "server",
      "distribution": "10.04",
      "cloud_instance_metadata": {},
      "vm_info": null,
      "container_info": null,
      "ubuntu_pro_info": null,
      "is_wsl_instance": false,
      "children": [],
      "parent": null
    }
  ],
  "next": "https://landscape.canonical.com/api/v2/computers?limit=1&offset=1",
  "previous": null
}
```

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/computers?query=id:1%20OR%20id:2 -H "Authorization: Bearer $JWT" -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "title": "Application Server 1",
      "comment": "",
      "hostname": "appserv1",
      "total_memory": 1024,
      "total_swap": 1024,
      "reboot_required_flag": false,
      "update_manager_prompt": "normal",
      "clone_id": null,
      "secrets_name": null,
      "last_exchange_time": null,
      "last_ping_time": "2024-07-10T23:32:16Z",
      "tags": [
        "lucid",
        "server",
        "webfarm"
      ],
      "access_group": "server",
      "distribution": "10.04",
      "cloud_instance_metadata": {},
      "vm_info": null,
      "container_info": null,
      "default_child": null,
      "ubuntu_pro_info": null,
      "is_wsl_instance": false,
      "children": [],
      "is_default_child": null,
      "parent": null
    },
    {
      "id": 2,
      "title": "Application Server 2",
      "comment": "",
      "hostname": "appserv2",
      "total_memory": 1024,
      "total_swap": 1024,
      "reboot_required_flag": false,
      "update_manager_prompt": "normal",
      "clone_id": null,
      "secrets_name": null,
      "last_exchange_time": null,
      "last_ping_time": "2024-07-10T23:31:16Z",
      "tags": [
        "precise",
        "server",
        "webfarm"
      ],
      "access_group": "server",
      "distribution": "12.04",
      "cloud_instance_metadata": {},
      "vm_info": null,
      "container_info": null,
      "default_child": null,
      "ubuntu_pro_info": null,
      "is_wsl_instance": false,
      "children": [],
      "is_default_child": null,
      "parent": null
    }
  ],
  "next": null,
  "previous": null
}
```

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/computers/?query=profile:wsl:1:compliant&with_wsl_profiles=true -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "count": 1,
  "results": [
    {
      "id": 6,
      "title": "Jane's Windows Laptop",
      "comment": "",
      "hostname": "jane",
      "total_memory": 1024,
      "total_swap": 1024,
      "reboot_required_flag": false,
      "update_manager_prompt": "normal",
      "clone_id": null,
      "secrets_name": null,
      "last_exchange_time": null,
      "last_ping_time": "2024-02-07T21:16:41Z",
      "tags": [
        "laptop",
        "windows"
      ],
      "access_group": "server",
      "distribution": "10 / 11",
      "cloud_instance_metadata": {},
      "vm_info": null,
      "container_info": null,
      "ubuntu_pro_info": null,
      "is_wsl_instance": false,
      "children": [
        {
          "id": 11,
          "title": "Bionic WSL",
          "comment": "",
          "hostname": "bionic-wsl",
          "total_memory": 1024,
          "total_swap": 1024,
          "reboot_required_flag": false,
          "update_manager_prompt": "normal",
          "clone_id": null,
          "secrets_name": null,
          "last_exchange_time": null,
          "last_ping_time": "2024-02-07T21:11:41Z",
          "tags": [
            "bionic",
            "wsl"
          ],
          "access_group": "global",
          "distribution": "18.04",
          "cloud_instance_metadata": {},
          "vm_info": null,
          "container_info": null,
          "ubuntu_pro_info": null,
          "is_wsl_instance": true
        },
        {
          "id": 12,
          "title": "Focal WSL",
          "comment": "",
          "hostname": "focal-wsl",
          "total_memory": 1024,
          "total_swap": 1024,
          "reboot_required_flag": false,
          "update_manager_prompt": "normal",
          "clone_id": null,
          "secrets_name": null,
          "last_exchange_time": null,
          "last_ping_time": "2024-02-07T21:10:41Z",
          "tags": [
            "focal",
            "wsl"
          ],
          "access_group": "global",
          "distribution": "20.04",
          "cloud_instance_metadata": {},
          "vm_info": null,
          "container_info": null,
          "ubuntu_pro_info": null,
          "is_wsl_instance": true
        }
      ],
      "parent": null,
      "wsl_profiles": [
        {
          "id": 1,
          "name": "Bionic WSL",
          "title": "Bionic Profile",
          "type": "wsl"
        },
        {
          "id": 2,
          "name": "Focal WSL",
          "title": "Focal Profile",
          "type": "wsl"
        }
      ]
    }
  ],
  "next": null,
  "previous": null
}
```

## GET `/computers/<int:computer_id>`

Get information on a specific computer in the account.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- `with_annotations`: If true, include the details of all custom annotation information known.
- `with_grouped_hardware`: If true, include the details of all hardware information known, grouped by hardware  type.
- `with_hardware`: If true, include the details of all hardware information known.
- `with_network`: If true, include the details of all network devices attached to the computer.
- `with_profiles`: If true, include details about all profiles the computer is associated with.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/computers/1?with_profiles=true -H "Authorization: Bearer $JWT" 
```

Example response:

```json
{
  "access_group": "server",
  "archived": false,
  "children": [],
  "clone_id": null,
  "cloud_init": {
    "availability_zone": "us-east-1"
  },
  "cloud_instance_metadata": {},
  "comment": "",
  "container_info": null,
  "default_child": null,
  "distribution": "10.04",
  "distribution_info": {
    "code_name": "lucid",
    "description": "Ubuntu 10.04 LTS",
    "distributor": "Ubuntu",
    "release": "10.04"
  },
  "employee_id": null,
  "hostname": "appserv1",
  "id": 1,
  "is_default_child": null,
  "is_wsl_instance": false,
  "last_exchange_time": null,
  "last_ping_time": "2025-06-27T21:17:37Z",
  "livepatch_info": null,
  "num_child": 0,
  "parent": null,
  "profiles": [
    {
      "id": 7,
      "name": "desktop-packages",
      "title": "Desktop Packages",
      "type": "package"
    },
    {
      "id": 7,
      "name": "engineering-repos",
      "title": "Engineering Repos",
      "type": "repository"
    },
    {
      "id": 22,
      "name": "one-month-removal",
      "title": "One Month Removal",
      "type": "removal"
    }
    {
      "id": 4,
      "name": "server-packages",
      "title": "Server Packages",
      "type": "package",
    },
  ],
  "reboot_required_flag": false,
  "secrets_name": null,
  "tags": [
    "lucid",
    "server",
    "webfarm"
  ],
  "title": "Application Server 1",
  "total_memory": 1024,
  "total_swap": 1024,
  "ubuntu_pro_info": null,
  "ubuntu_pro_reboot_required_info": null,
  "update_manager_prompt": "normal",
  "vm_info": null
}
```

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/computers/1?with_grouped_hardware=true -H "Authorization: Bearer $JWT" 
```

Example output:

```json
{
  "id": 1,
  "title": "Application Server 1",
  "comment": "",
  "hostname": "appserv1",
  "total_memory": 1024,
  "total_swap": 1024,
  "reboot_required_flag": false,
  "update_manager_prompt": "normal",
  "clone_id": null,
  "secrets_name": null,
  "last_exchange_time": null,
  "last_ping_time": "2024-07-10T23:32:16Z",
  "tags": [
    "lucid",
    "server",
    "webfarm"
  ],
  "access_group": "server",
  "distribution": "10.04",
  "cloud_instance_metadata": {},
  "vm_info": null,
  "container_info": null,
  "default_child": null,
  "ubuntu_pro_info": null,
  "is_wsl_instance": false,
  "children": [],
  "is_default_child": null,
  "parent": null,
  "grouped_hardware": {
    "cpu": [
      {
        "architecture": "64 b'bits'",
        "cache": {
          "L1 cache": "32 KiB"
        },
        "clock_speed": "2.66 GHz",
        "flags": [
          {
            "code": "fpu",
            "title": "[mathematical co-processor]"
          },
          {
            "code": "fpu_exception",
            "title": "[FPU exceptions reporting]"
          },
          {
            "code": "wp",
            "title": "wp"
          },
          {
            "code": "vme",
            "title": "[virtual mode extensions]"
          },
          {
            "code": "de",
            "title": "[debugging extensions]"
          },
          {
            "code": "pse",
            "title": "[page size extensions]"
          },
          {
            "code": "tsc",
            "title": "[time stamp counter]"
          },
          {
            "code": "msr",
            "title": "[model-specific registers]"
          },
          {
            "code": "pae",
            "title": "[4GB+ memory addressing (Physical Address Extension)]"
          },
          {
            "code": "mce",
            "title": "[machine check exceptions]"
          },
          {
            "code": "cx8",
            "title": "[compare and exchange 8-byte]"
          },
          {
            "code": "apic",
            "title": "[on-chip advanced programmable interrupt controller (APIC)]"
          },
          {
            "code": "sep",
            "title": "[fast system calls]"
          },
          {
            "code": "mtrr",
            "title": "[memory type range registers]"
          },
          {
            "code": "pge",
            "title": "[page global enable]"
          },
          {
            "code": "mca",
            "title": "[machine check architecture]"
          },
          {
            "code": "cmov",
            "title": "[conditional move instruction]"
          },
          {
            "code": "pat",
            "title": "[page attribute table]"
          },
          {
            "code": "pse36",
            "title": "[36-bit page size extensions]"
          },
          {
            "code": "clflush",
            "title": "clflush"
          },
          {
            "code": "dts",
            "title": "[debug trace and EMON store MSRs]"
          },
          {
            "code": "acpi",
            "title": "[thermal control (ACPI)]"
          },
          {
            "code": "mmx",
            "title": "[multimedia extensions (MMX)]"
          },
          {
            "code": "fxsr",
            "title": "[fast floating point save/restore]"
          },
          {
            "code": "sse",
            "title": "[streaming SIMD extensions (SSE)]"
          },
          {
            "code": "sse2",
            "title": "[streaming SIMD extensions (SSE2)]"
          },
          {
            "code": "ss",
            "title": "[self-snoop]"
          },
          {
            "code": "ht",
            "title": "[HyperThreading]"
          },
          {
            "code": "tm",
            "title": "[thermal interrupt and status]"
          },
          {
            "code": "pbe",
            "title": "[pending break event]"
          },
          {
            "code": "syscall",
            "title": "[fast system calls]"
          },
          {
            "code": "nx",
            "title": "[no-execute bit (NX)]"
          },
          {
            "code": "x86-64",
            "title": "[64bits extensions (x86-64)]"
          },
          {
            "code": "constant_tsc",
            "title": "constant_tsc"
          },
          {
            "code": "arch_perfmon",
            "title": "arch_perfmon"
          },
          {
            "code": "pebs",
            "title": "pebs"
          },
          {
            "code": "bts",
            "title": "bts"
          },
          {
            "code": "rep_good",
            "title": "rep_good"
          },
          {
            "code": "nopl",
            "title": "nopl"
          },
          {
            "code": "aperfmperf",
            "title": "aperfmperf"
          },
          {
            "code": "pni",
            "title": "pni"
          },
          {
            "code": "dtes64",
            "title": "dtes64"
          },
          {
            "code": "monitor",
            "title": "monitor"
          },
          {
            "code": "ds_cpl",
            "title": "ds_cpl"
          },
          {
            "code": "vmx",
            "title": "vmx"
          },
          {
            "code": "smx",
            "title": "smx"
          },
          {
            "code": "est",
            "title": "est"
          },
          {
            "code": "tm2",
            "title": "tm2"
          },
          {
            "code": "ssse3",
            "title": "ssse3"
          },
          {
            "code": "cx16",
            "title": "cx16"
          },
          {
            "code": "xtpr",
            "title": "xtpr"
          },
          {
            "code": "pdcm",
            "title": "pdcm"
          },
          {
            "code": "sse4_1",
            "title": "sse4_1"
          },
          {
            "code": "xsave",
            "title": "xsave"
          },
          {
            "code": "lahf_lm",
            "title": "lahf_lm"
          },
          {
            "code": "tpr_shadow",
            "title": "tpr_shadow"
          },
          {
            "code": "vnmi",
            "title": "vnmi"
          },
          {
            "code": "flexpriority",
            "title": "flexpriority"
          },
          {
            "code": "cpufreq",
            "title": "[CPU Frequency scaling]"
          }
        ],
        "model": "Intel(R) Core(TM)2 Duo CPU     P8800  @ 2.66GHz",
        "vendor": "Intel Corp."
      },
      {
        "architecture": "Not available",
        "cache": {
          "L1 cache": "32 KiB"
        },
        "clock_speed": "2.66 GHz",
        "flags": [
          {
            "code": "cpufreq",
            "title": "[CPU Frequency scaling]"
          }
        ],
        "model": "Not available",
        "vendor": "Intel(R) Corporation"
      }
    ],
    "display": {
      "model": "G96 [GeForce 9600M GT]",
      "vendor": "nVidia Corporation"
    },
    "memory": {
      "size": "8 GiB RAM"
    },
    "multimedia": {
      "model": "MCP79 High Definition Audio",
      "vendor": "nVidia Corporation"
    },
    "network": [
      {
        "description": "Ethernet interface",
        "ip": "Not available",
        "mac": "00:25:4b:d0:76:92",
        "product": "MCP79 Ethernet",
        "vendor": "nVidia Corporation"
      },
      {
        "description": "Wireless interface",
        "ip": "192.168.1.102",
        "mac": "00:25:00:49:ef:80",
        "product": "BCM4322 802.11a/b/g/n Wireless LAN Controller",
        "vendor": "Broadcom Corporation"
      }
    ],
    "pci": [
      {
        "attached_devices": [],
        "description": "PCI bridge",
        "model": "MCP79 PCI Bridge",
        "vendor": "nVidia Corporation"
      },
      {
        "attached_devices": [
          {
            "vendor": "nVidia Corporation",
            "model": "G96 [GeForce 9600M GT]",
            "description": "VGA compatible controller"
          }
        ],
        "description": "PCI bridge",
        "model": "MCP79 PCI Express Bridge",
        "vendor": "nVidia Corporation"
      },
      {
        "attached_devices": [
          {
            "vendor": "Broadcom Corporation",
            "model": "BCM4322 802.11a/b/g/n Wireless LAN Controller",
            "description": "Wireless interface"
          }
        ],
        "description": "PCI bridge",
        "model": "MCP79 PCI Express Bridge",
        "vendor": "nVidia Corporation"
      },
      {
        "attached_devices": [
          {
            "vendor": "Agere Systems",
            "model": "FW643 PCI Express1394b Controller (PHY/Link)",
            "description": "FireWire (IEEE 1394)"
          }
        ],
        "description": "PCI bridge",
        "model": "MCP79 PCI Express Bridge",
        "vendor": "nVidia Corporation"
      }
    ],
    "scsi": [
      {
        "description": "SCSI Disk",
        "model": "SD Card Reader",
        "vendor": "APPLE"
      }
    ],
    "storage": [
      {
        "description": "ATA Disk",
        "partitions": [
          {
            "description": "EFI GPT partition",
            "filesystem": "Not available",
            "size": "Not available"
          },
          {
            "description": "Darwin/OS X HFS+ partition",
            "filesystem": "hfsplus",
            "size": "285 GB"
          },
          {
            "description": "Linux LVM Physical Volume partition",
            "filesystem": "Not available",
            "size": "34 GB"
          }
        ],
        "product": "Hitachi HTS54503",
        "size": "320 GB",
        "vendor": "Hitachi"
      },
      {
        "description": "SCSI Disk",
        "partitions": [],
        "product": "SD Card Reader",
        "size": "Not available",
        "vendor": "APPLE"
      }
    ],
    "system": {
      "bios_capabilities": [
        {
          "code": "pci",
          "title": "[PCI bus]"
        },
        {
          "code": "upgrade",
          "title": "[BIOS EEPROM can be upgraded]"
        },
        {
          "code": "shadowing",
          "title": "[BIOS shadowing]"
        },
        {
          "code": "cdboot",
          "title": "[Booting from CD-ROM/DVD]"
        },
        {
          "code": "bootselect",
          "title": "[Selectable boot path]"
        },
        {
          "code": "acpi",
          "title": "[ACPI]"
        },
        {
          "code": "ieee1394boot",
          "title": "[Booting from IEEE1394 (Firewire)]"
        },
        {
          "code": "smartbattery",
          "title": "[Smart battery]"
        },
        {
          "code": "netboot",
          "title": "[Function-key initiated network service boot]"
        }
      ],
      "bios_date": "06/15/09",
      "bios_vendor": "Apple Inc.",
      "bios_version": "MBP53.88Z.00AC.B03.0906151647",
      "chassis": "notebook",
      "model": "MacBookPro5,3 (System SKU#)",
      "serial": "W892214V642",
      "vendor": "Apple Inc."
    },
    "usb": [
      {
        "description": "USB Controller",
        "model": "MCP79 OHCI USB 1.1 Controller",
        "vendor": "nVidia Corporation"
      },
      {
        "description": "USB Controller",
        "model": "MCP79 EHCI USB 2.0 Controller",
        "vendor": "nVidia Corporation"
      },
      {
        "description": "USB Controller",
        "model": "MCP79 OHCI USB 1.1 Controller",
        "vendor": "nVidia Corporation"
      },
      {
        "description": "USB Controller",
        "model": "MCP79 EHCI USB 2.0 Controller",
        "vendor": "nVidia Corporation"
      }
    ]
  }
}
```

## GET `/computers/activities`

Get details of the activities for specified computer(s).

Path parameters:

- None

Query parameters:

- (Required) `computer_ids`: An ID assigned to a specific computer.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/computers/activities?limit=1&computer_ids=1" -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "count": 26,
  "results": [
    {
      "id": 143,
      "creation_time": "2024-03-01T20:58:14Z",
      "creator": {
        "name": "John Smith",
        "email": "john@example.com",
        "id": 1
      },
      "type": "ChangePackagesRequest",
      "summary": "Remove package abs-guide",
      "result_text": null,
      "computer_id": 1,
      "approval_time": null,
      "delivery_time": null,
      "deliver_after_time": null,
      "deliver_before_time": null,
      "package_ids": [
        73
      ],
      "changes": [
        {
          "package": "abs-guide",
          "complemented": false,
          "type": "remove",
          "version": "10-3"
        }
      ],
      "parent_id": 142,
      "modification_time": "2024-03-01T20:58:14Z",
      "completion_time": null,
      "schedule_before_time": null,
      "schedule_after_time": null,
      "result_code": null,
      "activity_status": "undelivered",
      "children": []
    }
  ],
  "next": "https://landscape.canonical.com/api/v2/computers/activities?limit=1&computer_ids=1&offset=1",
  "previous": null
}
```

## GET `/computers/<int:computer_id>/groups`

Get all user groups for the provided computer ID.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- None

## GET `/computers/<int:computer_id>/packages`

Get packages associated with a computer ID.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- `query`: A query string used to select computers to query packages on.
- `search`: A string to restrict the search to (optional). All fields are searched, not just those returned. (e.g., description)
- `names`: Restrict the search to these package names. Multiple names can be specified by numbering the names with `names.1`, `names.2`, etc.
- `installed`: If true only packages in the installed state will be returned, if false only packages not installed will be returned. If not given both installed and not installed packages will be returned.
- `available`: If true only packages in the available state will be returned, if false only packages not available will be returned. If not given both available and not available packages will be returned.
- `upgrade`: If true, only installable packages that are upgrades for an installed one are returned. If false, only installable packages that are not upgrades are returned. If not given, packages will be returned regardless of whether they are upgrades or not.
- `held`: If true, only installed packages that are held on computers are returned. If false, only packages that are not held on computers are returned. If not given, packages will be returned regardless of the held state.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/computers/23/packages?limit=2" -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "count": 92372,
  "results": [
    {
      "name": "0ad",
      "summary": "Real-time strategy game",
      "status": "available",
      "current_version": null,
      "available_version": "0.0.25b-2"
    },
    {
      "name": "0ad-data",
      "summary": "Real-time strategy game (data files)",
      "status": "available",
      "current_version": null,
      "available_version": "0.0.25b-1"
    }
  ],
  "next": "https://landscape.canonical.com/api/v2/computers/23/packages?limit=2&offset=2",
  "previous": null
}
```

## GET `/computers/<int:computer_id>/snaps/installed`

List all installed snaps on a single computer.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/computers/22/snaps/installed?limit=2" -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "count": 4,
  "results": [
    {
      "version": "4.0.9-a29c6f1",
      "revision": "24061",
      "tracking_channel": "4.0/stable/ubuntu-20.04",
      "held_until": null,
      "confinement": "strict",
      "snap": {
        "id": "J60k4GY0HppDwOeW8dZdWc8obX0xujRu",
        "name": "lxd",
        "publisher": {
          "username": "canonical",
          "validation": "verified"
        },
        "summary": "LXD - container and VM manager"
      }
    },
    {
      "version": "2.61.1",
      "revision": "20671",
      "tracking_channel": "latest/stable",
      "held_until": null,
      "confinement": "strict",
      "snap": {
        "id": "PM2rV4ml8uWu4RDBT8dSGnJUYbevVhc4",
        "name": "snapd",
        "publisher": {
          "username": "canonical",
          "validation": "verified"
        },
        "summary": "Daemon and tooling that enable snap packages"
      }
    }
  ],
  "next": "https://landscape.canonical.com/api/v2/computers/22/snaps/installed?limit=2&offset=2",
  "previous": null
}
```

## GET `/computers/<int:computer_id>/users/<string:username>/groups`

Get all the groups for the provided username on the given computer ID.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.
- `username`: The username of the account.

Query parameters:

- None

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/computers/22/users/ubuntu/groups" -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "groups": [
    {
      "id": 1020,
      "computer_id": 22,
      "gid": 4,
      "name": "adm"
    },
    {
      "id": 1022,
      "computer_id": 22,
      "gid": 29,
      "name": "audio"
    },
  ]
}
```

## GET `/computers/<int:computer_id>/processes`

Gets the active processes for the computer.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Query parameters:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/computers/22/processes?limit=2" -H "Authorization: Bearer $JWT"
```

Example output:

```json
{
  "count": 84,
  "results": [
    {
      "id": 2551,
      "computer_id": 22,
      "pid": 1525,
      "gid": 1000,
      "name": "(sd-pam)",
      "state": "S",
      "start_time": "2024-02-07T20:26:55Z",
      "vm_size": 104024,
      "cpu_utilisation": 0
    },
    {
      "id": 2552,
      "computer_id": 22,
      "pid": 1530,
      "gid": 1000,
      "name": "-bash",
      "state": "S",
      "start_time": "2024-02-07T20:26:55Z",
      "vm_size": 10032,
      "cpu_utilisation": 0
    }
  ],
  "next": "https://landscape.canonical.com/api/v2/computers/22/processes?limit=2&offset=2",
  "previous": null
}
```

## POST `/computers/<int:computer_id>/usergroups/update_bulk`

Update all the groups for the provided username on the given computer ID.

Required path parameters:

- `computer_id`: An ID assigned to a specific computer.

Required parameters:

- `usernames`: A list of strings of the usernames to be updated.
- `action`: The action to be performed on the users.
- `groupnames`: A list of strings with the group names.

Optional parameters:

- None

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/1/usergroups/update_bulk" -H "Authorization: Bearer $JWT"  -d '{"action": "add", "usernames": ["john", "jane"], "groupnames": ["finance", "admin"]}'
```

Example output:

```json
{
  "id": 407,
  "creation_time": "2024-03-21T21:52:12Z",
  "creator": {
    "name": "John Smith",
    "email": "john@example.com",
    "id": 1
  },
  "type": "ActivityGroup",
  "summary": "Adding user(s) to group(s)",
  "completion_time": null,
  "parent_id": null,
  "deliver_delay_window": 0,
  "result_text": null,
  "result_code": null,
  "activity_status": "undelivered"
}
```

## POST `/computers/<computer_id>/restart`

Restarts the specified computer

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Optional query parameters:

- `deliver_after`: A time in the future to deliver the reboot activity
- `deliver_delay_window`: Randomize delivery within the given time frame (minutes)

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/29/restart" \
  -H "Authorization: Bearer $JWT" \
```

Example response:

```json
{
  "activity_status": "undelivered",
  "approval_time": null,
  "completion_time": null,
  "creation_time": "2024-11-22T00:01:18Z",
  "creator": {
    "email": "john@example.com",
    "id": 1,
    "name": "John Smith"
  },
  "deliver_delay_window": 0,
  "id": 2225,
  "parent_id": null,
  "result_code": null,
  "result_text": null,
  "summary": "Restart computer",
  "type": "ActivityGroup"
}
```
