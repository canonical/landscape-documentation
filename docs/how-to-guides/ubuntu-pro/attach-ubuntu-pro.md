(how-to-attach-ubuntu-pro)=
# How to attach your Ubuntu Pro subscription

> See also: [Ubuntu Pro documentation](https://documentation.ubuntu.com/pro/)

```{note}
You must be running Landscape Server 23.03 or above and Landscape Client 23.02 or above to use the Ubuntu Pro Client to attach your Pro subscription to Landscape.
```

Attaching the [Ubuntu Pro](https://ubuntu.com/pro) subscription to Ubuntu brings you the [enterprise lifecycle](https://ubuntu.com/about/release-cycle), including [Linux kernel livepatching](https://ubuntu.com/security/livepatch), access to [FIPS-validated packages](https://ubuntu.com/security/fips), and [compliance with security profiles](https://ubuntu.com/security/certifications) such as CIS. This is not required for Ubuntu Pro instances [through public clouds](https://ubuntu.com/public-cloud) such as [AWS](https://ubuntu.com/aws/pro), [Azure](https://ubuntu.com/azure/pro) or [GCP](https://ubuntu.com/gcp/pro), since these are automatically attached from launch.

The following instructions explain how to attach your Ubuntu Pro subscription to your Ubuntu systems.

Note that Ubuntu Pro isn't just for enterprise customers. Anyone can get [a personal Ubuntu Pro subscription](https://ubuntu.com/pro) for free on up to 5 machines, or 50 if you are an [official Ubuntu Community member](https://wiki.ubuntu.com/Membership).

## Manual attachment per-client

### Step 1: Install the Ubuntu Pro Client

This step is necessary for Ubuntu Pro users or holders of personal subscriptions. If you are an Ubuntu Pro user through a public cloud offering, your subscription is already attached and you can skip these instructions.

First, make sure that you have the latest version of the Ubuntu Pro Client running. The package used to access the Pro Client (`pro`) is `ubuntu-advantage-tools`:

```bash
sudo apt update && sudo apt install ubuntu-advantage-tools
```

If you already have `ubuntu-advantage-tools` installed, this install command will upgrade the package to the latest version.

### Step 2: Attach your subscription

To attach your machine to a subscription, run the following command in your terminal:

```bash
sudo pro attach
```

You should see output like this, giving you a link and a code:

```bash
ubuntu@test:~$ sudo pro attach
Initiating attach operation...

Please sign in to your Ubuntu Pro account at this link:
https://ubuntu.com/pro/attach
And provide the following code: H31JIV
```

Open the link without closing your terminal window.

In the field that asks you to enter your code, copy and paste the code shown in the terminal. Then, choose which subscription you want to attach to. By default, the Free Personal Token will be selected.

If you have a paid subscription and want to attach to a different token, you may want to log in first so that your additional tokens will appear.

Once you have pasted your code and chosen the subscription you want to attach your machine to, click **Submit**.

The attach process will then continue in the terminal window, and you should eventually be presented with the following message:

```
Attaching the machine...
Enabling default service esm-apps
Updating Ubuntu Pro: ESM Apps package lists
Ubuntu Pro: ESM Apps enabled
Enabling default service esm-infra
Updating Ubuntu Pro: ESM Infra package lists
Ubuntu Pro: ESM Infra enabled
Enabling default service livepatch
Installing snapd snap
Installing canonical-livepatch snap
Canonical Livepatch enabled
This machine is now attached to 'Ubuntu Pro - free personal subscription'
```

When the machine has successfully been attached, you will also see a summary of which services are enabled and information about your subscription.

Available services can be enabled or disabled on the command line with `pro enable <service name>` and `pro disable <service name>` after you have attached.

## Automated attachment across multiple clients

### Step 1: Register clients with Landscape Server

```{note}
You must be running Landscape Server 25.10 or above and Landscape Client 25.10 or above to use automated attachment on clients for licensing.
```

This step will place clients into an unlicensed state where Landscape is aware of the instance to manage Ubuntu Pro.

### Step 2: Attach Ubuntu Pro to instances.

Navigate to the instances page and select instances you would like to attach an Ubuntu Pro subscription to. Select `Pro Services` in the UI and select `Attach Token`, then providing your token and selecting `Attach`. This will then send an activity to the client to attach Ubuntu Pro and on success will properly license the instance.

```{note}
This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts and the licensing management activities are unavailable for offline client deployments as well as snap and Core devices.
```


## Related topics

- [Ubuntu Pro Client documentation](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/)
- [Ubuntu Pro Client documentation on basic commands](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/tutorials/basic_commands.html)

