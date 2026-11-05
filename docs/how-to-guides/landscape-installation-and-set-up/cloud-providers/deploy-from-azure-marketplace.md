---
myst:
  html_meta:
    description: "Deploy Landscape Server from the Azure Marketplace as a managed application. Create the deployment in the Azure portal, sign in to the web portal, and delete the deployment."
---

(how-to-deploy-from-azure-marketplace)=
# How to deploy Landscape Server from the Azure Marketplace

Canonical provides Landscape Server as an Azure Marketplace managed application. You deploy it from the Azure portal, and it creates the Azure resources that run Landscape Server in your own Azure subscription. You don't need to install Landscape Server yourself.

Canonical operates the deployment. It uses Juju to deploy Landscape Server, together with HAProxy, PostgreSQL, and RabbitMQ, on Ubuntu 24.04 LTS VMs in your subscription, and pins the Landscape Server version that it deploys.

The deployment provides the Landscape URL and its TLS certificate. The URL is in the form `https://landscape-<project-unique-string>.<region>.azure.canonicalmanagedapps.com`. You don't need to provide a domain name or certificate, but you need to provide your own SMTP relay credentials.

Azure places the managed application in the application resource group you select and creates a separate managed resource group for its deployed resources. Your access to the managed resource group is limited; see {ref}`how-to-deploy-from-azure-marketplace-managed-rg`.

