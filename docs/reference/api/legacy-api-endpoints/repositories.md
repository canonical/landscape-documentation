(reference-legacy-api-repositories)=
# Repositories


These methods give access to repository management.

## CreateDistribution

Create a repository distribution associated with the account.

This method takes a mandatory argument:

- `name`: The name of the distribution. It must be unique within the account, start with an alphanumeric character and only contain lowercase letters, numbers and `-` or `+` signs.
- `access_group`: An optional name of the access group to create the distribution into.

For example, the following request creates a distribution named ‘ubuntu’:

```text
?action=CreateDistribution&name=ubuntu
```

The following errors may be raised:

- `DuplicateDistribution`: A distribution with same name already exists.
- `UnknownAccessGroup`: The access group provided is not defined in the account.
- `Unauthorized`: The user does not have authorized permissions to create distributions or on the supplied `access_group`.

The method returns JSON serialized info of the created distribution:

```text
{
    "name": "ubuntu",
    "access_group": "global",
    "series": [],
    "creation_time": "2011-07-27T09:01:55Z"
}
```

## GetDistributions

Get info about distributions.

This method takes an optional argument:

- `names.#`: A list of distribution names to get info for. If this is not provided, the call will return all distributions for the account.

For example, the following request returns info about a distribution named ‘ubuntu’:

```text
?action=GetDistributions&names.1=ubuntu
```

The method returns JSON serialized info on the distributions:

```text
[
    {
        "creation_time": "2011-07-19T12:51:18Z",
        "name": "ubuntu",
        "series": [
            {
                "creation_time": "2011-07-19T12:51:18Z",
                "name": "lucid",
                "pockets": [
                    {
                        "architectures": [],
                        "components": [
                            "main",
                            "foo"
                        ],
                        "creation_time": "2011-07-19T12:51:18Z",
                        "mirror_suite": "suite",
                        "mirror_uri": "http://example.com",
                        "mode": "mirror",
                        "name": "other"
                    },
                    {
                        "architectures": [
                            "i386",
                            "source"
                        ],
                        "components": [],
                        "creation_time": "2011-07-19T12:51:18Z",
                        "mode": "upload",
                        "name": "updates"
                    }
                ]
            },
            {
                "creation_time": "2011-07-19T12:51:18Z",
                "name": "natty",
                "pockets": []
            }
        ]
    }
]
```

## RemoveDistribution

Remove the specified repository distribution.

This method takes a mandatory argument:

- `name`: The name of the distribution.

For example, the following request removes a distribution named ‘ubuntu’:

```text
?action=RemoveDistribution&name=ubuntu
```

The following error may be raised:

- `UnknownDistribution`: Distribution with specified name doesn’t exist.
- `OperationInProgress`: Another operation is in progress on the distribution.

## CreateSeries

Create a series associated with a distribution in the account.

This method takes 2 mandatory arguments:

- `name`: The name of the series. It must be unique within series within the distribution, start with an alphanumeric character and only contain lowercase letters, numbers and `-` or `+` signs.
- `distribution`: The name of the distribution to create the series in.
- `pockets.#`: Pockets that will be created in the series, they will be in mirror mode by default. This parameter is optional.
- `components.#`: Components for the created pockets. This parameter is optional if no pocket is specified.
- `architectures.#`: List of architectures for the created pockets. This parameter is optional if no pocket is specified.
- `gpg_key`: The name of the GPG key to use to sign packages lists of the created pockets. This parameter is optional if no pocket is specified.
- `mirror_gpg_key`: The name of the GPG key to use to verify the mirrored repositories for created pockets. If none is given, the stock Ubuntu archive one will be used.
- `mirror_uri`: The URI to mirror for the created pockets. This parameter is optional if no pocket is specified.
- `mirror_series`: Optionally, the remote series to mirror. If not specified, it defaults to the name of the series being created. If a pockets parameter also passed, each of the created pockets will mirror the relevant `dists/<mirror_series>-<pocket>` repository of the remote archive.
- `include_udeb`: Whether the pocket should include selected components also for .udeb packages (debian-installer). It’s ‘false’ by default.

For example, the following request creates a series named ‘lucid’ in the ‘ubuntu’ distribution, with a ‘release’ pocket (mirroring the ‘lucid’ suite) and an ‘updates’ one (mirroring the ‘lucid-updates’ suite):

```text
?action=CreateSeries&name=lucid&distribution=ubuntu
    &pockets.1=release&pockets.2=updates&components.1=main
    &components.2=universe&components.3=multiverse
    &components.4=restricted&architectures.1=amd64&gpg_key=my-key
    &mirror_uri=http://archive.ubuntu.com/ubuntu
```

The following errors may be raised:

