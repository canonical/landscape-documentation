(how-to-wsl-set-up-environment)=
# How to set up a Windows 11 environment to use WSL with Landscape

```{note}
If you already have a Windows machine with WSL 2 and Ubuntu installed, you don’t need to go through this guide.
```

This guide provides an example of how you could set up an environment to use WSL with Landscape. It’s intended for users who want to create a Windows VM, although later steps in the guide are still relevant for users who already have a Windows machine. 

## Step 1: Configure Ubuntu for virtualization with QEMU and libvirt

To enable libvirt-based virtualization on Ubuntu, run the following commands:

```bash
sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients -y
sudo adduser $(id -un) libvirt
sudo adduser $(id -un) kvm
sudo modprobe kvm
sudo apt-get install virt-manager -y
```

For those who want a more detailed understanding, here’s what each command does:

1. `sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients -y`: Installs QEMU, the libvirt daemon and libvirt clients. QEMU enables virtualization, and libvirt is a toolkit that manages the virtualization. The daemon and clients are part of the libvirt toolkit. The `-y` automatically answers “yes” to any prompts.
2. `sudo adduser $(id -un) libvirt` and `sudo adduser $(id -un) kvm`: Adds the current user (output of `$(id -un)`) to the `libvirt` and `kvm` groups.
3. `sudo modprobe kvm`: Loads the KVM module into the kernel.
4. `sudo apt-get install virt-manager -y`: Installs Virtual Machine Manager, which is the desktop software you’ll use to manage your Windows VM. The `-y` automatically answers “yes” to any prompts.

```{note}
A reboot typically isn’t required at this stage, but if you encounter issues, try rebooting your machine to ensure all changes get applied properly.
```

## Step 2: Create and provision a Windows 11 VM using an ISO

```{note}
This ISO disk image is unactivated and generally used for Windows testing and development purposes. There may be some differences between the ISO and a licensed copy of Windows. For more information, refer to Microsoft’s documentation.
```

To create and provision your Windows 11 VM using an ISO:

### Download and prepare the ISO file

1. Download the Windows 11 ISO file:
    
    ```bash
    wget https://software.download.prss.microsoft.com/dbazure/Win11_23H2_English_x64v2.iso
    ```
    
    The `wget` command downloads the file from Microsoft’s website.
    
2. Move the ISO file to the libvirt images directory:
    
    ```bash
    sudo mv Win11_23H2_English_x64v2.iso /var/lib/libvirt/images/
    ```
    

### Create and provision your VM

1. Get the model of your machine’s CPU:
    
    ```bash
    cpu_model=$(virsh capabilities | grep -oP '<model>\K[^<]+' | head -n 1)
    ```
    
    This is needed so the VM can emulate the same CPU model of your host machine.
    
2. Define the name of the VM:
    
    ```bash
    vm_name="win11-vm"
    ```
    
    This example assigns the name of your VM to `win11-vm`. You can change `win11-vm` to whatever name you want without changing any of the following steps.
    
3. Create and provision the VM:
    
    ```bash
    virt-install \
    --name "$vm_name" \
    --ram 8192 \
    --vcpus 4 \
    --cpu custom,model="$cpu_model" \
    --disk path=/var/lib/libvirt/images/$vm_name.qcow2,size=64 \
    --os-variant "win11" \
    --graphics spice \
    --cdrom /var/lib/libvirt/images/Win11_23H2_English_x64v2.iso \
    --boot hd,cdrom \
    --noautoconsole
    ```
    
    The settings here are suitable for most computers. However, you can adjust them based on the available resources on your computer. Landscape requires a bare minimum of 2 vCPU and 4 GB of RAM.
    
4. Stop the VM:
    
    ```bash
    virsh destroy $vm_name
    ```
    

### Configure your VM

