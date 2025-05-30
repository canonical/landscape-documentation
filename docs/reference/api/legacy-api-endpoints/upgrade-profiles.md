(reference-legacy-api-upgrade-profiles)=
# Upgrade Profiles


The methods defined here let you schedule automatic upgrades.

## AssociateUpgradeProfile

Associate an upgrade profile to computers with the specified tags, or all computers.

Arguments:

- `name`: Name of the upgrade profile.
- `tags.#`: A list of tag names to associate to the profile.
- `all_computers`: `true` if the profile should be associated to all computers. This parameter is optional and defaults to `false`. Individual tags associated to the profile will remain, but they will only be effective if the `all_computers` flag is later disabled.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request:

```text
?action=AssociateUpgradeProfile&name=test-1
    &tags.1=server&tags.2=lucid
```

The following errors may be raised:

- `UnknownUpgradeProfile`: No profile with the specified name exists.
- `InvalidParameterCombination`: The set of arguments are not compatible when specified together.

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

## CreateUpgradeProfile

Create an upgrade profile.

Arguments:

- `title`: The human readable title for this upgrade profile.
- `every`: The frequency at which you wish this upgrade to be executed. Valid choices are `hour` and `week`.
- `on_days`: A list of days of the week on which the upgrade profile will be run. The day names must be abbreviated to their first two letters, as: `mo`, `tu`, `we`, `th`, `fr`, `sa`, `su`. Must be specified when the every parameter is `week`, but optional if the every parameter is `hour`.
- `at_hour`: The hour, in 24h format, at which the upgrade profile will be run.
- `at_minute`: The minute of the hour (`0-59`) at which the upgrade profile will be run.
- `deliver_within`: An optional number of hours within which the upgrade task should be delivered to computers. The window will be from the time specified by this API call (`on_days`, `at_hour`, `at_minute`) until the provided number of hours later. Defaults to 1 hour.
- `deliver_delay_window`: Randomise delivery within the given timeframe specified in minutes. (optional)
- `security_upgrade`: Optional, defaults to False. Whether this upgrade is a security upgrade or not. Deprecated, use upgrade_type instead.
- `upgrade_type`: This profile should apply to all package upgrades or only security upgrades. Must be either `security` or `all`.
- `autoremove`: Optional, defaults to False. Whether the upgrade profile should also perform an autoremove of old packages.
- `access_group`: An optional name of the access group to create the profile into.

The following errors may be raised:

- `InvalidScheduleFormat`: The given schedule string is not valid.
- `InvalidParameterCombination`: The set of arguments are not compatible when specified together.
- `UnknownAccessGroup`: The given access group is not known.
- `Unauthorised`: The person is not authorised to copy upgrade profiles in the given access group.

For example, the following request creates an upgrade profile schedule that updates all packages every Monday and Sunday at 1:30pm:

```text
?action=CreateUpgradeProfile&name=test1&every=week&on_days.1=mo
    &on_days.2=su&at_hour=13&at_minute=30
```

The method returns a JSON serialized representation of the newly created object:

```text
[
    {
        "id": 1,
        "title": "Test 1",
        "name": "test-1",
        "tags": [],
        "all_computers": false,
        "upgrade_type": "all",
        "deliver_within": 1,   
        "deliver_delay_window": 0,
        "every": "week",
        "at_minute": 30,
        "at_hour": 13,
        "on_days": [
            "mo",
            "su"
        ]
    }
]
```

## DisassociateUpgradeProfile

Disassociate an upgrade profile from computers with the specified tags, or from all computers.

Arguments:

- `name`: Name of the upgrade profile.
- `tags.#`: A list of tag names to disassociate from the profile.
- `all_computers`: if `true`, the profile will only remain enabled for computers with tags associated to the profile. This parameter is optional and defaults to `false`.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request:

```text
?action=DisassociateUpgradeProfile&name=test-1
    &tags.1=server&tags.2=lucid
```