- `InvalidParameterValue`: The Name parameter has an invalid value.
- `UnknownDistribution`: No distribution with the specified name exists.
- `DuplicateSeries`: A series with same name already exists in the specified distribution.
- `UnknownGPGKey`: No GPG key with the specified name exists.
- `GPGKeyHasNoSecret`: The GPG key requested for signing does not have a secret key associated.
- `OperationInProgress`: Another operation is in progress on the distribution.

The method returns JSON serialized info of the created series:

```text
{
    "name": "lucid",
    "pockets": [],
    "creation_time": "2011-07-27T09:04:03Z"
}
```

## RemoveSeries

Remove a repository series from a distribution.

This method takes 2 mandatory arguments:

- `name`: The name of the series.
- `distribution`: The name of the distribution.

For example, the following request removes a series named ‘lucid’ for the ‘ubuntu’ distribution:

```text
?action=RemoveSeries&name=lucid&distribution=ubuntu
```

The following errors may be raised:

- `UnknownDistribution`: Distribution with specified name doesn’t exist.
- `UnknownSeries`: No series with the specified name exists.

## DeriveSeries

Derive a series from another one in the same distribution. The derived series will have pockets with names corresponding to the origin series, each one configured to pull from the pocket in origin series.

This method takes 3 mandatory arguments:

- `name`: The name of the derived series. It must be unique within the distribution, start with an alphanumeric character and only contain lowercase letters, numbers and `-` or `+` signs.
- `origin`: The name of the origin series.
- `distribution`: The name of the distribution to derive the series in.

For example, the following request derive a series named ‘lucid-staging’ from the ‘lucid’ series in the ‘ubuntu’ distribution:

```text
?action=DeriveSeries&name=lucid-staging&origin=lucid
    &distribution=ubuntu
```

The following errors may be raised:

- `InvalidParameterValue`: The Name parameter has an invalid value.
- `UnknownDistribution`: No distribution with the specified name exists.
- `UnknownSeries`: No origin series with the specified name exists.
- `DuplicateSeries`: A series with same name already exists in the specified distribution.
- `EmptySeries`: The series to derive from does not contain pockets.
- `OperationInProgress`: Another operation is in progress on the distribution.

The method returns JSON serialized info of the derived series:

```text
{
    "creation_time": "2011-07-26T15:15:17Z",
    "name": "lucid-staging",
    "pockets": [
        {
            "name": "release",
            "creation_time": "2011-07-26T15:15:17Z",
            "pull_pocket": "lucid/release",
            "architectures": [
                "i386"
            ],
            "components": [
                "main",
                "contrib"
            ],
            "mode": "pull"
        },
        {
            "name": "updates",
            "creation_time": "2011-07-26T15:15:17Z",
            "pull_pocket": "lucid/updates",
            "architectures": [
                "i386",
                "amd64"
            ],
            "components": [
                "main"
            ],
            "mode": "pull"
        }
    ]
}
```

## CreatePocket

Create a pocket associated with a series in the account.

This method takes the following arguments:

