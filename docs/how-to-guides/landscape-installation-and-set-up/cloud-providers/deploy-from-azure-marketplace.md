---
myst:
  html_meta:
    description: "Deploy self-hosted Landscape Server from the Azure Marketplace as a managed application. Create the deployment in the Azure portal, access the web portal, manage SSH access, and delete the deployment."
---

(how-to-deploy-from-azure-marketplace)=
# How to deploy Landscape Server from the Azure Marketplace

Canonical provides self-hosted Landscape Server as an Azure Marketplace managed application. You deploy it from the Azure portal, and it creates the Azure virtual machine (VM) and other resources that run Landscape Server in your own Azure subscription. You don't need to install Landscape Server yourself.

A managed application uses two resource groups in your subscription:

- **Application resource group**: Contains the managed application resource. You have full access to this resource group, and you use the managed application to manage the deployment's lifecycle.
- **Managed resource group**: Contains the resources that the application deploys, such as the VM, its disks, and its network resources. Your access to this resource group might be limited. For more information, see {ref}`how-to-deploy-from-azure-marketplace-managed-rg`.

For more information about managed applications, see [Microsoft's overview of Azure Managed Applications](https://learn.microsoft.com/en-us/azure/azure-resource-manager/managed-applications/overview).

```{note}
To build your own Landscape Server VM on Azure with the Azure CLI and cloud-init instead, see {ref}`how-to-install-on-microsoft-azure`. That method gives you full control of the VM and its configuration. The Azure Marketplace offer creates the resources for you from the Azure portal.
```

```{warning}
Deploying this offer costs money. The Azure resources that it creates, such as VMs, disks, public IP addresses, and network traffic, are billed to your Azure subscription for as long as they exist. Any software or plan charges for the offer are shown on the offer's page in the Azure portal and are also billed through your subscription.

To stop these charges, delete the managed application as described in {ref}`how-to-deploy-from-azure-marketplace-delete`.
```

## Prerequisites

You need:

- An Azure subscription with a valid payment method. Your account needs at least the Contributor role on the subscription, or on the resource group that you deploy the managed application to. Your organization might also restrict Marketplace purchases. For more information, see [Microsoft's documentation on purchasing from the Marketplace](https://learn.microsoft.com/en-us/marketplace/azure-purchasing-invoicing).
- An SSH key pair, to sign in to the Landscape Server VM. If you don't have one, you can create an ED25519 key pair with:

  ```bash
  ssh-keygen -t ed25519
  ```

  For more information, see [Microsoft's documentation on SSH keys for Linux VMs](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/mac-create-ssh-keys).

% TODO(LNDENG-5582): confirm from the offer's createUiDefinition.json whether the offer asks for a host name or domain
- A domain name for Landscape Server, and access to its DNS records, if the offer asks you for a host name.

## Deploy the managed application

% TODO(LNDENG-5582): confirm the final public Marketplace listing name and URL (see CPC-12375 for the production offer and plan), and add a direct link
1. Sign in to the Azure portal, go to **Marketplace**, and search for **Landscape**.
2. Select the Landscape offer from Canonical. If the offer has more than one plan, select the plan that you want, then select **Create**.
3. On the **Basics** tab, enter the details that all managed applications require:

    - **Subscription**: The subscription to deploy to, and to bill.
    - **Resource group**: The resource group for the managed application. You can create a new one.
    - **Region**: The Azure region to deploy to.
    - **Application name**: A name for the managed application.
    - **Managed resource group**: The name of the managed resource group that Azure creates for the deployed resources. You can keep the default name.

% TODO(LNDENG-5582): confirm the offer's wizard tabs and fields (for example VM size, administrator user name, SSH public key, host name, and email) from the offer's createUiDefinition.json
4. Complete the offer's other settings. When you're asked for an SSH public key, paste the contents of your public key file, for example `~/.ssh/id_ed25519.pub`. Note the administrator user name, because you need it to sign in to the VM with SSH.
5. On the **Review + create** tab, check your settings and the offer's terms and price, then select **Create**.

The portal shows the deployment's progress. When the deployment is complete, the managed application is in the resource group that you selected, and the deployed resources are in the managed resource group.

## Access the Landscape web portal

% TODO(LNDENG-5582): confirm the offer's outputs (for example the Landscape URL, public IP address, or FQDN) from the offer's mainTemplate.json and createUiDefinition.json
To find the address of your Landscape server, open the managed application in the Azure portal and check its outputs. You can also show the managed application's outputs with the Azure CLI:

```bash
az managedapp show --name <application-name> --resource-group <resource-group> --query outputs
```

Alternatively, open the managed resource group, select the VM, and find its public IP address on the VM's **Overview** page.

If you use a domain name for Landscape Server, create an A record for it in your DNS service that points to the VM's public IP address.

Then, to configure Landscape:

1. Navigate to the Landscape web portal by entering the FQDN or IP address of the Landscape VM into a browser window.

2. Provide a name, email address, and password for the first global administrator on the machine.

## Manage the deployment

(how-to-deploy-from-azure-marketplace-managed-rg)=
### Understand your access to the managed resource group

The publisher of a managed application chooses how much access you have to the managed resource group. In the default permission scenario, a deny assignment on the managed resource group limits you to read actions, plus any actions that the publisher allows. Depending on the offer, you might not be able to change, stop, or delete individual resources in the managed resource group, such as the VM or its network security group.

% TODO(LNDENG-5582): confirm the offer's permission scenario (deny assignment and allowed customer actions) from the offer's plan configuration
To check your access, open the managed resource group in the Azure portal, select **Access control (IAM)**, and check the **Deny assignments** tab.

### Sign in to the VM with SSH

% TODO(LNDENG-5582): confirm from the offer's mainTemplate.json that the network security group allows inbound SSH (port 22)
To sign in to the Landscape Server VM, use SSH with the administrator user name that you entered when you deployed the offer, and the private key that matches the public key that you entered:

```bash
ssh -i ~/.ssh/id_ed25519 <admin-username>@<public-ip-address-or-fqdn>
```

### Add or reset an SSH key

To add an SSH public key for a user on the VM, or to replace a lost key, you can use the Azure CLI or the Azure portal. Both use the VMAccess extension, which changes the VM. If the managed resource group has a deny assignment that doesn't allow this action, the change fails.

With the Azure CLI, run the following command. It adds the public key to the user's `~/.ssh/authorized_keys` file, and doesn't remove existing keys:

```bash
az vm user update \
    --resource-group <managed-resource-group> \
    --name <vm-name> \
    --username <admin-username> \
    --ssh-key-value ~/.ssh/id_ed25519.pub
```

To find the VM's name, run `az vm list --resource-group <managed-resource-group> --output table`.

In the Azure portal, select the VM, then select **Help** > **Reset password**. Select **Reset SSH public key** as the mode, enter the user name and the SSH public key, then select **Update**.

If you can already sign in with SSH, you can also add keys yourself by editing `~/.ssh/authorized_keys` on the VM.

### Upgrade Landscape Server

% TODO(LNDENG-5582): confirm how the offer installs Landscape Server (for example Quickstart installation) and whether the offer provides its own upgrade mechanism
To upgrade Landscape Server, sign in to the VM with SSH and follow {ref}`how-to-upgrade`.

(how-to-deploy-from-azure-marketplace-delete)=
## Delete the deployment

When you no longer need the deployment, delete the managed application. Azure then deletes the managed resource group and all the resources in it, and the charges for them stop.

In the Azure portal, open the managed application, select **Delete**, and confirm.

With the Azure CLI, run:

```bash
az managedapp delete --name <application-name> --resource-group <resource-group>
```

If you created a resource group only for the managed application, you can then delete that resource group too:

```bash
az group delete --name <resource-group>
```
