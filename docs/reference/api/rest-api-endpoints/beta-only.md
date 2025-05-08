(reference-rest-api-beta-only)=
# Beta-only

```{note}
The following endpoints are only in beta.
```

## POST `/computers/<computer_id>/archive`

Archives the selected computer after it has been manually sanitized.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Required parameters:

- `computer_title`: Confirm the name of the computer to archive

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/29/archive" -H "Authorization: Bearer $JWT" -d '{"computer_title": "test computer"}'
```

Example output:

```json
{
 "id": 124,
 "activity_status": "succeeded",
 "approval_time": null,
 "completion_time": "2025-02-22T02:14:19Z",
 "creation_time": "2025-02-22T02:14:19Z",
 "creator": {
     "email": "john@example.com",
     "id": 1,
     "name": "John Smith"
 },
 "deliver_delay_window": 0,
 "parent_id": null,
 "result_code": null,
 "result_text": null,
 "summary": "Archive computer",
 "type": "ActivityGroup"
}
```

## POST `/computers/<computer_id>/delete-children`

Creates an activity to delete WSL instances on a Windows host. The WSL instance does not have to be managed in Landscape.

Required parameters:

- `computer_names`

Example request:

```bash
curl -X POST https://landscape.canonical.com/api/v2/computers/20/delete-children -H "Authorization: Bearer $JWT" -d '{"computer_names": ["Ubuntu-24.04", "Focal WSL"]}'
```

Example output:

```json
{
  "id": 119,
  "creation_time": "2025-02-22T02:03:26Z",
  "creator": {
    "email": "john@example.com",
    "id": 1,
    "name": "John Smith"
  },
  "summary": "Deleting child computer(s)",
  "type": "ActivityGroup",
  "deliver_delay_window": 0,
  "approval_time": null,
  "completion_time": null,
  "parent_id": null,
  "result_code": null,
  "result_text": null,
  "activity_status": "undelivered"
}
```

## POST `/computers/<computer_id>/sanitize`

```{note}
**Please make sure you are sanitizing the correct computer. This action is irreversible.**
```

Sanitizes the selected computer. This action will make the data on the selected computer permanently irrecoverable by erasing the keyslots of every encrypted volume. A configurable delay can be set in the service.conf file.

Path parameters:

- `computer_id`: An ID assigned to a specific computer.

Required parameters:

- `computer_title`: Confirm the name of the computer to sanitize

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/computers/29/sanitize" -H "Authorization: Bearer $JWT" -d '{"computer_title": "test computer"}'
```

Example output:

```bash
{
 "id": 119,
 "activity_status": "scheduled",
 "approval_time": null,
 "completion_time": null,
 "creation_time": "2025-01-07T05:27:39Z",
 "creator": {
     "email": "john@example.com",
     "id": 1,
     "name": "John Smith"
 },
 "deliver_delay_window": 0,
 "parent_id": null,
 "result_code": null,
 "result_text": null,
 "summary": "Sanitizing computer",
 "type": "ActivityGroup"
}
```


## POST `/employee_groups`

Imports selected staged OIDC groups from their OIDC provider.

Optional parameters:

- `import_all_from`: Pass the id of the staged OIDC group import session to import all staged OIDC groups from that session.
- `staged_oidc_group_ids`: A list IDs of the staged OIDC groups to import.

Note: exactly one of `import_all_from` and `staged_oidc_group_ids` should be included with the request.

Example requests:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/employee_groups" -H "Authorization: Bearer $JWT" -d '{"staged_oidc_group_ids": [1, 2, 3]}'
```

```bash
curl -X POST "https://landscape.canonical.com/api/v2/employee_groups" -H "Authorization: Bearer $JWT" -d '{"import_all": 7}'
```

Example response:

```bash
{
    "count": 1000
    "results": [
        1,
        2,
        3,
        ...
    ]
}
```

## POST `/oidc/groups/import_session`

Creates a new OIDC group import session. The groups will be staged in a background task.

Required parameters:

- `issuer_id`: The id of the issuer.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/oidc/groups/import_session" -H "Authorization: Bearer $JWT" -d '{"issuer_id": 123}'
```

Example output:

```bash
{
   "id": 1,
   "account_id": 312,
   "status": "IN_PROGRESS",
   "issuer_id": 123,
   "synced_at": "2024-02-07T17:30:16Z"
}
```

## GET `/oidc/groups/import_session/<id>`

Gets information about an OIDC group import session. Used as a polling endpoint while the group import completes.

Path parameters:

- `id`: ID of the OIDC groups import session.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/oidc/groups/import_session/1" -H "Authorization: Bearer $JWT"
```

Example output:

```bash
{
   "id": 1,
   "account_id": 312,
   "status": "IN_PROGRESS",
   "issuer_id": 123,
   "synced_at": "2024-02-07T17:30:16Z"
}
```

## GET `/oidc/groups/staged`

Lists all staged OIDC groups.

Required query parameters:

- `import_session_id`: The ID of the OIDC group import session.

Optional query parameters:

- `include_imported`: Whether or not to include OIDC groups that have already been imported. Defaults to `false`.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/oidc/groups/staged" -H "Authorization: Bearer $JWT"
```

Example output:

```bash
{
   "count": 500,
   "results": [
       {
           "id": 1,
           "account_id": 312,
           "issuer_id": 123,
           "group_id": "1239fzxv39fvzcz3fcwp",
           "name": "Marketing",
           "import_session_id": 3
       },
       {
           "id": 2,
           "account_id": 312,
           "issuer_id": 123,
           "group_id": "ij9v3490vjxczl209jxc",
           "name": "Engineering",
           "import_session_id": 3
       },
       ...
   ]
}
```




