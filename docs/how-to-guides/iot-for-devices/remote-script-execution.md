(how-to-remote-script-execution)=
# How to use remote script execution with the Landscape Client snap

> See also: [Landscape's scripts repository on GitHub](https://github.com/canonical/landscape-scripts)

The Landscape Client snap allows remote script execution, but its behavior differs slightly from the Landscape Client deb package. This is because the Landscape Client snap is typically used on Ubuntu Core, and Ubuntu Core devices don’t use the same user model as desktop and server devices.

This document describes some differences and gives examples of how remote script execution can be used with the snap.

## Background information

### Landscape Client snap design

Snaps are designed to be secure. As part of this, they operate in a confined environment. The Landscape Client snap is considered “strictly confined,” which is required for it to work on an Ubuntu Core device. Strict confinement restricts the snap from interacting with the system, except when interacting via specifically configured, audited and authorized interfaces. More information on how this works can be found in [Snapcraft’s documentation on interfaces](https://snapcraft.io/docs/interfaces).

Some standard connected interfaces are:

- `hardware-observe`: Access hardware information
- `mount-observe`: Read mount table and quota information
- `network`: Enables network access
- `network-bind`: Operate as a network service
- `network-observe`: Query network status information
- `scsi-generic`: Read and write access to SCSI Generic driver devices
- `shutdown`: Restart or power off the device
- `snapd-control`: Install or remove software
- `system-observe`: Read process and system information

For more information on what these interfaces permit, see [Snapcraft’s documentation on supported interfaces](https://snapcraft.io/docs/supported-interfaces).

When the Landscape client snap attempts to execute a remote script, it’s bound by this confinement security which limits the ability to access the system other than via the permitted interfaces. As such, it’s not always possible to use the same commands you would from a command line, or write scripts in the same way.

### Script options

Snaps execute all scripts as root, regardless of the user selected when the activity is initiated. However, this doesn’t grant full device-level root privileges; the script execution is still confined by the properties of the snap, which restricts what actions the snap can perform. Snaps can’t modify immutable elements of the client or violate any limitations of the connected interfaces.

The Landscape Client snap uses the `snapd-control` interface to manage its own activities. This grants the snap the ability to do anything SnapD is capable of via the SnapD REST API.

As the interface does not allow access directly to the SnapD binary, remotely executed scripts need to use the REST API. You can use the `snapd-control` interface to interact with the SnapD REST API directly, or use Canonical's [SNAP-HTTP library](https://github.com/canonical/snap-http) for easier interaction. This library is included in Landscape Client.

### How remote scripts work in the snap

To give an example of how remote scripts work in the snap, say you want to run a script that installs the `nano-strict` text editor snap and then connects one of its interfaces so it can access files from removable devices. From the command line you could run the following:

```bash
snap install nano-strict
snap connect nano-strict:removable-media
```

However, if you attempt to execute these commands from inside the Landscape client snap, you would receive the following error:

```bash
snap install nano-strict
bash: /usr/bin/snap: Permission denied
```

This is because access to the snap binary is blocked by the confinement rules. Instead, you should use a Python script and the SNAP-HTTP API because the client supports Python scripts directly.

```python
#!/usr/bin/env python3 

from landscape.client import snap_http
snap_http.install("nano-strict")

snap_http.http.post(
    "/interfaces",
    {
        "action": "connect",
        "slots": [{"slot": "removable-media"}],
        "plugs": [{"snap": "nano-strict", "plug": "removable-media"}],
    },
)
```

While this isn't as compact, it allows your Core device and your Snap to maintain the security and robustness that strict confinement offers while still giving full access to manage your snaps and your system.

```{note}
The Landscape team has a [repository of example scripts in GitHub](https://github.com/canonical/landscape-scripts/tree/main) that covers many scenarios you may encounter. The repository is also open to pull requests. If you have a script you think would be useful to others and want to include in the repository, please open a PR.
```

## Example scripts to run on your device

You can use these examples to explore running remote scripts on your devices. You may need to adapt parts of them to fit your configuration. It’s also recommended that you explore the example scripts available in the [Landscape Scripts repository](https://github.com/canonical/landscape-scripts).

### Example #1: Install the `nano-strict` snap on the remote device using Python

Run the following:

```python
#!/usr/bin/env python3 

import requests
import socket
import json

from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool
from requests.adapters import HTTPAdapter

class SnapdConnection(HTTPConnection):
    def __init__(self):
        super().__init__("localhost")

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect("/run/snapd.socket")

class SnapdConnectionPool(HTTPConnectionPool):
    def __init__(self):
        super().__init__("localhost")

    def _new_conn(self):
        return SnapdConnection()

class SnapdAdapter(HTTPAdapter):
    def get_connection(self, url, proxies=None):
        return SnapdConnectionPool()

session = requests.Session()
session.mount("http://snapd/", SnapdAdapter())
response = session.post("http://snapd/v2/snaps/nano-strict",
                      data=json.dumps({"action": "install", "channel": "stable"}),
                       )
```

### Example #2: Install the `nano-strict` snap using the SNAP-HTTP library

Run the following:

```python
#!/usr/bin/env python3 

from landscape.client import snap_http

snap_http.install("nano-strict")
```

### Example #3: Set the logging level to “debug”

This example sets a configuration value of the Landscape Client snap to set the logging level to “debug”:

```python
#!/usr/bin/env python3 

from landscape.client import snap_http

snap_http.set_conf("landscape-client", {"logging-level": "debug"})
```

### Example #4: Use an attachment with `testscript.py`

You can also use a file attachment. Add the `testscript.py` file in the web portal as an attachment and run this script:

```text
#!/bin/bash

python3 $LANDSCAPE_ATTACHMENTS/testscript.py
```

## Debug scripts

One of the limitations of remote script execution is that when a script fails, the returned information can be limited. The options provided here can help you debug your scripts.

### Pipe the output of your script to a file

One option to debug your script is to pipe the output of your script to a file, such as `/tmp/output.txt`. You’ll then be able to access that file from the main device shell.

### Use heredocs for Python scripts

You can use heredocs within a Bash shell to debug a Python script by wrapping the code in a heredoc:

```python
#!/bin/bash
{
python3 - << EOF
# Insert Python script here
EOF
} &> /tmp/scriptoutput
```

In this script, the Bash shell is asked to execute this doc and pipe any console output to the `/tmp/scriptoutput` file.

Here is the full script using the code from a previous example:

```python
#!/bin/bash
{
python3 - << EOF

import requests
import socket
import json
import pprint

from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool
from requests.adapters import HTTPAdapter

class SnapdConnection(HTTPConnection):
    def __init__(self):
        super().__init__("localhost")

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect("/run/snapd.socket")

class SnapdConnectionPool(HTTPConnectionPool):
    def __init__(self):
        super().__init__("localhost")

    def _new_conn(self):
        return SnapdConnection()

class SnapdAdapter(HTTPAdapter):
    def get_connection(self, url, proxies=None):
        return SnapdConnectionPool()

session = requests.Session()
session.mount("http://snapd/", SnapdAdapter())
response = session.post("http://snapd/v2/snaps/nano-strict",
                      data=json.dumps({"action": "install", "channel": "stable"}),
                       )
pprint.pprint(response.json())
EOF
} &> /tmp/scriptoutput
```
