---
myst:
  html_meta:
    description: "Understand how Landscape manages NVIDIA DGX Spark systems running DGX OS, and how NVIDIA's Landscape reference scripts fit into that workflow."
---

(explanation-related-tools-nvidia-dgx-spark)=
# Landscape and NVIDIA DGX Spark

[NVIDIA DGX Spark](https://docs.nvidia.com/dgx/dgx-spark/) is a compact AI computer that runs DGX OS, NVIDIA's customized Linux distribution based on Ubuntu. Organizations can manage multiple DGX Spark systems centrally with Landscape, alongside their other Ubuntu systems.

NVIDIA describes Landscape as its [primary recommended management platform for DGX Spark](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html). Landscape is available with [Ubuntu Pro](https://ubuntu.com/pro) subscriptions. This page describes how Landscape and DGX Spark fit together.

## How Landscape manages a DGX Spark

Landscape manages a DGX Spark like any other Ubuntu-based system. Landscape Client is the software that runs on the DGX Spark and communicates with your Landscape server. After you register your DGX Spark with Landscape, the DGX Spark appears in your Landscape account as a managed instance alongside your other machines.

From there, you use the same Landscape features you use everywhere else, such as:

- Inventory and status reported by Landscape Client,
- Package and security-update management,
- {ref}`Tags <reference-terms-tags>` and {ref}`access groups <reference-terms-access-groups>`, which let you group DGX Spark systems and target actions at them, and
- {ref}`Remote script execution <explanation-remote-script-execution>`, where each run is tracked as an {ref}`activity <explanation-activities>`.

## NVIDIA's Landscape reference scripts

Some DGX Spark operations are specific to the platform rather than to Ubuntu. For these, [NVIDIA publishes](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html) two kinds of automation:

- **[Production tools](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html#production-tools-11)**, which NVIDIA intends for general fleet automation.
- **[Landscape reference scripts](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html#canonical-landscape-reference-scripts-8)**, which are example implementations written for Landscape's remote script execution. They return short output and write detailed evidence to the DGX Spark itself.

NVIDIA provides the reference scripts as examples for customer adaptation rather than supported production software, so treat them as a starting point and review them before relying on them. A DGX Spark must be registered with Landscape before you can use the scripts.

Running these scripts through Landscape means DGX-specific tasks use the same targeting and activity history as your other scripted operations. For what each script does and how to interpret its results, see [NVIDIA's Enterprise Lifecycle Integration documentation](https://docs.nvidia.com/dgx/dgx-spark/enterprise-fleet-lifecycle.html).

## Other DGX Spark operations

Landscape manages the Ubuntu-based DGX OS installation. Use NVIDIA's tooling and [DGX Spark documentation](https://docs.nvidia.com/dgx/dgx-spark/) for hardware, firmware, drivers, recovery, provisioning, and out-of-band management.

## Next steps

- {ref}`Set up NVIDIA DGX Spark for Landscape management <how-to-set-up-nvidia-dgx-spark>`
- {ref}`Use NVIDIA DGX Spark management scripts with Landscape <how-to-manage-nvidia-dgx-spark>`