## POST `/v2/rebootprofiles`

Creates a new reboot profile that schedules a system reboot on selected days and time.

Required parameters:

- `title`: The human readable title for this reboot profile.
- `on_days`: A list of days (abbreviated: mo, tu, we, th, fr, sa, su) on which the reboot will run.
- `at_hour`: The hour (0–23) at which the reboot will run.

Optional parameters:

- `at_minute`: The minute (0–59) at which the reboot will run. Defaults to `0`.
- `all_computers`: Whether to apply this reboot profile to all computers. Defaults to `false`.
- `deliver_within`: Number of hours within which the task should be delivered. Defaults to `1`.
- `deliver_delay_window`: Randomize delivery within this number of minutes. Defaults to `0`.
- `access_group`: The access group name where the profile will be created. Defaults to `"global"`.
- `tags`: A list of computer tags to target instead of `all_computers`.

**Note:** The scheduled time (`at_hour` and `at_minute`) is interpreted in **UTC**.

Example request:

```
curl -X POST "https://landscape.canonical.com/api/v2/rebootprofiles" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "rebootprofile1",
    "on_days": ["mo"],
    "at_hour": 21,
    "tags": ["laptop"]
}'
```

Example output:

```
{
    "access_group": "global",
    "all_computers": false,
    "at_hour": 21,
    "at_minute": 0,
    "deliver_delay_window": 0,
    "deliver_within": 1,
    "id": 9,
    "next_run": "2025-04-21T21:00:00Z",
    "num_computers": 14,
    "on_days": [
        "mo"
    ],
    "profile_data": {},
    "profile_type": "reboot_profile",
    "tags": [
        "laptop"
    ],
    "title": "rebootprofile1"
}
```

## PATCH `/v2/rebootprofiles/<profile_id>`

Updates an existing reboot profile. 

You must provide **at least one field** to modify. If updating the schedule (`every`, `on_days`, `at_hour`, `at_minute`), you must provide **all four** fields together.

Path parameters:

- `profile_id`: The ID of the reboot profile to update.

Optional parameters:

- `title`: The human readable title for this reboot profile.
- `every`: The frequency at which the reboot should run. Only `"week"` is supported at this time.
- `on_days`: A list of days (abbreviated: mo, tu, we, th, fr, sa, su) on which the reboot will run.
- `at_hour`: The hour (0–23) at which the reboot will run. This time is interpreted in UTC.
- `at_minute`: The minute (0–59) at which the reboot will run. This time is interpreted in UTC.
- `all_computers`: Whether to apply this reboot profile to all computers.
- `deliver_within`: Number of hours within which the task should be delivered.
- `deliver_delay_window`: Randomize delivery within this number of minutes.
- `access_group`: The access group name where the profile is stored.
- `tags`: A list of computer tags to target instead of `all_computers`.

Example request:

```
curl -X PATCH "https://landscape.canonical.com/api/v2/rebootprofiles/11" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "newtitle"
}'
```

Example output:

```
{
    "access_group": "global",
    "all_computers": false,
    "at_hour": 21,
    "at_minute": 0,
    "deliver_delay_window": 0,
    "deliver_within": 1,
    "every": "week",
    "id": 11,
    "next_run": "2025-04-21T21:00:52Z",
    "num_computers": 0,
    "on_days": [
        "mo"
    ],
    "profile_data": {},
    "profile_type": "reboot_profile",
    "tags": [],
    "title": "newtitle"
}
```


## GET `/v2/rebootprofiles`

Retrieves a list of reboot profiles.

Optional parameters:

- `limit`: The maximum number of results returned. Defaults to 1000.
- `offset`: The number of items to skip before starting to collect the result set.

Example request:

```
curl -X GET "https://landscape.canonical.com/api/v2/rebootprofiles?limit=2" \
  -H "Authorization: Bearer $JWT"
```

Example output:

```
{
    "count": 11,
    "next": "/v2/rebootprofiles?limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "access_group": "global",
            "all_computers": false,
            "at_hour": 21,
            "at_minute": 18,
            "deliver_delay_window": 0,
            "deliver_within": 1,
            "every": "week",
            "id": 2,
            "next_run": "2025-04-14T21:18:02Z",
            "num_computers": 1,
            "on_days": [
                "mo"
            ],
            "profile_data": {},
            "profile_type": "reboot_profile",
            "tags": [
                "world"
            ],
            "title": "hell777"
        },
        {
            "access_group": "global",
            "all_computers": false,
            "at_hour": 21,
            "at_minute": 17,
            "deliver_delay_window": 0,
            "deliver_within": 1,
            "every": "week",
            "id": 1,
            "next_run": "2025-04-14T21:17:48Z",
            "num_computers": 1,
            "on_days": [
                "mo"
            ],
            "profile_data": {},
            "profile_type": "reboot_profile",
            "tags": [
                "world"
            ],
            "title": "hell777"
        }
    ]
}
```



## DELETE `/v2/rebootprofiles/<profile_id>`

Deletes a reboot profile by its ID.

Path parameters:

- `profile_id`: The ID of the reboot profile to delete.

Example request:

```
curl -X DELETE "https://landscape.canonical.com/api/v2/rebootprofiles/1" \
  -H "Authorization: Bearer $JWT"
```

Example output:

*(empty response)*




