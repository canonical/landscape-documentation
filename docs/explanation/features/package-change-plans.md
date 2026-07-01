---
myst:
  html_meta:
    description: "Understand how package change plans work in Landscape, including how each action type resolves its input parameters into a set of planned operations."
---

(explanation-package-change-plans)=

# Package change plans

A package change plan is a staged set of package operations to be applied across a computer selection. When you create a plan, Landscape calculates which computers and packages are affected before any changes are made. You can inspect the plan, then execute it to trigger the underlying activities.

Each plan has exactly one action, which determines how the set of affected (computer, package) pairs is resolved.

## Actions

### Install

Install one or more packages across the computer selection. You can target packages by exact version or by name.

**Targeting by exact version:** A computer is included if the specified version is available on that computer and not already installed. A computer is excluded if that version is already installed, or if the version is not available on that computer.

**Targeting by name:** Landscape queries all known versions of each name and resolves which version to install per computer. Versions are considered newest-first. For each computer, Landscape installs the newest available version that is not already installed in any version. A computer is excluded if it already has any version of the package installed, or if no version of the package is available on it.

### Remove

Remove one or more packages across the computer selection. You can target packages by exact version or by name.

A computer is included if the specified package is installed on it. A computer is excluded if the package is not installed. When targeting by name, any installed version matching the name is removed.

### Hold

Pin specific packages at their current version across the computer selection, preventing them from being upgraded. A computer is included if the package is installed and not already held on it. A computer is excluded if the package is not installed, or if it is already held.

### Unhold

Release a package from its version pin across the computer selection, allowing it to be upgraded again. A computer is included if the package is currently held on it. A computer is excluded if the package is not held.

Packages cannot be held as "uninstalled". Only installed packages can be held by change plans.

### Upgrade

Upgrade packages across the computer selection. You can target a specific set of packages, or upgrade by category:

- **All upgrades** -- every package with an available upgrade.
- **Security upgrades only** -- only packages with an upgrade available from a security pocket.

When upgrading by category, you can also exclude specific packages from the upgrade set.

### Change version

Switch specific packages to a different version -- either an upgrade or a downgrade. Each operation maps a currently installed version to a desired target version. A computer is included if the current version is installed on it, the current version is not held, and the target version is available. A computer is excluded if the current version is not installed, the current version is held, or the target version is unavailable.

## Plan items and the summary

After creation, the plan contains a flat list of (computer, package) items, each representing one intended operation on one computer. Not every item will necessarily be executable. The plan summary groups items by package and breaks down counts by target state:

- **Applicable** -- the operation can be performed on this computer.
- **Not applicable** -- the operation cannot be performed on this computer.

Reviewing the summary before executing gives you visibility into the scope and impact of the plan.

## Execution

Executing a plan converts its applicable items into Landscape activities, which are then dispatched to the relevant computers. See {ref}`explanation-activities` for details on how activities progress through their lifecycle.
