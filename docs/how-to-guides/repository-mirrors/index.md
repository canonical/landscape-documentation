---
myst:
  html_meta:
    description: "Mirror Ubuntu and third-party repositories with Landscape. Create custom repositories and manage packages for offline deployments."
---

(how-to-guides-repository-mirrors-index)=
# Repository mirrors

Landscape can mirror Ubuntu package repositories and third-party repositories, enabling you to control which packages are available to your managed machines. This is particularly useful for creating controlled update environments, reducing bandwidth usage, and supporting airgapped or offline deployments.

```{toctree}
:titlesonly:
:maxdepth: 2
:glob:

Manage repositories in the web portal <manage-repositories-in-the-web-portal>
Manage repositories with the API <manage-repositories-with-the-api>
Manage repositories in an airgapped environment <manage-repositories-in-an-air-gapped-or-offline-environment>
Create tiered-repository mirrors <create-tiered-repository-mirrors>
