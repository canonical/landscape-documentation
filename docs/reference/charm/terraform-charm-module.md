(reference-charm-terraform-charm-module)=

# Landscape Server charm Terraform module

This is the base [Terraform](https://developer.hashicorp.com/terraform) module for the [Landscape Server charm](https://charmhub.io/landscape-server), using the [Terraform Juju provider](https://registry.terraform.io/providers/juju/juju/latest) to model the charm deployment onto any non-Kubernetes cloud managed by [Juju](https://juju.is).

It can be deployed in isolation, but is intended as a building block for higher-level Terraform modules such as the {ref}`Landscape Scalable product module <reference-landscape-product-modules-landscape-scalable>`.

Source: [`terraform/charm`](https://github.com/canonical/landscape-server-operator/tree/main/terraform/charm) in the `landscape-server-operator` repository.

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.10 |
| <a name="requirement_juju"></a> [juju](#requirement\_juju) | ~> 1.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_juju"></a> [juju](#provider\_juju) | ~> 1.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [juju_application.landscape_server](https://registry.terraform.io/providers/juju/juju/latest/docs/resources/application) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_app_name"></a> [app\_name](#input\_app\_name) | Name of the application in the Juju model. | `string` | `"landscape-server"` | no |
| <a name="input_base"></a> [base](#input\_base) | The operating system on which to deploy. | `string` | `"ubuntu@24.04"` | no |
| <a name="input_channel"></a> [channel](#input\_channel) | The channel to use when deploying a charm. | `string` | `"26.04/stable"` | no |
| <a name="input_charm_name"></a> [charm\_name](#input\_charm\_name) | The name of the charm to be deployed. | `string` | `"landscape-server"` | no |
| <a name="input_config"></a> [config](#input\_config) | Application config. Details about available options can be found at https://charmhub.io/landscape-server/configurations. | `map(string)` | `{}` | no |
| <a name="input_constraints"></a> [constraints](#input\_constraints) | Juju constraints to apply for this application. | `string` | `"arch=amd64"` | no |
| <a name="input_machines"></a> [machines](#input\_machines) | Set of machine IDs to deploy units to. When specified, the 'units' variable is ignored. | `set(string)` | `null` | no |
| <a name="input_model_uuid"></a> [model\_uuid](#input\_model\_uuid) | UUID of a Juju model. | `string` | n/a | yes |
| <a name="input_revision"></a> [revision](#input\_revision) | Revision number of the charm. | `number` | `null` | no |
| <a name="input_units"></a> [units](#input\_units) | Number of units to deploy. Ignored when 'machines' is set. | `number` | `1` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_app_name"></a> [app\_name](#output\_app\_name) | Name of the deployed application. |
| <a name="output_has_modern_haproxy_interface"></a> [has\_modern\_haproxy\_interface](#output\_has\_modern\_haproxy\_interface) | Indicates whether the deployed revision uses haproxy-route relations (26.04+) rather than the legacy external HAProxy website endpoint. |
| <a name="output_provides"></a> [provides](#output\_provides) | Map of integration endpoints this charm provides. |
| <a name="output_requires"></a> [requires](#output\_requires) | Map of integration endpoints this charm requires. |
<!-- END_TF_DOCS -->
