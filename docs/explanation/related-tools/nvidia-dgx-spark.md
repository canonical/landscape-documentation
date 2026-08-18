---
myst:
  html_meta:
    description: "Understand how Landscape and NVIDIA DGX Spark work together for operating-system management and NVIDIA reference-script execution."
---

(explanation-related-tools-nvidia-dgx-spark)=
# Landscape and NVIDIA DGX Spark

NVIDIA DGX Spark runs DGX OS, a customized Linux distribution based on Ubuntu. Landscape can manage the operating-system environment on a DGX Spark after the system is enrolled as a Landscape client. NVIDIA also provides Landscape-specific reference scripts for selected DGX Spark operations.

For the setup procedure, see {ref}`Set up NVIDIA DGX Spark for Landscape management <how-to-set-up-nvidia-dgx-spark>`. For using NVIDIA's scripts after enrollment, see {ref}`Use NVIDIA DGX Spark management scripts with Landscape <how-to-manage-nvidia-dgx-spark>`.

Landscape and NVIDIA documentation have different areas of responsibility. Landscape documents the client, web portal, activities, and management workflows. NVIDIA remains the source of truth for DGX Spark, DGX OS, and the behavior of its tools and reference scripts.

## Landscape's role

Landscape provides the management functions that apply to an enrolled client, including:

- system status and inventory information reported by Landscape Client;
- package and security-update management;
- tags and access groups for organizing and targeting instances; and
- remote script execution and the activities that track those operations.

These are existing Landscape capabilities, not DGX Spark-specific features. See the documentation for {ref}`remote script execution <explanation-remote-script-execution>`, {ref}`activities <explanation-activities>`, and the {ref}`Landscape web portal <how-to-guides-web-portal-index>`.

## NVIDIA's role

NVIDIA remains authoritative for DGX Spark and DGX OS, including platform compatibility, drivers, firmware, recovery, provisioning, hardware-level management, diagnostics, and the detailed behavior of NVIDIA tools.

NVIDIA's [Enterprise Lifecycle Integration](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html) documentation distinguishes between production tools and Landscape reference scripts. The production tools are intended for fleet automation. The Landscape scripts are reference implementations designed for use with Landscape remote script execution and may require adaptation for an organization's processes. They are not a replacement for NVIDIA's production tools.

## How the reference scripts fit

The [NVIDIA Enterprise Lifecycle Integration Scripts package](https://docscontent.nvidia.com/dc/04/5167e1c14532bac843d48d29bf36/enterprise-lifecycle-integration-scripts-20260520-1602.zip) contains the Landscape reference scripts and their setup documentation. Use NVIDIA's documentation to determine which script is appropriate, what the script requires, what it changes, and how to interpret its output.

Use Landscape to make a reference script available to enrolled clients, select the target systems, run the script, and inspect the resulting activity. Landscape does not interpret NVIDIA's output format or take ownership of the evidence that a script writes on the DGX Spark.

Landscape limits the output returned by remote script execution according to the client's `script_output_limit` setting. NVIDIA's reference scripts are designed to keep standard output short and may store detailed evidence on the client. Do not assume that all script output or NVIDIA evidence is retained in Landscape; follow NVIDIA's instructions for detailed evidence and troubleshooting.

For the Landscape workflow, see {ref}`how-to-manage-nvidia-dgx-spark`.

## Hardware-level management

Landscape manages DGX Spark through Landscape Client at the operating-system level. Hardware-level and out-of-band operations remain part of NVIDIA's DGX Spark management model. Consult [NVIDIA's DGX Spark documentation](https://docs.nvidia.com/dgx/dgx-spark/) for those operations.
