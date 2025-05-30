(getting-started-with-landscape)=
# Getting started with Landscape

> See also: {ref}`what-is-landscape`

This tutorial guides you through the process of installing Landscape Server on a Multipass virtual machine, configuring it, registering a client instance to Landscape, and running a script on your client instance. At the end, you'll also be guided through how to teardown your environment.

This tutorial should take about 45 minutes to complete.

## Prerequisites

There's a few things you'll need before starting this tutorial.

### Hardware

You'll need a workstation with enough disk space (25G) and memory (5G RAM) available to create two Multipass VMs: one with 20G disk space and 4G RAM for Landscape Server and one with 5G disk space and 1G RAM for Landscape Client. Your workstation will be called your "host machine" throughout this tutorial.

### Multipass

For this tutorial, Multipass needs to be installed on your host machine. To install Multipass, run the following in your terminal:

```bash
sudo snap install multipass
```

If you want to learn more about Multipass, see their [installation guide](https://canonical.com/multipass/docs/install-multipass) and [full documentation](https://canonical.com/multipass/docs).

### Ubuntu Pro token

You'll need an [Ubuntu Pro token](https://ubuntu.com/pro). Ubuntu Pro is free for up to 5 machines, and you can use the free version for this tutorial.

If you already have an Ubuntu Pro account, you can copy your token from your [Ubuntu Pro dashboard](https://ubuntu.com/pro/dashboard).

If you don't have an Ubuntu Pro account, first sign up for a [free personal Ubuntu Pro account](https://ubuntu.com/pro), then copy your token from your [Ubuntu Pro dashboard](https://ubuntu.com/pro/dashboard).

## Create the virtual machines

Now, let's create the Multipass virtual machines (VMs). From the command line, run:

```bash
multipass launch noble --cpus 2 --memory 4G --disk 20G --name tutorial-landscape-server-noble
multipass launch jammy --cpus 1 --memory 1G --disk 5G --name tutorial-landscape-client-jammy
```

This step will take a few minutes to complete, but you'll receive progress updates in the command line. These commands create two VMs total: one for your Landscape Server and one for Landscape Client. Your Landscape Server will run on Ubuntu 24.04 Noble Numbat (the VM named `tutorial-landscape-server-noble`) and Landscape Client will run on Ubuntu 22.04 Jammy Jellyfish (the VM named `tutorial-landscape-client-jammy`).

You'll need the IP address of the `tutorial-landscape-server-noble` VM later, so let's get it now. Run the following on your host machine:

```bash
multipass info tutorial-landscape-server-noble
```

Copy the IP address from the output, saving it somewhere you can access later.

The full output should be similar to the details below.

```text
Name:           tutorial-landscape-server-noble
State:          Running
Snapshots:      0
IPv4:           10.253.187.38
Release:        Ubuntu 24.04.1 LTS
Image hash:     28d2f9df3ac0 (Ubuntu 24.04 LTS)
CPU(s):         2
Load:           0.05 0.10 0.04
Disk usage:     1.8GiB out of 19.3GiB
Memory usage:   410.0MiB out of 3.8GiB
Mounts:         --
```

In this example output, the IP address for the `tutorial-landscape-server-noble` VM is `10.253.187.38`. We'll use that IP address throughout this tutorial, but the commands you run later should use the IP address that you just copied and saved.

## Install Landscape Server

Now, we're ready to install Landscape Server! We'll install Landscape Server on the `tutorial-landscape-server-noble` VM. To do this, open a shell on that VM:

```bash
multipass shell tutorial-landscape-server-noble
```

After running that command, the prompt should change to `ubuntu@tutorial-landscape-server-noble`. This means you're now in your `tutorial-landscape-server-noble` VM, and any commands will be run on that VM instead of your host machine.

Now install some required packages by running the command below:

```bash
sudo apt update && sudo apt install -y ca-certificates software-properties-common
```

Then add the `landscape/latest-stable` PPA to get access to the Landscape Server packages by running this command:

```bash
sudo add-apt-repository -y ppa:landscape/latest-stable
```

Your VM's package information will now be up-to-date and includes information about the Landscape packages. Run the command below to install Landscape Server on your VM:

```bash
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y landscape-server-quickstart
```

The installation will take some time during which you'll get a lot of output. You can ignore the output for this tutorial. For the full details on installing Landscape in quickstart mode, see {ref}`how-to-quickstart-installation`.

Once installation is complete, you can exit the shell by executing the `exit` command:

```bash
exit
```

You command prompt should go back to your standard host machine prompt after you exit the VM.

## Register the first Landscape administrator

From a browser on your host machine, navigate to `https://10.253.187.38` replacing the IP address in the URL with the one for your Landscape Server VM. Your browser will likely warn about a self-signed certificate. It's OK to accept the risk and continue in this case. Complete the form to create the first admin user for the `standalone` account. Once you complete the form, Landscape will automatically bootstrap your new account. Now you are logged in to Landscape and can start registering and managing client computers.

## Install and configure Landscape Client

From your host machine, open a shell to the `jammy` client VM.

```bash
multipass shell tutorial-landscape-client-jammy
```

Your prompt should now be `ubuntu@tutorial-landscape-client-jammy`.

Attach your pro token, replacing `your-pro-token` with your actual Pro token.

```bash
sudo pro attach your-pro-token
```

When completed, the output should include lines similar to the ones below (along with other lines that we are not displaying here):

```text
This machine is now attached to 'Ubuntu Pro - free personal subscription'

     Account: your_name@example.com
Subscription: Ubuntu Pro - free personal subscription
```

Next, get the server's public SSL certificate and save it where `landscape-client` can use it when it needs to make HTTPS requests to your Landscape Server. Replace the IP address with the one for your Landscape Server VM, but keep the `:443` port.

```bash
echo | openssl s_client -connect 10.253.187.38:443 | openssl x509 | sudo tee /etc/landscape/server.pem
```

Now you'll install Landscape Client.

```bash
sudo apt update && sudo apt install -y landscape-client
```

Edit the `/etc/landscape/client.conf` file to match the contents below. Be sure to replace the IP address in both `url` and `ping_url` with the one for your Landscape Server VM.

```ini
[client]
log_level = info
url = https://10.253.187.38/message-system
ping_url = http://10.253.187.38/ping
data_path = /var/lib/landscape/client
ssl_public_key = /etc/landscape/server.pem
account_name = standalone
computer_title = tutorial-landscape-client-jammy
include_manager_plugins = ScriptExecution
script_users = landscape,ubuntu
```

If you're not sure how to edit the file, you can use `nano` to do so.

```bash
sudo nano /etc/landscape/client.conf
```

Change the file as needed and press `CTRL-O` followed by `ENTER` to save the file and `CTRL-X` to exit.

Next, send a registration request to Landscape Server.

```bash
sudo landscape-config --silent
```

You should see a message indicating that the registration message was successfully sent to Landscape Server. If you get a message indicating that client was unable to connect to the server, double-check that you downloaded the server's certificate to the `/etc/landscape/` directory and that the IP address in the `/etc/landscape/client.conf` file is correct.

You can now exit your Jammy VM and return to your host machine.

```bash
exit
```

Go to your Landscape Server UI in your browser and click the arrow icon in the header. You should have a notification that a pending computer needs attention. Click that notification, select your computer, and click **Accept**.

## Run a script

From the **{spellexception}`Organisation`** home page in the Landscape web portal, click on the **Scripts** tab. Click **Add script** to create a script with the following contents to be run as the `ubuntu` user. Give it the name `Hello World` and save it.

```bash
#!/bin/bash
echo "Hello, World!" > /home/ubuntu/hello
```

From the **Computers** page, select your computer and then click the **Scripts** tab. Select the `Hello World` script and click **Next**. You can leave all the other defaults, then click **Run** to create an activity to run the script on your Jammy VM.

Once the activity succeeds, the status of your activity in the web portal will change to "1 activity finished successfully". You can check the file was created by opening a shell on your Jammy VM.

```bash
multipass shell tutorial-landscape-client-jammy
```

The directory listing should show the file `hello` in the `ubuntu` user's home directory.

```bash
ls -l
```

And the contents should be `Hello, World!`.

```bash
cat hello
```

After you've confirmed the file exists on your VM, you can return to your host machine:

```bash
exit
```

## Cleanup

Congratulations! You now have successfully installed Landscape Server on a Multipass VM, registered another Multipass VM running Landscape Client, and executed a script on that VM. Feel free to explore the other management features that Landscape Server has to offer.

When you're done, don't forget to remove the Multipass VMs from your host machine:

```bash
multipass delete tutorial-landscape-server-noble
multipass delete tutorial-landscape-client-jammy
multipass purge
```
