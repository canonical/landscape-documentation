(reference-rest-api-reboot-profiles)=
# Reboot Profiles

## POST `/v2/rebootprofiles`

Creates a new reboot profile that schedules a system reboot on selected days of the week at the specified time. Currently, only intervals over a week are supported (i.e., you cannot create a monthly reboot profile).

Required parameters:

- `title`: The human readable title for this reboot profile.
- `on_days`: A list of days of the week (abbreviated: `mo`, `tu`, `we`, `th`, `fr`, `sa`, `su`) on which the reboot will run.
- `at_hour`: The hour (0–23) at which the reboot will run.

Optional parameters:

- `at_minute`: The minute (0–59) at which the reboot will run. Defaults to `0`.
- `all_computers`: Whether to apply this reboot profile to all computers. Defaults to `false`.
- `deliver_within`: Number of hours within which the task should be delivered. Defaults to `1`.
- `deliver_delay_window`: Randomize delivery within this number of minutes. Defaults to `0`.
- `access_group`: The access group name where the profile will be created. Defaults to `"global"`.
- `tags`: A list of computer tags to target instead of `all_computers`.

```{note}
The scheduled time (`at_hour` and `at_minute`) is interpreted in **UTC**.
```

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/rebootprofiles"  \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "rebootprofile1",
    "on_days": ["mo"],
    "at_hour": 21,
    "tags": ["laptop"]
}'
```

Example response:

```json
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
  "on_days": ["mo"],
  "profile_data": {},
  "profile_type": "reboot_profile",
  "tags": ["laptop"],
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
- `on_days`: A list of days (abbreviated: `mo`, `tu`, `we`, `th`, `fr`, `sa`, `su`) on which the reboot will run.
- `at_hour`: The hour (0–23) at which the reboot will run. This time is interpreted in UTC.
- `at_minute`: The minute (0–59) at which the reboot will run. This time is interpreted in UTC.
- `all_computers`: Whether to apply this reboot profile to all computers.
- `deliver_within`: Number of hours within which the task should be delivered.
- `deliver_delay_window`: Randomize delivery within this number of minutes.
- `tags`: A list of computer tags to target instead of `all_computers`.

Example request:

```bash
curl -X PATCH "https://landscape.canonical.com/api/v2/rebootprofiles/11" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "newtitle"
}'
```

Example response:

```json
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
  "on_days": ["mo"],
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

```bash
curl -X GET "https://landscape.canonical.com/api/v2/rebootprofiles?limit=2" -H "Authorization: Bearer $JWT"
```

Example response:

```json
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
      "on_days": ["mo"],
      "profile_data": {},
      "profile_type": "reboot_profile",
      "tags": ["world"],
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
      "on_days": ["mo"],
      "profile_data": {},
      "profile_type": "reboot_profile",
      "tags": ["world"],
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

```bash
curl -X DELETE "https://landscape.canonical.com/api/v2/rebootprofiles/1" -H "Authorization: Bearer $JWT"
```

This endpoint returns an empty response.
