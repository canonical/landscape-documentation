---
myst:
  html_meta:
    description: "REST API endpoints for managing security profiles in Landscape. Create, read, update, delete, and audit CIS benchmark compliance profiles."
---

(reference-rest-api-security-profiles)=
# Security Profiles

The endpoints available here are related to management of security profiles.

## GET `/security-profiles`

Get security profiles associated with the current account, paginated and ordered by creation time.

Optional query parameters:

- `search`: filters profiles to only those with titles containing the provided string.
- `status`: must be either `archived` or `active`. Filters profiles to those with the selected status.
- `pass_rate_from`: an integer from 0 to 100. Filters profiles to those with a pass rate at or above the value.
- `pass_rate_to`: an integer from 0 to 100. Filters profiles to those with a pass rate at or below the value.
- `limit`: a positive integer used for pagination. Limits the results to the given number of profiles.
- `offset`: a non-negative integer used for pagination. Offsets the start of the results by the given number of profiles.

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/security-profiles -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "count": 2,
  "results": [
    {
      "access_group": "mdr-terminal-group",
      "account_id": 1,
      "all_computers": false,
      "associated_instances": 119,
      "benchmark": "cis_level2_workstation",
      "creation_time": "2025-03-18T16:34:51Z",
      "id": 1,
      "last_run_results": {
        "failing": 94,
        "in_progress": 10,
        "not_started": 0,
        "passing": 15,
        "pass_rate": 14,
        "report_uri": "in-progress",
        "timestamp": "2025-03-18T17:00:00Z"
      },
      "mode": "fix-restart-audit",
      "modification_time": "2025-03-18T17:50:12Z",
      "name": "mdr-terminals",
      "next_run_time": "2025-03-19T12:00:00Z",
      "restart_deliver_delay": 1,
      "restart_deliver_delay_window": 0,
      "retention_period": 730,
      "schedule": "RRULE:FREQ=WEEKLY",
      "status": "active",
      "tags": [
        "mdr"
      ],
      "tailoring_file_uri": null,
      "title": "Macrodata Refinement Terminals"
    },
    {
      "access_group": "hal-group",
      "account_id": 1,
      "all_computers": false,
      "associated_instances": 60,
      "benchmark": "cis_level2_server",
      "creation_time": "2025-03-18T16:45:44Z",
      "id": 2,
      "last_run_results": {
        "failing": 56,
        "in_progress": 0,
        "not_started": 0,
        "passing": 0,
        "pass_rate": 0,
        "report_uri": "Landscape_security_profile_audit_report_ID2-20250318.csv",
        "timestamp": "2025-03-18T17:00:00Z"
      },
      "mode": "fix-audit",
      "modification_time": "2025-03-18T16:45:44Z",
      "name": "hal",
      "next_run_time": "2025-03-19T13:00:00Z",
      "restart_deliver_delay_window": 0,
      "restart_deliver_delay": 1,
      "retention_period": 730,
      "schedule": "RRULE:FREQ=WEEKLY",
      "status": "active",
      "tags": [
        "hal"
      ],
      "tailoring_file_uri": "Landscape_security_profile_tailoring_file_ID2_20250318164544",
      "title": "HAL 9000"
    }
  ]
}
```

## POST `/security-profiles`

Create a security profile. The new security profile will perform its first run according to its schedule.

Required parameters:

- `benchmark`: The USG benchmark the security profile will enforce. See the [Ubuntu Security Guide](https://ubuntu.com/security/certifications/docs/usg) for options.
- `mode`: The run mode of the profile. One of `"audit"`, `"fix-audit"`, or `"fix-restart-audit"`.
- `schedule`: An [RFC 5545 "Recurrence Rule"](https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.10), determining how frequently the profile will audit its instances. Cannot be more frequent than weekly.
- `title`: The display name of the profile.
- `start_date`: An ISO 8601-formatted datestamp that sets the first run time of the profile. If it is the current date or in the past, the profile will start its first run immediately.

Optional parameters:

- `access_group`: The instance access group to apply the profile to. Defaults to `"global"`.
- `all_computers`: If `true`, the profile will be applied to all instances in `access_group`, regardless of `tags`.
- `restart_deliver_delay`: If `mode` is `"fix-restart-audit"`, delays the delivery of restart activities by this many hours after fix.
- `restart_deliver_delay_window`: If `mode` is `"fix-restart-audit"`, randomizes delivery of restart activities within the number of minutes provided
- `tags`: An array of tag strings. The profile will be applied only to instances with these tags.
- `tailoring_file`: The contents of an XML file used to customize which `benchmark` rules are applied during audit or fix. If provided, the `benchmark` parameter is ignored.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/security-profiles" -H "Authorization: Bearer $JWT" -d '
{
  "benchmark": "disa_stig",
  "mode": "audit",
  "schedule": "RRULE:FREQ=WEEKLY",
  "title": "Macrodata Refinement Terminals",
  "start_date": "2025-03-29T12:00:00Z",
  "access_group": "mdr-terminals",
  "all_computers": false,
  "restart_deliver_delay": 2,
  "restart_deliver_delay_window": 10,
  "tags": ["mdr"]
}'
```

