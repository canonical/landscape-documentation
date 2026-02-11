---
myst:
  html_meta:
    description: "API reference for event log retrieval. Legacy API endpoints to query and export account event log entries ordered by creation time."
---

(reference-legacy-api-event-log)=
# Event Log

Methods for retrieving or exporting an account’s Event Log

## GetEventLog

Retrieve event log entries for the account, ordered by creation time.

`days`: The number of days prior to today from which to fetch log entries.
`limit`: The maximum number of results returned by the method. It defaults to 1000.
`offset`: The offset inside the list of results.

For example, the following returns the last 7 days for event log entries in the account, limiting the result to 100 entries:

```text
?action=GetEventLog&days=7&limit=100
```

The method returns a JSON representation of the log entries returned:

```json
[
    {
        "creation_time": "2014-09-16T18: 37: 45Z",
        "entity_id": 2,
        "entity_name": "WebServer1",
        "entity_type": "Computer",
        "id": 1,
        "message": "Added tag \"apache\" to computer \"WebServer1\"",
        "person_id": 3,
        "person_name": "John Smith"
    },
    "..."
]
```
