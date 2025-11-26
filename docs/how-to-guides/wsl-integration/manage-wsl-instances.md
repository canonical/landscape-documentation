(how-to-manage-wsl-instances)=
# How to manage WSL instances

This guide describes how to create and register new WSL instances to Landscape and other management tasks.

You must have a Windows host machine registered with Landscape before making any WSL instances. To register a new Windows host with Landscape, visit {ref}`how-to-register-wsl-hosts`.

## Create and register new WSL instances in the Landscape web portal

```{note}
Only one instance of each Ubuntu image can be created per Windows host machine using the web portal.
```

You can register new WSL instances from the Landscape web portal. To do this:

1. Go to **Instances** > Open the Windows host machine > **WSL** tab > **Create new instance**
1. Complete the form

This creates an activity to create the new WSL instance. Once that activity succeeds, accept the pending WSL instance. You can do this from the homepage or under **Instances** > **Review pending instances**.

Now, your WSL instance is registered in your Landscape account. You can view it from the **WSL** tab under your Windows host machine.

## Use a Landscape API

You can register new WSL instances and manage existing ones with the REST API or legacy API. See the following endpoints: 
- {ref}`reference-rest-api-wsl`
- {ref}`reference-rest-api-child-instance-profiles`
- {ref}`reference-rest-api-computers`
- {ref}`WSL (Legacy API) <reference-legacy-api-wsl-set-default-child-computer>`

Note that you'll need IDs for many of the requests. If you don’t know the ID of your parent instance, visit {ref}`how to get computer IDs <howto-heading-manage-computers-get-ids>`.

## Set a WSL instance as default

The "default instance" is instance you log into if you run `wsl` in PowerShell from the Windows host. Within Landscape, you can only set a WSL instance as default with the **legacy** API. See {ref}`reference-legacy-api-wsl-set-default-child-computer`.

## Remove a WSL instance in the web portal

To remove a WSL instance in the web portal:

1. Go to **Instances** > Open the Windows host (parent) machine > **WSL** tab
1. Select your instance, and click **Uninstall**

If you remove a WSL instance from its Windows host machine outside of Landscape, the WSL instance will also be removed from your Landscape account.

## Use WSL profiles

You can use WSL profiles to provision WSL instances from official Ubuntu images in the Microsoft Store or from custom images. These WSL instances can be configured with cloud-init at the time of provisioning.

For more information, see {ref}`how-to-use-wsl-profiles`.
