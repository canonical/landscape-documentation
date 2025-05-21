(how-to-ubuntu-on-ubuntu-amazon-workspaces)=
# How to set up Ubuntu Amazon WorkSpaces on Landscape

> This guide is for users with [Amazon WorkSpaces](https://ubuntu.com/aws/workspaces) and [Ubuntu Pro](https://documentation.ubuntu.com/pro/) subscriptions.

You can use Landscape SaaS to centrally manage your Ubuntu WorkSpaces instances. Landscape SaaS is included with your Ubuntu Pro subscription.

If you're new to Landscape and want to learn more, see {ref}`what-is-landscape`.

## Prerequisites

You must have your Ubuntu WorkSpaces instances deployed before beginning this guide.

## Create your Ubuntu Pro account for Landscape SaaS

First, sign up for Landscape SaaS by visiting https://landscape.canonical.com/signup.

You can log in using your Ubuntu One account. If you don’t have an account, select *I don’t have an Ubuntu One account* and complete the required details.

After you're registered, you’ll receive a confirmation email to validate your address. Once validated, you’ll be redirected to the Landscape web portal.

## Log in to Landscape SaaS

```{note}
The instructions in this guide use Landscape's **classic** web portal. These steps still broadly apply to the newer web portal, which you can preview by clicking **New Web Portal** from the header in your Landscape account.
```

Once your account is set up, you can access Landscape SaaS at the following address: https://landscape.canonical.com/.

## Register your machines with Landscape

You need to register your machines with Landscape so they appear in your Landscape web portal. This involves installing the Landscape Client application on each Ubuntu WorkSpaces machine, and registering it to your Landscape SaaS account.

General instructions are provided here, but for more detailed information and advanced options, see our full documentation on {ref}`how-to-install-landscape-client` and {ref}`how-to-configure-landscape-client`.

### Step 1: Open the terminal

On the machine you want to register with Landscape, open a terminal window. Make sure you have the machine's password, as you'll need it later for `sudo` commands.

### Step 2: Update repositories

Ensure that your repositories are up-to-date:

```bash
sudo apt-get update
```

### Step 3: Install Landscape Client

Install Landscape Client on your machine:

```bash
sudo apt-get install landscape-client -y
```

### Step 4: Register your machine with Landscape

Use the following command to register your Ubuntu WorkSpaces machine in your Landscape account, replacing the following variables:

- `<MY_UBUNTU_WORKSPACE>`: The name you choose for this machine. For example, `dev_workstation`.
- `<ACCOUNT_NAME>`: Your account name. This can be found on the homepage of your Landscape portal.

```bash
sudo landscape-config --computer-title "<MY_UBUNTU_WORKSPACE>" --account-name "<ACCOUNT_NAME>"
```

You'll be prompted to answer some questions during registration, including a registration key for automatic enrollment, proxy configuration, and user/group settings for script execution. You can leave the settings as default, unless you have specific requirements.

This step can also be scripted in a single command, and machines can be auto-registered. You can also pass `--silent` to use the default settings and not prompt for additional information. See {ref}`how-to-configure-landscape-client` for more details.

### Step 5: Accept the new machine in Landscape

Once the Landscape client configuration is complete, go back into the Landscape web portal to accept the new machine:

1. Click the arrow icon in the header. You should have a notification that a pending computer needs attention.
1. Click that notification
1. Select your machine
1. Click **Accept**

Now, your machine is enrolled in Landscape. If you click the **Computers** page from the header, you'll see your machine in the list of all enrolled machines.

## (Optional) Enable script execution

If you need to run scripts across multiple machines, you can do this remotely from the Landscape web portal.

If you haven't already enabled this feature, you can enable it manually by running the following command on each instance:

```bash
sudo landscape-config --include-manager-plugins=ScriptExecution --script-users=root,landscape,nobody
```

And then restart your client machine:

```bash
sudo service landscape-client restart
```

For full details on setting up script execution, see {ref}`howto-heading-client-enable-script-execution`.

## Final notes

For any questions about [Ubuntu on AWS](https://documentation.ubuntu.com/aws/), see their [contact page](https://ubuntu.com/aws#get-in-touch).