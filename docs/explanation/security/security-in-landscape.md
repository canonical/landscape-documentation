# Security in Landscape

This page provides an overview of various security topics related to Landscape.

## Secure your deployment

We have the following how-to guides for configuring your Landscape deployment beyond the default security settings.

- [How to install Landscape Server on FIPS-compliant machines](/how-to-guides/landscape-installation-and-set-up/install-on-fips-compliant-machines)
- [How to harden your Landscape deployment](/how-to-guides/security/harden-your-deployment.md)

## Ubuntu Pro

[Ubuntu Pro](https://ubuntu.com/pro) enhances the security and compliance of your Ubuntu systems. The following guides cover how to use Ubuntu Pro with Landscape:

- [How to attach your Ubuntu Pro subscription](/how-to-guides/ubuntu-pro/attach-ubuntu-pro)
- [How to enable Landscape in the Ubuntu Pro Client](/how-to-guides/ubuntu-pro/enable-landscape)

## External authentication

For a more secure system, it’s recommended to use external authentication instead of password authentication. The following guides cover external authentication:

- [How to authenticate with Active Directory](/how-to-guides/external-authentication/active-directory)
- [How to enable OIDC authentication](/how-to-guides/external-authentication/openid-connect-oidc)
- [How to enable PAM authentication](/how-to-guides/external-authentication/pluggable-authentication-modules-pam)

## Air-gapped and restricted network environments

If you’re using Landscape in an air-gapped environment, we have the following guides related to installing Landscape and setting up repository mirrors for offline environments:

- [How to install Landscape in an air-gapped or offline environment](/how-to-guides/security/install-landscape-in-an-air-gapped-or-offline-environment)
- [How to manage repositories in an air-gapped or offline environment](/how-to-guides/security/manage-repositories-in-an-air-gapped-or-offline-environment)
- [How to create tiered repository mirrors for multi-region and air-gapped deployments](/how-to-guides/repository-mirrors/create-tiered-repository-mirrors.md)

## Livepatch

> See also: [Livepatch documentation](https://ubuntu.com/security/livepatch/docs)

You can use Livepatch to schedule high and critical Linux kernel vulnerability patches, which removes the immediate need to reboot to upgrade the kernel on critical infrastructure. We have the following guide on using Livepatch with Landscape:

- [How to manage Livepatch and kernel updates from the Landscape web portal](/how-to-guides/web-portal/web-portal-24-04-or-later/manage-livepatch-and-kernel-updates) (24.04 or later)

## Additional Landscape security topics

We also have the following explanations about security in Landscape:

- [Cryptographic technology in Landscape](/explanation/security/cryptographic-technology)
- [Security disclosure and reporting](/explanation/security/disclosure-and-reporting)
- [Data handling](/explanation/security/data-handling.md)
- [AppArmor and Landscape](/explanation/security/apparmor)

## Related topics

- [Ubuntu Pro documentation](https://documentation.ubuntu.com/pro/)
- [Ubuntu Security documentation](https://ubuntu.com/security)
- [Ubuntu Security | Security compliance and certifications for 22.04](https://ubuntu.com/security/certifications/docs/2204)