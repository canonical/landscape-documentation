---
myst:
  html_meta:
    description: "Perform common WSL tasks in Landscape: start, shutdown, set default instances, and remove WSL instances via web portal or API."
---

(how-to-wsl-perform-common-tasks)=
# How to perform common tasks with WSL in Landscape

> See also: {ref}`reference-legacy-api-wsl`

This guide describes some common tasks you may perform with Landscape for managed WSL instances and Windows hosts.

If you haven't registered your WSL hosts or WSL instances yet with Landscape, see {ref}`how-to-register-wsl-hosts` and {ref}`how-to-manage-wsl-instances`.

Note that you need your computer IDs for many of these calls. If you don’t know the IDs of your child computers, visit {ref}`how to get computer IDs <howto-heading-manage-computers-get-ids>`.

## Start WSL instances registered in your Landscape account

You can remotely start a list of one or more WSL instances via the Landscape API. To start a WSL instance, you need the **legacy** API. See {ref}`Start Child Computers (Legacy API) <reference-legacy-api-wsl-start-child-computer>`.

## Shutdown WSL instances registered in your Landscape account

You can remotely shutdown a list of one or more WSL instances via the Landscape API. To shutdown WSL instances, you need the **legacy** API. See {ref}`Stop Child Computers (Legacy API) <reference-legacy-api-wsl-stop-child-computer>`.

## Set a default WSL instance

The "default instance" is the instance you log into if you run `wsl` in PowerShell from the Windows host. You can set your default child computer in the Landscape web portal or via the API.

### Web portal

1. Go to **Instances** > Open the Windows host machine > **WSL** tab
1. Select the instance you want to make default > Open the dot menu > **Set as default**

This queues an activity to set that instance as default.

### API

Within Landscape, you can only set a WSL instance as default with the **legacy** API. See {ref}`Set Default Child Computer (Legacy API) <reference-legacy-api-wsl-set-default-child-computer>`.

## Remove a WSL instance

### Web portal

To remove a WSL instance in the web portal:

1. Go to **Instances** > Open the Windows host (parent) machine > **WSL** tab
1. Select your instance, and click **Uninstall**

If you remove a WSL instance from its Windows host machine outside of Landscape, the WSL instance will also be removed from your Landscape account.

### API

To remove a WSL instance via the API, you need the **legacy** API. See {ref}`Delete Child Computers (Legacy API) <reference-legacy-api-wsl-delete-child-computer>`.

(howto-heading-wsl-view-computers)=
## View WSL host machines and child computers

From the Landscape web portal, you can view all WSL host machines and their associated WSL instances (child computers).

To view all WSL host machines, go to **Instances** > **Filters** > **OS** > **Windows**

To view the WSL instances associated with a specific WSL host, go to **Instances** > Open the Windows host machine > **WSL** tab.

If you only want to view WSL machines, you can do this by applying tags to those machines. For more information, visit {ref}`how to apply tags to computers <howto-heading-manage-computers-appy-tags>`.
