(explanation-remote-script-execution)=

# Landscape remote script execution

This document explains how Landscape Client executes scripts.

## Overview

When an administrator requests a script execution, or when a script profile is scheduled, Landscape Server creates an `ExecuteScriptRequest` activity. See {ref}`explanation-activities` for details on how activities are delivered to clients.

### Attachments

Scripts may include attachments. Attachments are stored on Landscape Server, and clients can fetch them before execution.

### `execute-script` message

Landscape Server sends a message to Landscape Client in the following form:

```json
{
  "type": "execute-script",
  "interpreter": <interpreter>,
  "code": <code>,
  "username": <user>,
  "time-limit": <time_limit>,
  "operation-id": <activity_id>,
  "attachments": <attachments>,
  "env": {
    "LANDSCAPE_ACCOUNT": <account_name>, 
    "LANDSCAPE_COMPUTER_ID": <computer_id>,
    "LANDSCAPE_COMPUTER_TAGS": <computer_tags>,
    "LANDSCAPE_URL": <landscape_url>
    "LANDSCAPE_ACTIVITY_ID": <activity_id>,
    "LANDSCAPE_ACTIVITY_CREATOR_ID": <creator_id>,
    "LANDSCAPE_ACTIVITY_CREATION_TIME": <creation_time>,
  },
}
```

Field descriptions:

`interpreter`: The interpreter to run the script. This is parsed from the script code.
`code`: The script body, excluding the interpreter line.
`username`: The user under which the script will run. In the Landscape Client snap, this is always root.
`time_limit`: Maximum execution time before the process is forcibly terminated.
`activity_id`: Unique identifier of the activity.
`attachments`: List of attachment IDs stored on Landscape Server.
`env`: Environment variables provided by Landscape Server.
`account_name`: The name of the account on Landscape Server.
`computer_id`: The id of the computer.
`landscape_url`: The Landscape Server root URL.
`creator_id`: A unique id for the person that created the activity, if one exists.
`creation_time`: The time the activity was created.

### Script execution step-by-step

The following section explains what happens on Landscape Client after receiving the above message.

1. Landscape Client saves the message to the message store.
1. Landscape Client passes the message to the script execution manager plugin.
1. Landscape creates a temporary directory using `tempfile.mkdtemp`. The location is set with `--script-tempdir` or it will choose a default temporary directory, such as `/tmp/`.
1. A file is created with 700 permissions in the temporary directory. If Landscape Client snap is running, the specified user is granted ownership of the file. The script is written to the file.
1. The PATH environment variable is set to `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin`
1. The USER and HOME environment variables are set to the provided user and corresponding home path, if any.
1. The LANG, LC_ALL, LC_CTYPE, LD_LIBRARY_PATH, PYTHONPATH environment variables are copied from the root environment.
1. All of the environment variables in "env" from the message are also set.
1. If there are any attachments:
   1. A new temporary directory is created with 700 permissions and ownership is granted if on the snap version.
   1. Attachments are downloaded from Landscape Server using their unique identifiers into the temporary directory.
   1. Each attachment is given 600 permissions and ownership if on the snap.
   1. The LANDSCAPE_ATTACHMENTS environment variable is set to the temporary directory for attachments.
1. The script is executed with the environment variables. The output is limited by the `script_output_limit` configuration.
1. The script runs until it exits. If the time_limit is provided, the process will also exit after running for the provided time.
1. If the LANDSCAPE_ATTACHMENTS environment variable is set, Landscape Client will remove the attachments directory tree.
1. Landscape Client will send the output back to Landscape Server in an `operation-result` message. It will also report if the script was exited early due to timing out.
