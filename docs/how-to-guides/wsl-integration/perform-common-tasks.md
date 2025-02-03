(how-to-guides-wsl-integration-perform-common-tasks)=
# How to perform common tasks with WSL in Landscape

> See also: [WSL API methods](/reference/api/legacy-api-endpoints/wsl)

```{note}
This guide assumes that a registered WSL host and WSL instance already exist in Landscape. For more information, visit [how to register WSL hosts to Landscape](/how-to-guides/wsl-integration/register-wsl-hosts) and [how to register WSL instances to Landscape](/how-to-guides/wsl-integration/manage-wsl-instances).
```


## Start WSL instances registered in your Landscape account

You can remotely start a list of one or more WSL instances via the Landscape API. To start WSL instances, or child computers, by ID, make an API call such as:

```bash
?action=StartChildComputers&computer_id.1=21&computer_id.2=22
```

If you don’t know the IDs of your child computers, see [how to get computer IDs](https://ubuntu.com/landscape/docs/managing-computers#heading--get-computer-ids).

## Shutdown WSL instances registered in your Landscape account

You can remotely shutdown a list of one or more WSL instances via the Landscape API. To shutdown WSL instances, or child computers, by ID, make an API call such as:

```bash
?action=StopChildComputers&computer_id.1=21&computer_id.2=22
```

If you don’t know the IDs of your child computers, visit [how to get computer IDs](https://ubuntu.com/landscape/docs/managing-computers#heading--get-computer-ids).

## Set a default WSL instance

You can set a specific WSL instance as the default child computer. This will be the default instance you log into if you run `wsl` in PowerShell from the Windows host. You can set your default child computer in the Landscape web portal or via the API.

To set your default child computer in the Landscape web portal:

1. Navigate to the **Computers** page in the header

2. Click the name of the Windows machine that you want to set a default instance on

3. Click **Set as default** near the name of the child computer you want to set as default

To set your default child computer via the Landscape API, make an API call such as:

```bash
?action=SetDefaultChildComputer&parent_id=30&child_id=32
```

If you don’t know the IDs of your child computers, visit [how to get computer IDs](https://ubuntu.com/landscape/docs/managing-computers#heading--get-computer-ids).

## Log in to any WSL instance

You can log into any WSL instance that is a child computer from your Windows host. To do this, run the following in PowerShell. Replace `{CHILD_COMPUTER_NAME}` with your specific computer name.

```powershell
wsl -d {CHILD_COMPUTER_NAME}
```

An example command could be:

```powershell
wsl -d Ubuntu-22.04
```

If you’re logging into your default child computer, you only need to run `wsl` in PowerShell.

## Delete a WSL instance

You can delete, or uninstall, any WSL instances from the Landscape web portal or via the API.

To delete a WSL instance from the Landscape web portal:

1. Navigate to the **Computers** page in the header

2. Click the name of the Windows machine that hosts the WSL instance you will delete

3. Click **Uninstall** near the name of the WSL instance you want to delete

To delete a WSL instance via the API, make an API call such as:

```bash
?action=DeleteChildComputers&computer_id.1=21
```

If you don’t know the IDs of your child computers, visit [how to get computer IDs](https://ubuntu.com/landscape/docs/managing-computers#heading--get-computer-ids).

## View WSL host machines and child computers

From the Landscape web portal, you can view all WSL host machines and their associated WSL instances, or child computers. All machines associated with WSL indicate their status next to their name in the **Select computers** table. WSL child instances also display their parent Windows machine next to their name.

If you only want to view WSL machines, you can do this by applying tags to those machines. For more information, visit [how to apply tags to computers](https://ubuntu.com/landscape/docs/managing-computers#heading--apply-tags-to-computers).

You can also get a list of all WSL hosts via the Landscape API. To do this, make an API call such as:

```bash
?action=GetWSLHosts
```

