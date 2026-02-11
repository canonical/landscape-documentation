---
myst:
  html_meta:
    description: "Integrate Landscape with Microsoft Active Directory using PAM and SSSD. Configure domain authentication for self-hosted servers."
---

(how-to-external-auth-active-directory)=
# How to authenticate with Active Directory

This document describes how to enable authentication for self-hosted Landscape with Active Directory using Pluggable Authentication Modules (PAM).

Once enabled, users will be required to authenticate with an Active Directory account.

Note that this document is for integrating with [Microsoft's Active Directory](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/active-directory-overview), not Microsoft Entra ID (formerly "Azure Active Directory").

```{note}
Landscape uses Active Directory only for authentication decisions.
Landscape doesn't currently integrate with external roles, groups, or existing user metadata.
You still need to invite users and assign their roles and permissions within Landscape.
```

## Integrate Landscape with Active Directory

To integrate Landscape with Active Directory:

1. Install the System Security Services Daemon (sssd) and helper tools:

    ```bash
    sudo apt install sssd-ad sssd-tools realmd adcli samba-common-bin policykit-1 packagekit
    ```

2. Verify connectivity to the domain controller by discovering the Active Directory domain. Replace `{DOMAIN}` with the name of the Active Directory domain you want to connect to:

    ```bash
    sudo realm -v discover {DOMAIN}
    ```

    You’ll receive output similar to:

    ```bash
     * Resolving: _ldap._tcp.example.com
     * Performing LDAP DSE lookup on: 192.168.0.133
     * Successfully discovered: example.com
    example.com
      type: kerberos
      realm-name: EXAMPLE.COM
      domain-name: example.com
      configured: kerberos-member
      server-software: active-directory
      client-software: sssd
      required-package: sssd-tools
      required-package: sssd
      required-package: libnss-sss
      required-package: libpam-sss
      required-package: adcli
      required-package: samba-common-bin
      login-formats: %U@example.com
      login-policy: allow-realm-logins
    ```

3. Join the computer to the Active Directory domain. Replace `{DOMAIN}` with the domain you specified earlier.

    ```bash
    sudo realm -v join {DOMAIN}
    ```

    You’ll be prompted to authenticate as the administrator of the domain. If you need to use a different administrator account, include the `-U` flag and specify the account you want to authenticate as:

    ```bash
    sudo realm -v join -U {USER_ACCOUNT}@{DOMAIN} {DOMAIN}
    ```

    Once you’ve successfully joined the domain, you’ll be able to run commands such as `id {USER_ACCOUNT}` and `getent passwd {USER_ACCOUNT}` on Active Directory accounts to return group membership and other information.

4. Create a file named `/etc/pam.d/landscape` and add the following lines to it:

    ```bash
    #%PAM-1.0
    auth    required pam_sss.so
    account required pam_sss.so
    session required pam_sss.so
    ```

    This registers Active Directory as a PAM service.

5. Restart Landscape:

    ```bash
    sudo lsctl restart
    ```

## Create the first administrator account

To create the first administrator account:

1. Navigate to the IP of your Landscape instance
2. Complete the requested information to register the first administrator account
    - In the **Identity** field, enter the user’s relative distinguished name. In Active Directory, this is the “User Principal Name” and is most commonly defined with the user’s email address.

```{note}
Other Active Directory users will need to be invited individually in Landscape. This process does not automatically grant access to all Active Directory users. 
```

## Migrate users to Active Directory authentication

```{note}
Once a user is migrated to Active Directory authentication, the user’s password that was previously stored by Landscape will no longer be usable for login.
```

Users that have already been created in Landscape can be migrated to Active Directory authentication individually. To migrate users:

1. Log in to Landscape as the user that will be migrated
2. Click your username in the top right corner
3. Click **Edit settings**
4. Complete the **Identity** and **Passphrase** fields
    - In the **Identity** field, enter the user’s relative distinguished name. In Active Directory, this is the “User Principal Name” and is most commonly defined with the user’s email address.

If the user was correctly verified, they will be migrated to Active Directory for authentication.
