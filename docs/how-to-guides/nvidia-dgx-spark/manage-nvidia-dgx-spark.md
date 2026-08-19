---
myst:
  html_meta:
    description: "Use NVIDIA DGX Spark Landscape reference scripts with Landscape remote script execution."
---

(how-to-manage-nvidia-dgx-spark)=
# How to use NVIDIA DGX Spark management scripts with Landscape

This guide describes how to run NVIDIA's Landscape reference scripts on registered DGX Spark systems using Landscape remote script execution. For each script's purpose, prerequisites, behavior, and output, see [NVIDIA's documentation](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html).

Before you start, complete {ref}`Set up NVIDIA DGX Spark for Landscape management <how-to-set-up-nvidia-dgx-spark>`. Note that your user account needs permission to run scripts to perform the steps in this guide. If you set up the Landscape account, your user account has the necessary administrator privileges by default. Otherwise, see {ref}`How to manage administrators and roles <how-to-web-portal-manage-admins-and-roles>`.

## Obtain the NVIDIA reference script

1. Open NVIDIA's [Enterprise Lifecycle Integration](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html) documentation and follow its link to the Enterprise Lifecycle Integration Scripts package.
1. Extract the package and read its `README.md` and `LANDSCAPE_REFERENCE_SCRIPTS_SETUP.md` documentation before selecting a script.
1. Follow NVIDIA's instructions for the selected script's dependencies, permissions, and any files that must already be present on the DGX Spark.

The package contains both production tools and Landscape reference scripts. This guide covers the Landscape reference scripts, which are shell scripts such as `signing_verification.sh` and `encryption_at_rest.sh`. See NVIDIA's documentation for the current set of reference scripts and each script's purpose. To run a production tool through Landscape, follow NVIDIA's deployment instructions for that tool.

## Add the script to Landscape

For each script you plan to use:

1. In the Landscape web portal, go to **Scripts** from the sidebar > **Add script**.
1. Copy the NVIDIA reference script into the script editor and complete the form, including its title and access group.
1. Add attachments only when the NVIDIA script documentation requires them, such as a configuration file that the script reads. Use the attachment names expected by that script.
1. **Add script**

If an NVIDIA script relies on an attached file, Landscape downloads its attachments to a temporary directory on the client when the script runs and sets the `LANDSCAPE_ATTACHMENTS` environment variable to that directory. NVIDIA scripts locate a bundled file such as `default.json` through this variable, for example `"$LANDSCAPE_ATTACHMENTS/default.json"` in Bash or `os.environ["LANDSCAPE_ATTACHMENTS"]` in Python, so add the file as an attachment using the name the script expects. For the full attachment behavior, see {ref}`explanation-remote-script-execution`.

These steps use Landscape's normal script workflow. For more general information about using scripts in Landscape, see {ref}`How to use remote script execution <how-to-web-portal-use-remote-script-execution>`. You can also add and run scripts programmatically with the {ref}`Landscape REST API <how-to-rest-api-request>`.

## Run the script

1. Identify the DGX Spark systems in Landscape. You can select instances directly, or filter by the tag you applied during setup, such as `dgx-spark`, and by access group.
1. Select the target instances, then **Operations** > **Run script**.
1. Select the NVIDIA reference script, then set the run-as user and time limit required by the NVIDIA script documentation. NVIDIA's reference scripts typically run as `root`, and the run-as user must be one you authorized with `--script-users` during setup.
1. Click **Run**.

Start with one DGX Spark or a small test group before running a state-changing script across a larger group. Apply NVIDIA's change-control guidance for scripts that modify the system or initiate updates.

## Review the result

Landscape creates an {ref}`activity <explanation-activities>` for each script execution. Monitor the activities from the **Activities** page or from the target instance's **Activities** tab. Open the activity to inspect its status and the output returned by the client. Because each execution is recorded as an activity, you keep a central history of which reference scripts ran on your DGX Spark systems and what they returned.

The output that Landscape returns is limited by the client's `script_output_limit` configuration. NVIDIA's reference scripts are designed for this: they return a short summary and write their detailed evidence to files on the DGX Spark itself. A successful activity therefore doesn't mean that Landscape collected everything the script produced. To retrieve the detailed evidence, follow the NVIDIA reference script's documentation.

To run reference scripts automatically, on a recurring schedule, on a set date, or after an instance enrolls, self-hosted Landscape (25.04 and later) can use {ref}`script profiles <how-to-web-portal-use-script-profiles>`.

## Networking

With remote script execution, Landscape sends the script to Landscape Client, which runs it locally on the DGX Spark. Landscape Server doesn't need SSH access to the DGX Spark for this workflow, so you don't need to open inbound SSH for it. For more information on the connectivity that Landscape Server and Landscape Client do require, see {ref}`internal network requirements <reference-internal-network-requirements>`.

Note that NVIDIA may have separate network requirements for DGX Spark hardware management. Those are additional to Landscape's requirements.