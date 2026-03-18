---
myst:
  html_meta:
    description: "Execute scripts remotely on Landscape client instances using the web portal. Learn to run scripts, monitor execution, and handle results."
---

(how-to-web-portal-use-remote-script-execution)=
# How to use remote script execution

> See also: {ref}`explanation-remote-script-execution`, {ref}`reference-terms-script-profile`

Remote script execution allows you to run scripts on your registered client instances directly from the Landscape web portal. Scripts can be in any language, as long as an appropriate interpreter is available on the clients where they will run.

This document guides you how to use remote script execution for client instances on classic Ubuntu systems. If you're using the Landscape Client snap on Ubuntu Core, see {ref}`how-to-remote-script-execution`.

## Prerequisites

Before you can execute scripts from Landscape Server, you must have {ref}`remote script execution enabled <howto-heading-client-enable-script-execution>` on the target client instances.

## Add a new script

To add a new script:

1. Go to **Scripts** from the sidebar > **Add script**
1. Copy your script into the editor or populate it from a file
1. Complete the other portions of a form, including a title for the script, access group, and optional attachments, then **Add script**

You can edit, archive, run and more on the script using the dot menu under **Actions** for each script.

## Run a script on one or more instances

To run a script on one or more instances:

1. Go to **Instances** from the sidebar > Select the target instance(s) > **Run script**
1. In the side panel that opens, complete the form > **Run**
   - Note: **Time limit** is the maximum time the script can run before Landscape forcibly terminates it

## View script execution status and results

After you run a script, you can monitor its progress and view results.

### From the Activities page

The **Activities** page shows the activity status for all instances and all activities. Your script execution activities will appear here.

### From an instance's detail page

1. Go to **Instances** > Select your instance > **Activities** tab to view all activities for that instance, including script executions.
1. Click on a script execution activity to view details, such as status, when the script was run, and output/results from the script (if any).

## Schedule scripts with script profiles

To run scripts on a recurring schedule or at specific times, use {ref}`script profiles <reference-terms-script-profile>`. Script profiles allow you to run scripts based on certain triggers.

For details, see {ref}`how to use script profiles<how-to-web-portal-use-script-profiles>`.
