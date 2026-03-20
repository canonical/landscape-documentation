---
myst:
  html_meta:
    description: "Explore how to install and set up Landscape Server with quickstart, manual, Juju, LXD, cloud providers, FIPS, airgapped, and client configuration methods."
---

(how-to-guides-landscape-installation-and-set-up-index)=
# Landscape installation and set-up

Install and configure Landscape Server and Landscape Client using various deployment methods. Choose the installation approach that best fits your infrastructure and requirements.

## Cloud providers

Deploy Landscape Server on major cloud platforms including Google Cloud and Microsoft Azure.

```{toctree}
:titlesonly:
:maxdepth: 2

cloud-providers/index
```

## Landscape Server installation methods

### Quick setups for testing or SaaS

Get started quickly with simplified installation methods for SaaS or testing self-hosted environments.

```{toctree}
:titlesonly:
:maxdepth: 1

Quickstart installation <quickstart-installation>
SaaS account <create-saas-account>
```

### Production deployments

Install Landscape Server for production use with manual configuration or Juju-managed deployments.

```{toctree}
:titlesonly:
:maxdepth: 1

Manual installation <manual-installation>
Juju installation <juju-installation>
Juju HA installation <juju-ha-installation>
Install in a LXD container <install-in-a-lxd-container>
```

### Specialized environments

Deploy Landscape in environments with specific compliance or connectivity requirements.

```{toctree}
:titlesonly:
:maxdepth: 1

Install on FIPS-compliant machines <install-on-fips-compliant-machines>
Install in a DISA STIG compliant environment <disa-stig>
Install in an airgapped environment <install-landscape-in-an-air-gapped-or-offline-environment>
```

## Landscape Client

Install, register, and configure Landscape Client on machines you want to manage.

```{toctree}
:titlesonly:
:maxdepth: 1

Install Landscape Client <install-landscape-client>
Configure Landscape Client <configure-landscape-client>
```

## Additional service configuration

Configure supporting services for your Landscape deployment.

```{toctree}
:titlesonly:
:maxdepth: 1

Configure RabbitMQ <configure-rabbitmq>
Configure Postfix <configure-postfix>
```
