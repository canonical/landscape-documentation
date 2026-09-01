---
myst:
  html_meta:
    description: "Understand how Landscape package change plans use a snapshot of package data on Landscape Server, and how that can differ from the actual state on your instances."
---

(explanation-package-change-plan-snapshot)=
# Package change plans

A package change plan is a staged set of package actions to be applied across a computer selection.
When you create a plan, Landscape calculates which computers and packages are targeted before any changes
are made. You can inspect the plan, then execute it to trigger the underlying activities.

Each plan has exactly one action (e.g. install, remove, ...), which determines how
the affected computers, and packages are resolved.

```{note}
You must be running Landscape Server 26.10 or later to use the REST API for package management.

This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts.
```

A package change plan is built from the package data that Landscape Server
already holds for the selected instances. That data comes from what each
instance last reported through {ref}`package reporting
<explanation-package-reporting>`, combined with the package metadata from the
repositories Landscape knows about.

Landscape does not query the instances while you build a plan. The plan is a
snapshot: it reflects the last reported state, which may be minutes or hours
old, or older for instances that have been offline.

## What this means when you create a plan

- The package versions, installed and held states, and available upgrades shown
  in a plan come Landscape Server's stored package state, not a live query
  to the instance.
- Instances that cannot perform an action according to the snapshot
  are listed as exclusions. Those exclusions are also based on the
  snapshot.
- The snapshot is taken when the plan is created and is not refreshed when the
  plan is executed. Changes made on an instance in the meantime, locally or
  through another Landscape activity, are not reflected in the plan.

## What this means when you execute a plan

Executing a plan sends the package operations to the selected instances as
activities. Each instance applies them against its real, current state using its
own package manager, so the outcome can differ from the plan:

- An operation can fail or do nothing if the instance's state changed after the
  plan was created.
- The package manager resolves dependencies on the instance, so it may install,
  upgrade, or remove packages that the plan does not list.

Check the resulting activities for the actual per-instance outcome.

## Recommendations

- Keep instances checking in regularly so the snapshot stays reasonably up to date.
- Execute a plan soon after creating it, and create a new plan rather than
  executing a stale one.
- For instances that have been offline, review their reported package state
  before relying on a plan.
