(how-to-ubuntu-installer-provision-a-workstation)=
# How to provision a workstation using Landscape and the Ubuntu installer

The Ubuntu installer (24.04 and later) can use Landscape to serve an autoinstall file.
This is available on self-hosted and SaaS Landscape.
On SaaS Landscape, your account must be hosted on a subdomain.
Your Landscape administrator must have configured an OIDC login method.

## In the Ubuntu installer

1. In the Ubuntu installer menu, select **install with Landscape**.
1. Enter the URL of your Landscape deployment.

The installer will generate a 6 digit attach code for you.
Save this for the next step.

## In Landscape

1. Navigate to the `/attach` page in Landscape.
1. Enter your 6 digit attach code.
1. Landscape will confirm that the attach code is valid and will prompt you to log in.
1. Authenticate against your OIDC provider.

## Back in the Ubuntu installer

1. After successful authentication, Landscape will serve an autoinstall file to the Ubuntu installer.
1. Confirm the autoinstall file.

The Ubuntu installer will use the autoinstall file to provision your device.
