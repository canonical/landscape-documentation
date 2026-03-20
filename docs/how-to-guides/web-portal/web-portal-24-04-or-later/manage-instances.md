---
myst:
  html_meta:
    description: "View, search, and manage instances in Landscape's 24.04+ portal. Learn to manage instances, view details, and perform bulk operations."
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

To view detailed information about a specific instance, click on the instance name to open its **Info** page. That page displays information such as:

- Status
- Last ping time
- Access group
- Registration details

## Manage individual instances

You can perform several management tasks from each individual instance's page. Go to **Instances** > click the instance you want to manage.

From the specific instance's page, click into any of the tabs to view information or perform various management tasks on that instance. You can perform several tasks across the different tabs on this page, such as:

- View, cancel, and undo/redo activities
- View, upgrade, or downgrade the kernel
- Manage snaps and Debian packages
- Fix security issues
- View hardware information

## Perform actions on multiple instances

You can perform certain actions on multiple instances at once, such as restarting, attaching Pro tokens, or running scripts on the selected instances. From the **Instances** page:

1. Select one or more instances
1. Click the relevant action button

All actions will require you to confirm or provide more details in a side panel.

## Remove instances

To remove an instance from Landscape, go to **Instances** > click the name of the instance to delete > **More actions** > **Remove from Landscape**. You'll need to complete a prompt to confirm the removal.

Removing an instance only removes it from Landscape's management. This action doesn't affect the actual machine.

You can also use {ref}`removal profiles <reference-terms-removal-profile>` to automate removal of inactive client instances.
