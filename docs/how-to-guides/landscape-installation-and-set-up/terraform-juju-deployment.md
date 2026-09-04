(how-to-terraform-juju-deployment)=

# How to deploy Landscape with Terraform and Juju

Landscape can be deployed in a scalable, configurable, and reproducible way by using the {ref}`Landscape Scalable product module <reference-landscape-product-modules-landscape-scalable>`, which is powered by Juju and managed by Terraform.

In this deployment, Terraform manages the Landscape applications and their Juju integrations. You must first have a Juju controller and model available, and Terraform then deploys the Landscape module into that model.

## Install prerequisites

Make sure you have `juju` installed. You can install it as a snap with the following command:

```bash
sudo snap install juju --classic
```

Make sure you also have [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) or [OpenTofu](https://opentofu.org/docs/intro/install/) installed.

```{note}
This guide uses `terraform` for commands, but everything can also be done using `tofu` instead.
If using OpenTofu, consider creating an alias in your shell's configuration file:

    alias terraform=tofu

```

## Bootstrap or select a Juju controller

With Juju installed, use it to bootstrap a cloud by creating a controller. See [the Juju docs on managing and creating controllers](https://canonical.com/juju/docs/juju-cli/latest/howto/manage-controllers/) for more information. The controller must be configured and accessible before proceeding.

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

## Create the Terraform configuration

The Landscape Scalable product module is a Terraform module that deploys the Landscape Server charm and the applications it depends on, using Juju. It lives at `terraform/product/modules/landscape-scalable` in the `landscape-server-operator` repository, and builds on the lower-level {ref}`Landscape Server charm Terraform module <reference-charm-terraform-charm-module>` (at `terraform/charm` in the same repository). See the {ref}`reference page <reference-landscape-product-modules-landscape-scalable>` for its specific inputs and outputs.

Clone the `landscape-server-operator` repository, which contains the module itself along with a ready-to-use Terraform root configuration for it:

```sh
git clone https://github.com/canonical/landscape-server-operator.git
cd landscape-server-operator/terraform/product/modules/landscape-scalable
```

```{tip}
Check out a tagged revision (e.g. `git checkout rev505`) rather than using the default branch, so the module version, and the `landscape-server` revision it deploys, doesn't shift under you. See the repository's tags for available revisions: https://github.com/canonical/landscape-server-operator/tags
```

This directory ships two example variable files:

- **`terraform.legacy.tfvars`** (legacy, pre-26.04): `24.04/stable` channel, `ppa:landscape/self-hosted-24.04`.
- **`terraform.tfvars`** (modern, 26.04+): `26.04/stable` channel, `ppa:landscape/self-hosted-26.04`, `2.8/stable` HAProxy, `16/stable` PostgreSQL, and `enable_hostagent_messenger`/`enable_ubuntu_installer_attach` set.

Open `terraform.tfvars` (or `terraform.legacy.tfvars` if using the legacy deployment topology) and adjust it for your deployment, at minimum setting `landscape_server.config.root_url` to your own domain name. `landscape_debarchive` and `landscape_task_handler` are both required for 26.04+ (modern) deployments and should not be set to `null` unless you are creating a legacy deployment. When set, the module automatically integrates both with `landscape_server`, `postgresql`, `tls_certificates`, and, for the task handler's gRPC route, `haproxy`.

```{warning}
Setting `min_install = "true"` configures the deployment to not install the `landscape-hashids` package, which means the hash-id database will not be set up, resulting in slower package reporting. This should not be used for production deployments.
```

### Deploying against legacy (pre-26.04) topologies

This module is version-aware: it doesn't take a "mode" variable. Instead, once `landscape_server` is deployed, the module inspects the relation interfaces that revision actually supports (its `database`, `has_modern_haproxy_interface`, and `inbound_amqp`/`outbound_amqp` requires) and wires the matching integrations automatically. The same module works unmodified against a pre-26.04 `landscape_server.channel` revision (legacy `pgsql` database interface, `reverseproxy`/`website` HAProxy relation, single `amqp` relation); you don't need a different plan to support an older revision, just the matching `terraform.legacy.tfvars` file above.

```{note}
Both the legacy `pgsql` database interface and the legacy `reverseproxy`/`website` HAProxy interface are still available for backwards compatibility, but are deprecated. Support for both will be removed in Landscape 26.10. See {ref}`how-to-migrate-to-26-04-charm` to migrate to the modern interfaces.
```

### Alternative: vendoring the module into your own Terraform plan

If you're integrating Landscape into a larger, existing Terraform plan instead of deploying it standalone, reference the module by its Git source from your own configuration (for example, in a `main.tf` you create):

```hcl
terraform {
  required_providers {
    juju = {
      source  = "juju/juju"
      version = "~> 1.0"
    }
  }
}

# Uses your local Juju client's active controller by default. See
# https://registry.terraform.io/providers/juju/juju/latest/docs for
# other ways to configure the provider.
provider "juju" {}

variable "model_uuid" {
  type = string
}

module "landscape_landscape-scalable" {
  source = "git::https://github.com/canonical/landscape-server-operator//terraform/product/modules/landscape-scalable?ref=rev505"

  model_uuid = var.model_uuid

  landscape_server = {
    channel = "26.04/stable"
    base    = "ubuntu@24.04"
    config = {
      landscape_ppa = "ppa:landscape/self-hosted-26.04"
      root_url      = "https://landscape.example.com/"
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

## Initialize and apply the Terraform plan

Initialize the working directory so Terraform can download the required providers:

```sh
terraform init
```

Then, review and apply the plan, supplying the Juju model UUID and the selected `.tfvars` file:

```sh
terraform apply -var model_uuid=<model-uuid> -var-file=terraform.tfvars # or terraform.legacy.tfvars
```

## Monitor the deployment

After applying the plan, you can monitor the status of the Juju model using `juju status`, for example:

```sh
juju status -m landscape --watch 1s --relations
```

## Configure DNS and access the web portal

Once the deployment has finished, get the IPv4 address of the leader `haproxy` unit:

```bash
juju status -m landscape haproxy/leader
```

HAProxy routes traffic based on the `hostname` configured in `landscape_server.config.root_url`, not by IP address alone, so point that hostname at the HAProxy unit's address (via DNS, or `curl --resolve`/a `/etc/hosts` entry for testing) and access Landscape using that hostname in your browser.

```{important}
The same hostname resolution requirement applies internally: the outbox component on the `landscape_server` units connects to the Task Handler's gRPC server through HAProxy's `haproxy-route-tcp` passthrough, using the same hostname. If it doesn't resolve on the `landscape_server` units (for example, deploying locally without a real domain), add an `/etc/hosts` entry on those units pointing the hostname at the HAProxy unit's IP address. This dependency is one-directional: outbox (on `landscape_server`) connects to Task Handler, not the other way around.
```

## Get the initial credentials and finish setup (optional)

If provided as variables at apply time, the module's outputs include `admin_email` and `admin_password` (sensitive) for the initial Landscape administrator account, and `registration_key` for registering clients. Retrieve them with:

```sh
terraform output admin_email
terraform output admin_password
terraform output registration_key
```

```{note}
These commands will fail if these values were not set when the plan was applied.
```

The outputs also include `applications` (the deployed charms and their integration endpoints), `has_modern_amqp_relations`, and `has_modern_postgres_interface`. See the {ref}`reference page <reference-landscape-product-modules-landscape-scalable>` for the full list.

## Deploying with high availability

This module can be configured for high availability by configuring the `units` values of the input applications, for example:

```hcl
landscape_server = {
  units = 3
  config = {
    min_install = "false"
  }
}

postgresql = {
  units = 3
}

rabbitmq_server = {
  units = 3
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

Instead of deploying a dedicated HAProxy into the same model, you can integrate Landscape Server with an HAProxy already deployed in another model and shared out as a [Juju cross-model offer](https://canonical.com/juju/docs/juju-cli/latest/howto/manage-offers/) of its `haproxy-route` endpoint. This is useful when a single HAProxy fronts multiple applications or models.

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

For improved database performance and scalability in high-load deployments, set the `pgbouncer` input to deploy [PgBouncer](https://charmhub.io/pgbouncer) as a subordinate charm between Landscape Server and PostgreSQL. This requires a Landscape Server revision that supports the modern `postgresql_client` interface (rather than the legacy `pgsql` interface):

```hcl
pgbouncer = {
  config = {
    pool_mode = "transaction"
  }
}
```

```{tip}
Set the PgBouncer charm's [`max_db_connections`](https://charmhub.io/pgbouncer/configurations#max_db_connections) charm config option to control how many connections Landscape Server can use at a time.
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

The `pgbouncer` input only pools connections for `landscape_server`. Since a PgBouncer application's `database` endpoint can only serve one principal application, `landscape_debarchive` and `landscape_task_handler` cannot share `landscape_server`'s PgBouncer; each would need its own dedicated PgBouncer application. The example below connects them directly to PostgreSQL's `database` endpoint instead. See {ref}`explanation-pgbouncer-integration` for the dedicated-PgBouncer alternative and a known upstream issue to be aware of if you use it.

```hcl
resource "juju_integration" "debarchive_postgresql" {
  model_uuid = var.model_uuid

  application {
    name     = module.landscape_landscape-scalable.applications.landscape_debarchive.name
    endpoint = "database"
  }

  application {
    name     = "postgresql"
    endpoint = "database"
  }
}

resource "juju_integration" "task_handler_postgresql" {
  model_uuid = var.model_uuid

  application {
    name     = module.landscape_landscape-scalable.applications.landscape_task_handler.name
    endpoint = "task-db"
  }

  application {
    name     = "postgresql"
    endpoint = "database"
  }
}
```
