---
myst:
  html_meta:
    description: "Upgrade Landscape Server to 26.04 LTS from Ubuntu 22.04, 24.04 or 26.04. Install additional outbox and repository mirroring services as snaps.
---

(how-to-upgrade-to-26-04-lts)=
# How to upgrade to Landscape Server 26.04 LTS

```{important}
If you are using repository mirroring in your Landscape deployment, you should not attempt to upgrade to 26.04 LTS at this time. A migration guide for bringing over repository mirrors from 24.04 LTS to 26.04 LTS will be published at a later date.
```

To upgrade your self-hosted Landscape server to 26.04 LTS, you should first follow the basic upgrade instructions. See {ref}`how-to-upgrade`.

Note that you must be running Ubuntu 26.04 LTS Resolute Raccoon, 24.04 Noble Numbat, or 22.04 Jammy Jellyfish to upgrade to Landscape 26.04 LTS.

## Additional upgrade steps

After you’ve completed the basic upgrade instructions, you need to make some additional manual changes to finish your upgrade.

### Install the outbox Snap

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


The `landscape-debarchive` snap is required for repository mirroring from Landscape 26.04 LTS onwards. Install the `landscape-debarchive` snap on the same machine as your Landscape Server installation.

...

### Enable hostagent services (optional)

The hostagent services (`landscape-hostagent-consumer` and `landscape-hostagent-messenger`) are required to manage WSL instances via Ubuntu Pro for WSL. See [the hostagent_consumer section](/reference/config/service-conf.md/#the-hostagent-consumer-section) and [the hostagent_messenger section](/reference/config/service-conf.md/#the-hostagent-messenger-section) if you'd like to configure these services. If not configured, these services will fail to start, but all Landscape activities unrelated to WSL will still function properly.
