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

```{import}
This guide uses `terraform` for commands, but everything can also be done using `tofu` instead.
If using OpenTofu, consider creating an alias in your shell's configuration file:

    alias terraform=tofu

```

## Create a Juju model

Create a Juju model for the Landscape deployment. This can be done using the `juju` CLI or with the [Terraform Provider for Juju](https://documentation.ubuntu.com/terraform-provider-juju/latest/howto/manage-models/).

```{tip}
If creating the model as a Terraform resource (`juju_model`), make sure you deploy a [`juju_ssh_key` resource](https://documentation.ubuntu.com/terraform-provider-juju/latest/howto/manage-ssh-keys/) to be able to access the units via SSH.
```

### Deploying the Landscape Scalable product module

The Landscape Scalable product module is a Terraform module that can be used to deploy the Landscape Server charm and other applications it depends on using Juju. It can be deployed by itself or used in higher-level plans. It is based on the (deprecated) Landscape Scalable charm bundle. See the {ref}`reference page <reference-landscape-product-modules-landscape-scalable>` for its specific inputs and outputs.

In a Terraform plan, you need to provide the module with the name of a Juju model and any desired configurations for the Landscape Server, HAProxy, PostgreSQL, and RabbitMQ server charms, for example:

```hcl
variable "model_name" {
  type = string
}

module "landscape_landscape-scalable" {
  source  = "canonical/landscape/juju//modules/landscape-scalable"

  model = var.model_name

  landscape_server = {
    channel  = "25.10/edge"
    revision = 209
    base     = "ubuntu@22.04"
    config = {
      min_install      = true
      autoregistration = true
      landscape_ppa    = "ppa:landscape/self-hosted-25.10"
    }
  }

  postgresql = {
    base    = "ubuntu@24.04"
    channel = "16/stable"
  }
}
```

Then, apply the plan and supply the Juju model name as a variable:

```sh
terraform apply -var model_name=<model_name>
```

Example output:

```hcl
applications = {
  "haproxy" = {
    "app_name" = "haproxy"
    "provides" = {
      "cos_agent" = "cos-agent"
      "haproxy_route" = "haproxy_route"
      "ingress" = "ingress"
    }
    "requires" = {
      "certificates" = "certificates"
      "reverseproxy" = "reverseproxy"
    }
  }
  "landscape_server" = {
    "app_name" = "landscape-server"
    "provides" = {
      "cos_agent" = "cos-agent"
      "data" = "data"
      "hosted" = "hosted"
      "nrpe_external_master" = "nrpe-external-master"
      "website" = "website"
    }
    "requires" = {
      "application_dashboard" = "application-dashboard"
      "db" = "db"
      "inbound_amqp" = "inbound-amqp"
      "outbound_amqp" = "outbound-amqp"
    }
  }
  "postgresql" = {
    "application_name" = "postgresql"
    "provides" = {
      "cos_agent" = "cos-agent"
      "database" = "database"
    }
    "requires" = {
      "certificates" = "certificates"
      "s3_parameters" = "s3-parameters"
    }
  }
  "rabbitmq_server" = {
    "charm" = tolist([
      {
        "base" = "ubuntu@24.04"
        "channel" = "latest/edge"
        "name" = "rabbitmq-server"
        "revision" = 250
        "series" = "noble"
      },
    ])
    "config" = tomap({
      "consumer-timeout" = "259200000"
    })
    "constraints" = "arch=amd64"
    "endpoint_bindings" = toset(null) /* of object */
    "expose" = tolist([])
    "id" = "landscape:rabbitmq-server"
    "machines" = toset([
      "2",
    ])
    "model" = "landscape"
    "model_type" = "iaas"
    "name" = "rabbitmq-server"
    "placement" = "2"
    "principal" = tobool(null)
    "resources" = tomap(null) /* of string */
    "storage" = toset(null) /* of object */
    "storage_directives" = tomap(null) /* of string */
    "trust" = false
    "units" = 1
  }
}
has_modern_amqp_relations = true
has_modern_postgres_interface = false
self_signed_server = true
```

After applying the plan, you can monitor the status of the Juju model using `juju status`, for example:

```sh
juju status -m <model_name> --watch 1s --relations
```

## Accessing the Landscape UI

Once the deployment has finished, get the IPv4 address of the leader `haproxy` unit and access it with your browser:

```bash
juju status -m <model_name> haproxy/leader
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

Additionally, HAProxy can be configured to use custom TLS credentials by setting the `ssl_cert` and `ssl_key` keys of the `config` attribute on the `haproxy` object to the base64-encoded contents of a TLS certificate and TLS private key, respectively:

```hcl
haproxy = {
  config = {
    ssl_cert = filebase64(var.path_to_tls_cert)
    ssl_key  = filebase64(var.path_to_tls_key)
  }
}
```