For more information about managed applications, see [Microsoft's overview of Azure Managed Applications](https://learn.microsoft.com/en-us/azure/azure-resource-manager/managed-applications/overview).

```{note}
To build your own Landscape Server VM on Azure with cloud-init instead, see {ref}`how-to-install-on-microsoft-azure`. That method gives you full control of the VM and its configuration.
```

```{warning}
Deploying this offer costs money. The Azure resources that it creates, such as VMs, an AKS cluster, disks, public IP addresses, and network traffic, are billed to your Azure subscription for as long as they exist. A high availability deployment uses more VMs; see {ref}`how-to-deploy-from-azure-marketplace-includes`. Any software or plan charges for the offer are shown on the offer's page in the Azure portal and are also billed through your subscription.

To stop these charges, delete the managed application as described in {ref}`how-to-deploy-from-azure-marketplace-delete`.
```

(how-to-deploy-from-azure-marketplace-includes)=
## What the deployment includes

Every deployment includes:

- A bootstrap VM that Canonical uses to set up and operate the deployment.
- An AKS cluster with one node, which runs the Canonical Observability Stack (COS) Lite that Canonical uses to monitor the deployment.
- A public load balancer for Landscape.

The **Enable High Availability** setting changes the rest of the deployment:

| | Without high availability | With high availability |
| --- | --- | --- |
| Landscape Server VMs | 1 | 3 |
| Units of Landscape Server, HAProxy, PostgreSQL, RabbitMQ, the task handler, and the Debian archive service | 1 of each | 3 of each, one on each Landscape Server VM |
| RabbitMQ | Single node | Three-node cluster |
| Juju controller VMs | 1 | 3 |

The Landscape Server VMs use the **Landscape VM Size** that you select. The bootstrap VM and the AKS node use the **Components VM Size**.

## Prerequisites

You need:

- An Azure subscription with a valid payment method. Your account needs at least the Contributor role on the subscription, or on the resource group that you deploy the managed application to. Your organization might also restrict Marketplace purchases. For more information, see [Microsoft's documentation on purchasing from the Marketplace](https://learn.microsoft.com/en-us/marketplace/azure-purchasing-invoicing).
- The `Microsoft.Compute` and `Microsoft.Capacity` resource providers registered for the subscription. To register them, open the subscription in the Azure portal, select **Settings** > **Resource providers**, select each provider, then select **Register**. For more information, see [Microsoft's documentation on resource providers](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types).
- Enough vCPU quota in the region that you deploy to, for the VM sizes that you select. A high availability deployment needs quota for three Landscape Server VMs. For more information, see [Microsoft's documentation on vCPU quotas](https://learn.microsoft.com/en-us/azure/virtual-machines/quotas).
- An SMTP relay that Landscape can use to send invitation and notification emails, and its host, port, sender address, user name, and password. The relay must support PLAIN authentication with a user name and password. Other authentication mechanisms, such as CRAM-MD5, NTLM, and OAuth2, aren't supported.
- If users sign in to Landscape with OIDC: a client registered with your OIDC provider, and its issuer URL, client ID, and client secret. For more information, see {ref}`how-to-external-auth-oidc`.

## Deploy the managed application

% TODO(LNDENG-5612): add a direct link to the public listing when it's published (production offer and plan: `canonical:managed-landscape:self-service`, see CPC-12375)
1. Sign in to the Azure portal, go to **Marketplace**, and search for **Landscape**.
2. Select the Landscape offer from Canonical, then select **Create**.
3. On the **Basics** tab, enter:

    - **Subscription**: The subscription to deploy to, and to bill.
    - **Resource group**: The resource group for the managed application. You can create a new one. If you select an existing resource group, it must be in the same region as the deployment.
    - **Deployment location**: The Azure region to deploy to.
    - **Customer Name**: A short name that identifies your organization.
    - **Customer Email**: The email address that receives onboarding information and contact details.
    - **Application name**: A name for the managed application.
    - **Managed resource group**: The name of the managed resource group that Azure creates for the deployed resources. You can keep the default name.

4. On the **Landscape Configuration** tab, select the size of the deployment:

    - **Enable High Availability**: Select this to deploy three Landscape Server VMs for redundancy. For the full differences, see {ref}`how-to-deploy-from-azure-marketplace-includes`. This is the default, and is suitable for production. Without high availability, the deployment uses a single Landscape Server VM, which is suitable only for proofs of concept, development, and testing.
    - **Components VM Size**: The VM size for the deployment's supporting components. Each components VM needs at least 16 GB of RAM. The default size is enough for most deployments.
    - **Deployment size**: The number of machines that Landscape will manage: **Small (up to 500 machines)**, **Medium (500-5000 machines)**, or **Large (5000+ machines)**. This filters the VM sizes that you can select for Landscape Server.
    - **Landscape VM Size**: The VM size for each Landscape Server VM.

    The tab checks that the VM sizes are available to your subscription in the region, and that you have enough vCPU quota for them. If it shows an error, select different VM sizes, clear **Enable High Availability**, or request more quota for the VM families that it lists. If the quota check doesn't finish, you can select **I understand and want to proceed** to continue. Azure still checks the quota when you create the deployment.

5. On the same tab, select the **Authentication type**, then enter its settings:

    - **Admin user + password**: Enter and confirm the **Admin Password** for the first Landscape administrator.
    - **OpenID Connect (OIDC)**: Enter your OIDC provider's **OIDC Client ID**, **OIDC Client Secret**, and **OIDC Issuer URL**. Select **Automatically approve new OIDC accounts** to add people that you invite to Landscape after their first OIDC sign-in, without invitation emails.

6. If the **SMTP configuration** section is shown, enter your SMTP relay's **SMTP relay server**, **SMTP port**, **Sender address**, **SMTP user**, and **SMTP password**. Landscape uses the relay to send invitation emails. The wizard hides this section only if you use OIDC authentication and select **Automatically approve new OIDC accounts**, because Landscape doesn't send invitation emails then.
7. On the **Review + create** tab, check your settings and the offer's terms and price, then select **Create**.

The portal shows the deployment's progress. When the deployment is complete, the managed application is in the resource group that you selected, and the deployed resources are in the managed resource group. Canonical then finishes setting up Landscape Server on the deployed resources.

The provisioning process takes about an hour to complete. When it's complete, you receive an email at the **Customer Email** address with instructions to access Landscape.

## Sign in to Landscape

1. In a browser, go to the address of your Landscape server.
2. Sign in:

    - For password authentication: use the **Customer Email** address as the administrator's user name and email address, and the **Admin Password** that you entered when you deployed the offer.
    - For OIDC authentication: sign in with your OIDC provider.

To register client machines with your Landscape server, see {ref}`how-to-install-landscape-client`.

(how-to-deploy-from-azure-marketplace-managed-rg)=
## Understand your access to the managed resource group

The publisher of a managed application chooses how much access you have to the managed resource group. In the default permission scenario, a deny assignment on the managed resource group limits you to read actions, plus any actions that the publisher allows. You might not be able to change, stop, or delete individual resources in the managed resource group, such as the VMs or their network security groups.

To check your access, open the managed resource group in the Azure portal, select **Access control (IAM)**, and check the **Deny assignments** tab.

(how-to-deploy-from-azure-marketplace-delete)=
## Delete the deployment

When you no longer need the deployment, delete the managed application. Azure then deletes the managed resource group and its resources, and the charges for them stop.

1. In the Azure portal, open the managed application.
2. Select **Delete**, and confirm.

If you created a resource group only for the managed application, you can then delete that resource group too.
