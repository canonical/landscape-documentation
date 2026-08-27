---
myst:
  html_meta:
    description: "Understand how Landscape package change plans use a snapshot of package data on Landscape Server, and how that can differ from the actual state on your instances."
---

(explanation-package-change-plan-snapshot)=
# Package change plans

Available in Landscape 26.10 and later.

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
  in a plan come from the snapshot, not from the instance itself.
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

- Keep instances checking in regularly so the snapshot stays current.
- Execute a plan soon after creating it, and create a new plan rather than
  executing a stale one.
- For instances that have been offline, review their reported package state
  before relying on a plan.
