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

[Install Juju](https://canonical.com/juju/docs/juju-cli/latest/howto/manage-juju/) as a snap with this command:

```bash
sudo snap install juju --classic
```

To learn more about Juju and to bootstrap a Juju controller, check out their [getting started](https://canonical.com/juju/docs/juju-cli/latest/tutorial/) page.

## Deploy self-hosted Landscape Server

Choose the appropriate option for your Landscape charm deployment.

If you have an Ubuntu Pro subscription, attach your Pro token to each machine that will host Landscape Server components. For guidance, see {ref}`how-to-attach-ubuntu-pro`.

```{important}
Starting with the **26.04 version** of the `landscape-server` charm, the deployment architecture changes to PostgreSQL 14+ over the `database` relation (backed by the `postgresql_client` charm interface), HAProxy 2.8 over `haproxy-route`, and TLS via `tls-certificates`.

The Charmhub `landscape-scalable` bundle was deprecated in 26.04 and does not have a `26.04/*` track. For 26.04+ deployments, follow {ref}`how-to-juju-ha-installation`.
```

### Deploy with Terraform

You can deploy Landscape with the {ref}`Landscape Scalable Terraform product module <how-to-terraform-juju-deployment>` (see its {ref}`reference documentation <reference-landscape-product-modules-landscape-scalable>` for inputs and outputs), or with the Charmhub bundle described below.

### Other deployment methods

When deploying with Juju, you will use a Juju bundle. A bundle is an encapsulation of all of the parts needed to deploy the required services as well as associated relations and configurations that the deployment requires.

> See also: [Landscape-scalable bundle on Charmhub](https://charmhub.io/landscape-scalable)

The `landscape-scalable` bundle published on Charmhub was deprecated in 26.04 and should not be used for new deployments. It uses the older topology (external HAProxy charm, PostgreSQL 14 over the legacy `pgsql` interface).

For the 26.04 architecture (recommended), the new deployment approach uses:
- **External HAProxy charm** (`2.8/stable`) for load balancing via the `haproxy-route` interface
- PostgreSQL 14+ over the `database` relation (`postgresql_client` interface)
- TLS certificates provided via the `tls-certificates` interface integrated with HAProxy (e.g., `self-signed-certificates` charm)
- The **Debarchive** and **Landscape Task Handler** charms, integrated with Landscape Server for repository mirroring and offloaded task processing, respectively

Key benefits of the new approach:
- HAProxy charm handles all traffic routing and TLS termination
- True high-availability with multiple Landscape Server units behind HAProxy
- Better scalability and resilience

For detailed instructions on deploying with the new architecture, create and deploy a custom bundle as documented in {ref}`how-to-juju-ha-installation`.

Previously, there were additional bundles: `landscape-dense` and `landscape-dense-maas`. These bundles are now deprecated and should not be used for new deployments.

## Access self-hosted Landscape

Once the deployment has finished, Landscape Server is accessible in different ways depending on the deployment approach:

**Pre-26.04 deployment:**

  - Access via the IP address of the first `haproxy` unit
  - HAProxy typically runs on port 443 (HTTPS)

**26.04+ deployment:**

  - HAProxy routes traffic based on the `hostname` set in the `haproxy-route` relation, **not** by port alone, so you must connect using that hostname (for example, with `--resolve` or a DNS entry pointing it at the HAProxy unit's IP). Connecting directly to the HAProxy unit's own IP address (with no matching `Host` header) hits HAProxy's default page instead of Landscape.
  - If you set `root_url`, that hostname is what you must connect with.
  - If you leave `root_url` unset, the `landscape-server` charm falls back to using the leader unit's IP address as the routing hostname, so you'd need to connect using *that* IP as the `Host` header/SNI value (not the HAProxy unit's IP). In practice, setting `root_url` to a real hostname is much simpler for testing.
  - HAProxy handles load balancing across all Landscape Server units once you're routed correctly.

**With external load balancer (LBaaS):**

  - When using a cross-model HAProxy deployment
  - Access via the hostname specified in your `root_url`
  - The external HAProxy distributes traffic across Landscape Server units

```{tip}
For the 26.04+ deployment, set `root_url` to a real hostname and point that hostname (via DNS or `curl --resolve`) at your HAProxy unit's IP address (or external load balancer) before testing.
```
