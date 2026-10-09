---
myst:
  html_meta:
    description: "Understand how Landscape package change plans use a snapshot of package data on Landscape Server, and how that can differ from the actual state on your instances."
---

(explanation-package-change-plan-snapshot)=
# Package change plans

A package change plan is a staged set of package actions to apply across an instance selection. Landscape calculates the target instances and packages before it makes any changes. You can review the plan and then execute it to create the package activities.

Each plan has exactly one action (e.g. install, remove, ...), which determines how the affected instances and packages are resolved.

```{note}
You must be running Landscape Server 26.10 or later to use the REST API for package management.

This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts.
```

On self-hosted deployments, this feature may be enabled by setting both of the following flags in your service.conf:

```ini
[features]
package_change_plans = true
package_search_rest_api = true
```

## How plans are generated

Landscape uses the latest package state reported for each selected instance through {ref}`package reporting <explanation-package-reporting>`. Plans are created in the `pending` state, and Landscape automatically generates the plan in the background to populate the package changes that will occur on each instance. Check the plan status and wait until it is `ready` before reviewing or executing it.

Landscape does not query instances while generating a plan. The plan is a snapshot of their last reported state, which may be minutes or hours old, or older if an instance has been offline. Landscape does not refresh the snapshot when you execute the plan.

## Plan lifecycle

| State | What it means | What you can do |
| --- | --- | --- |
| `pending` or `generating` | Landscape is preparing the plan. | Check the plan status and wait until it is ready. |
| `ready` | The plan is ready to review and execute. It expires after the 24 hour review period. | Review its items and exclusions, then execute it before it expires. |
| `executing` | Landscape is creating the package activity. | Wait for the activity to be created. |
| `executed` | The package activity has been created; package operations may still be running. | Follow the activity to check progress and results. |
| `failed` | Landscape could not create the package activity. | Review the plan's error details and create a new plan to try again. |
| `expired` | The 24 hour review period has passed. | Create a new plan if you still want to execute the changes. |

## Plan items, exclusions, and summary

Plan items represent package actions for individual instances. View plan items to see the exact package changes that will be applied to each instance.

Exclusions are grouped by package names. For a package name known to Landscape, any selected instance that receives no change for that name is listed in the exclusions. Unknown package names are omitted from both the planned items and the exclusions.

The summary groups items by package action and reports how many instances each action affects. It also groups exclusions by package name and reports how many instances are affected. Review the summary to understand the plan's scope before executing it.

## Execution

Executing a plan creates a parent activity with child activities for instances that have plan items. Each instance applies the package operations against its current state using its package manager, so the outcome can differ from the plan if package state changed after generation. The package manager also resolves dependencies, so it may install, upgrade, or remove packages that are not listed in the plan. Follow the resulting {ref}`activity <explanation-activities>` for the actual progress and outcome.

## Recommendations

- Keep instances checking in regularly so the snapshot stays reasonably up to date.
- Execute a plan soon after it becomes ready, and create a new plan rather than executing a stale one.
- For instances that have been offline, review their reported package state before relying on a plan.

## Actions

### Install

Install packages across the instance selection by package ID (a specific version) or package name. An instance receives an install item when a requested version is available and no version of that package is already installed. When targeting by name, Landscape selects the newest applicable version for each instance. An instance with an installed version, or with no applicable available version, is excluded for that package name.

### Remove

Remove packages by package ID or package name. When targeting by ID, an instance receives a remove item only when a requested version is installed. When targeting by name, Landscape removes the package from any instance that has the package installed at any version. An instance with no version installed is excluded for that package name.

### Hold

Hold specific package versions to prevent them from being upgraded. An instance receives a hold item when the package is installed and not already held. If none of the requested versions for that package name are actionable, the instance appears in the exclusions.

### Unhold

Release specific package versions from their hold. An instance receives an unhold item when the package is held. If none of the requested versions for that package name are actionable, the instance appears in the exclusions.

### Upgrade

Upgrade packages by selecting package IDs or by category:

- **All upgrades**: every package with an available upgrade.
- **Security upgrades only**: packages with an available security upgrade.

When selecting a category, you can exclude specific packages from the upgrade set.

### Change version

Change a package from a specific version to another version of the same package, either as an upgrade or downgrade. An instance receives an item when the source version is installed and not held, and the target version is available and not installed. If none of the requested version changes for that package name are actionable, the instance appears in the exclusions.
