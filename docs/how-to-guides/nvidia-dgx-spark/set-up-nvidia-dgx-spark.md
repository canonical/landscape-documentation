---
myst:
  html_meta:
    description: "Register an NVIDIA DGX Spark running DGX OS with Landscape and enable remote script execution for management."
---

(how-to-set-up-nvidia-dgx-spark)=
# How to set up NVIDIA DGX Spark for Landscape management

> See also: {ref}`Landscape and NVIDIA DGX Spark <explanation-related-tools-nvidia-dgx-spark>`.

This guide describes how to register an existing NVIDIA DGX Spark with Landscape and prepare the system to run NVIDIA's Landscape reference scripts.

This guide doesn't cover installing or reinstalling DGX Spark, see [NVIDIA's DGX Spark documentation](https://docs.nvidia.com/dgx/dgx-spark/) for more information.

## Before you begin

You need:

- A DGX Spark running DGX OS
- A {ref}`Landscape SaaS account <howto-create-saas-account>` or {ref}`self-hosted Landscape Server deployment <how-to-guides-landscape-installation-and-set-up-index>`

## Install and register Landscape Client

Register the DGX Spark with Landscape so that it appears in your Landscape account as a managed instance.

1. On the DGX Spark, install and register Landscape Client:

   ```bash
   sudo pro enable landscape
   ```

   This command installs Landscape Client and starts the registration wizard.

1. When prompted, provide your Landscape account name and a descriptive title. If you register the DGX Spark with a self-hosted Landscape Server, also provide the server URL.

1. In the Landscape web portal, accept the pending instance if your account requires manual acceptance, then confirm that the DGX Spark appears as a managed instance before continuing.

For non-interactive registration, see {ref}`How to enable Landscape in the Ubuntu Pro Client <how-to-ubuntu-pro-enable-landscape>`.

## Enable remote script execution

[NVIDIA provides Landscape reference scripts for selected DGX Spark management operations](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html#canonical-landscape-reference-scripts-8). These scripts run locally on the DGX Spark through Landscape Client. Remote script execution is disabled by default, so you must enable the script execution plugin before you can run these scripts.

On the DGX Spark:

1. Enable the script execution plugin and authorize the system users that the scripts run as:

   ```bash
   sudo landscape-config \
     --include-manager-plugins=ScriptExecution \
     --script-users=root,landscape,nobody
   ```

   This allows the `root`, `landscape`, and `nobody` system users to run scripts. Adjust `--script-users` to match the run-as user required by the NVIDIA script you intend to use.

1. Restart Landscape Client to apply the change:

   ```bash
   sudo systemctl restart landscape-client
   ```

For other configuration options, see {ref}`Enable script execution <howto-heading-client-enable-script-execution>` in the Landscape Client configuration guide.

## Tag the DGX Spark systems

{ref}`Tag <reference-terms-tags>` each DGX Spark with a consistent identifier, such as `dgx-spark`, so that you can target these systems as a group in a mixed fleet. A shared tag lets you run NVIDIA scripts against every DGX Spark at once and filter them from other Ubuntu instances in your Landscape account.

Landscape manages a DGX Spark as an ordinary Ubuntu instance and doesn't automatically distinguish it from your other machines, so a tag is the recommended way to group these systems.

## Next steps

Now that the DGX Spark is registered and set up for remote script execution, continue to {ref}`Use NVIDIA DGX Spark management scripts with Landscape <how-to-manage-nvidia-dgx-spark>` to add and run NVIDIA's reference scripts on your DGX Spark systems.