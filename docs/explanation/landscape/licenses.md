(explanation-licenses)=
# Landscape licenses

Most Landscape accounts have a licensing mechanism; either Ubuntu Pro or a `license.txt` file. For Landscape SaaS accounts, the Ubuntu Pro license is already included in your subscription.

For self-hosted Landscape accounts, users running version 23.03 or newer typically have Ubuntu Pro subscriptions. Users with older versions (or offline deployments) may use our older licensing mechanism. This older method involves manually downloading a `license.txt` file and applying it during the configuration process.

For Ubuntu Pro subscriptions, see the [Ubuntu Pro documentation](https://documentation.ubuntu.com/pro/), the [Pro Client documentation](https://canonical-ubuntu-pro-client.readthedocs-hosted.com/en/latest/) and {ref}`how-to-attach-ubuntu-pro` to learn more.

For the `license.txt` method, you get your first `license.txt` file from Canonical and manually upload the file to your server: `/etc/landscape/license.txt`. You’ll need to re-upload your license every time you renew, but you can download your new license in your Landscape account from `https://landscape.canonical.com/account/<account_id>/self-hosted`.

Along with the `license.txt` method and Ubuntu Pro subscription, Landscape introduced a feature to accept clients without any valid licensing available in versions `25.10x` or newer. This will place clients into an `unlicensed` state where they are unable to be managed however, you can run an activity on the client to attach a Pro token, in turn licensing the instance. For more details see {ref}`license-management`.

```{note}
This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts and unavailable for offline deployments.
```

## License type

You can view the number of seats used per license type for each computer in the classic web portal. This functionality is in the **Licenses** tab.

Here’s a summary of the different license types in Landscape and what they indicate:

- **Full:** License for a physical machine using Landscape SaaS
- **Virtual** or **Container:** License for a VM or container using Landscape SaaS
- **LDS:** License for a physical machine using self-hosted Landscape (self-hosted equivalent for Full)
- **LDS-Virtual:** License for a VM or container for Landscape self-hosted (self-hosted equivalent for Virtual)
- **Pro:** License for any client machine that's attached to Ubuntu Pro under an active contract (Physical or Virtual)
    * These don't require the `license.txt` file to be installed or have available seats on the Landscape server
    * Requires `landscape-client` 23.x or higher to report the Pro attachment information to the Landscape server

