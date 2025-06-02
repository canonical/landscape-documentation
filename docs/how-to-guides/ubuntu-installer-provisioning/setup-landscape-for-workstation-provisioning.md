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

1. Navigate to **Org settings > Identity providers**.
2. Configure a Google OAuth 2.0 client.
3. Request the **groups** claim when configuring the client.
4. Assign the **groups** claim to the **Autoinstall file** resource.

The **groups** claim will be used to identify an autoinstall file for a user when they authenticate.

## (Optional) Configure Hashicorp Vault for secure, versioned autoinstall storage

(Not delivered in 25.10)

Landscape supports integration with Hashicorp Vault for secure, versioned storage.
When configured as a storage backend, Landscape will store autoinstall files in the Vault.

## Upload autoinstall files

1. Navigate to the **Employees > Autoinstall** tab.
2. Upload your autoinstall files to Landscape.

## (Optional) Set default autoinstall file

If a user hasn't been assigned an autoinstall file, they can still provision a device with a specified default autoinstall file.
Only one file may be the default file at a time.
You may change the default file at any time.

## Associate your autoinstall files with users

Associate each autoinstall file with a particular value of the **groups** claim.
When a user reports a **groups** claim with this value, they will be assigned the corresponding autoinstall file.

### (Optional) Assign priorities

If a user reports multiple **groups** claim values, they may be associated with multiple autoinstall files.
However, Landscape will only serve users a single file.
You may assign each file a priority to break ties if this situation arises.
If two files have the same priority or no priority assigned, Landscape will internally resolve the tie and deterministically serve a single file.
