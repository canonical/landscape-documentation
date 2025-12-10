(how-to-manage-wsl-instances)=
# How to manage WSL instances

This guide describes how to create, register, and provision new WSL instances to Landscape.

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

## Use WSL profiles

You can use {ref}`WSL profiles <reference-terms-wsl-profile>` to provision WSL instances from official Ubuntu images in the Microsoft Store or from custom images. These WSL instances can be configured with cloud-init at the time of provisioning.

For more information, see {ref}`how-to-use-wsl-profiles`.
