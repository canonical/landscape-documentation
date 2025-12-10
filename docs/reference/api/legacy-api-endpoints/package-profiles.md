(reference-legacy-api-package-profiles)=
# Package Profiles

A package profile is a set of package constraints that can be applied to managed computers.

The methods available are related to package profile management. The user can search, create, copy, read, update and delete profiles associated with the account.

## GetPackageProfiles

Get the details of all Package Profiles defined in the account.

- `names`: Specific profile names to limit results. (optional)

For example, the following command limits the results to return the single package profile named “mysqlprofile” in this account:

```text
?action=GetPackageProfiles&names.1=mysqlprofile
```

The method returns a JSON representation of the package profiles. It includes a list of computers which are constrained by this profile as well as a list of constrained computers which are non-compliant:

```json
[
    {
        "id": 2,
        "creation_time": "2012-03-06T18:52:09Z",
        "computers": {
            "constrained": [
                4,
                13,
                79,
                945
            ],
            "non-compliant": [
                13
            ]
        },
        "modification_time": "2012-03-06T18:52:09Z",
        "description": "Package profile to lock down mysql to >= 5.1.0",
        "version": "2",
        "tags": [
            "server",
            "desktop"
        ],
        "constraints": [("depends",
            "mysql >= 5.1.0"),
                    ("conflicts",
            "python-mysqldb < 1.2.2")
        ],
        "name": "mysqlprofile",
        "title": "MySQL Profile"
    }
]
```

## CopyPackageProfile

Copy an existing package profile to a package profile with a new name.

- `name`: A name of the existing package profile to copy.
- `destination_name`: The profile name of the copied package profile. (optional)
- `title`: The title of the copied package profile. By default the title of the source profile is used. (optional)
- `description`: The description of the copied package profile. By default the description of the source profile is used. (optional)
- `access_group`: An optional name of the access group to copy the profile to. Defaults to the origin’s access group.

For example, the following command copies the package profile ‘mysqlprofile’ to ‘copiedprofilename’ within registered with the account:

```text
?action=CopyPackageProfile&name=mysqlprofile
    &destination_name=copiedprofilename
```

The method returns a JSON representation of the copied package profile:

```json
[
    {
        "id": 3,
        "creation_time": "2012-03-06T18:52:09Z",
        "computers": {
            "constrained": [
                4,
                13,
                79,
                945
            ],
            "non-compliant": [
                13
            ]
        },
        "modification_time": "2012-03-06T18:52:09Z",
        "description": "Package profile to lock down mysql to >= 5.1.0",
        "version": "2",
        "constraints": [("depends",
            "mysql >= 5.1.0"),
                    ("conflicts",
            "python-mysqldb < 1.2.2")
        ],
        "name": "copiedprofilename"
    }
]
```

The following errors may be raised:

- `UnknownPackageProfileName`: source package profile name does not exist.
- `DuplicatePackageProfile`: destination package profile name already exists.
- `UnknownAccessGroup`: The given access group is not known.
- `Unauthorised`: The person is not authorized to copy package profiles in the given access group.

## CreatePackageProfile

Create a package profile.

- `title`: The title of the package profile to create.
- `description`: The description of the new profile.
- `source_computer_id`: A computer ID to find a computer which will be used as the basis of the package profile. (optional)
- `material`: Package data in the format of ‘dpkg –get-selections’ or CSV. (as exported by Landscape). This should be passed as a string, not a path to a file. (optional)
- `constraints`: A list of constraints to populate the package profile. (optional)
- `access_group`: An optional name of the access group to create the profile into.

`source_computer_id` and `material` are mutually exclusive.

For example, the following command creates a package profile ‘newprofile’ based on the packages installed on computer 500:

```text
?action=CreatePackageProfile&title=New%20profile
    &description=New%20profile
    &source_computer_id=500
```

The method returns a JSON representation of the created package profile:

