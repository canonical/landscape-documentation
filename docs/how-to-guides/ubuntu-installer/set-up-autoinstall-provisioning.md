(how-to-ubuntu-installer-provisioning-set-up-autoinstall-provisioning)=
# How to set up autoinstall provisioning

> See also: [Ubuntu installation (Subiquity) documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/index.html)

The Ubuntu installer (24.04 and later) can use Landscape to serve an autoinstall file.
This is available on self-hosted and Landscape SaaS.
On Landscape SaaS, your account must be hosted on a subdomain.
Your Landscape account must use OIDC authentication.

```{note}
This feature is available from Landscape server `25.10~beta.4` onwards.
```

## Background information

[Autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) is a means to automate an Ubuntu installation.
Landscape integrates with the Ubuntu installer to deliver an Autoinstall file at installation time.

## Before you start

If you're on SaaS, you'll need to request that this feature is enabled for your account.

If you're on self-hosted, you'll need to configure your deployment to enable this feature. See {ref}`how-to-ubuntu-installer-provisioning-deployment-configuration`.

## Configure OIDC

Landscape uses OIDC authentication for the workstation provisioning experience.

Only users that are known to the OIDC provider will be able to use the provisioning experience.
A local Landscape user that logs in with username/password will not.

### Self-hosted

See {ref}`how-to-external-auth-oidc`.

### SaaS

1. Navigate to **Org settings > Identity providers**.
2. Configure an OIDC provider.

## Create and test your autoinstall file

```{important}
Landscape requires the use of the top-level `"autoinstall"` keyword.
```

See [Ubuntu's Autoinstall configuration reference](https://canonical-subiquity.readthedocs-hosted.com/en/latest/reference/autoinstall-reference.html)
for more details on creating an autoinstall file.

It is strongly recommended that you test your file by provisioning a workstation.
See {ref}`how-to-ubuntu-installer-provision-a-workstation` for details on provisioning a workstation.
Landscape injects some configuration into the autoinstall file to enable the workstation to register with the server after installation.

## Upload autoinstall file

```{note}
Currently, only the default file can be served to users.
You can set the default file in the Landscape web portal.
```

1. Navigate to the **Org. settings > Employees > Autoinstall files** tab.
2. Upload your autoinstall file(s) to Landscape.
3. Set the autoinstall file to be your default autoinstall file.

Only one file can be set as the default, but you can change this default at any time.
