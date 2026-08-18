---
myst:
  html_meta:
    description: "Register an NVIDIA DGX Spark running DGX OS with Landscape and enable remote script execution for management."
---

(how-to-set-up-nvidia-dgx-spark)=
# Set up NVIDIA DGX Spark for Landscape management

This guide covers bringing an existing NVIDIA DGX Spark under Landscape management. It uses the normal Landscape Client installation and registration workflow and leaves the system ready for NVIDIA's Landscape reference scripts.

This guide does not cover installing or reinstalling DGX Spark. For recovery or custom installation, follow [NVIDIA's DGX Spark documentation](https://docs.nvidia.com/dgx/dgx-spark/), including its [system recovery](https://docs.nvidia.com/dgx/dgx-spark/system-recovery.html) guidance.

## Before you begin

You need:

- an existing DGX Spark running the DGX OS baseline documented by NVIDIA;
- a Landscape SaaS account or access to a self-hosted Landscape account; and
- permission to register a computer in that Landscape account.

NVIDIA describes DGX OS as a customized Linux distribution based on Ubuntu and identifies it as the supported baseline for its DGX Spark enterprise manageability guidance. NVIDIA does not publish a separate Landscape Client version matrix for DGX Spark. Follow the current Landscape and Ubuntu Pro requirements for the client installation method you choose.

## Install and register Landscape Client

Choose the registration path that matches your Landscape deployment:

- For **Landscape SaaS**, follow {ref}`How to create a SaaS account and register your first client <howto-create-saas-account>`. The `pro enable landscape` method installs Landscape Client and starts the registration wizard after Ubuntu Pro is attached.
- For **self-hosted Landscape**, follow {ref}`How to install Landscape Client <how-to-install-landscape-client>` and {ref}`How to configure and register Landscape Client <how-to-configure-landscape-client>`. Provide the account name and Landscape Server URL for your deployment.

NVIDIA's current registration example uses Ubuntu Pro and `pro enable landscape` with the self-hosted option set to **No**. That example is for Landscape SaaS. Use Canonical's self-hosted instructions when registering with your own Landscape Server.

When registering the DGX Spark, choose a descriptive computer title. After registration, an administrator may need to accept the pending computer in the Landscape web portal. Confirm that the DGX Spark appears as a managed instance before continuing.

## Enable remote script execution

Enable the Landscape Client script execution plugin on the DGX Spark. Follow {ref}`Enable script execution <howto-heading-client-enable-script-execution>` in the Landscape Client configuration guide. That page documents the supported `landscape-config` options, including the system users allowed to run scripts, and the required client restart.

Remote script execution is a Landscape capability. It does not require a DGX-specific client plugin or a separate NVIDIA registration mechanism.

## Organize the DGX Spark systems

You can apply an ordinary Landscape tag, such as `dgx-spark`, to identify these systems in a mixed fleet. Tags are optional and are chosen by your organization; Landscape does not create a special DGX Spark object type.

For tag and access-group administration, see the {ref}`Landscape web portal documentation <how-to-guides-web-portal-index>`.

## Verify the setup

Before using an NVIDIA reference script, confirm that:

1. The DGX Spark appears as a managed instance in Landscape.
1. Landscape Client is running after the script execution configuration was applied.
1. Remote script execution is enabled for the client and the intended run-as user is allowed by the client configuration.

When these conditions are met, continue to {ref}`Use NVIDIA DGX Spark management scripts with Landscape <how-to-manage-nvidia-dgx-spark>`.