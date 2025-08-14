(how-to-register-wsl-hosts)=
# How to set up Ubuntu Pro for WSL and register WSL hosts to Landscape

> See also: [Ubuntu Pro for WSL documentation](https://canonical-ubuntu-pro-for-wsl.readthedocs-hosted.com/en/latest/)

```{note}
Ubuntu Pro for WSL is **not available yet** for everyone in the Microsoft Store. It's currently in beta.
```

```{note}
If this is the first time you've installed Landscape, you can continue with this guide. If you've upgraded from Landscape 23.10 or earlier, you first need to configure it to enable WSL-related services. For more information, visit {ref}`how-to-wsl-configure-landscape-beta`.
```

This guide describes how to set up Ubuntu Pro for WSL and register new WSL hosts (Windows machines) to Landscape.

## Check prerequisites

```{note}
You must be running Windows 11 to use Ubuntu Pro for WSL.
```

To use the WSL-Landscape integration, you must have the following applications downloaded from the Microsoft Store:

- [Windows Subsystem for Linux](https://apps.microsoft.com/detail/9P9TQF7MRM4R)
- An Ubuntu application, such as [Ubuntu 24.04 LTS](https://apps.microsoft.com/detail/9nz3klhxdjp5?)

If you don't want to download your Ubuntu image from the Microsoft Store, you can manually specify a different image source instead. See {ref}`how-to-wsl-use-specific-image-source`.

Also, you must have WSL 2 installed instead of WSL 1. If you've just now installed WSL from the Microsoft store, then you've installed WSL 2 and can proceed to the next steps. If you've previously installed WSL and aren't sure if it's WSL 1 or WSL 2, run `wsl -l -v` in PowerShell or Command Prompt to get the version. If you have WSL 1, you need to upgrade to WSL 2. For more information, see [Microsoft's guide on upgrading from WSL 1 to WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2).

## Install and configure Ubuntu Pro for WSL

```{note}
The documentation here is for a future release of Landscape beta. Ubuntu Pro for WSL is **not available yet** for everyone in the Microsoft Store.
```

There are two ways to configure Ubuntu Pro for WSL for Ubuntu Pro and Landscape: via the Ubuntu Pro for WSL GUI or the Windows Registry.

### Using the GUI

From your Windows machine:

1. Install Ubuntu Pro for WSL from the Microsoft Store
1. Click **Start** when the installation is complete.
1. Click the arrow beside "Already have a token?"
1. Paste your Ubuntu Pro token in during the setup process and click **Confirm**. You can get your token from your [Ubuntu Pro account dashboard](https://ubuntu.com/pro/dashboard).
    - If you don't have an Ubuntu Pro subscription yet, [register for a new Ubuntu Pro subscription](https://ubuntu.com/pro/subscribe) to get a token. You can register up to 5 machines for free with the personal subscription option.

You'll then have to complete your Landscape configuration. This can be done with either of the following options:

- For quick setups:
    - Select **Quick Setup**
    - Enter the FQDN of your server in the **Landscape FQDN** field
    - Click **Continue**
- For custom setups:
    - Select **Custom Configuration**
    - Enter the path for your client configuration file. For more information on the client configuration file, see [Ubuntu Pro for WSL's documentation on the client config](https://documentation.ubuntu.com/wsl/en/latest/reference/landscape_config/) or the following section in this guide.

Once Landscape is successfully configured, you’ll receive confirmation on the next page that your Ubuntu Pro subscription is active and you can close the Ubuntu Pro for WSL window.

### Using the Windows Registry

From your Windows machine:

1. Install Ubuntu Pro for WSL from the Microsoft Store
1. Download Landscape Server's public certificate and save it to your Windows machine. If you used the Landscape Quickstart installation, the auto-generated self-signed certificate can be found at `/etc/ssl/certs/landscape_server.pem`.
1. Open the Registry Editor in your Windows machine
    - To open the Registry Editor, either press the `Windows key + R` and type `regedit` or search “Registry Editor” in the taskbar and select it from the results.
1. Go to `HKEY_CURRENT_USER\Software\Canonical\UbuntuPro`.
   - This key won't exist until you've run Ubuntu Pro for WSL at least once. If you don't run Ubuntu Pro for WSL, you'll need to create the key and values yourself. For more information, see [Microsoft's documentation on Windows registry information for advanced users](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/windows-registry-advanced-users).
1. Open the `UbuntuProToken` key and add your Ubuntu Pro token with Right Click > **Modify**, then write your token in the **Value data** field. You can get your token from your [Ubuntu Pro dashboard](https://ubuntu.com/pro/dashboard).
1. Open the `LandscapeConfig` key and add the following lines in the **Value data** field:
    
    ```bash
    [host]
    url = {HOST_URL:PORT}
    
    [client]
    account_name = {ACCOUNT_NAME}
    registration_key = {REGISTRATION_KEY}
    url = {CLIENT_URL}
    log_level = debug
    ping_url = {PING_URL}
    ssl_public_key = {SSL_CERT}
    ```
    
    Replace these values:
    
    - `{HOST_URL:PORT}`: The URL of your Landscape account (without `https://`) followed by a colon (`:`) and the port number. Port 6554 is the default for Landscape Quickstart installations. For example, `landscape-server.domain.com:6554`.
    - `{ACCOUNT_NAME}`: The Landscape account name this computer belongs to. This is located on your organization’s home page in the Landscape web portal. For self-hosted Landscape accounts, the account name defaults to “standalone”.
    - `{REGISTRATION_KEY}`: An optional account-wide key used to register new clients. There is no key defined by default, but one can be set in your Landscape account settings. If you have a registration key, it's located on your organization’s home page in your Landscape web portal. If you don’t have a registration key, leave this field blank.
    - `{CLIENT_URL}`: The main URL for the Landscape Server to connect this client to. This defaults to the URL of your Landscape account suffixed with `/message-system`, although you may be using a different URL. For example, `https://landscape-server.domain.com/message-system`.
    - `{PING_URL}`: The ping URL you want this client to report to. This defaults to the URL of your Landscape account suffixed with `/ping`, although you may be using a different URL. For example, `http://landscape-server.domain.com/ping`. Your ping URL use HTTP (not HTTPS).
   - `{SSL_CERT}`: The location of Landscape Server's public certificate on your Windows machine. If you saved the certificate to the user `Downloads` directory, this value would similar to `C:\Users\user\Downloads\landscape_server.pem`.
    

    Your final `LandscapeConfig` key should be similar to the following example:
    
    ```bash
    [host]
    url = landscape-server.domain.com:6554
    
    [client]
    account_name = standalone
    url = https://landscape-server.domain.com/message-system
    log_level = debug
    ping_url = http://landscape-server.domain.com/ping
    ssl_public_key = C:\Users\user\Downloads\landscape_server.pem
    ```
    
## Finalize the Windows machine registration

To finish registering your WSL host to Landscape:

1. Log in to your Landscape web portal
2. Wait for your Windows machine to appear in your Landscape account. This can take a few minutes, and you may need to refresh the page.
3. Accept the pending computer
    - To accept it, tick the checkbox near its name, assign it to an access group, and click **Accept**

That's it! Your Windows host machine is now registered in Landscape. To register WSL-Ubuntu instances, see {ref}`how-to-manage-wsl-instances`.

(howto-heading-register-wsl-host-troubleshoot)=
## (If necessary) Troubleshoot

> See also: [Ubuntu Pro for WSL's logs](https://documentation.ubuntu.com/wsl/en/latest/howto/06-access-the-logs/)

If your Windows host machine doesn’t appear as a pending computer in your Landscape account:

- **Ensure you’re logged in to the same Landscape account that your WSL host is registering with**
    
    You must be logged into the Landscape account associated your WSL host registration.
    
- **Wait a few minutes and refresh your Landscape account**
    
    The registration process won’t be immediate; it may take a few minutes. If you haven’t already, wait a few minutes and try refreshing the page to see if your Windows machine appears as a pending computer in your Landscape account.
    
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

- **Ensure your firewall settings are configured appropriately**

   > See also: [Ubuntu Pro for WSL documentation on firewall requirements](https://canonical-ubuntu-pro-for-wsl.readthedocs-hosted.com/en/latest/reference/firewall_requirements/)
    
    You may need to adjust your firewall settings to allow inbound and outbound traffic on Port 6554, or whichever port you’re routing traffic on if you’ve changed the port. Port 6554 is the default for `landscape-server-quickstart` installations.

 - **If your Landscape URL isn't registered with a public or private DNS, you may need to register it or update your Windows Hosts file**

    Your domain name won't resolve if it's not registered with DNS. If you plan to update your Windows Hosts file instead of registering the domain with DNS, it's recommended that you proceed with extreme caution and consult Microsoft's documentation first.
    
- **If you’re using a registration key, ensure that the registration key in the `LandscapeConfig` key matches the registration key in your Landscape account**
    
    If you're using a registration key, the registration key you use in your `LandscapeConfig` key must match exactly with the registration key in your Landscape account. Your registration key can be found in the **Account** tab on the web portal. 
    
- **If you have auto-registration enabled, check if your Windows machine is already listed as a computer in your Landscape account**
    
    Landscape has an auto-registration feature that allows you to register computers without manually approving each one. If you’re using a registration key and you have this feature enabled, your Windows machine won’t appear as a pending computer. Instead, it’ll auto-register and appear in your list of computers. For more information, see {ref}`how to auto-register new computers <howto-heading-client-autoregister>`.
    
- **Check that your Ubuntu Pro token was applied correctly**
    
    If you successfully completed the previous steps on activating Ubuntu Pro for WSL, your Ubuntu Pro token should be active. However, you can also check if it’s active in the Registry Editor. In `HKEY_CURRENT_USER\Software\Canonical\UbuntuPro`, there should be a key titled `UbuntuProToken` with your token inside. If this isn’t there, you can add these values in to the Registry Editor, or you can re-do the previous steps on installing and activating Ubuntu Pro for WSL.

- **Access the Ubuntu Pro for WSL logs**
    
   If you’ve completed the previous troubleshooting steps and your Windows machine still doesn’t appear as a pending computer in Landscape, you should review the Ubuntu Pro for WSL logs. To access those logs, see [Ubuntu Pro for WSL's guide on how to access the logs](https://documentation.ubuntu.com/wsl/en/latest/howto/06-access-the-logs/).

  Landscape won’t have awareness of the Windows host machine until it's a pending computer or auto-registered in your Landscape account. The Landscape logs won’t be helpful when troubleshooting this registration issue.

