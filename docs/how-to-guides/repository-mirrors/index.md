---
myst:
  html_meta:
    description: "Mirror Ubuntu and third-party repositories with Landscape. Create custom repositories and manage packages for offline deployments."
---

(how-to-guides-repository-mirrors-index)=
# Repository mirrors

Landscape can mirror Ubuntu package repositories and third-party repositories, enabling you to control which packages are available to your managed machines. This is particularly useful for creating controlled update environments, reducing bandwidth usage, and supporting airgapped or offline deployments.

## Core workflows

Use these guides for standard repository mirror setup and management. The web portal guide covers both the Landscape Server 26.04 LTS and later repository model and the model used in 25.10 and earlier.

```{toctree}
:titlesonly:
:maxdepth: 1

Manage repositories in the web portal <manage-repositories-in-the-web-portal>
Manage repositories with the Legacy API <manage-repositories-with-the-api>
Set up repository mirroring end-to-end (26.04 and later) <set-up-repository-mirroring-end-to-end>
```

## Specialized environments

Use these guides when your deployment has connectivity constraints or multi-tier mirror requirements.

```{toctree}
:titlesonly:
:maxdepth: 1

Manage repositories in an airgapped environment <manage-repositories-in-an-air-gapped-or-offline-environment>
Create tiered-repository mirrors <create-tiered-repository-mirrors>
```

## See also

- {ref}`explanation-repo-mirroring`
- {ref}`how-to-migrate-repository-mirrors-to-debarchive`
- {ref}`how-to-guides-landscape-installation-and-set-up-index`
