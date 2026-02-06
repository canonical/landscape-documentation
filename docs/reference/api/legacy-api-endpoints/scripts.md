(reference-legacy-api-scripts)=
# Scripts

The methods available here are related to stored scripts.

## GetScripts

Retrieve stored scripts associated with the current account.

It also supports two optional arguments:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

For example, the following request looks for stored scripts associated with the account and limits the result to 20 scripts:

```text
?action=GetScripts&limit=20
```

The method returns a JSON serialized list of scripts, like the following result:

```text
[
    {
        "creator": {
            "name": "John Smith",
            "id": 12345,
            "email": "john@example.com"
        },
        "interpreter": "/bin/bash",
        "title": "some script",
        "time_limit": 300,
        "username": "root",
        "id": 12345,
        "access_group": "somegroup",
        "attachments": [
            "file 1"
        ]
    }
]
```

## GetScriptCode

Retrieve the code portion of a given script.

- `script_id`: The id of the script you wish to get the code for.

The following errors may be raised:

- `UnknownScript`: No script with the given id could be found.

For example, the following request will get the code for a given script:

```text
?action=GetScriptCode&script_id=1
```

The method returns a JSON serialized representation of the new script:

```text
"import sys\nprint sys.version"
```

## ExecuteScript

```{note}
To use this API endpoint, you must have remote script execution enabled to run scripts on the target Landscape Client. For more information, visit {ref}`how to enable script execution <howto-heading-client-enable-script-execution>`.
```

Execute script on computers.

This method requires the following mandatory arguments:

- `query`: A query string used to select the computers to execute the script on. (See `query` under `GetComputers` for additional details.)
- `script_id`: The id of the script stored in the server.
- `username`: The username to execute the script as on the client. Required if the script has no default username.

It also supports an optional argument:

- `deliver_after`: Run the script after the specified time. The time format is `YYYY-MM-DDTHH:MM:SSZ`.

For example, the following request will execute the Script with Id 19000 on all computers with the server tag:

```text
?action=ExecuteScript&query=tag:server&script_id=19000
```

The method returns a JSON structure with the activity that was created:

```json
{
    "computer_id": "None",
    "creation_time": "2012-11-26T23: 36: 20Z",
    "creator": {
        "email": "john@example.com",
        "id": 3,
        "name": "John"
    },
    "id": 155,
    "parent_id": "None",
    "summary": "Run script: foo",
    "type": "ActivityGroup"
}
```

The following errors may be raised:

- `UnknownScript`: No script with the given id could be found.
- `RequiresUserError`: The script does not have a user to run as, so the user must be specified when executing the script.

## RemoveScript

Remove a stored script.

This method takes one mandatory argument:

- `script_id`: The id of a stored script identities in the server.

For example, the following request removes stored script 1:

```text
?action=RemoveScript&script_id=1
```

The following errors may be raised:

- `UnknownScript`: No script with the given id could be found.
- `Unauthorised`: The user doesn’t have permission to remove the specified script.

## CreateScript

Create a new script.

- `title`: The title you wish to give the new script.
- `time_limit`: The time, in seconds, after which the script is considered defunct. The process will be killed, and the script execution will be marked as failed after this limit expires.
- `code`: The content of the script, encoded in UTF-8, then encoded in base64.
- `username`: The system username to execute the script as. (optional)
- `access_group`: The name of the access group to create the new script into. (optional)

For example, the following request creates a new script:

```text
?action=CreateScript&title=Example&interpreter=python&time_limit=200&code=aGVsbG8=
```

The following errors may be raised:

- `DuplicateScript`: A script with this title already exists in the account.
- `ScriptEncoding`: The code (script body) is not UTF-8 decodeable.
- `EmptyScriptCode`: The code (script body) is of zero length or commented.
- `EmptyScriptInterpreter`: The code (script body) does not start with a script interpreter. (e.g.,: `#!/bin/bash`)
- `UnknownAccessContext`: The specified access context could not be found for the current script.
- `Unauthorised`: The user doesn’t have permission to create the specified script.

The method returns a JSON serialized description of the script, like the following result:

```text
{
    "creator": {
        "name": "John Smith",
        "id": 12345,
        "email": "john@example.com"
    },
    "interpreter": "/bin/bash",
    "title": "some script",
    "time_limit": 300,
    "username": "root",
    "id": 12345,
    "access_group": "somegroup",
    "attachments": [
        "file 1"
    ]
}
```

