(explanation-landscape-self-hosted-landscape)=
# Self-hosted Landscape

Self-hosted Landscape is the standalone edition of Landscape that you can install on premises or in a public cloud.

Feature enhancements are released in our scheduled release windows which occur twice per year, typically in April and October. Security patches and bug fixes will be provided outside of our scheduled release windows at the earliest possible opportunity.

The following table applies to [Quickstart](/how-to-guides/landscape-installation-and-set-up/quickstart-installation) and [Manual](/how-to-guides/landscape-installation-and-set-up/manual-installation) installations of Landscape Server.

| **Major version**                | **Release date** | **Standard Support** | **Expanded security maintenance (ESM)** | **Installs on Ubuntu LTS version**  |
| ----------------------           | ---------------- | ------------------- | ------------------- | ---------------------  |
| [24.04 LTS](/reference/release-notes/24-04-lts-release-notes)     | 2024-Apr   | **2029-Apr**     |  **2036-Apr**   | 22.04 LTS or 24.04 LTS |
| [24.10](/reference/release-notes/24-10-release-notes) | 2024-Nov | **2025-Apr** | No ESM | 22.04 LTS or 24.04 LTS
| [23.03](/reference/release-notes/23-03-release-notes)  | 2023-Mar         | **2025-Apr**        | **2030-Apr**        | 20.04 LTS or 22.04 LTS             |

The [Landscape Server charm](https://charmhub.io/landscape-server) typically follows the same release cycles, although there can be some differences.

```{note}
For the most up-to-date information on the charm and what versions of Ubuntu the charms support, visit [Charmhub](https://charmhub.io/).
```

Landscape 23.03 manages all versions of Ubuntu 16.04 LTS (Xenial Xerus) onwards. Landscape 23.03 also manages two future Ubuntu releases, which includes the following interim release (Ubuntu 23.10) and LTS release (Ubuntu 24.04).

Landscape 24.04 LTS manages the previous four Ubuntu LTS releases, from Ubuntu 16.04 LTS (Xenial Xerus) onwards. Landscape 24.04 LTS will also manage future Ubuntu releases, including Ubuntu 26.04 LTS, and interim releases Ubuntu 24.10, Ubuntu 25.04, and Ubuntu 25.10.

Compatibility beyond this range to older and newer versions of Ubuntu is on a best effort basis and is not guaranteed.

```{note}
Landscape Client is available in the `main` repository in all Ubuntu releases, and is published independently of the self-hosted Landscape Server releases. For information on installing Landscape Client, see [how to install Landscape Client](/how-to-guides/landscape-installation-and-set-up/install-landscape-client).
```

## Landscape PPAs

You can access self-hosted Landscape from one of our PPAs:

- **Long Term Support (LTS)**: Our LTS PPA that comes with 10 years of support and aligns with the Ubuntu LTS release cadence. This is our most stable PPA and includes five point release updates after the initial release. These updates include bug fixes and security patches. We recommend using LTS versions for production deployments. New LTS releases are released every two years, usually in April of each even year, and the point releases are typically published in August and February of each year.
- **Latest Stable**: A stable rolling release for users who need access to the latest features. The latest stable PPA is suitable for production, but each version is only supported until the next latest stable release. Users on this PPA should always upgrade to the most recent release for continuous support. New latest stable versions are released every six months, usually around October and April.
- **Beta**: The newest beta features, mainly used for testing and development. You can explore the latest features here, but stability is not guaranteed. The beta PPA should not be used for production deployments.

## Installation

Self-hosted Landscape consists of two parts:

* **Database server**
* **Application server**

Depending on your deployment method, these may exist on the same machine or different machines. Here is how you can get started:

### Quickstart

* **[Quickstart](/how-to-guides/landscape-installation-and-set-up/quickstart-installation)**, for when you don't have Juju but quickly want to check out self-hosted Landscape. Not recommended for production environments when having more than 500 clients.

### Juju deployed

* **[Juju deployed](/how-to-guides/landscape-installation-and-set-up/juju-installation)** for a truly scalable deployment.

### Manual installation

* **[Manual installation](/how-to-guides/landscape-installation-and-set-up/manual-installation)**: for when you don't have a suitable Juju environment but need a scalable deployment.

## Installation requirements

### System Requirements

The bare minimum compute power required to run Landscape is 4 GB of RAM and 20 GB of disk space.
- The `landscape-server-quickstart` package requires 2 vCPUs or one dual core processor
- The Juju-based installation can be deployed on a single vCPU, but a minimum of 2 is recommended.

Our recommendation is to allocate 8 vCPUs or cores, 16GB RAM, and 512 GB of storage. When performing a manual or Juju based installation to address high availability requirements, each machine including the Juju controller should be allocated this many resources for the best outcome. If Landscape will be responsible for repository mirroring, it is advisable to mount an additional 2 TB of storage to the machine running the Landscape Server software.

One machine with these specifications will run the landscape-server-quickstart package. When using Juju or manually installing across multiple machines, none of the machines should be configured below these baseline compute power specifications.

The operating system to run Landscape Server and its dependencies are Ubuntu Server 20.04 LTS or 22.04 LTS on amd64, arm64, s390x, or ppc64el CPU architectures.

### Network access

Any machines you manage with Landscape should be able to access your Landscape installation over network ports 80/TCP (HTTP) and 443/TCP (HTTPS). You can optionally open port 22/TCP (SSH) as well for maintenance of your Landscape installation.

The machine(s) running as the application server will also need the following external network access:

 * HTTPS access to `usn.ubuntu.com` in order to download the USN database and detect security updates. Without this, the available updates won't be distinguished between security related and regular updates
 * HTTP access to the public Ubuntu archives and `changelogs.ubuntu.com`, in order to update the hash-id-database files and detect new distribution releases. Without this, the release upgrade feature won't work
 * HTTPS access to `landscape.canonical.com` in order to query for available self-hosted Landscape releases. If this access is not given, the only drawback is that Landscape won't display a note about the available releases in the account page.

If this external network access is unavailable, Canonical's professional services include assistance with setting up Landscape in a fully air-gapped environment.

## Unsupported Versions
| **major version**                | **Release date** | **Support expired on** | **Version of Ubuntu**  |
| ----------------------           | ---------------- | ------------------------ | ---------------------  |
| [23.10](/reference/release-notes/23-10-release-notes)      | 2023-Oct    | **2024-Apr**     | 20.04 LTS or 22.04 LTS |
| [19.10](/reference/release-notes/older-release-notes/19-10-release-notes)  | 2019-Oct         | **2023-May-31**        |  18.04 LTS              |
| [19.01](/reference/release-notes/older-release-notes/19-01-release-notes)  | 2019-Jan         | **2020-Jan**             | 18.04 LTS              |
| [18.03](/reference/release-notes/older-release-notes/18-03-release-notes)  | 2018-Jun         | **2019-Jun**             | 16.04 LTS or 18.04 LTS |
| [17.03](/reference/release-notes/older-release-notes/17-03-release-notes)  | 2017-Mar         | **2019-Mar**             | 16.04 LTS              |
| [16.06](/reference/release-notes/older-release-notes/16-06-release-notes)  | 2016-Jul         | **2017-Dec**             | 14.04 LTS or 16.04 LTS |
| [16.03](/reference/release-notes/older-release-notes/16-03-release-notes)  | 2016-Apr         | **2017-Apr**             | 14.04 LTS              |

