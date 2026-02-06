(how-to-ubuntu-pro-enable-landscape)=
# How to enable Landscape in the Ubuntu Pro Client

> See also: [Ubuntu Pro Client documentation](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/)

```{note}
You must be running Landscape client 23.02 or higher and Ubuntu 24.04 LTS (Noble) to enable Landscape with Ubuntu Pro. For more information, see the [Ubuntu Pro](https://documentation.ubuntu.com/pro/) and [Ubuntu Pro Client](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/) documentation.
```

If you have an Ubuntu Pro subscription, you can register a machine with Landscape via the `pro enable landscape` command. You can register interactively for convenience, or non-interactively which is useful for hands-off automation.

To register a machine, you'll need (at a minimum) your Landscape account name and a name for the machine you're registering. If you're not using Landscape SaaS, then you'll also need the URL of your hosted Landscape server.

## Attach your Pro subscription

If you haven't attached your Pro subscription (token), you need to attach it before moving on. See {ref}`how-to-attach-ubuntu-pro`.

## Enable interactively

To register your machine by interactively providing your Landscape account details at the CLI, run:

```bash
sudo pro enable landscape
```

This command will install `landscape-client` and start up an interactive wizard to complete the Landscape registration for the machine.

## Enable non-interactively

If you know the details of your Landscape setup then you can register a machine without using the wizard. Under the hood, ``pro`` installs and executes `landscape-config`, so you can pass any [parameters supported by](https://manpages.ubuntu.com/manpages/noble/en/man1/landscape-config.1.html) `landscape-config` to `pro enable landscape`.

You can use the `--assume-yes` flag to automatically accept the defaults for any un-provided parameters.

The command to enable Landscape takes the following format:

```bash
sudo pro enable landscape \
<pro enable parameters> \
-- \
<landscape-config parameters>
```

Which, when the parameters are added, should look something like this:

```bash
sudo pro enable landscape \
--assume-yes \
-- \
--account-name <my-account> \
--computer-title <my-computer>
```

That command will install `landscape-client` and pass the provided parameters after `--` to the `landscape-config` tool to automatically register the machine.

## What next?

After successfully running `pro enable landscape`, either interactively or non-interactively, an administrator of your Landscape account will need to go to the "Pending Computers" page in Landscape to accept the machine you just registered.

And that's it! The machine should now appear in the Landscape web portal for management.