Note: the script content is not returned in this representation, please use the `GetScriptCode` API method to retrieve it instead.

## EditScript

Edit an existing script.

- `script_id`: The id of the script that will be edited.
- `title`: The new title you wish to give to the script (optional).
- `time_limit`: The new time, in seconds, after which the script is considered defunct. The process will be killed, and the script execution will be marked as failed after this limit expires (optional).
- `code`: The content of the script, encoded in UTF-8, then encoded in base64 (optional).
- `username`: The new system username to execute the script as (optional).

For example, the following request edits the script with ID 2:

```text
?action=EditScript&script_id=2&title=NewTitle&interpreter=newpython
    &time_limit=999&username=foo&code=aGVsbG8
```

The following errors may be raised:

- `UnknownScript`: No script with the given id could be found.
- `DuplicateScript`: A script with this title already exists in the account.
- `ScriptEncoding`: The code (script body) is not UTF-8 decodeable.
- `EmptyScriptCode`: The code (script body) is of zero length or commented.
- `EmptyScriptInterpreter`: The code (script body) does not start with a script interpreter. (e.g.,: `#!/bin/bash`)
- `Unauthorised`: The user doesn’t have permission to remove the specified script.

The method returns a JSON serialized description of the new script, like the following result:

```text
{
    "creator": {
        "name": "John Smith",
        "id": 12345,
        "email": "john@example.com"
    },
    "interpreter": "newpython",
    "title": "NewTitle",
    "time_limit": 999,
    "username": "foo",
    "id": 12345,
    "access_group": "somegroup",
    "attachments": [
        "file 1"
    ]
}
```

Note: the script content is not returned in this representation, please use the GetScriptCode API method to retrieve it instead.

## CopyScript

Copy an existing script to a script with a new title.

Arguments:

- `script_id`: The id of an existing script to copy.
- `destination_title`: The title of the new script.
- `access_group`: The access group to place the script in. If none is given, the script will be placed in the same access group as the existing script. (optional)

The following errors may be raised:

- `UnknownScript`: No script with the given id could be found or do not have access to the script.
- `UnknownAccessGroup`: The specified access group could not be found.
- `DuplicateScript`: The script title is not unique.
- `Unauthorised`: The user doesn’t have permission to create a script in the destination access group.

For example, the following request creates a script from an existing script:

```text
?action=CopyScript&script_id=1&destination_title=ScriptCopy
```

The method returns a JSON serialized representation of the new script:

```json
{
    "creator": {
        "name": "John Smith",
        "id": 12345,
        "email": "john@example.com"
    },
    "interpreter": "/bin/bash",
    "title": "ScriptCopy",
    "time_limit": 300,
    "username": "root",
    "id": 2,
    "access_group": "somegroup",
    "attachments": [
        "file 1"
    ]
}
```

## RemoveScriptAttachment

Remove a script attachment from a given script.

Arguments:

- `script_id`: The id of the script the attachment belongs to.
- `filename`: The filename of the attachment you wish to delete.

The following errors may be raised:

- `UnknownScript`: No script with the given id could be found or do not have access to the script.
- `UnknownScriptAttachment`: An attachment with the specified filename could not be found in this script.
- `Unauthorised`: The user doesn’t have permission to remove the attachment.

For example, the following request deletes an attachment named “foo.jpg” from a script:

```text
?action=RemoveScriptAttachment&script_id=1&filename=foo.jpg
```

## CreateScriptAttachment

Creates a script attachment for a given script.

Arguments:

- `script_id`: The id of the script the attachment will be attached to.
- `file`: The file you wish to use as an attachment. The format for this parameter is: `<filename>$$<base64 encoded file contents>`.

The following errors may be raised:

- `DuplicateScriptAttachment`: An attachment with the same name already exists for the given script.
- `UnknownScriptAttachment`: An attachment with the specified filename could not be found in this script.
- `TooManyScriptAttachments`: The script you wish the attachment to belong to already has the maximum allowed number of scripts.
- `ScriptAttachmentSize`: The maximum allowed size for attachments is already reached, or would be reached should the creation have occurred.
- `Unauthorised`: The user doesn’t have permission to create the attachment.

For example, the following request creates an attachment named “foo.txt” containing “hello”:

```text
?action=CreateScriptAttachment&script_id=1&file=foo.txt$$aGVsbG8=
```

The method returns the newly created attachment’s filename:

```text
‘foo.txt’
```