Example response, the profile's state:

```json
{
  "access_group": "mdr",
  "account_id": 1,
  "all_computers": false,
  "associated_instances": 4,
  "benchmark": "disa_stig",
  "creation_time": "2025-03-28T11:22:03Z",
  "id": 3,
  "last_run_results": {
    "failing": 0,
    "passing": 0,
    "in_progress": 0,
    "not_started": 4,
    "pass_rate": null,
    "report_uri": null,
    "timestamp": null
  },
  "modification_time": "2025-03-28T11:22:03Z",
  "mode": "audit",
  "name": "macrodata-refinement-terminals",
  "next_run_time": "2025-03-29T11:22:03Z",
  "restart_deliver_delay": 2,
  "restart_deliver_delay_window": 10,
  "retention_period": 730,
  "schedule": "RRULE:FREQ=WEEKLY",
  "status": "active",
  "tags": [
    "mdr"
  ],
  "tailoring_file_uri": null,
  "title": "Macrodata Refinement Terminals"
}
```

## PATCH `/security-profiles/<id>`

Update a security profile. Be aware that not every field is editable.

Path parameters:

- `id`: The identification number of the profile to update.

Optional parameters:

- `all_computers`: If `true`, the profile will be applied to all instances in `access_group`, regardless of `tags`.
- `restart_deliver_delay`: If `mode` is `"fix-restart-audit"`, delays the delivery of restart activities by this many hours after fix.
- `restart_deliver_delay_window`: If `mode` is `"fix-restart-audit"`, randomizes delivery of restart activities within the number of minutes provided
- `schedule`: An [RFC 5545 "Recurrence Rule"](https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.10), determining how frequently the profile will audit its instances. Cannot be more frequent than weekly.
- `tags`: An array of tag strings. The profile will be applied only to instances with these tags.
- `title`: The display name of the profile.
  
Example request:

```bash
curl -X PATCH "https://landscape.canonical.com/api/v2/security-profiles/1" -H "Authorization: Bearer $JWT" -d '
{
  "schedule": "RRULE:FREQ=WEEKLY;BYDAY=MO",
  "title": "Macrodata Refinement Terminals Updated",
  "restart_deliver_delay_window": 300
}'
```

Example response:

```json
{
  "access_group": "global",
  "account_id": 1,
  "all_computers": false,
  "associated_instances": 25,
  "benchmark": "disa_stig",
  "creation_time": "2025-03-28T12:18:25Z",
  "id": 3,
  "last_run_results": {
    "failing": 0,
    "passing": 0,
    "in_progress": 25,
    "not_started": 0,
    "pass_rate": null,
    "report_uri": null
    "timestamp": "2025-03-28T13:00:00Z"
  },
  "modification_time": "2025-03-28T15:31:57Z",
  "mode": "audit",
  "name": "macrodata-refinement-terminals",
  "next_run_time": "2025-03-29T13:00:00Z",
  "restart_deliver_delay": 1,
  "restart_deliver_delay_window": 300,
  "retention_period": 730,
  "schedule": "RRULE:FREQ=WEEKLY;BYDAY=MO,FR",
  "status": "active",
  "tags": [],
  "tailoring_file_uri": null,
  "title": "Macrodata Refinement Terminals Updated"
}

```

## POST `/security-profiles/<id>:archive`

Archive a security profile. This makes it inactive.

Path parameters:

