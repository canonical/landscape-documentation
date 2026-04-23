---
myst:
  html_meta:
    description: "About self-hosted Landscape: deployment options, supported versions, PPAs, system requirements, and network access."
---

(explanation-about-self-hosted)=
# About self-hosted Landscape

Self-hosted Landscape is the standalone edition of Landscape that you install and operate yourself, either on-premises or in a public cloud. It gives you full control over the server, its data, and its network boundaries.

Feature enhancements are released in scheduled release windows twice per year, typically in April and October. Security patches and bug fixes are provided outside of these windows at the earliest possible opportunity.

For a comparison of all Landscape editions, see {ref}`explanation-about-landscape`.

## Deployment options

We offer three installation options for self-hosted Landscape Server:

| Method | Use case |
|--------|----------|
| {ref}`Quickstart <how-to-quickstart-installation>` | Single-machine deployment, evaluation, or smaller environments. Not recommended for production at scale. |
| {ref}`Juju <how-to-juju-installation>` | Scalable, production-grade deployment with high availability. |
| {ref}`Manual <how-to-manual-installation>` | Scalable deployment without Juju. Suitable when a Juju environment is not available. |

The Landscape Server charm follows similar release cycles to the other installation methods, although the timing can vary slightly. For more details and the charm-specific Ubuntu compatibility, see the [Landscape Server charm page on Charmhub](https://charmhub.io/landscape-server).

## Supported versions

Landscape Server has the following active or ESM-supported releases:

```{include} ../../reference/_includes/landscape-versions-table.md
```

LTS versions are released every two years and are recommended for production deployments. Latest stable versions are released every six months; each is supported only until the next release.

For more information, see {ref}`reference-supported-versions-and-ppas`.

## Package sources (PPAs)

Self-hosted Landscape is distributed via the following PPAs:

```{include} ../../reference/_includes/landscape-ppas-table.md
```

## Ubuntu compatibility

Each Landscape Server release manages a specific range of Ubuntu versions, including selected older LTS releases and upcoming LTS and interim releases. Compatibility outside the documented range is on a best-effort basis and not guaranteed.

For the version-by-version compatibility mapping, see {ref}`reference-supported-versions-and-ppas`.

Note that Landscape Client is available in the `main` repository for all Ubuntu releases and is published independently of Landscape Server. For information on installing Landscape Client, see {ref}`how-to-install-landscape-client`.

## System requirements

Landscape Server runs on Ubuntu Server (amd64, arm64, s390x, or ppc64el). Supported Ubuntu versions are listed in {ref}`reference-supported-versions-and-ppas`.

```{include} ../../reference/_includes/landscape-sizing-table.md
```

In high-availability or other multi-node deployments (Juju or manual), apply the recommended allocation to each machine, including the Juju controller.

(explanation-network-access)=
## Network access

Any client machines you manage with Landscape should be able to access your Landscape Server installation over network ports 80/TCP (HTTP) and 443/TCP (HTTPS). You can optionally open port 22/TCP (SSH) as well for maintenance of your Landscape Server.

Your Landscape Server will also need the following external network access:

- HTTPS access to `usn.ubuntu.com` in order to download the USN database and detect security updates. Without this, the available updates won't be distinguished between security related and regular updates
- HTTP access to the public Ubuntu archives and `changelogs.ubuntu.com`, in order to update the hash-id-database files and detect new distribution releases. Without this, the release upgrade feature won't work
- HTTPS access to `landscape.canonical.com` in order to query for available self-hosted Landscape releases. If this access is not given, the only drawback is that Landscape won't display a note about the available releases in the account page.
- HTTPS access to `ppa.launchpadcontent.net` if using the Landscape quickstart PPA
- HTTPS access to `contracts.canonical.com` for Ubuntu Pro authentication
- HTTPS access to `esm.ubuntu.com` for Ubuntu Pro APT package-based services
- HTTPS access to `livepatch.canonical.com` and `livepatch-files.canonical.com` for Livepatch
- HTTPS access to `ubuntu.com/security` for fetching security information
- HTTPS access to `api.snapcraft.io`, `dashboard.snapcraft.io`, `login.ubuntu.com`, and `*.snapcraftcontent.com` if using or downloading snaps (e.g., `landscape-api`)

If this external network access is unavailable, Canonical's professional services include assistance with setting up Landscape in a fully airgapped environment.
