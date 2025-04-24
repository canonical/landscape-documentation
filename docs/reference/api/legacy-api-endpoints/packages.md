(reference-legacy-api-packages)=
# Packages


The methods available here are related to package management operations.

## GetPackages

Get a list of packages associated with the account used for authentication.

- `query`: A query string used to select computers to query packages on. (See `query` under `GetComputers` for additional details.)
- `search`: A string to restrict the search to (optional). All fields are searched, not just those returned. (e.g., description)
- `names`: Restrict the search to these package names. Multiple names can be specified by numbering the names with `names.1`, `names.2`, etc.
- `installed`: If true only packages in the installed state will be returned, if false only packages not installed will be returned. If not given both installed and not installed packages will be returned.
- `available`: If true only packages in the available state will be returned, if false only packages not available will be returned. If not given both available and not available packages will be returned.
- `upgrade`: If true, only installable packages that are upgrades for an installed one are returned. If false, only installable packages that are not upgrades are returned. If not given, packages will be returned regardless of wether they are upgrades or not.
- `held`: If true, only installed packages that are held on computers are returned. If false, only packages that are not held on computers are returned. If not given, packages will be returned regardless of the held state.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

A package is considered installed if dpkg reports it as installed on the system.

A package is considered available if it can be fetched from an APT source. Note that this means that it’s possible for an installed package to be not available.

A package is considered an upgrade if it’s available and if it has a version higher than a non-held installed package with the same name.

For example, the following request looks for a package named with the tag ‘server’ with a limit of 20 packages:

```text
?action=GetPackages&query=tag:server&search=python&limit=20
```

The method returns a JSON serialized list of packages, with the list of computer IDs on which they are available, installed, or available as upgrades:

```text
[
    {
        "name": "python2.7",
        "summary": "An interactive high-level object-oriented language...",
        "computers": {
            "available": [
                12,
                17
            ],
            "installed": [],
            "upgrades": [],
            "held": []
        },
        "version": "2.7.2"
    },
    {
        "name": "python2.6",
        "summary": "An interactive high-level object-oriented language...",
        "computers": {
            "available": [
                12,
                17
            ],
            "installed": [
                12,
                17
            ],
            "upgrades": [],
            "held": [
                12
            ]
        },
        "version": "2.6.5"
    }
]
```

## InstallPackages

Install packages on selected computers.

Request the installation of named packages on a selection of computers.

`query`: A qualified criteria to be used in the search. (See `query` under `GetComputers` for additional details.)
`packages.#`: The list of package names to be installed, multiple names can be supplied.
`deliver_after`: Package installs will only take place when the computer contacts Landscape after this time (optional).
`deliver_delay_window`: Randomise delivery within the given time frame specified in minutes (optional).

Example of a valid request:

```text
?action=InstallPackages&query=tag:server&packages.1=python&
    packages.2=postgresql-8.4
```

The method returns a JSON serialized list of the parent activity created:

```text
{'activity_status': u'undelivered',
 'computer_id': None,
 'creation_time': '2011-07-13T00:53:56Z',
 'creator': {'email': u'person@example.com',
             'id': 66808,
             'name': u'Person'},
 'deliver_delay_window': 0,
 'id': 4,
 'parent_id': None,
 'summary': u'Install packages haskell-mode and python-mode',
 'type': 'ActivityGroup'}
```

The JSON equivalent of this output is:

```text
{
    "activity_status": "undelivered",
    "computer_id": "None",
    "creation_time": "2011-07-13T00:53:56Z",
    "creator": {
        "email": "person@example.com",
        "id": 66808,
        "name": "Person"
    },
    "deliver_delay_window": 0,
    "id": 4,
    "parent_id": "None",
    "summary": "Install packages haskell-mode and python-mode",
    "type": "ActivityGroup"
}
```

## RemovePackages

Remove packages on selected computers.

Request the removal of named packages on a selection of computers.

- `query`: A qualified criteria to be used in the search. (See `query` under `GetComputers` for additional details.)
- `packages.#`: The package names to be removed, multiple package names can be supplied.
- `deliver_after`: The removal will only take place when the computer contacts Landscape after this time (optional).
- `deliver_delay_window`: Randomise delivery within the given time frame specified in minutes (optional).

Example of a valid request:

```text
?action=RemovePackages&query=tag:server&packages.1=python&
    packages.2=postgresql-8.4
```

The method returns a JSON serialized list of the activity created:

```text
{'activity_status': u'undelivered',
 'computer_id': None,
 'creation_time': '2011-07-13T00:53:56Z',
 'creator': {'email': u'person@example.com',
             'id': 66808,
             'name': u'Person'},
 'deliver_delay_window': 0,
 'id': 4,
 'parent_id': None,
 'summary': u'Remove packages haskell-mode and python-mode',
 'type': 'ActivityGroup'}
```

The JSON equivalent of this output is:

```text
{
    "activity_status": "undelivered",
    "computer_id": "None",
    "creation_time": "2011-07-13T00:53:56Z",
    "creator": {
        "email": "person@example.com",
        "id": 66808,
        "name": "Person"
    },
    "deliver_delay_window": 0,
    "id": 4,
    "parent_id": "None",
    "summary": "Remove packages haskell-mode and python-mode",
    "type": "ActivityGroup"
}
```

## UpgradePackages

Request upgrading of all packages identified as being upgradable, on all computers selected by query.

- `query`: A qualified criteria to be used in the search. (See `query` under `GetComputers` for additional details.)
- `packages.#`: A string to restrict the upgraded packages to install (optional). Multiple package names can be supplied.
- `security_only`: If ‘true’ then only packages with USNs or from the security pocket, i.e. security upgrades will be applied (optional).
- `deliver_after`: The upgrade will only take place when the computer contacts Landscape after this time (optional).
- `deliver_delay_window`: Randomise delivery within the given time frame specified in minutes (optional).

Example of a valid request:

```text
UpgradePackages?query=tag:server&packages.1=python
```

The method returns a JSON serialized list of the activity created:

```text
{'computer_id': None,
 'creation_time': '2011-07-18T15:30:13Z',
 'creator': {'email': u'person@example.com', 'id': 8634,
             'name': u'Person'},
 'deliver_delay_window': 0,
 'id': 4547,
 'parent_id': None,
 'summary': u'Upgrade packages libpackz and packz',
 'type': 'ActivityGroup'}
```

The JSON equivalent of this output is:

```text
{
    "computer_id": "None",
    "creation_time": "2011-07-18T15:30:13Z",
    "creator": {
        "email": "person@example.com",
        "id": 8634,
        "name": "Person"
    },
    "deliver_delay_window": 0,
    "id": 4547,
    "parent_id": "None",
    "summary": "Upgrade packages libpackz and packz",
    "type": "ActivityGroup"
}
```

