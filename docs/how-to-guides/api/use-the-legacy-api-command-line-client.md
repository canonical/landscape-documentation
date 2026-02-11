---
myst:
  html_meta:
    description: "Install and configure landscape-api command-line client snap. Automate Landscape operations using CLI tools and environment variables."
---

(how-to-use-legacy-api-cli)=
# How to use the legacy API command-line client

The **landscape-api** package is available as a snap package, and also in the same PPA repository as Landscape Server.

Install the package as a self updating snap, by running:

```bash
sudo snap install landscape-api
```

To avoid having to pass the access key, secret key and endpoint URL every time you call landscape-api, you can put them in a file and source it. For example, you can create a `~/.landscape-api.rc` file with:

```bash
#!/bin/bash
export LANDSCAPE_API_KEY="<API access key>"
export LANDSCAPE_API_SECRET="<API secret key>"
export LANDSCAPE_API_URI="https://<landscape-hostname>/api/"
```

If you are using a custom Certificate Authority (CA), you will also need to tell the API tool where to find that certificate:

```bash
export LANDSCAPE_API_SSL_CA_FILE="/path/to/ca/file"
```

All these variables can also be specified as command-line options to the landscape-api tool.

Now, before making an API request, just source that file and you are ready to go:

```bash
source ~/.landscape-api.rc
```

The list of API methods supported by the client can be seen by just running it without any arguments. Each method has also its own quick usage description, which can be seen by running:

```bash
landscape-api help <method>
```

Note that the method names in the command-line client are all lowercase and use hyphens as a word separator. So, for example, the API method GetComputers is called `get-computers` in the client.

If valid JSON is a preferred over JSON serialized by Python, include the `--json` parameter, for example:

```bash
landscape-api get-computers --json
```

Would produce JSON output that looks like:

```text
[
    {
        "comment": "",
        "total_swap": 0,
        "total_memory": 64232,
        "title": "juju-09f25c-0",
        "last_ping_time": "2022-08-30T19:41:35Z",
        "hostname": "juju-09f25c-0.teapot.she.example.com",
        "container_info": "lxc",
        "last_exchange_time": "2022-08-30T19:40:43Z",
        "update_manager_prompt": "normal",
        "tags": [],
        "cloud_instance_metadata": {},
        "access_group": "global",
        "distribution": "22.04",
        "id": 328000,
        "reboot_required_flag": false,
        "vm_info": ""
    },
    {
        "comment": "",
        "total_swap": 0,
        "total_memory": 1987,
        "title": "tst",
        "last_ping_time": "2022-05-31T00:04:11Z",
        "hostname": "tst.teapot.she.example.com",
        "container_info": "",
        "last_exchange_time": "2022-05-31T00:02:43Z",
        "update_manager_prompt": "normal",
        "tags": [],
        "cloud_instance_metadata": {},
        "access_group": "global",
        "distribution": "22.04",
        "id": 273771,
        "reboot_required_flag": false,
        "vm_info": "kvm"
    },
    {
        "comment": "",
        "total_swap": 0,
        "total_memory": 1987,
        "title": "My Web Server",
        "last_ping_time": "2021-02-03T21:07:08Z",
        "hostname": "test-trusty.lxd",
        "container_info": "lxc",
        "last_exchange_time": "2020-12-29T13:32:16Z",
        "update_manager_prompt": "lts",
        "tags": [],
        "cloud_instance_metadata": {
            "instance-type": "m1.bastion",
            "ami-id": "ami-00000185",
            "instance-id": "i-0001d4ce"
        },
        "access_group": "global",
        "distribution": "14.04",
        "id": 211914,
        "reboot_required_flag": false,
        "vm_info": "kvm"
    },
    {
        "comment": "",
        "total_swap": 3,
        "total_memory": 1987,
        "title": "Mybastion",
        "last_ping_time": "2021-02-03T21:05:08Z",
        "hostname": "ivanhitos-bastion.cloud.sts",
        "container_info": "",
        "last_exchange_time": "2021-02-03T15:35:14Z",
        "update_manager_prompt": "lts",
        "tags": [],
        "cloud_instance_metadata": {
            "instance-type": "m1.bastion",
            "ami-id": "ami-00000185",
            "instance-id": "i-0001d4ce"
        },
        "access_group": "global",
        "distribution": "20.04",
        "id": 211915,
        "reboot_required_flag": true,
        "vm_info": "kvm"
    },
    {
        "comment": "",
        "total_swap": 0,
        "total_memory": 1987,
        "title": "MylxcFocal",
        "last_ping_time": "2021-02-03T21:22:17Z",
        "hostname": "test-focal.lxd",
        "container_info": "lxc",
        "last_exchange_time": "2020-12-29T13:19:14Z",
        "update_manager_prompt": "lts",
        "tags": [],
        "cloud_instance_metadata": {
            "instance-type": "m1.bastion",
            "ami-id": "ami-00000185",
            "instance-id": "i-0001d4ce"
        },
        "access_group": "global",
        "distribution": "20.04",
        "id": 211916,
        "reboot_required_flag": false,
        "vm_info": "kvm"
    }
]
```
