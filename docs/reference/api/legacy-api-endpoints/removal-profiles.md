(reference-legacy-api-removal-profiles)=
# Removal Profiles

Landscape can be configured to automatically remove computers that have not contacted the server within a set period of time.

## CreateRemovalProfile

Create a removal profile.

- `title`: The human-readable title of the profile.
- `days_without_exchange`: The length of time after which a computer may be removed.
- `access_group`: If specified, the name of the access group the profile will apply to.

For example, the following command creates a removal profile titled “New Profile” that will remove computers after 4 days:

```text
?action=CreateRemovalProfile&title=New%20Profile
    &days_without_exchange=4
```

The method returns a JSON representation of the created removal profile:

```text
{
    "id": 1,
    "name": "new-profile",
    "title": "New Profile",
    "days_without_exchange": 4,
    "access_group": "global"
}
```

The following errors may be raised:

`UnknownAccessGroup`: The given access group is not known.
`Unauthorised`: The person is not authorised to create removal profiles in the given access group.
`InvalidDaysWithoutExchangeValue`: The days_without_exchange value is less than 1.

## RemoveRemovalProfile

Remove an existing removal profile by name.

Arguments:

- `name`: The name of the removal profile to be removed.

For example, the following request deletes a removal profile with the name “test-1”:

```text
?action=RemoveRemovalProfile&name=test-1
```

The following errors may be raised:

- `UnknownRemovalProfile`: A profile with the specified name could not be found.

## GetRemovalProfiles

List existing removal profiles.

For example, the following request lists all removal profiles:

```text
?action=GetRemovalProfiles
```

The method returns a JSON serialized representation of the list:

```text
[
    {
        "id": 1,
        "name": "servers",
        "title": "Servers",
        "days_without_exchange": 28,
        "access_group",
        "global"
    },
    {
        "id": 2,
        "name": "testing",
        "title": "Testing Systems",
        "days_without_exchange": 14,
        "access_group": "testing"
    }
]
```

## EditRemovalProfile

Edit a removal profile.

Arguments:

- `name`: The name of the profile to edit.
- `title`: The new human-readable title of the profile.
- `days_without_exchange`: The length of time after which a computer may be removed.

For example, the following modifies the example profile in documented in CreateRemovalProfile to have a no communication period of 31 days:

```text
?action=EditRemovalProfile&name=newprofile&days_without_exchange=31
```

The method returns a JSON serialized representation of the modified object:

```text
{
    "id": 1,
    "name": "newprofile",
    "title": "New Profile",
    "days_without_exchange": 31,
    "access_group": "global"
}
```

The following errors may be raised:

`UnknownRemovalProfile`: A profile with the specified name could not be found.
`Unauthorised`: The person is not authorised to edit removal profiles in the associated access group.
`InvalidDaysWithoutExchangeValue`: The `days_without_exchange` value is less than 1.

## AssociateRemovalProfile

Associate a removal profile to computers with the specified tags, or all computers.

Arguments:

- `name`: Name of the removal profile.
- `tags.#`: A list of tag names to associate to the profile.
- `all_computers`: true if the profile should be associated to all computers. This parameter is optional and defaults to false. Individual tags associated to the profile will remain, but they will only be effective if the `all_computers` flag is later disabled.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request:

```text
?action=AssociateRemovalProfile&name=test-1
    &tags.1=server&tags.2=lucid
```

The following errors may be raised:

`UnknownRemovalProfile`: No profile with the specified name exists.
`InvalidParameterCombination`: The set of arguments are not compatible when specified together.

The method returns JSON serialized info of the profile status:

```text
{
    "name": "test-1",
    "id": 178,
    "upgrade_type": "all",
    "schedule": "FREQ=WEEKLY",
    "tags": [
        "my-computers",
        "lucid",
        "server"
    ],
    "all_computers": false
}
```

## DisassociateRemovalProfile

Disassociate a removal profile from computers with the specified tags, or from all computers.

Arguments:

- `name`: Name of the removal profile.
- `tags.#`: A list of tag names to disassociate from the profile.
- `all_computers`: if true, the profile will only remain enabled for computers with tags associated to the profile. This parameter is optional and defaults to false.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request:

```text
?action=DisassociateRemovalProfile&name=test-1
    &tags.1=server&tags.2=lucid
```

The following errors may be raised:

- `UnknownRemovalProfile`: No profile with the specified name exists.
- `InvalidParameterCombination`: The set of arguments are not compatible when specified together.

The method returns JSON serialized info of the profile status:

```text
{
    "name": "test-1",
    "id": 178,
    "upgrade_type": "all",
    "schedule": "FREQ=WEEKLY",
    "tags": [
        "my-computers"
    ],
    "all_computers": false
}
```

