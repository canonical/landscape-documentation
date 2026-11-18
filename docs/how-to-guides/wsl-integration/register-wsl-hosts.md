---
myst:
  html_meta:
    description: "Set up Ubuntu Pro for WSL and register Windows hosts to Landscape. Configure WSL 2 integration on Windows 11 with an Ubuntu Pro token."
---

(how-to-register-wsl-hosts)=
# How to set up Ubuntu Pro for WSL and register WSL hosts to Landscape

> See also: [Ubuntu on WSL documentation](https://ubuntu.com/wsl/docs/latest/)

```{note}
When Landscape 24.04 LTS was released, Ubuntu Pro for WSL was in beta and wasn't yet available to everyone in the Microsoft Store. For its current status and requirements, see the [Ubuntu on WSL documentation](https://ubuntu.com/wsl/docs/latest/).
```

```{note}
If this is the first time you've installed Landscape, continue with this guide. If you've upgraded from Landscape 23.10 or earlier, you first need to configure it to enable WSL-related services. See {ref}`how-to-wsl-configure-landscape-after-upgrade`.
```

This guide describes how to set up Ubuntu Pro for WSL and register new WSL hosts (Windows machines) to Landscape.

## Check prerequisites

```{note}
You must be running Windows 11 to use Ubuntu Pro for WSL.
```

To use the WSL-Landscape integration, you must have the following applications downloaded from the Microsoft Store:

- [Windows Subsystem for Linux](https://apps.microsoft.com/detail/9P9TQF7MRM4R)
- An Ubuntu application, such as [Ubuntu (Preview)](https://apps.microsoft.com/detail/9P7BDVKVNXZ6)

When Landscape 24.04 LTS was released, the WSL integration with Landscape required Ubuntu (Preview). If you already have the Ubuntu (Preview) application installed, you may need to update it to the newest version.

Also, you must have WSL 2 installed instead of WSL 1. If you've just now installed WSL from the Microsoft Store, then you've installed WSL 2 and can proceed to the next steps. If you've previously installed WSL and aren't sure if it's WSL 1 or WSL 2, run `wsl -l -v` in PowerShell or Command Prompt to get the version. If you have WSL 1, you need to upgrade to WSL 2. For more information, see [Microsoft's guide on upgrading from WSL 1 to WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2).

## Install and activate Ubuntu Pro for WSL

To install Ubuntu Pro for WSL from your Windows machine:

1. Install the Ubuntu Pro for WSL application from the Microsoft Store
1. Click **I already have a token**
1. Enter your Ubuntu Pro token. You can get this from your [Ubuntu Pro account dashboard](https://ubuntu.com/pro/dashboard).
1. Click **Apply**

If done successfully, you'll receive confirmation on the next page that your subscription is active.

You may also be prompted to provide details for your Landscape configuration. You can either provide this information via the Ubuntu Pro for WSL GUI, or you can use the steps in the following section to complete your Landscape configuration.

## Configure Ubuntu Pro for WSL for Landscape

```{note}
You may have completed these steps or portions of these steps in the Ubuntu Pro for WSL GUI. It's recommended that you still review this section to ensure you've configured Ubuntu Pro for WSL correctly.
```

To configure Ubuntu Pro for WSL so the Windows machine can be registered as a WSL host with Landscape:

1. Download Landscape Server's public certificate and save it to your Windows machine. If you used the Landscape Quickstart installation, the auto-generated self-signed certificate can be found at `/etc/ssl/certs/landscape_server.pem`.
1. Open the Registry Editor in your Windows machine
    - To open the Registry Editor, either press the `Windows key + R` and type `regedit` or search "Registry Editor" in the taskbar and select it from the results.
1. Go to `HKEY_CURRENT_USER\Software\Canonical\UbuntuPro`.
    - This key won't exist until you've run Ubuntu Pro for WSL at least once. If you don't run Ubuntu Pro for WSL, you'll need to create the key and values yourself. For more information, see [Microsoft's documentation on Windows registry information for advanced users](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/windows-registry-advanced-users).
1. Open the `UbuntuProToken` key and add your Ubuntu Pro token with Right Click > **Modify**, then write your token in the **Value data** field. You can get your token from your [Ubuntu Pro dashboard](https://ubuntu.com/pro/dashboard).
1. Open the `LandscapeConfig` key and add the following lines in the **Value data** field:

    ```ini
    [host]
    url = <HOST_URL:PORT>

    [client]
    account_name = <ACCOUNT_NAME>
    registration_key = <REGISTRATION_KEY>
    url = <CLIENT_URL>
    log_level = debug
    ping_url = <PING_URL>
    ssl_public_key = <SSL_CERT>
    ```

    Replace these values:

    - `<HOST_URL:PORT>`: The URL of your Landscape account (without `https://`) followed by a colon (`:`) and the port number. Port 6554 is the default for Landscape Quickstart installations. For example, `landscape-server.example.com:6554`.
    - `<ACCOUNT_NAME>`: The Landscape account name this computer belongs to. This is located on your organization's home page in the Landscape web portal. For self-hosted Landscape accounts, the account name defaults to "standalone".
    - `<REGISTRATION_KEY>`: An optional account-wide key used to register new clients. There is no key defined by default, but one can be set in your Landscape account settings. If you have a registration key, it's located on your organization's home page in your Landscape web portal. If you don't have a registration key, leave this field blank.
    - `<CLIENT_URL>`: The main URL for the Landscape Server to connect this client to. This defaults to the URL of your Landscape account suffixed with `/message-system`, although you may be using a different URL. For example, `https://landscape-server.example.com/message-system`.
    - `<PING_URL>`: The ping URL you want this client to report to. This defaults to the URL of your Landscape account suffixed with `/ping`, although you may be using a different URL. For example, `http://landscape-server.example.com/ping`. Your ping URL uses HTTP (not HTTPS) by default.
    - `<SSL_CERT>`: The location of Landscape Server's public certificate on your Windows machine. If you saved the certificate to the user `Downloads` directory, this value would be similar to `C:\Users\user\Downloads\landscape_server.pem`.

    Your final `LandscapeConfig` key should be similar to the following example:

    ```ini
    [host]
    url = landscape-server.example.com:6554

    [client]
    account_name = standalone
    url = https://landscape-server.example.com/message-system
    log_level = debug
    ping_url = http://landscape-server.example.com/ping
    ssl_public_key = C:\Users\user\Downloads\landscape_server.pem
    ```

## Finalize the Windows machine registration

To finish registering your WSL host to Landscape:

1. Restart Windows
1. Wait for your Windows machine to appear in your Landscape account. This can take a few minutes, and you may need to refresh the page.
1. Accept the pending computer
    - To accept it, tick the checkbox near its name, assign it to an access group, and click **Accept**

Your Windows host machine is now registered in Landscape. To register WSL-Ubuntu instances, see {ref}`how-to-manage-wsl-instances`.

(howto-heading-register-wsl-host-troubleshoot)=
## (If necessary) Troubleshoot

> See also: [Ubuntu Pro for WSL's logs](https://ubuntu.com/wsl/docs/latest/howto/06-access-the-logs/)

If your Windows host machine doesn't appear as a pending computer in your Landscape account:

- **Ensure you're logged in to the same Landscape account that your WSL host is registering with**

    You must be logged into the Landscape account associated with your WSL host registration.

- **Wait a few minutes and refresh your Landscape account**

    The registration process won't be immediate; it may take a few minutes. If you haven't already, wait a few minutes and try refreshing the page to see if your Windows machine appears as a pending computer in your Landscape account.

- **Check your `LandscapeConfig` key to ensure it has the correct information for your Landscape account**

    You should check closely that the values in your `LandscapeConfig` registry key match your system's configuration. In the `[client]` section, your `url` and `ping_url` values may be different than the defaults. Your `ssl_public_key` may also be stored in a different location.

- **Check that the `url` in the `[host]` section of your `LandscapeConfig` key includes the port number (usually Port 6554) and doesn't include `https://`**

    Your `[host]` `url` value must include the port number and must be written without `https://`. The Landscape Quickstart installation uses Port 6554 by default, although your specific port may be different if you've changed the configuration. For example:

    ```ini
    [host]
    url = landscape-server.example.com:6554
    ```

- **Ensure your firewall settings are configured appropriately**

    You may need to adjust your firewall settings to allow inbound and outbound traffic on Port 6554, or whichever port you're routing traffic on if you've changed the port. Port 6554 is the default for `landscape-server-quickstart` installations.

- **If your Landscape URL isn't registered with a public or private DNS, you may need to register it or update your Windows Hosts file**

    Your domain name won't resolve if it's not registered with DNS. If you plan to update your Windows Hosts file instead of registering the domain with DNS, it's recommended that you proceed with extreme caution and consult Microsoft's documentation first.

- **If you're using a registration key, ensure that the registration key in the `LandscapeConfig` key matches the registration key in your Landscape account**

    If you're using a registration key, the registration key you use in your `LandscapeConfig` key must match exactly with the registration key in your Landscape account. Your registration key can be found in the **Account** tab on the web portal.

- **If you have auto-registration enabled, check if your Windows machine is already listed as a computer in your Landscape account**

    Landscape has an auto-registration feature that allows you to register computers without manually approving each one. If you're using a registration key and you have this feature enabled, your Windows machine won't appear as a pending computer. Instead, it'll auto-register and appear in your list of computers. For more information, see {ref}`how to auto-register new computers <howto-heading-client-autoregister>`.

- **Check that your Ubuntu Pro token was applied correctly**

    If you successfully completed the previous steps on activating Ubuntu Pro for WSL, your Ubuntu Pro token should be active. However, you can also check if it's active in the Registry Editor. In `HKEY_CURRENT_USER\Software\Canonical\UbuntuPro`, there should be a key titled `UbuntuProToken` with your token inside. If this isn't there, you can add these values in the Registry Editor, or you can re-do the previous steps on installing and activating Ubuntu Pro for WSL.

- **Reboot your Windows machine**

    If you haven't already, try rebooting your Windows machine to ensure the Landscape configuration was applied.

- **Access the Ubuntu Pro for WSL logs**

    If you've completed the previous troubleshooting steps and your Windows machine still doesn't appear as a pending computer in Landscape, you should review the Ubuntu Pro for WSL logs. To access those logs, see [Ubuntu Pro for WSL's guide on how to access the logs for debugging](https://ubuntu.com/wsl/docs/latest/howto/06-access-the-logs/).

    Landscape won't have awareness of the Windows host machine until it's a pending computer or auto-registered in your Landscape account. The Landscape logs won't be helpful when troubleshooting this registration issue.
