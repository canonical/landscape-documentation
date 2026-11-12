---
myst:
  html_meta:
    description: "Create and register WSL instances in Landscape from the web portal or the legacy API."
---

(how-to-manage-wsl-instances)=
# How to manage WSL instances

> See also: {ref}`reference-legacy-api-wsl`

This guide describes how to create and register new WSL instances to Landscape.

You must have a Windows host machine registered with Landscape before making any WSL instances. To register a new Windows host with Landscape, visit {ref}`how-to-register-wsl-hosts`.

## Create and register new WSL instances in the Landscape web portal

### Web portal (24.04 LTS and later)

1. Go to **Instances** > Open the Windows host machine > **Instances** tab > **Install new instance**
1. Select the Ubuntu image under **Instance type**
1. Click **Install**

### Classic web portal

```{note}
Only one instance of each Ubuntu image can be created per Windows host machine using the web portal.
```

1. Navigate to the **Computers** page in the header
1. Click the name of the Windows machine that will host the new WSL instance
1. Click **Install new** above the **WSL Instances** table
1. Select the Ubuntu image that will be installed on the new WSL instance under **Instance Type**
1. Click **Submit**

Once this process is complete, your new WSL instance will appear in the **Select computers** list and in the Windows host machine's **Info** tab.

## Create and register new WSL instances with the API

You can register new WSL instances via the legacy API. To register new WSL instances with Landscape, make an API call such as:

```bash
?action=CreateChildComputer&parent_id=20&computer_name=Ubuntu
```

The `parent_id` is assigned by Landscape. You assign `computer_name` as the name of the child computer you're creating. If you don't know the ID of your parent computer, visit {ref}`how to get computer IDs <howto-heading-manage-computers-get-ids>`.

## Create and register new WSL instances with the API and cloud-init

```{note}
When Landscape 24.04 LTS was released, Ubuntu Pro for WSL didn't yet support cloud-init configuration.
```

To register new WSL instances based on cloud-init configurations, make an API call such as:

```bash
?action=CreateChildComputer&parent_id=20&computer_name=Ubuntu&cloud_init=<b64 encoded cloud_init file>
```

Or:

```bash
?action=CreateChildComputer&parent_id=20&computer_name=Ubuntu&data_id=data-id&token=vault-token
```

If your cloud-init file is not located in a vault, you can specify it in `cloud_init`. If it's located in a vault, you can specify the name of the vault secret in `data_id` and the authentication token to be passed to the secrets manager in `token`.

```{note}
Specifying both a cloud-init file and a vault secret will result in an error.
```
