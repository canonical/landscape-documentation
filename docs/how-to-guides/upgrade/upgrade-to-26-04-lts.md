---
myst:
  html_meta:
    description: "Upgrade Landscape Server to 26.04 LTS from Ubuntu 22.04, 24.04 or 26.04. Install additional outbox and repository mirroring services as snaps."
---

(how-to-upgrade-to-26-04-lts)=
# How to upgrade to Landscape Server 26.04 LTS
> <!-- TODO add when the release notes exist: See also: {ref}`reference-release-notes-26-04-lts` -->
```{important}
If you are using repository mirroring in your Landscape deployment, you should not attempt to upgrade to 26.04 LTS at this time. A migration guide for bringing over repository mirrors from 24.04 LTS to 26.04 LTS will be published at a later date.
```

```{important}
Quickstart installations and upgrades to Landscape 26.04 LTS are not supported on Ubuntu 26.04.
```

To upgrade your self-hosted Landscape server to 26.04 LTS, you should first follow the basic upgrade instructions. See {ref}`how-to-upgrade`.

Note that you must be running Ubuntu 26.04 LTS Resolute Raccoon, 24.04 Noble Numbat, or 22.04 Jammy Jellyfish to upgrade to Landscape 26.04 LTS.

## Service.conf migration

If you upgraded from a version prior to 25.10, your `service.conf` file will be migrated away from our deprecated naming system during the upgrade. A backup file from before the migration will be supplied in the same directory as your `service.conf`. Support for the deprecated config options is expected to be removed in the 26.10 release. See {ref}`reference-service-conf` for more details.

## Additional upgrade steps

After you’ve completed the basic upgrade instructions, you need to make some additional manual changes to finish your upgrade.

### Install the outbox snap

The `landscape-outbox` snap is critical to proper functioning of Landscape 26.04 LTS. Install the `landscape-outbox` snap on the same machine as your Landscape Server installation.

```bash
sudo snap install landscape-outbox
```

`landscape-outbox` is configured to work automatically with an existing Landscape Server by default. Check that the outbox is active and functioning properly.

```bash
sudo snap services landscape-outbox
sudo snap logs landscape-outbox
```

### Install the debarchive snap

The `landscape-debarchive` snap is required for repository mirroring from Landscape 26.04 LTS onwards. Follow the instructions in the [dedicated guide](/docs/how-to-guides/landscape-installation-and-setup/debarchive-repository-management.md)

### (WSL only) Enable hostagent services

These steps are only needed for WSL users. The hostagent services (`landscape-hostagent-consumer` and `landscape-hostagent-messenger`) are required to manage WSL instances via Ubuntu Pro for WSL. Follow the steps in [the hostagent_consumer section](/reference/config/service-conf.md/#the-hostagent-consumer-section) and [the hostagent_messenger section](/reference/config/service-conf.md/#the-hostagent-messenger-section) to configure these services. 

If you don't configure the hostagent services, you won't be able to use WSL with Landscape. Other activities unrelated to WSL will still function properly.

## Airgapped installations
If your deployment does not have internet access, you must carry the snaps into your airgapped environment as part of the 26.04 installation process.

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

Finally, verify the snaps are working properly according to the instructions above.
