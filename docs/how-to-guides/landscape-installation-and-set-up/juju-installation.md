---
myst:
  html_meta:
    description: "Deploy Landscape Server with Juju for scalable infrastructure management. Learn to use the landscape-scalable bundle and access your self-hosted server."
---

(how-to-juju-installation)=
# How to install Landscape Server with Juju

> See also: [Landscape Server charm (Charmhub)](https://charmhub.io/landscape-server)

You can deploy Landscape in a scalable way with Juju. This document provides a very high-level overview.

For detailed instructions on deploying Landscape with Juju in a high-availability environment, see {ref}`how-to-juju-ha-installation`.

## Install Juju

[Install Juju](https://canonical-juju.readthedocs-hosted.com/en/latest/user/howto/manage-juju/) as a snap with this command:

```bash
sudo snap install juju --classic
```

To learn more about Juju and to bootstrap a Juju controller, check out their [getting started](https://canonical-juju.readthedocs-hosted.com/en/latest/user/tutorial/) page.

## Deploy self-hosted Landscape Server

When deploying with Juju, you will use a Juju bundle. A bundle is an encapsulation of all of the parts needed to deploy the required services as well as associated relations and configurations that the deployment requires.

```{important}
Starting with the **26.04 beta version** of the Landscape Server charm, the deployment architecture has changed significantly. The charm now integrates directly with the external HAProxy charm (`2.8/edge`) using the `haproxy-route` interface and no longer uses the legacy `reverseproxy` interface. If you have an existing deployment using the older approach, see {ref}`how-to-migrate-to-26-04-charm` for migration instructions.
```

### Deployment approaches

There are two deployment approaches depending on which version of the Landscape Server charm you're using:

#### Pre-26.04 deployment

The older deployment uses:
- External HAProxy charm for load balancing
- PostgreSQL 14 with the legacy `pgsql` interface
- Separate HAProxy unit(s) for traffic management

This approach is deprecated and should only be used for existing deployments that haven't migrated yet.

#### 26.04 beta+ deployment (recommended)

The new deployment approach uses:
- **External HAProxy charm** (`2.8/edge`) for load balancing via the `haproxy-route` interface
- PostgreSQL 16 with the modern `database` interface
- TLS certificates provided via the `tls-certificates` interface integrated with HAProxy (e.g., `self-signed-certificates` charm)

Key benefits of the new approach:
- HAProxy charm handles all traffic routing and TLS termination
- True high-availability with multiple Landscape Server units behind HAProxy
- Better scalability and resilience

For detailed instructions on deploying with the new architecture, see {ref}`how-to-juju-ha-installation`.

### landscape-scalable bundle

> See also: [Landscape-scalable bundle on Charmhub](https://charmhub.io/landscape-scalable)

The **landscape-scalable** bundle provides a reference configuration for deploying Landscape Server in a high-availability setup. The bundle configuration varies depending on the charm version:

**For 26.04 beta+ deployments:**

```bash
juju deploy landscape-scalable --channel 26.04/beta
```

This will deploy:
- Multiple Landscape Server units
- HAProxy (`2.8/edge`) for load balancing
- PostgreSQL 16 for the database
- RabbitMQ Server for message queuing
- Self-signed certificates for TLS (integrated with HAProxy)

**For older deployments:**

```bash
juju deploy landscape-scalable --channel latest/stable
```

This deploys the older architecture with the external HAProxy charm.

### Other bundles

Previously, there were additional bundles: `landscape-dense` and `landscape-dense-maas`. These bundles are now deprecated and should not be used for new deployments.

## Access self-hosted Landscape

Once the deployment has finished, Landscape Server is accessible in different ways depending on the deployment approach:

**Pre-26.04 deployment:**

  - Access via the IP address of the first `haproxy` unit
  - HAProxy typically runs on port 443 (HTTPS)

**26.04 beta+ deployment:**

  - Access via the HAProxy unit IP address or your configured `root_url`
  - HAProxy handles load balancing across all Landscape Server units

**With external load balancer (LBaaS):**

  - When using a cross-model HAProxy deployment
  - Access via the hostname specified in your `root_url`
  - The external HAProxy distributes traffic across Landscape Server units

```{tip}
For the 26.04 beta+ deployment, it's recommended to set the `root_url` option and configure DNS to point to your HAProxy unit IP address, or to an external load balancer if you're using LBaaS.
```
