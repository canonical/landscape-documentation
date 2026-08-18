---
myst:
  html_meta:
    description: "Use NVIDIA DGX Spark Landscape reference scripts with Landscape remote script execution."
---

(how-to-manage-nvidia-dgx-spark)=
# Use NVIDIA DGX Spark management scripts with Landscape

Use Landscape remote script execution to run NVIDIA's Landscape reference scripts on registered DGX Spark systems. This guide covers the integration boundary; use NVIDIA's documentation for the script's purpose, prerequisites, behavior, and output.

Before starting, complete {ref}`Set up NVIDIA DGX Spark for Landscape management <how-to-set-up-nvidia-dgx-spark>`.

## Before you begin

You need:

- a DGX Spark running the DGX OS baseline supported by the NVIDIA documentation for the script you intend to use;
- the Landscape Client installed and registered on the DGX Spark; and
- permission to add and run scripts in the relevant Landscape access group.

For access groups and permissions, see the {ref}`Landscape web portal documentation <how-to-guides-web-portal-index>`.

## Obtain the NVIDIA reference script

1. Open NVIDIA's [Enterprise Lifecycle Integration](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html) documentation and follow its link to the Enterprise Lifecycle Integration Scripts package.
1. Extract the package and read its `README.md` and `LANDSCAPE_REFERENCE_SCRIPTS_SETUP.md` documentation before selecting a script.
1. Follow NVIDIA's instructions for the selected script's dependencies, permissions, and any files that must already be present on the DGX Spark.

The package contains both production tools and Landscape reference scripts. This guide concerns the Landscape reference scripts only. Do not assume that a production tool can be run through Landscape without following NVIDIA's deployment instructions.

## Enable remote script execution

Remote script execution must be enabled on each target Landscape Client. Follow {ref}`Enable script execution <howto-heading-client-enable-script-execution>` in the Landscape Client configuration guide. The guide documents the client configuration and the system users that can run scripts.

## Add the script to Landscape

1. In the Landscape web portal, go to **Scripts** > **Add script**.
1. Copy the NVIDIA reference script into the script editor and complete the form, including its title and access group.
1. Add attachments only when the NVIDIA script documentation requires them, and use the attachment names and paths expected by that script.
1. Select **Add script**.

These steps use Landscape's normal script workflow. For more information about adding scripts, see {ref}`How to use remote script execution <how-to-web-portal-use-remote-script-execution>`.

## Run the script

1. Identify the DGX Spark systems in Landscape. You can select instances directly or use the tags and access groups already used by your organization.
1. Select the target instances and choose **Operations** > **Run script**.
1. Select the NVIDIA reference script, choose the run-as user and time limit required by the NVIDIA script documentation, and select **Run**.

Start with one DGX Spark or a small test group before running a state-changing script across a larger group. Apply NVIDIA's change-control guidance for scripts that modify the system or initiate updates.

## Review the result

Landscape creates an activity for each script execution. Monitor the activity from the **Activities** page or from the target instance's **Activities** tab. Select the activity to inspect its status and the output returned by the client.

Landscape bounds returned script output using the client's `script_output_limit` configuration. A successful Landscape activity therefore does not mean that all NVIDIA evidence was transferred to Landscape. Use the output and local evidence according to the NVIDIA reference script's documentation, and contact NVIDIA for DGX-specific troubleshooting.

For an optional recurring or post-enrollment workflow, supported self-hosted Landscape deployments can use {ref}`script profiles <how-to-web-portal-use-script-profiles>`. Script profiles are available only in self-hosted Landscape 25.04 and later; they are not the foundation of this guide.

## Networking

Use Landscape's {ref}`internal network requirements <reference-internal-network-requirements>` for Landscape Server and client connectivity. Remote script execution sends the script to Landscape Client for local execution; Landscape Server does not need to SSH into the DGX Spark for this workflow. This does not define or replace any separate NVIDIA hardware-management or site-specific network requirements.