---
myst:
  html_meta:
    description: "Create a Landscape SaaS account with Ubuntu Pro. Sign up, attach your Pro subscription, and register your first client machines for cloud management."
---

(howto-create-saas-account)=
# How to create a SaaS account and register your first client

Landscape SaaS lets you manage your Ubuntu instances without having to maintain your own Landscape infrastructure. This guide describes how to create a Landscape SaaS account and register your first Landscape client machine.

Landscape is available with [Ubuntu Pro](https://ubuntu.com/pro) subscriptions. A free, personal Ubuntu Pro subscription allows you to manage up to 5 machines with Landscape SaaS. Paid Ubuntu Pro subscriptions include Landscape SaaS entitlement as well.

```{note}
If you want to join your organization's existing Landscape account rather than create a personal account, see the following section on [joining an existing account](#join-an-existing-landscape-account).
```

## Create your Landscape SaaS account

To create your new SaaS account:

1. Go to the [Landscape SaaS sign-up page](https://landscape.canonical.com/signup)

1. Log in using your Ubuntu One account. If you don't have an Ubuntu One account yet, create a new account on this page

    - For new accounts, you'll also receive a confirmation email and need to verify your email address

1. Once verified, you'll be redirected to the Landscape web portal. Provide your organization name and click **Sign up** to finish creating your SaaS account.

After account creation, you can access Landscape SaaS anytime at: [landscape.canonical.com](https://landscape.canonical.com)

## Attach your Ubuntu Pro subscription

> See also: {ref}`how-to-attach-ubuntu-pro`

You'll need an Ubuntu Pro subscription to register your first Landscape Client instance. You can get a free Ubuntu Pro subscriptions for up to 5 machines.

1. If you don't already have an Ubuntu Pro subscription, sign up for an [Ubuntu Pro account](https://ubuntu.com/pro).

1. Get your Ubuntu Pro token from your [Ubuntu Pro dashboard](https://ubuntu.com/pro/dashboard).

1. On the instance you want to manage with Landscape, open a terminal window and attach your Pro subscription:

   ```bash
   sudo pro attach <YOUR_PRO_TOKEN>
   ```

   Replace `<YOUR_PRO_TOKEN>` with your actual token from the Ubuntu Pro dashboard.

## Register your instance with Landscape SaaS

After attaching your Ubuntu Pro subscription, enable Landscape to install the client and register your machine.

1. Enable Landscape with Pro using the following command:

   ```bash
   sudo pro enable landscape
   ```

   This command will install Landscape Client and start an interactive configuration wizard.

1. Follow the prompts to configure your Landscape registration.

   - **Self-hosted Landscape**: Select **No** when asked if you're using your own self-hosted Landscape installation (you're using Landscape SaaS)
   - **Computer title**: Enter a descriptive name for this machine (e.g., `my-laptop`, `dev-server`)
   - **Account name**: Enter your account (organization) name. This is the organization name you provided earlier in the process, but you can also get it from your Landscape web portal homepage.
   - Additional configuration prompts will use sensible defaults for Landscape SaaS. You can press **Enter** to accept them.

1. Confirm that you want to request a new registration for that instance (computer) be selecting **Yes** when prompted

You'll receive confirmation that the registration request was sent successfully.

## Accept your new instance in the Landscape web portal

You need to accept the pending registration from the web portal:

1. Log into your [Landscape SaaS account](https://landscape.canonical.com)

1. Accept the pending computer using one of these methods:

   **In the new web portal:**
   - Click the **Pending** tile on the home page, or
   - Go to **Instances** > review pending instances > select your machine > click **Accept**

   **In the classic web portal:**
   - Click the **notifications** icon (arrow icon) in the header
   - Click the notification about a pending computer
   - Select your machine from the list > **Accept**

Your machine is now registered and will appear in your Landscape account.

## (Optional) Add secondary administrators

We recommend adding at least one secondary administrator to your Landscape account to ensure continuity of access. To invite additional administrators:

1. Navigate to:

    - New web portal: **Org. settings** > **Administrators** > **Invite administrator**
    - Classic web portal: **Administrators** > *Invite an administrator* section

1. Complete the form, entering the name and email address of the person you want to invite

Once you send the invite, the invited user will receive an email with subject line "You have been invited to the Landscape account [...]" from `noreply+landscape@canonical.com`. Note that the invitation email may land in the recipient's spam folder.

(join-an-existing-landscape-account)=
## Alternative: Join an existing Landscape account

If you want to join your organization's existing Landscape account, request access from an administrator on the account. You don't need to create a personal account.