- `name`: The name of the pocket. It must be unique within series, start with an alphanumeric character and only contain lowercase letters, numbers and `-` or `+` signs.
- `series`: The name of the series to create the pocket in.
- `distribution`: The name of the distribution the series belongs to.
- `components.#`: A list of components the pocket will handle.
- `architectures.#`: A list of architectures the pocket will handle.
- `mode`: The pocket mode. Can be `pull`, `mirror` and `upload`.
- `gpg_key`: The name of the GPG key to use to sign packages lists for this pocket. The GPG key provided must have a private key associated with it.
- `include_udeb`: Whether the pocket should include selected components also for .udeb packages (debian-installer). It’s ‘false’ by default.
- `mirror_uri`: In `mirror` mode, the base URI of the repository to mirror.
- `mirror_suite`: In `mirror` mode, the specific sub-directory under dists/ that should be mirrored. If the suite name ends with a ‘`/`’, the remote repository is flat (no dists/ structure, see http://wiki.debian.org/RepositoryFormat#Flat_Repository_Format); in this case a single value must be passed for the ‘components’ parameter. Packages from the remote repository will be mirrored in the specified component. This parameter is optional and defaults to the same name as local series and pocket.
- `mirror_gpg_key`: The name of the GPG key to use to verify the mirrored archive signature. If none is given, the stock Ubuntu archive one will be used.
- `pull_pocket`: The name of a pocket in current distribution to sync packages from for pockets in `pull` mode.
- `pull_series`: The name of the series pull_pocket belongs to. Must be a series in the same distribution series belongs to. If not specified, it defaults to series.
- `filter_type`: If specified, the type of the filter of the pocket. Can be either ‘allowlist’ or ‘blocklist’.
`upload_allow_unsigned`: For pockets in upload mode, a boolean indicating whether uploaded packages are required to be signed or not. It’s `false` by default.

For example, the following request creates a pocket named ‘updates’ in the ‘natty-staging’ series of the ‘ubuntu’ distribution, with packages for ‘main’ and ‘universe’ components for ‘i386’ architecture. The pocket will be in `pull` mode from the pocket ‘updates’ of the ‘natty’ series. The latter will be typically configured to fetch packages from an ubuntu mirror:

```text
?action=CreatePocket&name=updates&series=natty-staging
    &distribution=ubuntu&components.1=main&components.2=universe
    &architectures.1=i386&mode=pull&gpg_key=mykey
    &pull_pocket=updates&pull_series=natty&filter_type=allowlist
```

The following errors may be raised:

- `InvalidPocketMode`: The mode parameter has an invalid value.
- `UnknownDistribution`: No distribution with the specified name exists.
- `UnknownSeries`: No series with the specified name exists in the distribution.
- `DuplicatePocket`: A pocket with same name already exists in the specified series.
- `UnknownPocket`: No pocket with the specified name exists in the distribution.
- `UnknownGPGKey`: No GPG key with the specified name exists.
- `GPGKeyHasNoSecret`: The GPG key requested for signing does not have a secret key associated.
- `OperationInProgress`: Another operation is in progress on the distribution.
- `InvalidFilter`: Invalid filter type.

The method returns JSON serialized info of the created pocket:

```text
{
    "name": "updates",
    "architectures": [
        "i386"
    ],
    "creation_time": "2011-07-27T09:07:59Z",
    "components": [
        "main",
        "universe"
    ],
    "mode": "pull",
    "gpg_key": "mykey",
    "pull_pocket": "natty/updates"
}
```

## RemovePocket

Remove a repository pocket from a series in a distribution.

This method takes 3 mandatory arguments:

- `name`: The name of the pocket to remove.
- `series`: The name of the series containing the pocket.
- `distribution`: The name of the distribution containing the series.

For example, the following request removes a pocket named ‘updates’ from a series named ‘lucid’ for the ‘ubuntu’ distribution:

```text
?action=RemovePocket&name=updates&series=natty
    &distribution=ubuntu
```

The following errors may be raised:

- `UnknownDistribution`: No distribution with specified name exists.
- `UnknownSeries`: No series with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists.
- `OperationInProgress`: Another operation is in progress on the distribution containing the pocket.

## SyncMirrorPocket

Synchronize a mirror repository pocket.

This method takes 3 mandatory arguments:

- `name`: The name of the pocket to synchronize.
- `series`: The name of the series containing the pocket.
- `distribution`: The name of the distribution containing the series.

For example, the following request syncs a pocket named ‘updates’ in the ‘natty’ series of the ‘ubuntu’ distribution:

```text
?action=SyncMirrorPocket&name=updates&series=natty
    &distribution=ubuntu
```

The following errors may be raised:

- `UnknownDistribution`: No distribution with specified name exists.
- `UnknownSeries`: No series with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists.
- `InvalidPocketMode`: Pocket is not configured in `mirror` mode.

## PullPackagesToPocket

Import packages to a pocket in pull mode from its parent pocket.

This method takes 3 mandatory arguments:

- `name`: The name of the pocket to pull packages to.
- `series`: The name of the series containing the pocket.
- `distribution`: The name of the distribution containing the series.

For example, the following request pulls packages to a pocket named ‘updates’ in the ‘natty-staging’ series of the ‘ubuntu’ distribution:

```text
?action=PullPackagesToPocket&name=updates&series=natty-staging
    &distribution=ubuntu
```

The following errors may be raised:

- `UnknownDistribution`: No distribution with specified name exists.
- `UnknownSeries`: No series with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists.
- `InvalidPocketMode`: Pocket is not configured in `pull` mode.
- `OperationInProgress`: Another operation is in progress on the distribution containing the pocket.

## DiffPullPocket

Return a list of the changes between a pocket configured in pull mode and its origin one.

This method takes 3 mandatory arguments:

- `name`: The name of the pocket.
- `series`: The name of the series containing the pocket.
- `distribution`: The name of the distribution containing the series.

For example, the following request the diff of a pocket named ‘updates’ in the ‘lucid-staging’ series of the ‘ubuntu’ distribution:

```text
?action=DiffPullPocket&name=updates&series=lucid-staging
    &distribution=ubuntu
```

The following errors may be raised:

- `UnknownDistribution`: Distribution with specified name doesn’t exist.
- `UnknownSeries`: No series with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists.
- `InvalidPocketMode`: Pocket is not configured in `pull` mode. Can only diff pocket configured in ‘pull mode’ with their origin pocket.
- `OperationInProgress`: Another operation is in progress on the distribution containing the pocket.

The method returns JSON serialized info of changed packages between pockets for each component/architecture pair:

```text
{
    "main/i386": {
        "update": [
            [
                "package1",
                "1.0.0",
                "1.0.1"
            ],
            [
                "package2",
                "3.2",
                "3.3"
            ]
        ],
        "delete": [
            [
                "package3",
                "1.1"
            ]
        ]
    },
    "multiverse/amd64": {
        "update": [
            [
                "package4",
                "1.3",
                "1.4"
            ]
        ],
        "add": [
            [
                "package5",
                "1.1"
            ]
        ]
    }
}
```

## ListPocket

Return a list of the packages in a pocket.

This method takes 3 mandatory arguments:

- `name`: The name of the pocket to pull packages to.
- `series`: The name of the series containing the pocket.
- `distribution`: The name of the distribution containing the series.

For example, the following request the list of packages of a pocket named ‘updates’ in the ‘lucid-staging’ series of the ‘ubuntu’ distribution:

?action=ListPocket&name=updates&series=lucid-staging
    &distribution=ubuntu

The following errors may be raised:

- `UnknownDistribution`: Distribution with specified name doesn’t exist.
- `UnknownSeries`: No series with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists.
- `OperationInProgress`: Another operation is in progress on the distribution containing the pocket.

The method returns JSON serialized info of the packages in the pocket, for each section and architecture:

```text
{
    "main/i386": [
        [
            "package1",
            "1.0.0"
        ],
        [
            "package2",
            "3.2"
        ]
    ],
    "multiverse/amd64": [
        [
            "package4",
            "1.3"
        ],
        [
            "package5",
            "1.1"
        ]
    ]
}
```

## EditPocket

Edit configuration for a repository pocket from a series in a distribution. Provided details will overwrite the current ones.

This method takes the following arguments:

`name`: The name of the pocket to edit.
`series`: The name of the series containing the pocket.
`distribution`: The name of the distribution containing the series.
`components.#`: An optional list of components the pocket will handle. If provided, it will replace the current components.
`architectures.#`: An optional list of architectures the pocket will handle. If provided, it will replace the current architectures.
`gpg_key`: The name of the GPG key to use to sign packages lists for this pocket. The GPG key provided must have a private key associated with it.
`mirror_uri`: Optionally, the URI to mirror for pockets in `mirror` mode.
`mirror_suite`: Optionally, the repository entry under `dists/` to mirror for pockets in `mirror` mode.
`mirror_gpg_key`: Optionally, the name of the GPG key to use to verify the mirrored archive signature. If ‘`-`‘ is given, the stock Ubuntu archive one will be used.
`upload_allow_unsigned`: Optionally, for pockets in upload mode, a boolean indicating whether uploaded packages are required to be signed or not.
`include_udeb`: Optionally, whether the pocket should include selected components, also for `.udeb` packages (debian-installer).

For example, the following request updates the `mirror_uri` and `mirror-suite` parameters for a pocket named ‘updates’ from a series named ‘lucid’ for the ‘ubuntu’ distribution:

```text
?action=EditPocket&name=updates&series=natty
    &distribution=ubuntu&mirror_uri=http://example.com/mirror/ubuntu
    &mirror_suite=natty-updates
```

The following errors may be raised:

- `UnknownDistribution`: No distribution with specified name exists.
- `UnknownSeries`: No series with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists.
- `UnknownGPGKey`: No GPG key with the specified name exists.
- `GPGKeyHasNoSecret`: The GPG key requested for signing does not have a secret key associated.
- `OperationInProgress`: Another operation is in progress on the distribution containing the pocket.
- `InvalidPocketMode`: Provided parameters are not valid for the pocket mode.

The method returns JSON serialized info of the pocket state:

```text
{
    "name": "updates",
    "architectures": [
        "i386"
    ],
    "creation_time": "2011-07-27T09:07:59Z",
    "components": [
        "main",
        "universe"
    ],
    "mode": "mirror",
    "mirror_suite": "natty-updates",
    "mirror_uri": "http://example.com/mirror/ubuntu",
    "gpg_key": "mykey"
}
```

## RemovePackagesFromPocket

Remove packages from pockets in upload mode.

This method takes 4 mandatory arguments:

- `distribution`: The name of the distribution containing the series.
- `series`: The name of the series containing the pocket.
- `name`: The name of the pocket to remove packages from.
- `packages.#`: The names of the packages to be removed from the pockets.

For example, the following request removes packages named haskel and golang from a pocket named ‘updates’ in the ‘natty-staging’ series of the ‘ubuntu’ distribution:

```text
?action=RemovePackagesFromPockets&name=updates&series=natty-staging
    &distribution=ubuntu&packages.1=haskel&packages.2=golang
```

The following errors may be raised:

- `UnknownDistribution`: No distribution with specified name exists.
- `UnknownSeries`: No series with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists.
- `InvalidPocketMode`: Pocket is not configured in `upload` mode.
- `OperationInProgress`: Another operation is in progress on the distribution containing the pocket.

## CreateRepositoryProfile

Create a repository profile in the account.

- `title`: The title of the repository profile. It must start with an alphanumeric character and only contain lowercase letters, numbers and `-` or `+` signs.
- `description`: Description of the repository profile. (optional)
- `access_group`: The repository profile will be created within this access group. If not specified, the access group the user belongs to will be used. (optional)

Example of a valid request:

```text
?action=CreateRepositoryProfile&title=Lucid+Example
    &description=Example+Lucid+profile
```

The following errors may be raised:

- `Unauthorised`: The person is not authorised to create repository profiles.

The method returns a JSON representation of the created repository profile:

```text
{
    "all_computers": false,
    "description": "Example Lucid profile",
    "id": 1104,
    "name": "lucid-example",
    "tags": []
}
```

## GetRepositoryProfiles

Get a list of repository profiles in the account.

- `names`: A list of repository profile names to get info for. If not provided, the call will return all repository profiles in the account. (optional)

Example of a valid request:

```text
?action=GetRepositoryProfiles&names.1=lucid-example
```

The method returns a JSON serialized list of the repository profiles:

```text
[
    {
        "all_computers": false,
        "description": "Lucid packages for example application",
        "id": 1104,
        "name": "lucid-example",
        "tags": [
            "example"
        ]
    }
]
```

## GetAPTSources

Get a list of apt sources in the account used for authentication.

- `names.#`: List of names of the APT source to be returned. Multiple names can be supplied. (optional)

Example of a valid request:

```text
?action=GetAPTSources&names.1=lucid-mirror
```

The method returns a JSON serialized list of the APT sources:

```text
[
    {
        "id": 100,
        "name": "lucid-mirror",
        "access_group": "global",
        "line": "deb http://archive.ubuntu.com/ubuntu lucid main",
        "gpg_key": null
    }
]
```

## CreateAPTSource

Create an APT source in the account used for authentication.

- `name`: Name of the APT source. It must be unique within the account, start with an alphanumeric character and only contain lowercase letters, numbers and `-` or `+` signs.
- `apt_line`: the APT line of the source.
- `gpg_key`: Name of the GPG key used to sign the repository (optional).
- `access_group`: An optional name of the access group to create the APT source into.

Example of a valid request:

```text
?action=CreateAPTSource&name=lucid-mirror
    &apt_line=deb+http://archive.ubuntu.com/ubuntu/+lucid+main
```

The method returns a JSON serialized list of the created APT source:

```text
{
    "id": 100,
    "name": "lucid-mirror",
    "access_group": "global",
    "uri": "deb http://archive.ubuntu.com/ubuntu lucid main",
    "gpg_key": null
}
```

## RemoveAPTSource

Remove an apt source.

This method takes one mandatory argument:

- `name`: Name of the apt source to be removed.

Example of a valid request:

```text
?action=RemoveAPTSource&name=lucid-mirror
```

## RemoveAPTSources

**DEPRECATED**: use `RemoveAPTSource` instead.

Remove APT sources in the account used for authentication.

- `names.#`: List of names of the APT sources be removed. Multiple names can be supplied.

## AssociateRepositoryProfile

Associate repository profile to computers with specified tags or to all computers.

`name`: Name of the repository profile.
`tags.#`: List of tag names to associate to the profile.
`all_computers`: true if the profile should be associated to all computers. This parameter is optional and defaults to false. Individual tags associated to the profile will remain, but they will only be effective if the `all_computers` flag is later disabled.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request:

```text
?action=AssociateRepositoryProfile&name=lucid-example
    &tags.1=server&tags.2=lucid
```

The following errors may be raised:

- `UnknownRepositoryProfile`: No profile with the specified name exists.

The method returns JSON serialized info of the profile status:

```text
{"name": "lucide-example",
 "id": 178,
 "description": "A profile for ubuntu lucid",
 "tags": ["my-computers", "lucid", "server"],
 "all_computers": False,
 "pockets": []}

```

The JSON equivalent output is:

```text
{
    "name": "lucide-example",
    "id": 178,
    "description": "A profile for ubuntu lucid",
    "tags": [
        "my-computers",
        "lucid",
        "server"
    ],
    "all_computers": false,
    "pockets": []
}
```

## DisassociateRepositoryProfile

Disassociate repository profile from computers with specified tags or from all computers.

If all_computers=true, the profile will be unflagged as applying to all computers, but will still be enabled for computers which have specific tags associated with it.

- `name`: Name of the repository profile.
- `tags.#`: List of tag names to disassociate from the profile.
- `all_computers`: If true, the profile will only remain enabled for computers with tags associated to the profile. This parameter is optional and defaults to false.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request:

```text
?action=DisssociateRepositoryProfile&name=lucid-example
    &tags.1=server&tags.2=natty
```

The following errors may be raised:

`UnknownRepositoryProfile`: No profile with the specified name exists.
`UnknownTag`: No tag with the specified name exists.
`InvalidParameterCombination`: Some tags were specified and a `true` value for `all_computers` was passed.

The method returns JSON serialized info of the profile status:

```text
{"name": "lucide-example",
 "id": 178,
 "description": "A profile for ubuntu lucid",
 "tags": ["desktop", "my-computers"],
 "all_computers": False,
 "pockets": []}
```

The JSON equivalent output is:

```text
{
    "name": "lucide-example",
    "id": 178,
    "description": "A profile for ubuntu lucid",
    "tags": [
        "desktop",
        "my-computers"
    ],
    "all_computers": false,
    "pockets": []
}
```

## AddPocketsToRepositoryProfile

Add repository pockets to a repository profile.

An activity will be created to add the given pockets to the APT sources of the computers associated with the given profile.

- `name`: Name of the repository profile.
- `pockets.#`: The names of the pockets to add.
- `series`: The name of the series the pockets belongs to.
- `distribution`: The name of the distribution the series belongs to.

Example of a valid request:

```text
?action=AddPocketsToRepositoryProfile&name=lucid-example
    &pockets.1=staging&pockets.2=release&series=lucid
    &distribution=ubuntu
```

The method returns JSON serialized info of the profile status:

```text
{"name": "lucide-example",
 "id": 178,
 "description": "A profile for ubuntu lucid",
 "tags": ["desktop", "my-computers"],
 "all_computers": False,
 "pockets": [ ... ],
 "apt_sources": []}
```

The JSON equivalent output is:

```text
{
    "name": "lucide-example",
    "id": 178,
    "description": "A profile for ubuntu lucid",
    "tags": [
        "desktop",
        "my-computers"
    ],
    "all_computers": false,
    "pockets": [ ...
    ],
    "apt_sources": []
}
```

The following errors may be raised:

- `UnknownRepositoryProfile`: No profile with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists in the distribution.
- `UnknownSeries`: No series with the specified name exists in the distribution.
- `UnknownDistribution`: No distribution with the specified name exists.

## RemovePocketsFromRepositoryProfile

Remove repository pockets from a repository profile.

An activity will be created to remove the pockets from the APT sources of the computers associated with the given profile.

- `name`: Name of the repository profile.
- `pockets.#`: The names of the pockets to remove.
- `series`: The name of the series the pocket belongs to.
- `distribution`: The name of the distribution the series belongs to.

Example of a valid request:

```text
?action=RemovePocketsFromRepositoryProfile&name=lucid-example
    &pockets.1=staging&pockets.2=release&series=lucid
    &distribution=ubuntu
```

The method returns JSON serialized info of the profile status:

```text
{"name": "lucide-example",
 "id": 178,
 "description": "A profile for ubuntu lucid",
 "tags": ["desktop", "my-computers"],
 "all_computers": False,
 "pockets": [],
 "apt_sources": []}
```

The JSON equivalent output is:

```text
{
    "name": "lucide-example",
    "id": 178,
    "description": "A profile for ubuntu lucid",
    "tags": [
        "desktop",
        "my-computers"
    ],
    "all_computers": false,
    "pockets": [],
    "apt_sources": []
}
```

The following errors may be raised:

- `UnknownRepositoryProfile`: No profile with the specified name exists.
- `UnknownPocket`: No pocket with the specified name exists in the distribution.
- `UnknownSeries`: No series with the specified name exists in the distribution.
- `UnknownDistribution`: No distribution with the specified name exists.

## AddAPTSourcesToRepositoryProfile

Add APT sources to a repository profile.

An activity will be created to add the given source to the the computers associated with the given profile.

`name`: Name of the repository profile.
`apt_sources.#`: The names of the APT sources to add.

Example of a valid request:

```text
?action=AddAPTSourcesToRepositoryProfile&name=lucid-example
    &apt_sources.1=lucid-mirror&apt_sources.2=lucid-extra
```

The method returns JSON serialized info of the profile status:

```text
{"name": "lucide-example",
 "id": 178,
 "description": "A profile for ubuntu lucid",
 "tags": ["desktop", "my-computers"],
 "all_computers": False,
 "pockets": [],
 "apt_sources": [
     {"line": "deb http://example.com/ubuntu lucid main,
      "gpg_key": None,
      "id": 919,
      "name": "lucid-main"},
     {"line": u'deb http://example.com/ubuntu lucid universe",
      "'gpg_key": None,
      "id": 920,
      "name": "lucid-universe"}]}}
```

The JSON equivalent output is:

```text
{
    "name": "lucide-example",
    "id": 178,
    "description": "A profile for ubuntu lucid",
    "tags": [
        "desktop",
        "my-computers"
    ],
    "all_computers": false,
    "pockets": [],
    "apt_sources": [
        {
            "line": "deb http://example.com/ubuntu lucid main,"gpg_key": None,
            "id": 919,
            "name": "lucid-main"
        },
        {
            "line": u'deb http: //example.com/ubuntu lucid universe",
            "'gpg_key": None,
            "id": 920,
            "name": "lucid-universe"
        }
    ]
}
```

The following errors may be raised:

- `UnknownRepositoryProfile`: No profile with the specified name exists.
- `UnknownAPTSource`: No APT source with the specified name exists.

## RemoveRepositoryProfile

Remove a repository profile.

This method takes one mandatory argument:

- `name`: Name of the repository profile to be removed.

Example of a valid request:

```text
?action=RemoveRepositoryProfile&name=lucid-example
```

## RemoveAPTSourceFromRepositoryProfile

Remove APT source from a repository profile.

An activity will be created to remove the APT source from the computers associated with the given repository profile.

- `name`: Name of the repository profile.
- `apt_source`: The name of the APT source to remove.

Example of a valid request:

```text
?action=RemoveAPTSourcesFromRepositoryProfile&name=lucid-example
    &apt_source=lucid-mirror
```

The method returns JSON serialized info of the profile status:

```text
{"name": "lucide-example",
 "id": 178,
 "description": "A profile for ubuntu lucid",
 "tags": ["desktop", "my-computers"],
 "all_computers": false,
 "pockets": [],
 "apt_sources": []}
```

The JSON equivalent output is:

```text
{
    "name": "lucide-example",
    "id": 178,
    "description": "A profile for ubuntu lucid",
    "tags": [
        "desktop",
        "my-computers"
    ],
    "all_computers": false,
    "pockets": [],
    "apt_sources": []
}
```

The following errors may be raised:

- `UnknownRepositoryProfile`: No profile with the specified name exists.
- `UnknownAPTSource`: No APT source with the specified name exists.

## RemoveAPTSourcesFromRepositoryProfile

**DEPRECATED**: use `RemoveAPTSourceFromRepositoryProfile` instead.

Remove APT sources from a repository profile.

An activity will be created to remove the sources from the computers associated with the given profile.

- `name`: Name of the repository profile.
- `apt_sources.#`: The names of the APT sources to remove.

## RemoveRepositoryProfiles

**DEPRECATED**: use RemoveRepositoryProfile instead.

Remove repository profiles in the account.

- `names.#`: Name of the repository profile to be removed. Multiple names can be supplied.

## EditRepositoryProfile

Edit a repository profile in the account.

- `name`: Name of the repository profile to edit.
- `title`: New title of the profile.
- `description`: New description of the profile.

Example of a valid request:

```text
?action=EditRepositoryProfile&name=lucid-example
    &description=Example+Lucid+profile
```

The following errors may be raised:

`UnknownRepositoryProfile`: No profile with the specified name exists.

The method returns a JSON serialized dictionary of the repository profile:

```text
{"all_computers": False,
 "description": "Example Lucid profile",
 "id": 1104,
 "name": "lucid-example",
 "tags": ["example"]}
```

The JSON equivalent output is:

```text
{
    "all_computers": false,
    "description": "Example Lucid profile",
    "id": 1104,
    "name": "lucid-example",
    "tags": [
        "example"
    ]
}
```

## AddUploaderGPGKeysToPocket

Add GPG keys to a repository pocket in upload mode to validate uploaded packages.

- `name`: The name of the pocket.
- `series`: The name of the series the pocket belongs to.
- `distribution`: The name of the distribution the series belongs to.
- `gpg_keys.#`: The name(s) of the GPG keys to add.

Example of a valid request:

```text
?action=AddUploaderGPGKeysToPocket&name=devel
    &series=lucid&distribution=ubuntu&gpg_keys.1=mykey
```

The following errors may be raised:

- `UnknownPocket`: No pocket with the specified name exists in the distribution.
- `UnknownSeries`: No series with the specified name exists in the distribution.
- `UnknownDistribution`: No distribution with the specified name exists.
- `UnknownGPGKey`: No GPG key with the specified name exists.
- `InvalidPocketMode`: Pocket is not configured in `upload` mode.
- `GPGKeyAlreadyAssociated`: GPG key is already added to pocket.

The method returns JSON serialized info of the pocket:

```text
{"name": "devel",
 "architectures": ["i386"],
 "creation_time": "2011-07-27T09:07:59Z",
 "components": ["main", "universe"],
 "mode": "upload",
 "upload_gpg_keys": [
    {"id": 11,
    "name": "key",
    "fingerprint": "a404:34a3:e40c:1add:94fa:31b4:30a7:5431:a2eb:521a",
    "has_secret": false}]}
```

The JSON equivalent output is:

```text
{
    "name": "devel",
    "architectures": [
        "i386"
    ],
    "creation_time": "2011-07-27T09:07:59Z",
    "components": [
        "main",
        "universe"
    ],
    "mode": "upload",
    "upload_gpg_keys": [
        {
            "id": 11,
            "name": "key",
            "fingerprint": "a404:34a3:e40c:1add:94fa:31b4:30a7:5431:a2eb:521a",
            "has_secret": false
        }
    ]
}
```

## RemoveUploaderGPGKeysFromPocket

Remove GPG keys for uploaded packages validation from a repository pocket in upload mode.

- `name`: The name of the pocket.
- `series`: The name of the series the pocket belongs to.
- `distribution`: The name of the distribution the series belongs to.
- `gpg_keys.#`: The name(s) of the GPG keys to remove.

Example of a valid request:

```text
?action=RemoveUploaderGPGKeysFromPocket&name=devel
    &series=lucid&distribution=ubuntu&gpg_keys.1=mykey
```

The following errors may be raised:

- `UnknownPocket`: No pocket with the specified name exists in the distribution.
- `UnknownSeries`: No series with the specified name exists in the distribution.
- `UnknownDistribution`: No distribution with the specified name exists.
- `UnknownGPGKey`: No GPG key with the specified name exists.
- `InvalidPocketMode`: Pocket is not configured in `upload` mode.
- `GPGKeyNotAssociated`: GPG key is not associated with pocket.

The method returns JSON serialized info of the pocket:

```text
{
    "name": "devel",
    "architectures": [
        "i386"
    ],
    "creation_time": "2011-07-27T09:07:59Z",
    "components": [
        "main",
        "universe"
    ],
    "mode": "upload",
    "upload_gpg_keys": []
}
```

## AddPackageFiltersToPocket

Add package filters to a repository pocket. The pocket must be in pull mode and support blocklist/allowlist filtering.

- `name`: The name of the pocket.
- `series`: The name of the series the pocket belongs to.
- `distribution`: The name of the distribution the series belongs to.
- `packages.#`: The name(s) of the packages to add to the filter.

Example of a valid request:

```text
?action=AddPackageFiltersToPocket&name=devel
    &series=lucid&distribution=ubuntu&packages.1=bash&packages.2=python
```

The following errors may be raised:

- `UnknownPocket`: No pocket with the specified name exists in the distribution.
- `UnknownSeries`: No series with the specified name exists in the distribution.
- `UnknownDistribution`: No distribution with the specified name exists.
- `UnknownGPGKey`: No GPG key with the specified name exists.
- `InvalidPocketMode`: Pocket is not configured in `pull` mode.
- `NoPocketFiltering`: Pocket does not support filtering.

The method returns JSON serialized info of the pocket:

```text
{
    "name": "devel",
    "architectures": [
        "i386"
    ],
    "creation_time": "2011-07-27T09:07:59Z",
    "components": [
        "main",
        "universe"
    ],
    "mode": "pull",
    "filter_type": "allowlist",
    "filters": [
        "bash",
        "python"
    ]
}
```

## RemovePackageFiltersFromPocket

Remove package filters from a repository pocket. The pocket must be in pull mode and support blocklist/allowlist filtering.

- `name`: The name of the pocket.
- `series`: The name of the series the pocket belongs to.
- `distribution`: The name of the distribution the series belongs to.
- `packages.#`: The name(s) of the packages to remove from the filter.

Example of a valid request:

```text
?action=RemovePackageFiltersFromPocket&name=devel
    &series=lucid&distribution=ubuntu&packages.1=bash&packages.2=python
```

The following errors may be raised:

- `UnknownPocket`: No pocket with the specified name exists in the distribution.
- `UnknownSeries`: No series with the specified name exists in the distribution.
- `UnknownDistribution`: No distribution with the specified name exists.
- `UnknownGPGKey`: No GPG key with the specified name exists.
- `InvalidPocketMode`: Pocket is not configured in `pull` mode.
- `NoPocketFiltering`: Pocket does not support filtering.

The method returns JSON serialized info of the pocket:

```text
{
    "name": "devel",
    "architectures": [
        "i386"
    ],
    "creation_time": "2011-07-27T09:07:59Z",
    "components": [
        "main",
        "universe"
    ],
    "mode": "pull",
    "filter_type": "allowlist",
    "filters": [
        "cron"
    ]
}
```