```json
[
    {
        "id": 3,
        "creation_time": "2012-03-06T18:52:09Z",
        "computers": {
            "constrained": [
                4,
                13,
                79,
                945
            ],
            "non-compliant": [
                13
            ]
        },
        "modification_time": "2012-03-06T18:52:09Z",
        "description": "New profile",
        "version": "1",
        "constraints": [("depends",
            "mysql >= 5.1.0"),
                    ("conflicts",
            "python-mysqldb < 1.2.2")
        ],
        "name": "new-profile",
        "title": "New profile"
    }
]
```

The following errors may be raised:

- `InvalidPackageProfileName`: The name specified is not valid.
- `InvalidParameterCombination`: source_computer_id and material were both passed.
- `UnknownComputer`: An invalid source_computer_id was passed.
- `InvalidPackageProfileMaterial`: The material passed could not be parsed.
- `NoFoundPackages`: The specified computer did not have any package data
- `UnknownAccessGroup`: The given access group is not known.
- `Unauthorised`: The person is not authorized to create package profiles in the given access group. profile with no constraints. At least one valid constraint must be provided.

## RemovePackageProfile

Remove a package profile, given its name.

Example of a valid request that removes profile ‘foobar’:

```text
?action=RemovePackageProfile&name=foobar
```

The following errors may be raised:

- `UnknownPackageProfileName`: No package profile with the specified name exists.

## AssociatePackageProfile

Associate a package profile to computers with specific tags or to all computers.

`name`: Name of the package profile.
`tags.#`: List of tag names to associate to the profile.
`all_computers`: true if the profile should be associated to all computers. This parameter is optional and defaults to false. Individual tags associated to the profile will remain, but they will only be effective if the `all_computers` flag is later disabled.

`tags.#` and all_computers=true are mutually exclusive.

Example of a valid request that associates the profile ‘foobar’ with the tags ‘desktop’ and ‘laptop’:

```text
?action=AssociatePackageProfile&name=foobar
    &tags.1=desktop
    &tags.2=laptop
    &all_computers=false
```

The following errors may be raised:

- `UnknownPackageProfileName`: No package profile with the specified name exists.
- `InvalidParameterCombination`: Some tags were specified and a ‘true’ value for ‘all_computers’ was passed.

The state of the profile will be returned.

## DisassociatePackageProfile

Disassociate a package profile from computers with specified tags or from all computers.

If `all_computers=true`, the profile will be unflagged as applying to all computers, but will still be enabled for computers which have specific tags associated with it.

- `name`: Name of the package profile.
- `tags.#`: List of tag names to disassociate from the profile.
- `all_computers`: If true, the profile will only remain enabled for computers with tags associated to the profile. This parameter is optional and defaults to false.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request:

```text
?action=DisassociatePackageProfile&name=foobar
    &tags.1=desktop&tags.2=laptop
```

The following errors may be raised:

- `UnknownPackageProfileName`: No package profile with the specified name exists.
- `UnknownTag`: No tag with the specified name exists.
- `InvalidParameterCombination`: Some tags were specified and a ‘true’ value for ‘all_computers’ was passed.

The state of the profile will be returned.

## EditPackageProfile

Add or remove constraints related to a package profile. Constraints can be dependencies or conflicts.

- `name`: Name of the package profile.
- `title`: The new title of the package profile.
- `add_constraints.#`: Constraint specifications to add in the form of `depends packagename` or `conflicts packagename < 1.0`.
- `remove_constraints.#`: Constraint specifications to remove in the form of `depends packagename` or `conflicts packagename < 1.0`.

Example of a valid request:

```text
?action=EditPackageProfile&name=foobar
    &add_constraints.1=depends%20packagename
    &add_constraints.2=conflicts%20python%20%3C%202.5
    &remove_constraints.1=depends%20postgres
```

The following errors may be raised:

- `InvalidPackageConstraint`: The specified package constraint could not be parsed.
- `InvalidConstraintType`: A constraint type other than ‘depends’ or ‘conflicts’ was provided.
- `EmptyPackageProfile`: Cannot remove constraints as it leaves a profile with no constraints. An empty package profile should be removed instead.

The state of the profile will be returned.
