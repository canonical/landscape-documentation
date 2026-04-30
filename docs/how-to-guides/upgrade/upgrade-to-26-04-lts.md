---
myst:
  html_meta:
    description: "Upgrade Landscape Server to 26.04 LTS from Ubuntu 22.04, 24.04, or 26.04. Install additional outbox and repository mirroring services as snaps."
---

(how-to-upgrade-to-26-04-lts)=
# How to upgrade to Landscape Server 26.04 LTS
<!-- TODO add when the release notes exist: See also: {ref}`reference-release-notes-26-04-lts` -->
You must be running Ubuntu 26.04 LTS Resolute Raccoon, 24.04 Noble Numbat, or 22.04 Jammy Jellyfish to upgrade to Landscape 26.04 LTS.

Note that Quickstart installations and upgrades to Landscape 26.04 LTS are not supported on Ubuntu 26.04. You must use Ubuntu 24.04 LTS or 22.04 LTS for Quickstart installations.

If you use repository management in your Landscape deployment, we recommend waiting to upgrade to 26.04 LTS until the 26.04.1 point release (expected August 2026). A migration guide for bringing over repository mirrors from 24.04 LTS to 26.04 LTS will be published before the point release.

## Begin your upgrade

To upgrade your self-hosted Landscape server to 26.04 LTS, you should first follow the basic upgrade instructions. See {ref}`how-to-upgrade`.

## Additional upgrade steps

After you’ve completed the basic upgrade instructions and have the updated `service.conf` file, you need to make some additional manual changes to finish your upgrade.

### Install the outbox snap

Install the `landscape-outbox` snap on the same machine as your Landscape Server installation.

```bash
sudo snap install landscape-outbox
```

`landscape-outbox` is configured to work automatically with an existing Landscape Server by default. Confirm that the snap service is running.

```bash
sudo snap services landscape-outbox
```

The output should show the `outbox` service as **active**:

```bash
Service                  Startup  Current  Notes
landscape-outbox.outbox  enabled  active   -
```

To view outbox logs, run:

```bash
sudo snap logs landscape-outbox -n 50
```

### Install the debarchive snap

<!-- TODO add when the release notes exist: The `landscape-debarchive` snap is required for repository management from Landscape 26.04 LTS onwards. Follow the instructions in the [dedicated guide](/docs/how-to-guides/landscape-installation-and-setup/debarchive-repository-management.md) -->

### (WSL only) Enable hostagent services

These steps are only needed for WSL users. The hostagent services (`landscape-hostagent-consumer` and `landscape-hostagent-messenger`) are required to manage WSL instances via Ubuntu Pro for WSL. See the configuration docs for the {ref}`hostagent consumer <hostagent-consumer-section>` and {ref}`hostagent messenger<hostagent-messenger-section>` to set up these services.

If you don't configure the hostagent services, you won't be able to use WSL with Landscape. Other activities unrelated to WSL will still function properly.

## Airgapped environments
If your deployment does not have internet access, you must carry the snaps into your airgapped environment as part of the 26.04 upgrade process.

First, in an environment with internet access, download the snaps.

```bash
snap download landscape-outbox
snap download landscape-debarchive --edge
```

For each snap, a `.snap` file and a `.assert` file will be produced.

After transferring the files to the airgapped environment, install the snaps.

```bash
sudo snap ack landscape-outbox_*.assert
sudo snap install landscape-outbox_*.snap
sudo snap ack landscape-debarchive_*.assert
sudo snap install landscape-debarchive_*.snap
```
