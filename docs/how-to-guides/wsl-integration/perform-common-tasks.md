(how-to-wsl-perform-common-tasks)=
# How to perform common tasks with WSL in Landscape

> See also: {ref}`reference-legacy-api-wsl`

```{note}
This guide assumes that a registered WSL host and WSL instance already exist in Landscape. For more information, visit {ref}`how-to-register-wsl-hosts` and {ref}`how-to-manage-wsl-instances`.
```


## Start WSL instances registered in your Landscape account

You can remotely start a list of one or more WSL instances via the Landscape API. To start WSL instances, or child computers, by ID, make an API call such as:

```bash
?action=StartChildComputers&computer_id.1=21&computer_id.2=22
```

If you don’t know the IDs of your child computers, see {ref}`how to get computer IDs <howto-heading-manage-computers-get-ids>`.

## Shutdown WSL instances registered in your Landscape account

You can remotely shutdown a list of one or more WSL instances via the Landscape API. To shutdown WSL instances, or child computers, by ID, make an API call such as:

```bash
?action=StopChildComputers&computer_id.1=21&computer_id.2=22
```

If you don’t know the IDs of your child computers, visit {ref}`how to get computer IDs <howto-heading-manage-computers-get-ids>`.
## Set a default WSL instance

The "default instance" is the instance you log into if you run `wsl` in PowerShell from the Windows host. You can set your default child computer in the Landscape web portal or via the API.

### Web portal

1. Go to **Instances** > Open the Windows host machine > **WSL** tab
1. Select the instance you want to make default > Open the dot menu > **Set as default**

This queues an activity to set that instance as default.

### API

Within Landscape, you can only set a WSL instance as default with the **legacy** API. See {ref}`reference-legacy-api-wsl-set-default-child-computer`.

## Remove a WSL instance

### Web portal

To remove a WSL instance in the web portal:

1. Go to **Instances** > Open the Windows host (parent) machine > **WSL** tab
1. Select your instance, and click **Uninstall**

If you remove a WSL instance from its Windows host machine outside of Landscape, the WSL instance will also be removed from your Landscape account.

### API

To remove a WSL instance via the API, you need the **legacy** API. See {ref}`Computers (Legacy API)<reference-legacy-api-wsl>`.

If you don’t know the IDs of your child computers, visit {ref}`how to get computer IDs <howto-heading-manage-computers-get-ids>`.

(howto-heading-wsl-view-computers)=
## View WSL host machines and child computers

From the Landscape web portal, you can view all WSL host machines and their associated WSL instances, or child computers. All machines associated with WSL indicate their status next to their name in the **Select computers** table. WSL child instances also display their parent Windows machine next to their name.

If you only want to view WSL machines, you can do this by applying tags to those machines. For more information, visit {ref}`how to apply tags to computers <howto-heading-manage-computers-appy-tags>`.

You can also get a list of all WSL hosts via the Landscape API. To do this, make an API call such as:

```bash
?action=GetWSLHosts
```

