(explanation-licenses)=
# Landscape licenses

Most Landscape accounts have a licensing mechanism; either Ubuntu Pro or a `license.txt` file. For Landscape SaaS accounts, the Ubuntu Pro license is already included in your subscription.

For self-hosted Landscape accounts, users running version 23.03 or newer typically have Ubuntu Pro subscriptions. Users with older versions (or offline deployments) may use our older licensing mechanism. This older method involves manually downloading a `license.txt` file and applying it during the configuration process.

For Ubuntu Pro subscriptions, see the [Ubuntu Pro documentation](https://documentation.ubuntu.com/pro/), the [Pro Client documentation](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/) and {ref}`how-to-attach-ubuntu-pro` to learn more.

## License.txt Method

For the `license.txt` method, you get your first `license.txt` file from Canonical and manually upload the file to your server: `/etc/landscape/license.txt`. You’ll need to re-upload your license every time you renew, but you can download your new license in your Landscape account from `https://landscape.canonical.com/account/<account_id>/self-hosted`.

```{tip}
New `license.txt` files become available on their start date. For renewal customers, this is the day after your old licenses expire.
```

## Pro Client Method

For the Pro Client Method customers running Landscape version 23.03 or newer and landscape-client version 23.03 or newer you can use this method.

1. Ensure the Pro client is installed and attached to your Pro token on the system you wish to register to Landscape. See {ref}`how-to-attach-ubuntu-pro` for more details.

2. Then enable Landscape to initiate the registration process. See {ref}`how-to-ubuntu-pro-enable-landscape`.

3. Landscape will detect your Pro entitlement via the Pro token and create a license for your machine.


## Ubuntu Pro Licensing Method

Along with the `license.txt` method and Ubuntu Pro subscription, Landscape introduced a feature to accept clients without any valid licensing available in versions `25.10x` or newer. This will place clients into an `unlicensed` state where they are unable to be managed however, you can run an activity on the client to attach a Pro token, in turn licensing the instance. License management activities are only available for `landscape-client` versions `25.08.3` and newer. For more details see {ref}`license-management`.

```{note}
This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts and the licensing management activities are unavailable for offline client deployments as well as snap and core devices.
```

## Legacy License types

You can view the number of seats used per license type for each computer in the classic web portal. This functionality is in the **Licenses** tab.

Here’s a summary of the different license types in Landscape and what they indicate:

- **Full:** License for a physical machine using Landscape SaaS
- **Virtual** or **Container:** License for a VM or container using Landscape SaaS
- **LDS:** License for a physical machine using self-hosted Landscape (self-hosted equivalent for Full)
- **LDS-Virtual:** License for a VM or container for Landscape self-hosted (self-hosted equivalent for Virtual)
- **Pro:** License for any client machine that's attached to Ubuntu Pro under an active contract (Physical or Virtual)
    * These don't require the `license.txt` file to be installed or have available seats on the Landscape server
    * Requires `landscape-client` 23.x or higher to report the Pro attachment information to the Landscape server

## License types for Ubuntu Pro Licensing
- **Unlicensed:** Computers that are not licensed and cannot be managed outside of license management.
- **Free Pro:** Computers that are licensed through an Ubuntu Pro Free Subscription.
- **Pro:** Computers that are licensed through Ubuntu Pro.
- **Legacy:** Computers that are licensed through a `license.txt` file.

```{note}
A max of 5 Free Pro client machines are allowed per account or deployment.
```