- `id`: The identification number of the profile to archive.
  
Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/security-profiles/1:archive" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "access_group": "global",
  "account_id": 1,
  "all_computers": false,
  "associated_instances": 25,
  "benchmark": "disa_stig",
  "creation_time": "2025-03-28T12:18:25Z",
  "id": 3,
  "last_run_results": {
    "failing": 0,
    "passing": 25,
    "in_progress": 0,
    "not_started": 0,
    "pass_rate": 100,
    "report_uri": "Landscape_security_profile_audit_report_ID3-20250328.csv",
    "timestamp": "2025-03-28T13:00:00Z"
  },
  "modification_time": "2025-03-28T12:30:43Z",
  "mode": "audit",
  "name": "macrodata-refinement-terminals",
  "next_run_time": null,
  "restart_deliver_delay": 1,
  "restart_deliver_delay_window": 0,
  "retention_period": 730,
  "schedule": "RRULE:FREQ=WEEKLY",
  "status": "archived",
  "tags": [],
  "tailoring_file_uri": null,
  "title": "Macrodata Refinement Terminals"
}
```

## POST `/security-profiles/<id>:execute`

Creates a run of the security profile immediately, rather than waiting for the next scheduled run.
Returns the created activity.

Path parameters:

- `id`: The identification number of the profile to execute.

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/security-profiles/1:execute" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "activity_status": "in-progress",
  "approval_time": null,
  "completion_time": null,
  "creation_time": "2025-06-04T15:36:54Z",
  "creator": {
    "id": 24,
    "email": "mark.s@lumen.example.com",
    "name": "Mark S"
  },
  "deliver_delay_window": 0,
  "id": 25487,
  "parent_id": null,
  "result_text": null,
  "result_code": null,
  "summary": "usg audit for instance",
  "type": "UsgActivity"
}
```

## GET `/security-profiles/<id>/report`

Either returns the URI at which the report can be downloaded, or starts an activity to produce the
requested report. The URI can be used with the `/security-profiles/blob` endpoint.

Path parameters:

- `id`: The identification number of the profile the report applies to.

Required query parameters:

- `start_date`: the start time for the data that the report should include. If it is the only parameter provided, then only data from the run at this time will be included.

Optional query parameters:

- `end_date`: the end time for the data that the report should include. If it is provided, then data from runs that occurred from `start_date` to `end_date` will be included.
- `detailed`: if `true`, then a detailed report will be provided instead of a summary report. Defaults to `false`.

Example requests:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/security-profiles/1/report?start_date=2025-02-28T12:34Z" -H "Authorization: Bearer $JWT"

curl -X GET "https://landscape.canonical.com/api/v2/security-profiles/1/report?start_date=2025-02-26&end_date=2025-03-02&detailed=true" -H "Authorization: Bearer $JWT"
```

Example response (when a report already exists):

```json
{
  "id": null,
  "result_text": "Landscape_security_profile_audit_report_ID1-20250218.csv",
  "activity_status": "succeeded",
  "result_code": 0
}
```

Example response (when a report will be created):

```json
{
  "activity_status": "in-progress",
  "approval_time": null,
  "completion_time": null,
  "creation_time": "2025-06-04T15:36:54Z",
  "creator": {
    "id": 24,
    "email": "mark.s@lumen.example.com",
    "name": "Mark S"
  },
  "deliver_delay_window": 0,
  "id": 25488,
  "parent_id": null,
  "result_text": null,
  "result_code": null,
  "summary": "Generate security profile compliance report.",
  "type": "GenerateUsgReportActivity"
}
```

If you make the same query later, you can retrieve the report URI from the `result_text`.
Alternatively, you can monitor the status of the activity using its `id`:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/activities/25488" -H "Authorization: Bearer $JWT"
```

The URI can be found in the `result_text` of the activity:

```json
{
  "activity_status": "complete",
  "approval_time": null,
  "completion_time": null,
  "creation_time": "2025-06-04T15:36:54Z",
  "creator": {
    "id": 24,
    "email": "mark.s@lumen.example.com",
    "name": "Mark S"
  },
  "deliver_delay_window": 0,
  "id": 25488,
  "parent_id": null,
  "result_text": "Landscape_security_profile_audit_report_ID1-20250218.csv",
  "result_code": null,
  "summary": "Generate security profile compliance report.",
  "type": "GenerateUsgReportActivity"
}
```

## GET `/security-profiles/blob`

Returns the file for the given `path`. This could be a compliance report or a tailoring file.

Required query parameters:

- `path`: the path of the file, as retrieved from `/security-profiles/<id>/report` or the status of a security profile from `/security-profiles` or `/security-profiles/<id>`.

Example request:

```bash
curl -X GET "https://landscape.canonical.com/api/v2/security-profiles/blob?path=Landscape_security_profile_audit_report_ID1-20250218.csv" -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "file_content": "Instance ID,Report,Rule ID,Severity,Identifiers and References,Description,Rationale,Pass,Report Time\\r\\n..."
}
```
