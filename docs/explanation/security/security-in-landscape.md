---
myst:
  html_meta:
    description: "Learn about security in Landscape including deployment hardening, Ubuntu Pro integration, external authentication, and security updates management."
---

(explanation-security-overview)=
# Security in Landscape

This page provides an overview of various security topics related to Landscape.

## Secure your deployment

We have the following how-to guides for configuring your Landscape deployment beyond the default security settings.

- {ref}`how-to-install-fips-compliant`
- {ref}`how-to-harden-deployment`

## Ubuntu Pro

[Ubuntu Pro](https://ubuntu.com/pro) enhances the security and compliance of your Ubuntu systems. The following guides cover how to use Ubuntu Pro with Landscape:

- {ref}`how-to-attach-ubuntu-pro`
- {ref}`how-to-ubuntu-pro-enable-landscape`

## External authentication

For a more secure system, it’s recommended to use external authentication instead of password authentication. The following guides cover external authentication:

- {ref}`how-to-external-auth-active-directory`
- {ref}`how-to-external-auth-oidc`
- {ref}`how-to-external-auth-pam`

## Air-gapped and restricted network environments

If you’re using Landscape in an air-gapped environment, we have the following guides related to installing Landscape and setting up repository mirrors for offline environments:

- {ref}`how-to-install-airgapped`
- {ref}`how-to-manage-repos-airgapped`
- {ref}`how-to-create-tiered-repo-mirrors`

## Security updates and Livepatch

> See also: [Livepatch documentation](https://ubuntu.com/security/livepatch/docs)

You can use Landscape to apply security updates to your client machines, and Livepatch (within Landscape) to schedule high and critical Linux kernel vulnerability patches. We have the following guides on applying security updates with Landscape:

- {ref}`how-to-apply-security-updates`
- {ref}`how-to-web-portal-manage-livepatch` (24.04 or later)

## Additional Landscape security topics

We also have the following explanations about security in Landscape:

- {ref}`explanation-cryptographic-technology`
- {ref}`explanation-security-disclosure`
- {ref}`explanation-data-handling`
- {ref}`explanation-apparmor`

## Related topics

- [Ubuntu Pro documentation](https://documentation.ubuntu.com/pro/)
- [Ubuntu Security documentation](https://ubuntu.com/security)
- [Ubuntu Security | Security compliance and certifications for 22.04](https://ubuntu.com/security/certifications/docs/2204)
