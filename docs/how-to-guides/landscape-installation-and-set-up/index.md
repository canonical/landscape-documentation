(how-to-guides-landscape-installation-and-set-up-index)=
# Landscape installation and set-up

## Quickstart Installation
Debian meta-package that will install and configure all necessary dependencies (Landscape Server, PostgreSQL, RabbitMQ, Apache)
- Everything is installed in one machine or container
- Great way to try out Landscape or deploy a proof of concept
- Ideal for small production deployments

## Juju Installation
A fully scalable deployment where each Landscape component is installed in a separate virtual machine or container
- Allows independent scaling of individual components (Landscape Server, PostgreSQL, RabbitMQ, HAProxy)
- Includes Haproxy load balancer to proxy requests across multiple Landscape Server units
- Balance between ease of setup and enterprise scalability
- Uses Canonical's Juju (an open source orchestration engine) for deployment and scaling, 

## SaaS Option
A cloud solution hosted in Canonical's infrastructure.
- Requires no server installation or maintenance by the user
- Register and manage client machines right away
- Works best for small to medium-sized environments
- May experience slowdowns with accounts exceeding 1000 computers

## Manual Installation
A customizable installation process where each component can be individually installed and configured
- Recommended for advanced users with system administration experience
- Requires knowledge of each component's configuration options (e.g. Apache, PostgreSQL, RabbitMQ)
- Ideal for users with specific requirements

| Deployment Option | Cloud | Fully Custom | Quick Setup | Scalable |
|-------------------|-------|--------------|------------|----------|
| Juju              |       |              | ✓          | ✓        |
| Manual Install    |       | ✓            |            |          |
| Quickstart        |       |              | ✓          |          |
| SaaS              | ✓     |              | ✓          |          |

There are multiple different ways to install and configure Landscape.
```{toctree}
:titlesonly:
:maxdepth: 2
:glob:

Quickstart installation <quickstart-installation>
Manual installation <manual-installation>
Juju installation <juju-installation>
Juju HA installation <juju-ha-installation>
Install in a LXD container <install-in-a-lxd-container>
Install on Google Cloud <install-on-google-cloud>
Install on Microsoft Azure <install-on-microsoft-azure>
Install on FIPS-compliant machines <install-on-fips-compliant-machines>
Install Landscape Client <install-landscape-client>
Configure Landscape Client <configure-landscape-client>
Configure RabbitMQ <configure-rabbitmq>
Configure Postfix <configure-postfix>
