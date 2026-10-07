---
myst:
  html_meta:
    description: "Discover Landscape's web portal with comprehensive management features."
---

(how-to-guides-web-portal-index)=
# Web portal

The web portal is Landscape's primary interface and the default in Landscape 26.10 and later. It was introduced in Landscape 24.04 LTS and has almost achieved full feature parity with the legacy web portal - albeit some features are still a work in progress.

The legacy web portal is Landscape's previous interface. It remains the default in Landscape 24.04 LTS through 26.04 LTS, but you can still switch to the web portal.

There are some differences in features between the two portals. Unless a guide specifies otherwise, use the web portal.

## Instance management

Manage instances in your estate and perform common tasks.

## Administration and access control

Manage administrators, roles, and access groups to control who can access Landscape and what they can do.

## Package and update management

Manage software on your instances, including Debian packages, snaps, Livepatch, and the kernel.

## Profiles and scripting

Use profiles and scripts to apply configuration and automate tasks across instances.

## Additional actions

Perform supporting instance actions such as adding annotations for context and sanitizing machines before decommissioning.

**Contents:**

```{toctree}
:titlesonly:
:maxdepth: 2

web-portal-24-04-or-later/manage-instances
web-portal-24-04-or-later/manage-administrators-and-roles
web-portal-24-04-or-later/manage-access-groups
web-portal-24-04-or-later/manage-packages-and-snaps
web-portal-24-04-or-later/manage-livepatch-and-kernel-updates
web-portal-24-04-or-later/use-profiles
web-portal-24-04-or-later/use-remote-script-execution
web-portal-24-04-or-later/use-annotations
web-portal-24-04-or-later/sanitize-instances
classic-web-portal/index
