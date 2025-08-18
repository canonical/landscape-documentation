(how-to-ubuntu-installer-provisioning-setup-landscape)=
# How to set up Landscape for workstation provisioning

Recent releases of the Ubuntu installer (24.04+) can use Landscape to serve an autoinstall file.
This is available on self-hosted and SaaS Landscape.
On SaaS Landscape, your account must be hosted on a subdomain.
Your Landscape account must use OIDC authentication.

```{note}
This feature is available from Landscape server `25.08` onwards.
```

## Install the `landscape-ubuntu-installer-attach` package

Landscape requires an additional service for the Ubuntu installer attach experience.

```sh
sudo add-apt-repository ppa:landscape/latest-stable
sudo apt update
sudo apt install landscape-ubuntu-installer-attach
```

## Enable the feature

On self-hosted, you'll need to set the feature flag in your `service.conf`:

```ini
[features]
[...]
enable-employee-management = true
```

On SaaS, you'll need to make a request to support.

## Configure OIDC

Landscape uses OIDC authentication for the workstation provisioning experience.

Only users that are known to the OIDC provider will be able to use the provisioning experience.
A local Landscape user that logs in with username/password will not.

### Self-hosted

See {ref}`how-to-external-auth-oidc`.

### SaaS

1. Navigate to **Org settings > Identity providers**.
2. Configure an OIDC client.

## Upload autoinstall file

```{note}
Currently, only the default file can be served to users.
Ensure that you set a default file.
```

1. Navigate to the **Employees > Autoinstall** tab.
2. Upload your autoinstall file(s) to Landscape.
3. Set the autoinstall file to be your default autoinstall file.

Only one file may be the default.
