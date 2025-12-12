(explanation-deployment-models)=
# Landscape deployment models

> See also: {ref}`what-is-landscape`

Landscape can be deployed in different ways depending on the scale and reliability requirements of your deployment. There are two primary deployment models: single-server and multi-server.

- **Single-Server Deployment**: A minimal setup where Landscape Server, PostgreSQL, and RabbitMQ all run on the same machine. This is ideal for small-scale deployments or testing purposes.
- **Multi-Server Deployment**: A scalable setup with multiple Landscape servers, and multiple instances of HAProxy, PostgreSQL, and RabbitMQ. This is ideal for large-scale, production deployments and can be set up for high-availability deployments.

Landscape is also commonly used with other Canonical products.

## Single-Server Deployment

This is the simplest deployment model where Landscape Server and its components all run on a single machine, and there’s only one instance of each component. Each Landscape Client registers directly with the single Landscape server.

Single-server deployments should be installed using the {ref}`Quickstart <how-to-quickstart-installation>` guide.

![Landscape single-server deployment](https://assets.ubuntu.com/v1/efcf89cc-Deployment_Landscape%20(1).png)

## Multi-Server Deployment

This setup provides redundancy and scalability to production and large-scale deployments and can be used in high-availability environments. This deployment uses a load balancer (HAProxy) to distribute requests across multiple Landscape servers, and includes multiple instances of Landscape Server and its components (PostgreSQL and RabbitMQ). Landscape Clients communicate through HAProxy, which then distributes the requests to available Landscape Servers.

Multi-server deployments are usually installed with {ref}`how-to-juju-installation`. For HA deployments, see {ref}`how-to-juju-ha-installation`.

![Landscape multi-server deployment with the scalable charm](https://assets.ubuntu.com/v1/fbb9e2c3-HA_Deployment_Landscape%20(1).png)

You can also use the {ref}`Manual <how-to-manual-installation>` installation method for multi-server deployments instead of Juju, but this isn't recommended for HA deployments.

## Products used with Landscape

Here are some Canonical products that are commonly used with Landscape:

- **Ubuntu**: You can manage [Ubuntu Server](https://documentation.ubuntu.com/server/), [Ubuntu Desktop](https://help.ubuntu.com/), and [Ubuntu Core](https://ubuntu.com/core/docs) systems with Landscape.
- [**Ubuntu Pro**](https://documentation.ubuntu.com/pro/): A subscription service that extends the security and maintenance support for Ubuntu LTS releases. Landscape is included in Ubuntu Pro subscriptions.
- [**Livepatch**](https://ubuntu.com/security/livepatch/docs): Enables kernel patching without reboots and is integrated into Landscape.
- [**Juju**](https://documentation.ubuntu.com/juju/latest/): Handles service orchestration and simplifies the deployment of Landscape for high-availability deployments.

The following products are also sometimes used in large-scale deployments that include Landscape:

- [**MAAS (Metal as a Service)**](https://maas.io/docs): Provisions and configures bare-metal Ubuntu servers.
- [**COS (Canonical Observability Stack)**](https://charmhub.io/topics/canonical-observability-stack): Monitors the full deployment.

There are many other [Canonical products](https://canonical.com/) that may complement your full deployment. This section only mentions the products that are most commonly used alongside Landscape.