The following errors may be raised:

- `UnknownUpgradeProfile`: No profile with the specified name exists.
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

## EditUpgradeProfile

Edit an upgrade profile.

Arguments:

- `name`: The name for this upgrade profile.
- `title`: Optional, the new title for this upgrade profile.
- `every`: The frequency at which you wish this upgrade profile to be executed. Valid choices are `hour` and `week`.
- `on_days`: A list of days of the week on which the upgrade profile will be run. The day names must be abbreviated to their first two letters, as: `mo`, `tu`, `we`, `th`, `fr`, `sa`, `su`. Only needed in case the every parameter is `week` and optional when the every parameter is `hour`.
- `at_hour`: The hour, in 24h format, at which the upgrade profile will be run.
- `at_minute`: The minute of the hour (`0-59`) at which the upgrade profile will be run.
- `deliver_within`: An optional number of hours within which the upgrade task should be delivered to computers. The window will be from the time specified by this API call (`on_days`, `at_hour`, `at_minute`) until the provided number of hours later. Defaults to 1 hour.
- `deliver_delay_window`: Randomise delivery within the given timeframe specified in minutes. (optional)
- `security_upgrade`: Optional, defaults to False. Whether this profile will target only security upgrades (instead of all upgrades). Deprecated, use upgrade_type instead.
- `upgrade_type`: This profile should apply to all package upgrades or only security upgrades. Must be either `security` or `all`.
- `autoremove`: Optional, defaults to False. Whether the upgrade profile should also perform an autoremove of old packages.

The following errors may be raised:

- `UnknownUpgradeProfile`: A profile with the specified name could not be found in the database.
- `InvalidScheduleFormat`: The given schedule string is not valid.
- `InvalidParameterCombination`: The set of arguments are not compatible when specified together.

For example, the following is a request to update the example created in `CreateUpgradeProfile` with an upgrade schedule to update all packages on an hourly basis instead, at 35 past the hour:

```text
?action=EditUpgradeProfile&name=test1&every=hour&on_minute=35
```

The method returns a JSON serialized representation of the modified object:

```text
[
    {
        "id": 1,
        "name": "test1",
        "tags": [],
        "all_computers": false,
        "upgrade_type": "all",
        "autoremove": false,
        "deliver_within": 1,
        "deliver_delay_window": 0,
        "every": "hour",
        "at_minute": 35
    }
]
```

## RemoveUpgradeProfile

Remove an existing upgrade profile by name.

Arguments:

- `name`: The name of the upgrade profile you wish to cancel.

The following errors may be raised:

- `UnknownUpgradeProfile`: A profile with the specified name could not be found in the database.

For example, the following request deletes an upgrade profile schedule with the name “test-1”:

```text
?action=RemoveUpgradeProfile&name=test-1
```

## GetUpgradeProfiles

List all previously created upgrade profiles.

Arguments:

- `upgrade_type`: Optional. The type of upgrade you wish to list. This can be either `all` or `security`, in which case the result will be a list of upgrade profiles with an upgrade type of `all` or `security` respectively. If omitted, the resulting list will contain all upgrade profiles, regardless of their upgrade type.

The following errors may be raised:

- `InvalidParameterValue`: If upgrade_type is not `all` or `security`.

For example, the following request lists all upgrade profile schedules:

```text
?action=GetUpgradeProfiles
```

The method returns a JSON serialized representation of the list:

```text
[
    {
        "id": 1,
        "name": "test1",
        "schedule": "FREQ=HOURLY;BYMINUTE=30",
        "tags": [
            "my-computers",
            "lucid",
            "server"
        ],
        "all_computers": false,
        "upgrade_type": "all"
    }
{
        "id": 2,
        "name": "test2",
        "schedule": "FREQ=WEEKLY",
        "tags": [
            "my-computers",
            "lucid",
            "server"
        ],
        "all_computers": false,
        "upgrade_type": "security"
    }
]
```