1. Add the CPU to the VM configuration:
    
    ```bash
    sudo sed -i "/<\/cpu>/i \    <feature policy='require' name='vmx' />" "/etc/libvirt/qemu/${vm_name}.xml"
    ```
    
    The `sed` command edits the VM's XML configuration file to add the CPU feature. These changes to the XML file may not immediately be reflected in Virtual Machine Manager’s (VMM) XML editor. This is because VMM often maintains its own cache or database of VM configurations for performance reasons.
    
2. Restart the libvirt daemon:
    
    ```bash
    sudo systemctl restart libvirtd
    ```
    
3. Close and launch Virtual Machine Manager:
    
    ```bash
    kill $(pgrep virt-manager)
    virt-manager
    ```
    

### Launch the VM

1. Launch the VM:
    
    ```bash
    virsh start $vm_name && virt-viewer $vm_name
    ```
    
    Once the VM opens in the console, you’ll need to press a key to boot from CD. If the installer requests you eject the CD during or after the installation process, press **Enter** and continue. The ISO disk image will be considered ejected (or unmounted) when this warning appears, and no additional steps are needed.
    

## Step 3: Set up WSL, Ubuntu and helper utilities

### Install Chocolatey and necessary drivers

1. In your Windows 11 VM, open an elevated PowerShell window. Right click **PowerShell > Run as Administrator**
2. Set the execution policy to bypass PowerShell's default policy:
    
    ```bash
    Set-ExecutionPolicy Bypass -Scope Process -Force
    ```
    
    Bypassing PowerShell's execution policy should generally be used with caution. The execution policy is set to `Bypass` here to ensure the rest of the script runs smoothly. When you close your PowerShell window, the execution policy will return to the default.
    
3.  Install Chocolatey:
    
    ```bash
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    ```
    
4. Enable global confirmation for Chocolatey:
    
    ```bash
    choco feature enable -n allowGlobalConfirmation
    ```
    
    Enabling this feature tells Chocolatey to always confirm prompts that appear during the installation or upgrade process. This feature should generally be used with caution, but it’s useful here so you won’t need to manually confirm any prompts.
    
5. Install VM utilities:
    
    ```bash
    choco install spice-agent virtio-drivers
    ```
    
6. Restart your VM to apply these changes:
    
    ```bash
    Restart-Computer -Force
    ```
    

### Enable WSL and other necessary software

1. After your machine restarts, open an elevated PowerShell window again.
2. Enable Hyper-V, Virtual Machine Platform and WSL:
    
    ```bash
    Enable-WindowsOptionalFeature -FeatureName Microsoft-Hyper-V-All -Online -NoRestart
    Enable-WindowsOptionalFeature -FeatureName VirtualMachinePlatform -Online -NoRestart
    Enable-WindowsOptionalFeature -FeatureName Microsoft-Windows-Subsystem-Linux -Online -NoRestart
    ```
    
3. Restart your VM again to apply these changes:
    
    ```bash
    Restart-Computer -Force
    ```
    

### Install Ubuntu on WSL

1. After your VM restarts, open the Command Prompt.
2. Update WSL:
    
    ```bash
    wsl --update
    ```
    
3. Check your WSL version:
    
    ```bash
    wsl -l -v
    ```
    
    The output will be similar to:
    
    ```powershell
      NAME      STATE           VERSION
    * Ubuntu    Stopped         2
    ```
    
    Your WSL version number is in the `VERSION` column. You need to use WSL version 2, not version 1. If you’re on WSL 1, see [Microsoft’s guide on upgrading from WSL 1 to WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2).
    
4. If WSL is on version 2, install Ubuntu:
    
    ```bash
    wsl --install Ubuntu
    ```
    

Your environment is now set up to use WSL with Landscape. Next, you’ll need to install and configure Ubuntu Pro for WSL and register your Windows host machine. For these steps, see [how to set up Ubuntu Pro for WSL and register WSL hosts to Landscape](/how-to-guides/wsl-integration/register-wsl-hosts).

