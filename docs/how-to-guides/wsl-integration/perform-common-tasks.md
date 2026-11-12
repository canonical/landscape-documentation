---
myst:
  html_meta:
    description: "Perform common WSL tasks in Landscape: start, shut down, set default instances, and delete WSL instances via the web portal or API."
---

(how-to-wsl-perform-common-tasks)=
# How to perform common tasks with WSL in Landscape

> See also: {ref}`reference-legacy-api-wsl`

This guide describes some common tasks you may perform with Landscape for managed WSL instances and Windows hosts.

If you haven't registered your WSL hosts or WSL instances yet with Landscape, see {ref}`how-to-register-wsl-hosts` and {ref}`how-to-manage-wsl-instances`.

Note that you need your computer IDs for many of these calls. If you don't know the IDs of your child computers, visit {ref}`how to get computer IDs <howto-heading-manage-computers-get-ids>`.

## Start WSL instances

You can remotely start a list of one or more WSL instances via the legacy API. To start WSL instances, or child computers, by ID, make an API call such as:

```bash
?action=StartChildComputers&computer_ids.1=21&computer_ids.2=22
```

## Shut down WSL instances

You can remotely shut down a list of one or more WSL instances via the legacy API. To shut down WSL instances, or child computers, by ID, make an API call such as:

```bash
?action=StopChildComputers&computer_ids.1=21&computer_ids.2=22
```

## Set a default WSL instance

You can set a specific WSL instance as the default child computer. This will be the default instance you log into if you run `wsl` in PowerShell from the Windows host. You can set your default child computer in the Landscape web portal or via the API.

### Web portal (24.04 LTS and later)

1. Go to **Instances** > Open the Windows host machine > **Instances** tab
1. Click the pin icon (**Set default instance**) next to the WSL instance you want to set as default, then click **Set default**

### Classic web portal

1. Navigate to the **Computers** page in the header
1. Click the name of the Windows machine that you want to set a default instance on
1. Click **Set as default** near the name of the child computer you want to set as default

### API

To set your default child computer via the legacy API, make an API call such as:

```bash
?action=SetDefaultChildComputer&parent_id=30&child_id=32
```

## Log in to any WSL instance

You can log into any WSL instance that is a child computer from your Windows host. To do this, run the following in PowerShell. Replace `<CHILD_COMPUTER_NAME>` with your specific computer name.

```powershell
wsl -d <CHILD_COMPUTER_NAME>
```

An example command could be:

```powershell
wsl -d Ubuntu-22.04
```

If you're logging into your default child computer, you only need to run `wsl` in PowerShell.

## Delete a WSL instance

You can delete, or uninstall, any WSL instances from the Landscape web portal or via the API.

### Web portal (24.04 LTS and later)

1. Go to **Instances** > Open the Windows host machine > **Instances** tab
1. Click the delete icon (**Delete instance**) next to the WSL instance you want to delete, then click **Delete**

### Classic web portal

1. Navigate to the **Computers** page in the header
1. Click the name of the Windows machine that hosts the WSL instance you will delete
1. Click **Uninstall** near the name of the WSL instance you want to delete

### API

To delete a WSL instance via the legacy API, make an API call such as:

```bash
?action=DeleteChildComputers&computer_ids.1=21
```

(howto-heading-wsl-view-computers)=
## View WSL host machines and child computers

From the classic web portal, you can view all WSL host machines and their associated WSL instances, or child computers. All machines associated with WSL indicate their status next to their name in the **Select computers** table. WSL child instances also display their parent Windows machine next to their name.

If you only want to view WSL machines, you can do this by applying tags to those machines. For more information, visit {ref}`how to apply tags to computers <howto-heading-manage-computers-appy-tags>`.

You can also get a list of all WSL hosts via the legacy API. To do this, make an API call such as:

```bash
?action=GetWSLHosts
```
