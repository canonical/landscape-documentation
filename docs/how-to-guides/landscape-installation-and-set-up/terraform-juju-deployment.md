(how-to-terraform-juju-deployment)=

# How to deploy Landscape with Terraform and Juju

Landscape can be deployed in a scalable, configurable, and reproducible way by using the {ref}`Landscape Scalable product module <reference-landscape-product-modules-landscape-scalable>`, which is powered by Juju and managed by Terraform.

## Install Juju

Make sure you have `juju` installed. You can install it as a snap with the following command:

```bash
sudo snap install juju --classic
```

## Create a Juju controller

With Juju installed, use it to bootstrap a cloud by creating a controller. See [the Juju docs on managing and creating controllers](https://documentation.ubuntu.com/juju/latest/howto/manage-controllers/) for more information. The controller must be configured and accessible before proceeding.

## Install Terraform or OpenTofu

Make sure you have [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) or [OpenTofu](https://opentofu.org/docs/intro/install/) installed.

```{note}
This guide uses `terraform` for commands, but everything can also be done using `tofu` instead.
If using OpenTofu, consider creating an alias in your shell's configuration file:

    alias terraform=tofu

```

## Create a Juju model

Create a Juju model for the Landscape deployment:

```sh
juju add-model landscape
```

Unlike most Terraform Juju provider resources, this module identifies the model by its **UUID**, not its name. Get it with:

```sh
juju show-model landscape
```

Copy the value of `model-uuid`.

```{tip}
If you have [`jq`](https://github.com/jqlang/jq) installed:

    juju show-model landscape --format=json | jq -r '.landscape["model-uuid"]'
```

### Deploying the Landscape Scalable product module

The Landscape Scalable product module is a Terraform module that can be used to deploy the Landscape Server charm and other applications it depends on using Juju. It can be deployed by itself or used in higher-level plans. It is based on the (deprecated) Landscape Scalable charm bundle. See the {ref}`reference page <reference-landscape-product-modules-landscape-scalable>` for its specific inputs and outputs.

In a Terraform plan, you need to provide the module with the UUID of a Juju model and any desired configurations for the Landscape Server, HAProxy, PostgreSQL, and RabbitMQ server charms, for example:

```hcl
variable "model_uuid" {
  type = string
}

module "landscape_landscape-scalable" {
  # Pin to a charm revision tag (e.g. `rev474`) rather than the default
  # branch, so the module version, and the landscape-server revision it
  # deploys, doesn't shift under you. See the repository's tags for
  # available revisions: https://github.com/canonical/landscape-server-operator/tags
  source = "git::https://github.com/canonical/landscape-server-operator//terraform/product/modules/landscape-scalable?ref=rev474"

  model_uuid = var.model_uuid

  landscape_server = {
    channel = "26.04/stable"
    base    = "ubuntu@24.04"
    config = {
      landscape_ppa     = "ppa:landscape/self-hosted-26.04"
      root_url          = "https://landscape.example.com/"
    }
  }

  postgresql = {
    channel = "16/stable"
    base    = "ubuntu@24.04"
  }

  haproxy = {
    channel = "2.8/stable"
    base    = "ubuntu@24.04"
  }

  landscape_debarchive = {
    channel = "latest/stable"
    base    = "ubuntu@24.04"
  }

  landscape_task_handler = {
    channel = "latest/stable"
    base    = "ubuntu@24.04"
  }
}
```

`landscape_debarchive` and `landscape_task_handler` are optional (set to `null` to skip deploying them); when set, the module automatically integrates them with `landscape_server`, `postgresql`, `tls_certificates`, and, for the task handler's gRPC route, `haproxy`.

Then, apply the plan and supply the Juju model UUID as a variable:

```sh
terraform apply -var model_uuid=<model-uuid>
```

The module's outputs include `applications` (the deployed charms and their integration endpoints), `admin_email`, `admin_password` (sensitive), `registration_key`, `has_modern_amqp_relations`, and `has_modern_postgres_interface`. See the {ref}`reference page <reference-landscape-product-modules-landscape-scalable>` for the full list.

After applying the plan, you can monitor the status of the Juju model using `juju status`, for example:

```sh
juju status -m landscape --watch 1s --relations
```

## Deploying against legacy (pre-26.04) or modern (26.04+) topologies

This module is version-aware: it doesn't take a "mode" variable. Instead, once `landscape_server` is deployed, the module inspects the relation interfaces that revision actually supports (its `database`, `has_modern_haproxy_interface`, and `inbound_amqp`/`outbound_amqp` requires) and wires the matching integrations automatically. The same module works unmodified whether `landscape_server.channel` points at a pre-26.04 revision (legacy `pgsql` database interface, `reverseproxy`/`website` HAProxy relation, single `amqp` relation) or a 26.04+ revision (modern `database` interface, `haproxy-route`, split `inbound-amqp`/`outbound-amqp`).

The `terraform/product/modules/landscape-scalable` directory in `landscape-server-operator` ships two example variable files for each topology; copy the one matching your target revision to `terraform.tfvars`:

- **`terraform.tfvars.example`** (legacy, pre-26.04): `24.04/stable` channel, `ppa:landscape/self-hosted-24.04`.
- **`terraform.tfvars.modern`** (modern, 26.04+): `26.04/stable` channel, `ppa:landscape/self-hosted-26.04`, `2.8/stable` HAProxy, `16/stable` PostgreSQL, and `enable_hostagent_messenger`/`enable_ubuntu_installer_attach` set.

```sh
cp terraform.tfvars.modern terraform.tfvars   # or terraform.tfvars.example for legacy
terraform init
terraform apply -var model_uuid=<model-uuid>
```

## Accessing the Landscape UI

Once the deployment has finished, get the IPv4 address of the leader `haproxy` unit and access it with your browser:

```bash
juju status -m landscape haproxy/leader
```

## Deploying with high availability

This module can be configured for high availability by configuring the `units` values of the input applications, for example:

```hcl
landscape_server = {
  units = 2
}

postgresql = {
  units = 2
}

rabbitmq_server = {
  units = 2
}
```

TLS is not configured on the `haproxy` object itself: the `2.8/stable` HAProxy charm has no `ssl_cert`/`ssl_key` config options. Instead, the module deploys a certificates charm via the `tls_certificates` input and integrates it with HAProxy over the `certificates` relation; by default this is [`self-signed-certificates`](https://charmhub.io/self-signed-certificates). To use your own CA-signed certificate instead, point `tls_certificates` at a different provider charm, for example [`manual-tls-certificates`](https://charmhub.io/manual-tls-certificates) or [`lego`](https://charmhub.io/lego):

```hcl
tls_certificates = {
  charm_name = "manual-tls-certificates"
  channel    = "latest/stable"
}
```

## Using a shared, cross-model HAProxy (LBaaS)

Instead of deploying a dedicated HAProxy into the same model, you can integrate Landscape Server with an HAProxy already deployed in another model and shared out as a [Juju cross-model offer](https://documentation.ubuntu.com/juju/latest/howto/manage-offers/) of its `haproxy-route` endpoint. This is useful when a single HAProxy fronts multiple applications or models.

To use this, set `haproxy` to `null` (so the module doesn't deploy its own) and provide the offer URL instead:

```hcl
haproxy                 = null
haproxy_route_offer_url = "<model-owner>/<offering-model>.<offer-name>"
```

If `enable_hostagent_messenger` or `enable_ubuntu_installer_attach` are enabled in `landscape_server.config`, those endpoints use the separate `haproxy-route-tcp` interface (for gRPC/TCP passthrough) and need their own offer, consumed via `haproxy_route_tcp_offer_url`:

```hcl
haproxy_route_tcp_offer_url = "<model-owner>/<offering-model>.<tcp-offer-name>"
```

`haproxy_route_offer_url` and `haproxy_route_tcp_offer_url` are independent of each other and of `haproxy`: `haproxy` controls whether this module deploys its own HAProxy, while the offer URLs control whether Landscape Server's `*-haproxy-route`/`*-haproxy-route-tcp` endpoints are integrated with that in-model HAProxy or with an external offer instead.

## Using PgBouncer as a connection pooler

For improved database performance and scalability in high-load deployments, set the `pgbouncer` input to deploy [PgBouncer](https://charmhub.io/pgbouncer) as a subordinate charm between Landscape Server and PostgreSQL. This requires a Landscape Server revision that supports the modern `database` interface (rather than the legacy `pgsql`/`db` endpoint):

```hcl
pgbouncer = {
  config = {
    pool_mode = "transaction"
  }
}
```

If you're also deploying PostgreSQL through this module's `postgresql` input, the module automatically integrates PgBouncer's `backend-database` endpoint with it. If instead you're using an external PostgreSQL deployment (`postgresql = null`), you need to create that integration yourself, connecting PgBouncer's `backend-database` endpoint to your PostgreSQL application's `database` endpoint (the application name is `"postgresql"` by default; override it below if you deployed it under a different name):

```hcl
resource "juju_integration" "pgbouncer_postgresql" {
  model_uuid = var.model_uuid

  application {
    name     = module.landscape_landscape-scalable.applications.pgbouncer.name
    endpoint = "backend-database"
  }

  application {
    name     = "postgresql"
    endpoint = "database"
  }
}
```
