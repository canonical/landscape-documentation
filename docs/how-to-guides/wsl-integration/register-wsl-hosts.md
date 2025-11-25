(how-to-register-wsl-hosts)=
# How to set up Ubuntu Pro for WSL and register WSL hosts to Landscape

> See also: [Ubuntu on WSL documentation](https://documentation.ubuntu.com/wsl/latest/)

```{note}
Ubuntu Pro for WSL is **not available yet** for everyone in the Microsoft Store. It's currently in beta.
```

```{note}
If this is the first time you've installed Landscape, you can continue with this guide. If you've upgraded from Landscape 23.10 or earlier, you first need to configure it to enable WSL-related services. See {ref}`how-to-wsl-configure-landscape-beta`.
```

This guide describes how to set up Ubuntu Pro for WSL and register new WSL hosts (Windows machines) to Landscape.

## Check prerequisites

```{note}
You must be running Windows 11 to use Ubuntu Pro for WSL.
```

To use the WSL-Landscape integration, you must an [Ubuntu Pro account](https://ubuntu.com/pro) and the following applications from the Microsoft Store:

- [Windows Subsystem for Linux](https://apps.microsoft.com/detail/9P9TQF7MRM4R)
- An Ubuntu application, such as [Ubuntu 24.04 LTS](https://apps.microsoft.com/detail/9nz3klhxdjp5?)

If you don't want to download your Ubuntu image from the Microsoft Store, you can manually specify a different image source instead. See {ref}`how-to-wsl-use-specific-image-source`.

Also, you must have WSL 2 installed instead of WSL 1. If you've just now installed WSL from the Microsoft store, then you've installed WSL 2 and can proceed to the next steps. If you've previously installed WSL and aren't sure if it's WSL 1 or WSL 2, run `wsl -l -v` in PowerShell or Command Prompt to get the version. If you have WSL 1, you need to upgrade to WSL 2. For more information, see [Microsoft's guide on upgrading from WSL 1 to WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2).

## Install and configure Ubuntu Pro for WSL

> See also: [Ubuntu on WSL's full documentation](https://documentation.ubuntu.com/wsl/latest/)

```{note}
This feature is in beta. Ubuntu Pro for WSL is **not available yet** for everyone in the Microsoft Store.
```

There are two ways to configure Ubuntu Pro for WSL for Ubuntu Pro and Landscape: via the Ubuntu Pro for WSL GUI or the Windows Registry.

### Option #1: Using the GUI

From your Windows machine:

1. Install Ubuntu Pro for WSL from the Microsoft Store and start the application
1. Provide your Ubuntu Pro token. You can get your token from your [Ubuntu Pro account dashboard](https://ubuntu.com/pro/dashboard).

Next, complete your Landscape configuration:

- Manual configuration (recommended if your Landscape server uses default settings):
    - Enter the FQDN of your server
    - (Optional) Provide a registration key and SSL cert
- Advanced configuration:
    - Enter the path for your client configuration file. The default location is `/etc/landscape/client.conf`, although this may differ if you manage a custom configuration. 

Once Landscape is successfully configured, you’ll receive confirmation on the next page that your Ubuntu Pro subscription is active and you can close the Ubuntu Pro for WSL window.

### Option #2: Using the Windows Registry

From your Windows machine:

1. Install Ubuntu Pro for WSL from the Microsoft Store, and run the application at least once. This guarantees that the key and values necessary for configuration will be set up in the registry.
1. Open the Registry Editor in your Windows machine (`Windows key + R` and type `regedit`)
1. Go to `HKEY_CURRENT_USER\Software\Canonical\UbuntuPro`.
1. Open the `LandscapeConfig` key and add your Landscape configuration in the **Value data** field:
    
    ```bash
    [host]
    url = <HOST_URL:PORT>
    
    [client]
    url = <CLIENT_URL>
    log_level = debug
    ping_url = <PING_URL>
    ssl_public_key = <SSL_CERT>
    ```
    
    Replace these values:
    
    - `<HOST_URL:PORT>`: The FQDN and port of your Landscape server. Port 6554 is the default for Landscape Quickstart installations. For example, `landscape-server.domain.com:6554`.
    - `<CLIENT_URL>`: The main URL for the Landscape server to connect this client to. This defaults to the URL of your Landscape account suffixed with `/message-system`, although you may be using a different URL. For example, `https://landscape-server.domain.com/message-system`.
    - `<PING_URL>`: The ping URL you want this client to report to. This defaults to the URL of your Landscape account suffixed with `/ping`, although you may be using a different URL. For example, `http://landscape-server.domain.com/ping`. Your ping URL uses HTTP (not HTTPS) by default.
   - `<SSL_CERT>` (optional): Path to the Landscape server's public certificate on your Windows machine. For example, `C:\Users\username\Downloads\landscape_server.pem`. Note that Ubuntu Pro for WSL follows the Windows OS certificate stores. You only need to specify the certificate if the machine running your Landscape server isn't trusted on your network.

    Example `LandscapeConfig`:
    
    ```bash
    [host]
    url = landscape-server.domain.com:6554
    
    [client]
    url = https://landscape-server.domain.com/message-system
    log_level = debug
    ping_url = http://landscape-server.domain.com/ping
    ssl_public_key = C:\Users\username\Downloads\landscape_server.pem
    ```
    
## Finalize the Windows machine registration

To finish registering your WSL host to Landscape:

1. Log into your Landscape web portal and refresh the page.
3. Go to **Instances** > review pending instances > accept the Windows host machine

Your Windows host machine is now registered in Landscape. To register WSL-Ubuntu instances, see {ref}`how-to-manage-wsl-instances`.

(howto-heading-register-wsl-host-troubleshoot)=
## (If necessary) Troubleshoot

> See also: [Ubuntu Pro for WSL's logs](https://documentation.ubuntu.com/wsl/en/latest/howto/06-access-the-logs/)

If your Windows host machine doesn’t appear as a pending instance in your Landscape account:

- **Ensure you’re logged in to the same Landscape account that your WSL host is registering with**
    
    You must be logged into the Landscape account associated your WSL host registration.
    
- **Wait a few minutes and refresh your Landscape account**
    
    The registration process won’t be immediate; it may take a few minutes. If you haven’t already, wait a few minutes and try refreshing the page to see if your Windows machine appears as a pending instance in your Landscape account.
    
- **Check your `LandscapeConfig` key to ensure it has the correct information for your Landscape account**
    
    You should check closely that the values in your `LandscapeConfig` registry key match your system's configuration. In the `[client]` section, your `url` and `ping_url` values may be different than the defaults. Your `ssl_public_key` may also be stored in a different location.
    
- **Check that the `url` in the `[host]` section of your `LandscapeConfig` key includes the port number (usually Port 6554) and doesn't include `https://`**
    
    Your `[host]` `url` value must include the port number and must be written without `https://`. The Landscape Quickstart installation uses Port 6554 by default, although your specific port may be different if you’ve changed the configuration. For example:
    
    ```bash
    [host]
    url = landscape-server.domain.com:6554
    ```

- **Check that the `enable-wsl-child-instance-profiles` in the `[features]` section of your `LandscapeConfig` key is set to `true`.**

    ```bash
    [features]
    enable-wsl-child-instance-profiles = true
    ```
    This setting didn't exist in older installations of Landscape. See {ref}`how-to-wsl-configure-landscape-beta`.

- **Ensure your firewall settings are configured appropriately**

   > See also: [Ubuntu Pro for WSL documentation on firewall requirements](https://documentation.ubuntu.com/wsl/latest/reference/firewall_requirements/)
    
    You may need to adjust your firewall settings to allow inbound and outbound traffic on Port 6554, or whichever port you’re routing traffic on if you’ve changed the port. Port 6554 is the default for `landscape-server-quickstart` installations.

 - **If your Landscape URL isn't registered with a public or private DNS, you may need to register it or update your Windows Hosts file**

    Your domain name won't resolve if it's not registered with DNS. If you plan to update your Windows Hosts file instead of registering the domain with DNS, it's recommended that you proceed with extreme caution and consult Microsoft's documentation first.
    
- **If you’re using a registration key, ensure that the registration key in the `LandscapeConfig` key matches the registration key in your Landscape account**
    
    If you're using a registration key, the registration key you use in your `LandscapeConfig` key must match exactly with the registration key in your Landscape account. Your registration key can be found in the **Account** tab on the web portal. 
    
- **If you have auto-registration enabled, check if your Windows machine is already listed as a computer in your Landscape account**
    
    Landscape has an auto-registration feature that allows you to register computers without manually approving each one. If you’re using a registration key and you have this feature enabled, your Windows machine won’t appear as a pending instance. Instead, it’ll auto-register and appear in your list of computers. For more information, see {ref}`how to auto-register new computers <howto-heading-client-autoregister>`.

- **Access the Ubuntu Pro for WSL logs**
    
   If you’ve completed the previous troubleshooting steps and your Windows machine still doesn’t appear as a pending computer in Landscape, you should review the Ubuntu Pro for WSL logs. To access those logs, see [Ubuntu Pro for WSL's guide on how to access the logs for debugging](https://documentation.ubuntu.com/wsl/latest/howto/06-access-the-logs/).

  Landscape won’t have awareness of the Windows host machine until it's a pending instance or auto-registered in your Landscape account. The Landscape logs won’t be helpful when troubleshooting this registration issue.

