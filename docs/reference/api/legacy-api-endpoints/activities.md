(reference-legacy-api-activities)=
# Activities


The methods available here are related to activity management. This includes searching activities, cancelling activities and approving activities.

## GetActivities

Retrieve activities associated with the current account, ordered by creation time.

Arguments:

- `query`: A query string used to filter the returned activities. It can be one of the following space-separated criteria:
    - `id:N`: Search for activities with a specific ID.
    - `parent-id:N`: Search for children activities of a specific ID.
    - `status:STATUS_NAME`: Search for activities by status. The available values are undelivered, unapproved, delivered, canceled, failed, succeeded, and scheduled.
    - `created-after:DATE`: Search for activities created after a specific date or time, specified with the ISO-8601 format. The precision depends on how far you specify, for example `2011-01`, `2011-01-01`, `2011-01-01T10:30` are valid values.
    - `created-before`: Search for activities created before a specific date or time. The format is the same as created-after.
    - `creator:EMAIL`: Search for activities created by a particular person (specified by email address).
    - `computer:CRITERIA`: Search for activities related to the given computers. The criteria is itself another query argument to search computers. See Computer Queries for details.
    - `type:TYPE`: Search for activities of a specific type.
    - `OR`: This specific keyword can be used to combine criteria non-exclusively.
    - `NOT`: This specific keyword can be used to match the opposite of a criteria.
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

For example, the following request looks for the succeeded activities on the computers with the laptop tag, and limit the result to 20 elements:

```text
?action=GetActivities&query=status:succeeded+computer:tag:laptop
    &limit=20
```

The method returns a JSON serialized list of activities with a limit of 20. The output would be similar to the following:

```text
[
    {
        "id": 86,
        "delivery_time": "2023-03-06T18:52:09Z",
        "computer_id": 4,
        "activity_status": "succeeded",
        "result_text": "Installed!",
        "creator": {
            "email": "jane@example.com",
            "name": "Jane Doe",
            "id": 5
        },
        "creation_time": "2023-03-06T18:52:09Z",
        "package_ids": [
            36,
            1127
        ],
        "completion_time": "2023-03-06T18:52:09Z",
        "modification_time": "2023-03-06T18:52:09Z",
        "parent_id": 85,
        "deliver_after_time": null,
        "approval_time": null,
        "summary": "Install packages python-twisted-conch and python...",
        "changes": [
            {
                "package": "python-twisted-conch",
                "type": "install",
                "version": "1:0.8.0-1",
                "complemented": false
            },
            {
                "package": "python-twisted-mail",
                "type": "install",
                "version": "0.4.0-1",
                "complemented": false
            }
        ],
        "type": "ChangePackagesRequest"
    }
]
```

Some activities requested take an extended period of time to complete. These activities will not have discrete `activity_status` values. Instead they will report estimated percent complete in the progress field for the activity. The progress field will have one of the following values:

- `0`: If activity is not started
- `-1`: If an error occurred
- `1` to `100`: Percent complete of ongoing activity

Common examples of activities with a `progress` field would be syncing a pocket repository mirror or provisioning a new system.

For example, the a `GetActivities` request that reports activities with ongoing progress could output something like:

```text
[
    {
        "id": 73,
        "creator": {
            "email": "jane@example.com",
            "name": "Jane Doe",
            "id": 5
        },
        "creation_time": "2023-03-06T22:11:52Z",
        "pocket_id": 1,
        "computer_id": null,
        "summary": "Sync pocket 'release' of series 'lucid' in distribution 'ubuntu'",
        "parent_id": null,
        "pocket_name": "release",
        "progress": 37,
        "type": "SyncPocketRequest"
    }
]
```

## GetActivityTypes

Retrieve a list of possible activity types for use with the `type` query criteria.

For example, the following request gets a list of all possible activity types:

```text
?action=GetActivityTypes
```

The method returns a JSON serialized list of activity types, like the following result:

```text
[
    "RestartRequest",
    "EditUserRequest",
    "SyncPocketRequest",
    "TerminateSystemRequest",
    "ResynchronizeRequest",
    "CreateGroupRequest",
    "ShutdownRequest",
    "..."
]
```

## CancelActivities

Cancel activities associated with the current account.

Required argument:

- `query`: A query string used to select activities to be canceled.

This method returns a list of activities ids that were cancelled.

For example, the following query will select activities of all computers with tag server and status undelivered and cancel them:

```text
?action=CancelActivities&query=status:undelivered computer:tag:server
```

If any of the selected activities cannot be canceled, an HTTP 400 error is returned with an error message:

```text
activity id => message 
activity id => message 
```

## ApproveActivities

Approve activities associated with the current account.

Required argument:

- `query`: A query string used to select activities to be approved.

This method returns a list of activity ids that were approved.

For example, the following query will select activities of all computers with tag server and status unapproved and approve them:

```text
?action=ApproveActivities&query=status:unapproved computer:tag:server
```

If any of the selected activities cannot be approved, an HTTP 400 error is returned with an error message:

```text
activity id => message 
activity id => message 
```

