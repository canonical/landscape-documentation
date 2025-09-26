(explanation-licenses)=
# Landscape licenses

Landscape's main licensing mechanism is [Ubuntu Pro](https://ubuntu.com/pro). For Landscape SaaS accounts, the Ubuntu Pro license is already included in your subscription. You can also get a free Landscape SaaS account with Ubuntu Pro, which allows you to manage up to 5 machines for free. Most self-hosted Landscape accounts also use Ubuntu Pro.

For more information on Ubuntu Pro subscriptions, see the [Ubuntu Pro documentation](https://documentation.ubuntu.com/pro/), the [Ubuntu Pro Client documentation](https://documentation.ubuntu.com/pro-client/en/latest/) and {ref}`how-to-attach-ubuntu-pro`. The Ubuntu Pro Client is a command-line tool that helps you manage your Ubuntu Pro subscription.

Users with older versions of Landscape (or offline deployments) may use our legacy licensing mechanism. This older method involves manually downloading a `license.txt` file and applying it during the configuration process.

## Ubuntu Pro subscription

To use Ubuntu Pro with Landscape, you must be running Landscape Server version 23.03 or newer, and Landscape Client version 23.03 or newer. We have the following guides to help you get started:

1. {ref}`how-to-attach-ubuntu-pro`

2. {ref}`how-to-ubuntu-pro-enable-landscape`

After you've enabled Landscape, Landscape will detect your Pro entitlement via the Pro token and create a license for your machine.

## License.txt method

For the `license.txt` method, you get your first `license.txt` file from Canonical and manually upload the file to your server: `/etc/landscape/license.txt`. You’ll need to re-upload your license every time you renew, but you can download your new license in your Landscape account from `https://landscape.canonical.com/account/<account_id>/self-hosted`.

Note that new `license.txt` files become available on their start date. For renewal customers, the start date is the day after your old licenses expire.

## License types (classic web portal)

In the classic web portal, you can view the number of seats used per license type for each computer from the **Licenses** tab.

Here’s a summary of the different license types in Landscape and what they indicate:

- **Full:** License for a physical machine using Landscape SaaS
- **Virtual** or **Container:** License for a VM or container using Landscape SaaS
- **LDS:** License for a physical machine using self-hosted Landscape (self-hosted equivalent for Full)
- **LDS-Virtual:** License for a VM or container for Landscape self-hosted (self-hosted equivalent for Virtual)
- **Pro:** License for any client machine that's attached to Ubuntu Pro under an active contract (Physical or Virtual)
    * These don't require the `license.txt` file to be installed or have available seats on the Landscape server
    * Requires `landscape-client` 23.x or higher to report the Pro attachment information to the Landscape server

## New licensing states

For Landscape Server versions `25.10x` or greater there will be new licensing states. These states will allow for a user to register a client with Landscape without having any proper licensing mechanisms (e.g., Ubuntu Pro and `license.txt`). In this new unlicensed state client machine management will be limited, only allowing for operations to license that instance. This will allow for users to register client machines with Landscape, then attach Ubuntu Pro to desired client machines without needing to perform operation on each individual instance.

```{note}
This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts and the licensing management activities are unavailable for offline client deployments as well as snap and core devices.
```

### Client states

- **Unlicensed:** Computers that are not licensed and cannot be managed outside of license management operations.
- **Free Pro:** Computers that are licensed through an Ubuntu Pro Free Subscription.
- **Pro:** Computers that are licensed through Ubuntu Pro.
- **Legacy:** Computers that are licensed through a `license.txt` file.
