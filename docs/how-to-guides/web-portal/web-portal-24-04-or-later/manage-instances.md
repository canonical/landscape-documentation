---
myst:
  html_meta:
    description: "View, search, and manage instances in Landscape's 24.04+ portal. Learn to manage instances, use saved searches, view details, and perform bulk operations."
---

(how-to-web-portal-manage-instances)=
# How to manage instances

You can use the web portal to view, manage, and perform actions on your Ubuntu client instances.

## View and search all instances

Go to **Instances** from the sidebar to view your instances. The default view displays a list of all the instances you have permission to view, and includes information such as:

- Instance hostname or title
- Status (online/offline, alerts, reboot required, etc.)
- Operating system and version
- Tags

You can also use the search bar to find specific client instances.

## Save and reuse instance searches

Saved searches let you save and reuse instance queries in Landscape. They’re useful for quickly filtering instances by specific criteria without rebuilding the query each time.

Note that saved searches can only be used to filter instances.

```{note}
This feature is only available in self-hosted **Landscape 26.04 LTS** and later.
```

**Create a saved search**

There are two ways to create a saved search: directly from the search bar or from the full saved searches management panel. The first option lets you quickly save a query you're currently using, and the second option lets you create a new search query.

**(Option #1) From the search bar:**

1. Type your query in the **Instances** search bar
2. Click **Save search**
3. Enter a title > **Add saved search**

**(Option #2) From the management panel:**

1. Click the search bar > **Manage** > **Add saved search**
2. Enter a title and search query > **Add saved search**

The search query editor provides auto-complete and syntax suggestions to help you construct valid queries.

**Apply a saved search**

To filter your instances, click the search bar on the **Instances** page and select a saved search from the list.

**Edit or delete a saved search**

You can manage your saved searches from the dropdown list or the management panel.

To **edit**, click the **pencil** icon next to the saved search. Note that you can only edit the search query, not the title.

To **delete**, click the **trash can** icon next to the saved search and confirm the deletion.

## Manage individual instances

You can perform several management tasks from each individual instance's page. Go to **Instances** > click the instance you want to manage.

From the specific instance's page, click into any of the tabs to view information or perform various management tasks on that instance. You can perform several tasks across the different tabs on this page, such as:

- View, cancel, and undo/redo activities
- View, upgrade, or downgrade the kernel
- Manage snaps and Debian packages
- Fix security issues
- View hardware information

To view detailed information about a specific instance, click on the instance name to open its **Info** page. That page displays information such as:

- Status
- Last ping time
- Access group
- Registration details

## Perform actions on multiple instances

You can perform certain actions on multiple instances at once, such as restarting, attaching Pro tokens, or running scripts on the selected instances. From the **Instances** page:

1. Select one or more instances
1. Click the relevant action button

All actions will require you to confirm or provide more details in a side panel.

## Remove instances

To remove an instance from Landscape, go to **Instances** > click the name of the instance to delete > **More actions** > **Remove from Landscape**. You'll need to complete a prompt to confirm the removal.

Removing an instance only removes it from Landscape's management. This action doesn't affect the actual machine.

You can also use {ref}`removal profiles <reference-terms-removal-profile>` to automate removal of inactive client instances.
