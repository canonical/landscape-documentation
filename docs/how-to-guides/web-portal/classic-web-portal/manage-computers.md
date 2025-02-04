(how-to-guides-web-portal-classic-web-portal-manage-computers)=
# How to manage computers

## Register computers

To register computers with a Landscape server:

1. Navigate to your organization's home page
2. Click the link in the text *You can register new computers by following these instructions.*

This link provides the complete instructions for registering client computers with a Landscape server, which are also available at `https://yourserver/standalone/how-to-register`. You need to register computers with the server in order to manage them in Landscape.

## Select computers

You can select computers by selecting them individually, using searches or using [tags](/reference/terms/tags). 

To select computers individually:

1. Navigate to the **Computers** page in the header
2. Select each computer's checkbox in the **Select computers** list

To select computers using searches:

1. Navigate to the **Computers** page in the header
2. Enter search criteria using the search bar
3. Press **Enter**
4. Select the checkbox for each computer or click **All**

Landscape searches both the name and hostname associated with all computers for a match with the search term. Searches are not case-sensitive. A list of matching computers is displayed on the right side of the screen.

To select computers using tags:

1. Navigate to the **Computers** page in the header
2. Click any tag to display the list of computers associated with that tag
3. Select the checkbox for each computer or click **All**

## Apply tags to computers

To apply [tags](/reference/terms/tags) to computers:

1. Navigate to the **Computers** page in the header
2. Select the computers you want to associate with that tag
   - For more information, see [Select computers](#select-computers)
3. Click the **Info** tab
4. Enter the tag you want to use in the **Tags** row
5. Click **Add**

## Access information about computers

From the **Computers** page, you can get information about selected computers by clicking on tabs in the navigation menu. Commonly used tabs are described here.

* The **Activities** tab displays information about actions that may be applied to computers. You can filter by specific activities in the activity log by clicking **All**, **Pending**, **Unapproved** or **Failed**. You can also click on each activity in the list to display a screen with details about the activity. On that screen, you can **Approve**, **Cancel**, **Undo** or **Redo** the activity by clicking on the relevant button.

* The **Hardware** tab displays information about the selected computer's processor, memory, network, storage, audio, video, PCI and USB hardware, as well as BIOS information and CPU flags.

* The **Monitoring** tab displays graphs of key performance statistics, such as CPU load, memory use, disk use and network traffic.

  You can also create custom graphs to display at the top of the page by clicking **Create some now!**. A dropdown menu at the top of the screen lets you specify the timeframe the graph data covers: one day, three days, one week,or four weeks. You can download the data for each graph by clicking the relevant button under the graph.

* The **Processes** tab displays information about all processes running on a computer at the last time it contacted the Landscape server, and lets you end or kill processes by selecting them and clicking on the relevant buttons.

* The **Reports** tab displays seven visualizations that show what percentage of computers:

  * are securely patched
  * are covered by upgrade profiles
  * have contacted the server within the last five minutes
  * have applied security updates - four visualizations show computers that have applied Ubuntu Security Notices within the last two, 14, 30, and 60+ days

## Get computer IDs

There are two ways to locate the IDs for a specific computer:

- **Landscape API**: You can make a web request with `GetComputers` or use `get-computers` in the `landscape-api` command-line package. These methods output a list of all computers with information that includes their ID. For more information on using these methods, see [API Methods: Computers](https://ubuntu.com/landscape/docs/api-computers) and [using the landscape-api package](https://ubuntu.com/landscape/docs/command-line-client).
- **Landscape dashboard URL**: You can find the computer ID in the URL of the specific computer’s information page. The computer’s ID comes after `/computer` and before `/info`. For example, the computer ID would be 20 in the following URL: `https://landscape-server/account/standalone/computer/20/info`.
    
    To navigate to a specific computer’s information page:
    
    1. Click the **Computers** tab
    2. Locate and click the name of the specific computer you want the ID for

## Access the activity log

The **Activities** tab in the **Computers** page shows the status of Landscape activities in reverse chronological order.

You can view details on an individual activity by clicking on its description. Each activity is labelled with a status. Possible values are:

* Succeeded
* In progress
* Scheduled
* Queued
* Unapproved
* Cancelled
* Failed

You can select a subset to view by clicking **All**, **Pending**, **Unapproved**, or **Failed** above the table.

In addition to the status and description of each activity, the table shows what computers the activity applied to, who created it and when.

## Manage users

The **Users** tab in the **Computers** page displays a list of users on each of the selected computers.

You can select one or more users, and click one of the buttons at the top of the screen:

You must specify the person's name, a username and a passphrase. You may also specify a location and telephone numbers. Click **Add** at the bottom of the screen to complete the operation. **Delete** lets you delete the selected users.

You may also select a checkbox to delete the user's home folders as well. Click **Delete** at the bottom of the screen to complete the operation.

* **Edit** displays a **User details** page that lets you change details, including **Person's name**, **Primary Group**, **Passphrase**, **Location**, **Work phone** and **Home phone**. You can also click **Add** to add a user or **Remove** to remove a user from groups on the selected computers.
* The LOCK button prevents the selected users from logging into their accounts.
* The UNLOCK button unlocks previously locked accounts.

## Manage roles

Landscape offers Role-Based Access Control (RBAC) management of permissions for all users in the web portal. There are three main roles configured by default:

- GlobalAdministrator
- Auditor
- SupportAnalyst

To view the existing roles, navigate to your organization’s home page and click the **Roles** tab.

To add a new role from the **Roles** tab:

1. Click **Add role**
2. Provide a name in the **Role name** field
3. To set permissions that are applied globally, select the appropriate permissions in the *Global Permissions* section
4. To set permissions for certain access groups, select the appropriate permissions and access group(s) in the *Permissions* section
5. Click **Save**

To assign a role to a new user or edit the role(s) of an existing user:

1. Navigate to the **Roles** tab
2. Select the relevant cells for each user to grant or revoke their role status
3. Click **Save**

## Manage alerts

Landscape uses [alerts](/reference/terms/alerts) to notify administrators of conditions that require attention. The following types of alerts are available:

* when a pending computer needs to be accepted or rejected
* when you are exceeding your license entitlements for Landscape Dedicated Server (This alert does not apply to the hosted version of Landscape.)
* when new package updates are available for computers
* when new security updates are available for computers
* when a package profile is not applied
* when package reporting fails (Each client runs the command `apt-get update` every 60 minutes. Anything that prevents that command from succeeding is considered a package reporting failure.)
* when an activity requires explicit administrator acceptance or rejection
* when a computer has not contacted the Landscape server for more than five minutes
* when computers need to be rebooted in order for a package update (such as a kernel update) to take effect

To configure alerts, navigate to your organization's home page and click **Configure alerts** or the **Alerts** tab. Select the checkbox next to each type of alert you want to subscribe to, or click  **All** or **None** at the top of the table, then click **Subscribe** or **Unsubscribe**.

The **Alerts** tab displays the status of each alert. If an alert has not been triggered, the status is **OK**; if it has, the status is **Alerted**. The **Enabled for** column indicates whether the alert applies to all computers, a specified set of tagged computers, or your account. Pending computers, for example, are not yet Landscape clients, but they are part of your account.

If an alert is triggered, an administrator should typically investigate it. You can view active alerts from your organization's home page. If you click on an alert, the resulting screen displays additional information, such as the computer(s) affected, the error code, and error output text.

For some alerts, you can download a list of affected computers as a CSV file. Click **Save this search** to save the criteria that was generated from the alert.

## Manage scripts

```{note}
You must have remote script execution enabled to run scripts on the target Landscape Client. For more information, visit [how to enable script execution](https://ubuntu.com/landscape/docs/configure-landscape-client#heading--enable-script-execution).
```

You can run [scripts](/reference/terms/scripts) on the computers registered in your account. The scripts can be in any language, but an interpreter for that language must be present on the computers they're run on.

From your organization's home page, click the **Scripts** tab to display a list of existing scripts, the access group they belong to, and the creator. To add a new script, click **Add script**. On the next page, you must enter a title, interpreter, the script code, the time within which the script must complete, and the access group to which the script belongs. You may enter a default user to run the script. If you don't, you'll have to specify the user when you choose to run the script. You may also attach up to five files with a maximum of 1MB in total size. On each computer on which a script runs, attachments are placed in the directory specified by the environment variable LANDSCAPE_ATTACHMENTS, and are deleted once the script has been run. After specifying all the information for a stored script, click **Save** to save it.

To remove one or more existing scripts, select the checkbox next to each script you want to remove and click **Remove**. If you have the proper permissions, Landscape erases the script immediately without asking for confirmation. You can also edit or view a script by clicking on its script title.

To run a stored script, navigate to the **Scripts** tab from the **Computers** page in the header. Select the script you want to run or **Run a new script** to create a new script. When you choose to run an existing script, Landscape displays the script details, which allows you to modify any information. You must specify the user on the target computers to run the script, and schedule the script to run either as soon as possible, or at a specified time. When you're ready to run the script, click **Run**.

To run a new script, enter most of the same information you would if you were creating a stored script. You must specify the user on the target computers to run the script as, and you may optionally select **Save script** to save the new script. You must also schedule the script to run either as soon as possible, or at a specified time. When you're ready to run the script, click **Run**.

## Manage upgrade profiles

An [upgrade profile](/reference/terms/profiles/upgrade-profile) defines a schedule for the times when upgrades are to be automatically installed on the machines associated with a specific access group. You can associate zero or more computers with each upgrade profile via tags to install packages on those computers. You can also associate an upgrade profile with an access group, which limits its use to only computers within the specified access group. You can manage upgrade profiles from the **Upgrade Profiles** link in the **Profiles** tab on your organization's home page.

If you click **Upgrade Profiles**, Landscape displays a list of the names and descriptions of existing upgrade profiles.

To see the details of an existing profile, click on its name to display a screen that shows the name, schedule, and tags of computers associated with the upgrade profile. If you want to change the upgrade profile's name or schedule, click **Edit upgrade profile**. If you want to change the computers associated with the upgrade profile, select the checkboxes next to the appropriate tags on the lower part of the screen, then click **Change**. Although you can view the access group associated with the upgrade profile, you cannot change the access groups anywhere but from their association with a computer.

To add an upgrade profile, click **Add upgrade profile**.

On the resulting **Create an upgrade profile** page, you must enter a name for the upgrade profile. Names can contain only letters, numbers, and hyphens. You may select a checkbox to make the upgrade profile apply only to security upgrades; if you leave it unchecked, it will target all upgrades. Specify the access group to which the upgrade profile belongs from a dropdown menu. Finally, specify the schedule on which the upgrade profile can run. You can specify a number of hours to let the upgrade profile run; if it doesn't complete successfully in that time, Landscape will trigger an alert. Click **Save** to save the new upgrade profile.

To delete one or more upgrade profiles, select the checkbox next to the upgrade profiles' names, then click **Remove**.

## Manage removal profiles

A [removal profile](/reference/terms/profiles/removal-profile) defines a maximum number of days that a computer can go without exchanging data with the Landscape server before it's automatically removed. If more days pass than the profile's *Days without exchange*, that computer will automatically be removed and the license seat it held will be released. This helps Landscape keep license seats open and ensure Landscape is not tracking stale or retired computer data for long periods of time. You can associate zero or more computers with each removal profile via tags to ensure those computers are governed by this removal profile. You can also associate a removal profile with an access group, which limits its use to only computers within the specified access group. You can manage removal profiles from the **Removal profiles** page in the **Profiles** tab under your organization's home page.

When you do so, Landscape displays a list of the names and descriptions of existing removal profiles.

To see the details of an existing profile, click on its name to display a page that shows the title, name and number of days without exchange before the computer is automatically removed, and tags of computers associated with the removal profile. If you want to change the removal profile's title or number of days before removal, click **Edit removal profile**. If you want to change the computers associated with the removal profile, select the checkboxes next to the tags on the lower part of the screen, then click **Change**. Although you can view the access group associated with the removal profile, you cannot change the access groups anywhere but from their association with a computer.

To add a removal profile, click **Add removal profile**.

On the resulting **Create a removal profile** page, you must enter a title for the removal profile. Specify the access group to which the removal profile belongs from a dropdown menu. Finally, specify the number of days without exchange that computers will be allowed without contact before they are automatically removed and their license seat is released. If a computer doesn't contact Landscape within that number of days, it will be removed. Click **Save** to save the new removal profile.

To delete one or more removal profiles, select the checkbox next to the removal profiles' names, then click **Remove**.

