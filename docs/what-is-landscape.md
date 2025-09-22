(what-is-landscape)=
# What is Landscape?

Landscape is Canonical’s systems management solution. You can use Landscape to manage all of your Ubuntu systems—desktops, servers, cloud instances, IoT devices, and more.

At its core, Landscape allows you to manage all of your systems from a single portal. This includes tasks such as: managing software updates across your Ubuntu estate, configuring Role-Based Access Control (RBAC), monitoring your client machines, executing scripts on your clients remotely, managing packages and repositories, and much more.

## How Landscape works

Landscape is a client-server application in which there are two main components: Landscape Server and Landscape Client.

- **Landscape Server** is installed on a single, centralized server and manages all of your Ubuntu client machines and devices. Landscape Server is generally what users of Landscape interact with the most, and it’s where you perform system administration tasks. You can manage your system with Landscape Server using the web portal or API.
- **Landscape Client** is installed on each Ubuntu machine in your system. It communicates with Landscape Server by sending client information to the server, receiving updates from the server, and executing commands on the client from the server.

Although “Landscape” refers to both the Landscape Server and Landscape Client applications, it most often describes Landscape Server in the documentation because the server is where management activities are performed. If you see “Landscape” mentioned without further clarification, it’s probably discussing the Server component.

In addition, Landscape Server relies on the following third-party infrastructure:

- **Apache**: The web server that handles the HTTPS traffic sent to the Server from client machines, the API, and users accessing the web portal.
- **PostgreSQL**: The database.
- **RabbitMQ**: The message server. This handles message sending between client and server.
- (Sometimes) **HAProxy**: The reverse proxy used for high-availability deployments.

## What Landscape does

Landscape performs your system management tasks. You can use Landscape for lots of different activities, such as:

- **System monitoring, management, and alerts:** Monitor the health of your system, view system details such as hardware information, and configure alerts to notify you for certain activities, such as when security upgrades are available, when a client machine needs to be rebooted, and more.
- **Package and upgrade management:** Install, remove, and upgrade packages on your client machines and ensure your system is up-to-date with the latest software and security patches.
- **User management and Role-Based Access Control (RBAC):** Add, remove, and edit user accounts on your client machines and use RBAC to configure specific permissions.
- **Remote scripting:** Run custom scripts on your client machines remotely from your Landscape Server web portal or via the API.

## Editions of Landscape

There are three different editions of Landscape: {ref}`SaaS <header-what-is-landscape-saas>`, {ref}`Managed <header-what-is-landscape-managed>`, and {ref}`Self-hosted <header-what-is-landscape-self-hosted>`.

(header-what-is-landscape-saas)=
### Landscape SaaS

Landscape SaaS is our standard SaaS offering. It’s a cloud-based version of Landscape that’s hosted and maintained by Canonical, bundled with your [Ubuntu Pro](https://ubuntu.com/pro) subscription. Landscape SaaS is hosted on Canonical’s shared infrastructure (multi-tenanted) and is ready to use immediately, with no setup required.

While the majority of Landscape features are offered in SaaS, there are certain features that aren’t available in SaaS due to the shared-tenancy or because these features require dedicated infrastructure. Landscape SaaS doesn't currently offer {ref}`explanation-repo-mirroring` or configuring a custom external identity provider.

Organizations interested in using Landscape SaaS at enterprise-scale should [contact Canonical Sales](https://ubuntu.com/landscape#get-in-touch).

(header-what-is-landscape-managed)=
### Managed Landscape

Managed Landscape is a single-tenant version of Landscape with dedicated resources that’s hosted by Canonical and comes with an SLA. It’s for organizations that want private, dedicated resources but don’t want to manage their own infrastructure. With Managed Landscape, you get your own private Landscape instance that’s managed by Canonical but customized to your organization’s needs.

The Managed Landscape offering comes with all Landscape features, including {ref}`explanation-repo-mirroring` and configuring custom external identity providers.

Organizations interested in Managed Landscape should [contact Canonical Sales](https://ubuntu.com/landscape#get-in-touch).

(header-what-is-landscape-self-hosted)=
### Self-hosted Landscape

Self-hosted Landscape is the on-premises version of Landscape that’s set-up, hosted, and maintained by the user or organization. It’s customizable, controlled by the user, and can also be deployed to public cloud resources. The self-hosted version gives you the most control over your Landscape instance, but it requires more technical knowledge and resources to set-up and maintain. All Landscape features are available for self-hosted Landscape instances.

For self-hosted installations, there are multiple ways to install Landscape Server and Landscape Client.

**Landscape Server:**

- **Quickstart** or **Manual** (Debian): The Landscape Server Debian packages, which can be used for any type of deployment. The Quickstart version is mainly used for simple deployments or exploring Landscape, and the Manual version is used for customizable production deployments. In the Quickstart version, all Landscape components are installed on a single server. In the Manual version, you manually configure Landscape Server, PostgreSQL, RabbitMQ, and all other dependencies.
- **Charm** (Juju-managed): The Landscape Server Charm deploys Landscape using Juju. The charm is recommended for large, high-availability (HA) deployments because Juju can simplify orchestration and scaling. See the [Juju documentation](https://juju.is/docs/juju) for more details on Juju.

**Landscape Client:**

- **Landscape Client** (Debian): This is the default version of Landscape Client and is installed using traditional APT-based package management. This form of Landscape Client is available in Ubuntu’s `main` repository.
- **Landscape Client Snap**: This is the snap version of Landscape Client. It’s mainly for IoT device deployments, and it’s designed to be used with Ubuntu Core.
- **Landscape Client Charm**: This deploys Landscape Client on Juju-managed systems. You should use the Landscape Client Charm if you’re also using the Juju-managed Landscape Server Charm.

For more details on self-hosted Landscape installations, see our {ref}`explanation-about-self-hosted` page. Organizations interested in using self-hosted Landscape at enterprise-scale should [contact Canonical Sales](https://ubuntu.com/landscape#get-in-touch).


## Useful Links

- [Knowledge Base - Landscape Section](https://support-portal.canonical.com/knowledge-base?topic=Landscape): content published by Canonical Support, typically addressing FAQs and providing workarounds for bugs

- [GitHub - script repository for Landscape](https://github.com/canonical/landscape-scripts): a collection of scripts to make Landscape more powerful.
