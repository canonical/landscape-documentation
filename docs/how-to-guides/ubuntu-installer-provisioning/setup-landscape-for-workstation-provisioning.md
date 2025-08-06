(how-to-ubuntu-installer-provisioning-setup-landscape)=
# How to set up Landscape for workstation provisioning

Recent releases of the Ubuntu installer (24.04+) can use Landscape to serve an autoinstall file.
This is available on self-hosted and SaaS Landscape.
On SaaS Landscape, your account must be hosted on a subdomain.
Your Landscape account must use OIDC authentication.

## Configure OIDC

Landscape uses OIDC authentication for the workstation provisioning experience.

Only users that are known to the OIDC provider will be able to use the provisioning experience.
A local Landscape user that logs in with username/password will not.

1. Navigate to **Org settings > Identity providers**.
2. Configure an OIDC client.

## Upload autoinstall file

1. Navigate to the **Employees > Autoinstall** tab.
2. Upload your autoinstall file(s) to Landscape.
3. Set the autoinstall file to be your default autoinstall file. This ensures it is served to all users that successfully authenticate.

Only one file may be the default.
