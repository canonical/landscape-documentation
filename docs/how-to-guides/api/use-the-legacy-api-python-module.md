(how-to-use-legacy-api-python)=
# How to use the legacy API Python module

The **landscape-api** package also has a Python module to use the Landscape API. Once the package is installed, the `API` class can be imported.

In a similar way as happened with the command-line client, the API methods are slightly mangled here. The method names are converted to lowercase and an underscore (“`_`”) is used as a word separator. For example, instead of using `GetComputers`, the method defined in the `API` class is called `get_computers`.

Each Python method has documentation explaining its purpose, parameters and types. To see the full list, run:

```bash
pydoc landscape_api.base
```

To get help about a specific method, like `get_computers`, run:

```bash
pydoc landscape_api.base.API.get_computers
```

Alternatively, the method’s `__doc__` attribute can be used, or even the builtin help:

```python
>>> from landscape_api.base import API
>>> print (API.get_computers.__doc__)
Get a list of computers associated with the account.
...
>>> help(API.get_computers)
Help on method get_computers in module landscape_api.base:

get_computers(self, query="", limit=1000, offset=0, with_network=False, ...
...
```

Here is a quick example showing how to list and get information about all computers that have pending security upgrades:

```python
#!/usr/bin/python3
import os, json, sys
from landscape_api.base import API, HTTPError

# change these accordingly
uri = "https://landscape.example.com/api/"
key = "1R3XGCT17NWIXKU5AM5J"
secret = "vYtjUFeNiTJfBdr0oPqKa/QUr8OKXEj8fYOCbquc"
ca = "/home/ubuntu/ca.pem"

api = API(uri, key, secret, ca)
try:
    computers = api.get_computers(query="alert:security-upgrades")
except HTTPError as e:
    print ("\nGot server error:\n"
           "Code: {}\n"
           "Message: {}\n".format(e.code, e.message))
    sys.exit(1)

if len(computers) == 0:
   print ("No computers have pending security upgrades.")
else:
    for computer in computers:
        print ("Id:", computer["id"])
        print ("Title:", computer["title"])
        print ("Hostname:", computer["hostname"])
        print ("Last ping:", computer["last_ping_time"])
        print ("Memory:", computer["total_memory"])
        if computer["reboot_required_flag"]:
            print ("Needs to reboot!")
        print()
```

Note that API methods will return python objects by default. To return the raw JSON result of the call, the ‘json’ boolean parameter of the API class can be provided:

```python
api = API(uri, key, secret, ca, json=True)
```
