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

### landscape-scalable bundle

> See also: [Landscape-scalable bundle on Charmhub](https://charmhub.io/landscape-scalable)

In the **landscape-scalable** bundle configuration, each service gets its own machine. Currently that means you will need 4 machines for Landscape, and one for the controller node. Test it out using:

```bash
juju deploy landscape-scalable
```

For more detailed instructions on deploying the Landscape server with the bundle, see {ref}`how-to-juju-ha-installation`.

### Other bundles

The Landscape Scalable bundle is the only bundle currently supported. Previously, there were two additional bundles: `landscape-dense` and `landscape-dense-maas`. These bundles are now deprecated.

## Access self-hosted Landscape

Once the deployment has finished, get the address of the first `haproxy` unit and access it with your browser:

```bash
juju status haproxy
```
