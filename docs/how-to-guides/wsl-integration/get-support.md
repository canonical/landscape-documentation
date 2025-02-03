(how-to-guides-wsl-integration-get-support)=
# How to get support for WSL machines that connect to Landscape

This document describes multiple ways to get support for Windows Subsystem for Linux (WSL) machines that connect to Landscape and troubleshoot some basic issues.

## Check minimum requirements

The following minimum requirements are needed to register WSL machines with Landscape:

- A machine that meets all WSL requirements. For more information, visit [Microsoft’s WSL documentation](https://learn.microsoft.com/en-us/windows/wsl/install).
- Self-hosted Landscape Server Beta in a public cloud or on premise with the following specifications:
    - **Minimum:** A dual-core 2 GHz processor, 4 GB of RAM, and 20 GB of disk space
    - **Recommended:** 4 CPU cores, 8 GB of RAM, and 100 GB of disk space

If you don't meet these minimum requirements, you will encounter issues when attempting to register WSL machines with Landscape.

## Troubleshoot basic issues and misconfigurations

You will encounter issues with the following scenarios.

- **Attempting to use WSL 1**
    
    You must use WSL 2 to register and use WSL machines with Landscape. For more information on the difference between WSL 1 and WSL 2, visit [Microsoft’s guide on comparing WSL 1 and WSL 2](https://learn.microsoft.com/en-us/windows/wsl/compare-versions). To learn how to upgrade from WSL 1 to WSL 2, visit [Microsoft’s guide on upgrading from WSL 1 to WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2).
    
- **Attempting to use Landscape SaaS**
    
    WSL is not supported for Landscape SaaS at this time. You must have Landscape Server Beta self-hosted in a public cloud or on premise to use WSL with Landscape. 
    
- **Attempting to use Landscape Server 23.10 Stable or earlier**
    
    WSL is not supported for Landscape Server 23.10 Stable or earlier. You must have Landscape Server Beta self-hosted in a public cloud or on premise to use WSL with Landscape. To install Landscape Server with the latest source code from the Landscape Beta PPA, visit [how to install Landscape Server in quickstart mode.](https://ubuntu.com/landscape/docs/quickstart-deployment)
    
- **Attempting to use Landscape Client 23.10 Stable or earlier**
    
    WSL is not supported for Landscape Client 23.10 Stable or earlier. You must have the Landscape Beta PPA to install Landscape Client Beta. To install Landscape Client with the latest source code from the Landscape Beta PPA, visit [how to install Landscape Client](https://ubuntu.com/landscape/docs/install-landscape-client).

To troubleshoot issues with your Windows host registration, see the [troubleshooting guide for registering WSL hosts with Landscape](https://ubuntu.com/landscape/docs/register-wsl-hosts-to-landscape#heading--troubleshoot).
    
## Contact Support

Ubuntu Pro customers can receive support through [Canonical’s Support portal](https://support.canonical.com/). Before contacting Support, you should know the versions of all your major software components. This includes:

- Windows version
- WSL version
    - You can get this by running `wsl -l -v` in PowerShell
- Landscape Client version
    - You can get this by running `apt policy landscape-client` in the command line.
- Landscape Server version
    - You can get this by adding `/about` to the URL of your Landscape account. For example, `https://landscape-server.domain.com/about`.

