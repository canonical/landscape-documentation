(how-to-ubuntu-installer-provision-a-workstation)=
# How to provision a workstation with Autoinstall using Landscape and the Ubuntu installer

The Ubuntu installer (24.04 and later) can use Landscape to serve an autoinstall file.
This is available on self-hosted and Landscape SaaS.
On Landscape SaaS, your account must be hosted on a subdomain.
Your Landscape administrator must have configured an OIDC login method.
Your Landscape administrator must have set up your Landscape deployment for workstation provisioning. See {ref}`how-to-ubuntu-installer-set-up-landscape`.

## In the Ubuntu installer

1. In the Ubuntu installer menu, select **install with Landscape**.
1. Enter the URL of your Landscape deployment.

The installer will generate a 6 digit attach code for you.
Save this for the next step.

## In Landscape

1. Navigate to `https://<LANDSCAPE_SERVER_DOMAIN>/attach`.
2. Enter your 6 digit attach code. Landscape will confirm that the attach code is valid and prompt you to log in.
3. Log in with your OIDC provider.

## Back in the Ubuntu installer

After successful authentication, Landscape will serve an autoinstall file to the Ubuntu installer.
You need to confirm this autoinstall file.
The Ubuntu installer will use the autoinstall file to provision your device.
