(how-to-ubuntu-installer-provisioning-setup-landscape)=
# How to set up Landscape for workstation provisioning

Recent releases of the Ubuntu installer (24.04+) can use Landscape to serve an autoinstall file.
This is available on self-hosted and SaaS Landscape.
On SaaS Landscape, your account must be hosted on a subdomain.
Your Landscape account must use OIDC authentication. Currently, only Google OAuth 2.0 is supported.

## Configure OIDC

Landscape uses OIDC authentication for the workstation provisioning experience.
Configure Google OAuth 2.0 OIDC (link).

Only users that are known to the OIDC provider will be able to use the provisioning experience.
A local Landscape user that logs in with username/password will not.

## Upload autoinstall files

Add your autoinstall files to Landscape.

## (Optional) Set default autoinstall file

If a user hasn't been assigned an autoinstall file, they can still provision a device with a specified default autoinstall file.
Only one file may be the default file at a time.
You may change the default file at any time.

## Associate your autoinstall files with users

TBD:

- Option 1: explain the group import and association process
- Option 2: custom claims
