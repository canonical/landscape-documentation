---
myst:
  html_meta:
    description: "Deploy Landscape Server from the Azure Marketplace as a managed application. Create the deployment in the Azure portal, sign in to the web portal, and delete the deployment."
---

(how-to-deploy-from-azure-marketplace)=
# How to deploy Landscape Server from the Azure Marketplace

Canonical provides Landscape Server as an Azure Marketplace managed application. You deploy it from the Azure portal, and it creates the Azure resources that run Landscape Server in your own Azure subscription. You don't need to install Landscape Server yourself.

The deployment uses Juju to deploy the Landscape Server charms, together with HAProxy, PostgreSQL, and RabbitMQ, on Ubuntu 24.04 LTS virtual machines (VMs). Canonical operates the deployment and pins the Landscape Server version that it deploys.

A managed application uses two resource groups in your subscription:

- **Application resource group**: Contains the managed application resource. You have full access to this resource group, and you use the managed application to manage the deployment's lifecycle.
- **Managed resource group**: Contains the resources that the application deploys, such as the VMs, their disks, and their network resources. Your access to this resource group is limited. For more information, see {ref}`how-to-deploy-from-azure-marketplace-managed-rg`.

For more information about managed applications, see [Microsoft's overview of Azure Managed Applications](https://learn.microsoft.com/en-us/azure/azure-resource-manager/managed-applications/overview).

```{note}
To build your own Landscape Server VM on Azure with cloud-init instead, see {ref}`how-to-install-on-microsoft-azure`. That method gives you full control of the VM and its configuration.
```

```{warning}
Deploying this offer costs money. The Azure resources that it creates, such as VMs, disks, public IP addresses, and network traffic, are billed to your Azure subscription for as long as they exist. A high availability deployment uses three Landscape Server VMs instead of one. Any software or plan charges for the offer are shown on the offer's page in the Azure portal and are also billed through your subscription.

To stop these charges, delete the managed application as described in {ref}`how-to-deploy-from-azure-marketplace-delete`.
```

## Prerequisites

You need:

- An Azure subscription with a valid payment method. Your account needs at least the Contributor role on the subscription, or on the resource group that you deploy the managed application to. Your organization might also restrict Marketplace purchases. For more information, see [Microsoft's documentation on purchasing from the Marketplace](https://learn.microsoft.com/en-us/marketplace/azure-purchasing-invoicing).
- A host name for Landscape Server, such as `landscape.example.com`.
- One of the following, depending on how users sign in to Landscape:
  - For password authentication: an SMTP relay that Landscape can use to send emails, and its host, port, sender address, user name, and password.
  - For OIDC authentication: a client registered with your OIDC provider, and its issuer URL, client ID, and client secret. If you don't let Landscape approve new OIDC accounts automatically, you also need an SMTP relay. For more information, see {ref}`how-to-external-auth-oidc`.

% TODO(LNDENG-5612): confirm who creates the DNS record for the host name and how the TLS certificate is issued (the offer's Terraform uses lego with a Cloudflare DNS token that Canonical provides)

## Deploy the managed application

% TODO(LNDENG-5612): add a direct link to the public listing when it's published (production offer and plan: `canonical:managed-landscape:self-service`, see CPC-12375), and confirm the wizard's tab and field labels
1. Sign in to the Azure portal, go to **Marketplace**, and search for **Landscape**.
2. Select the Landscape offer from Canonical, then select **Create**.
3. On the **Basics** tab, enter the details that all managed applications require:

    - **Subscription**: The subscription to deploy to, and to bill.
    - **Resource group**: The resource group for the managed application. You can create a new one.
    - **Region**: The Azure region to deploy to.
    - **Application name**: A name for the managed application.
    - **Managed resource group**: The name of the managed resource group that Azure creates for the deployed resources. You can keep the default name.

    ```{tip}
    The **Subscription** list shows only the subscriptions that you can deploy the offer to. If the offer is available to you as a private or preview offer, the list shows only the subscriptions in the offer's audience. To deploy to another subscription, ask your Canonical contact to add its subscription ID to the offer's audience.
    ```

4. Enter the deployment settings:

    - **VM sizes**: The Azure VM sizes for the control plane VM and for the Landscape Server VMs.
    - **High availability**: Whether to deploy three Landscape Server VMs instead of one.
    - **Public IP address**: Whether to give the Landscape Server VMs public IP addresses.
    - **Host name**: The host name for Landscape Server, without `https://`. Landscape is available at `https://<host-name>`.

5. Enter the authentication settings. Select password or OIDC authentication, then enter:

    - For password authentication: the email address, user name, and password for the first Landscape administrator.
    - For OIDC authentication: your OIDC provider's issuer URL, client ID, client secret, and redirect URI, and whether Landscape approves new OIDC accounts automatically.

6. If Landscape needs to send emails, enter your SMTP relay's host, port, sender address, user name, and password. Landscape sends invitation emails unless you use OIDC authentication and approve new accounts automatically. The deployment uses TLS on port 465, and STARTTLS on other ports.
7. On the **Review + create** tab, check your settings and the offer's terms and price, then select **Create**.

The portal shows the deployment's progress. When the deployment is complete, the managed application is in the resource group that you selected, and the deployed resources are in the managed resource group.

## Sign in to Landscape

1. In a browser, go to `https://<host-name>`, where `<host-name>` is the host name that you entered when you deployed the offer.
2. Sign in:

    - For password authentication: use the administrator email address and password that you entered when you deployed the offer.
    - For OIDC authentication: sign in with your OIDC provider.

To register client machines with your Landscape server, see {ref}`how-to-install-landscape-client`.

(how-to-deploy-from-azure-marketplace-managed-rg)=
## Understand your access to the managed resource group

The publisher of a managed application chooses how much access you have to the managed resource group. In the default permission scenario, a deny assignment on the managed resource group limits you to read actions, plus any actions that the publisher allows. You might not be able to change, stop, or delete individual resources in the managed resource group, such as the VMs or their network security groups.

To check your access, open the managed resource group in the Azure portal, select **Access control (IAM)**, and check the **Deny assignments** tab.

(how-to-deploy-from-azure-marketplace-delete)=
## Delete the deployment

When you no longer need the deployment, delete the managed application. Azure then deletes the managed resource group and all the resources in it, and the charges for them stop.

1. In the Azure portal, open the managed application.
2. Select **Delete**, and confirm.

If you created a resource group only for the managed application, you can then delete that resource group too.
