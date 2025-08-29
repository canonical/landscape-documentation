(explanation-remote-script-execution)=

# Landscape remote script execution

This document explains how Landscape Client executes scripts.

## Overview

When an administrator requests a script execution, or when a script profile is scheduled, Landscape Server creates an `ExecuteScriptRequest` activity. See {ref}`explanation-activities` for details on how activities are delivered to clients.

## Attachments

Scripts may include attachments. Attachments are stored on Landscape Server, and clients can fetch them before execution.

## `execute-script` message

Landscape Server sends a message to Landscape Client in the following form:

```json
{
  "type": "execute-script",
  "interpreter": "INTERPRETER",
  "code": "SCRIPT_CODE",
  "username": "USER",
  "time-limit": "TIME_LIMIT",
  "operation-id": "ACTIVITY_ID",
  "attachments": ["ATTACHMENT_IDS"],
  "env": {
    "LANDSCAPE_ACCOUNT": "ACCOUNT_NAME",
    "LANDSCAPE_COMPUTER_ID": "COMPUTER_ID",
    "LANDSCAPE_COMPUTER_TAGS": ["COMPUTER_TAGS"],
    "LANDSCAPE_URL": "LANDSCAPE_URL",
    "LANDSCAPE_ACTIVITY_ID": "ACTIVITY_ID",
    "LANDSCAPE_ACTIVITY_CREATOR_ID": "CREATOR_ID",
    "LANDSCAPE_ACTIVITY_CREATION_TIME": "CREATION_TIME"
  }
}
```

Field descriptions:

`interpreter`: The interpreter to run the script. This is parsed from the script code.
`code`: The script body, excluding the interpreter line.
`username`: The user under which the script will run. In the Landscape Client snap, this is always root.
`time_limit`: Maximum execution time before the process is forcibly terminated.
`activity_id`: Unique identifier of the activity.
`attachments`: List of attachment IDs stored on Landscape Server.
`env`: Environment variables provided by Landscape Server, including account name, computer metadata, and activity metadata.

## Execution flow on Landscape Client

Once Landscape Client receives the `execute-script` message, it executes the following steps:

1. Save the message to the message store.
1. Passes the message to the script execution manager plugin.
1. Create a temporary file via `tempfile.mkstemp`. The directory location is defined by the `script_tempdir` configuration option or defaults to `/tmp/`.
    1. File permissions are set to `700`.
    1. In the snap version, the specified user is given ownership.
1. Set up environment variables:
    1. `PATH` -> `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin`
    1. `USER` and `HOME` -> set according to the requested user.
    1. `LANG`, `LC_ALL`, `LC_CTYPE`, `LD_LIBRARY_PATH`, `PYTHONPATH` -> copied from root.
    1. All variables from the message's `env` block are set.
1. If attachments are included:
    1. Create a new temporary directory via `tempfile.mkdtemp`. The directory location is defined by the `script_tempdir` configuration or defaults to `/tmp/`. Give the directory `700` permissions. Give ownership to the specified user if on the snap.
    1. Download attachments from Landscape Server using their IDs.
    1. Save each attachment with `600` permissions to this temporary directory. Grant ownership if on the snap.
    1. Set the `LANDSCAPE_ATTACHMENTS` environment variable to the attachments directory path.
1. Execute the script with the configured environment.
    1. The output is limited by the `script_output_limit` configuration.
    1. Execution continues until the script exits or the `time_limit` is reached.
1. If attachments were used, remove the attachments directory after execution.
1. Send the results back to Landscape Server in an `operation-result` message, including script output and whether the script was terminated early due to timeout.
