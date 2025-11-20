(how-to-manage-wsl-instances)=
# How to manage WSL instances

> See also: {ref}`reference-legacy-api-wsl`

This guide describes how to create and register new WSL instances to Landscape.

You must have a Windows host machine registered with Landscape before making any Windows Subsystem for Linux (WSL) instances. To register a new WSL host with Landscape, visit {ref}`how-to-register-wsl-hosts`.

## Register new WSL instances in the Landscape web portal

```{note}
Only one instance of each Ubuntu image can be created per Windows host machine using the web portal.
```

You can register new WSL instances from the Landscape web portal. To do this:

1. Navigate to the **Computers** page in the header
2. Click the name of the Windows machine that will host the new WSL instance
3. Click **Install new** above the **WSL Instances** table
4. Select the Ubuntu image that will be installed on the new WSL instance under **Instance Type**
5. Click **Submit**

Once this process is complete, your new WSL instance will appear in the **Select computers** list and in the Windows host machine’s **Info** tab.

## Register new WSL instances using a Landscape API

You can register new WSL instances via Landscape's legacy or REST APIs. To register new WSL instances with Landscape, make an API call such as:

```bash
?action=CreateChildComputer&parent_id=20&computer_name=Ubuntu
```
Or:

```bash
curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu"}'
```

The `parent_id` is assigned by Landscape. The `computer_name` is the name of the child computer you’re creating. Unless you are specifying a `rootfs_url`, this `computer_name` must match exactly the name of one of the supported Ubuntu WSL images in the Windows Store: `Ubuntu`, `Ubuntu-22.04`, or `Ubuntu-24.04`. If you don’t know the ID of your parent computer, visit {ref}`how to get computer IDs <howto-heading-manage-computers-get-ids>`.


## Register new WSL instances with cloud-init

```{note}
Cloud-init configuration isn't supported yet by Ubuntu Pro for Windows. This feature is planned in a future beta release.
```

You can use Landscape's legacy or REST API to register new WSL instances based on cloud-init configurations. Make an API call such as:

```bash
?action=CreateChildComputer&parent_id=20&computer_name=Ubuntu&cloud_init=<b64 encoded cloud_init file contents>
```
Or:

```bash
curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu", "cloud_init": "<b64 encoded cloud_init file contents>"}'
```

Or:

```bash
?action=CreateChildComputer&parent_id=20&computer_name=Ubuntu&data_id=data-id&token=vault-token
```
Or:

```bash
curl -X POST https://your-landscape.domain.com/api/v2/computers/20/children -H "Authorization: Bearer $JWT" -d '{"computer_name": "Ubuntu", "data_id": "data-id", "token": "vault-token"}'
```

If your cloud-init file is not located in a vault, you can specify it in `cloud_init`. If it's located in a vault, you can specify the name of the vault secret in `data_id` and the authentication token to be passed to the secrets manager in `token`.

```{note}
Specifying both a cloud-init file and a vault secret will result in an error.
```

## Set a WSL instance as default

You can set a default instance with the legacy API. To set a managed WSL instance as the default one on the Windows machine, make an API call such as:

```bash
?action=SetDefaultChildComputer&parent_id=20&child_id=21
```
Or:
```bash
landscape-api set-default-child-computer 20 21
```

## Remove a WSL instance

You can remove an instance with the legacy API. To remove managed WSL instances from their Windows host machines, make an API call such as:

```bash
?action=DeleteChildComputers&computer_ids.1=21&computer_ids.2=34
```
Or:

```bash
landscape-api delete-child-computers 21,34
```

Removing a WSL instance from its Windows host machine will also remove the associated WSL instance from Landscape.

## Use WSL profiles

```{note}
This feature is currently in beta.
```

You can use WSL profiles to provision WSL instances from official Ubuntu images in the Microsoft Store or from custom images at scale. These WSL instances can be configured with cloud-init at the time of provisioning.

For more information, see {ref}`how-to-use-wsl-profiles`.

