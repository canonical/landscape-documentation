---
myst:
  html_meta:
    description: "Explore Landscape Server charm integration compatibility with HAProxy, Charmed PostgreSQL, and RabbitMQ Server charms for Juju deployments."
---

(explanation-charm-compatibility)=

# Landscape Server charm integration compatibility

The [Landscape Server charm](https://charmhub.io/landscape-server) requires integration with the following charms, depending on the version:

**All versions:**
- `postgresql`
- `rabbitmq-server`

**Landscape 26.04 LTS beta+:**
- A TLS certificates provider (e.g., `self-signed-certificates`, `lego`)

**Before Landscape 26.04:**
- `haproxy`

For a recommended charm bundle configuration and more information about deploying Landscape Server with Juju, see {ref}`how-to-juju-installation` and {ref}`how-to-juju-ha-installation`.

Compatibility with a Landscape Server charm revision is limited to specific revisions and channels of the required charms. Incompatibility can occur if the charm's base (e.g., `ubuntu@24.04`), architecture (e.g., `amd64`), or interfaces change.

```{tip}
Learn more about [Juju integrations](https://canonical.com/juju/integrations).
```

## Deployment architectures

The Landscape Server charm supports two deployment architectures:

**Landscape 26.04 LTS beta+ (recommended):**
- Internal HAProxy on each Landscape Server unit
- PostgreSQL 14+ with modern `database` interface
- TLS certificates via `tls-certificates` interface provider
- Optional `ingress-configurator` integration for external load balancer integration

**Before 26.04:**
- External HAProxy charm for load balancing
- PostgreSQL ≥ 14 with legacy `pgsql` interface

For migration from older deployments to 26.04 beta+, see {ref}`how-to-migrate-to-26-04-charm`.

## Required integrations by version

| Charm                         | Landscape 26.04 LTS beta+                       | Before 26.04                                |
| ----------------------------- | ----------------------------------------------- | ------------------------------------------- |
| **PostgreSQL**                | Required (PostgreSQL 14+, `database` interface) | Required (PostgreSQL 14, `pgsql` interface) |
| **RabbitMQ Server**           | Required                                        | Required                                    |
| **HAProxy**                   | Not used (internal HAProxy)                     | Required (external charm)                   |
| **TLS Certificates Provider** | Required (e.g., `self-signed-certificates`)     | Not used                                    |
| **Ingress Configurator**      | Optional (for external LB integration)          | Not applicable                              |

```{note}
This feature is available in Landscape 26.04 LTS beta+.
```

## TLS certificates charm interface

Starting with the 26.04 beta version, the Landscape Server charm handles load balancing internally using HAProxy bundled within each unit. This architecture requires integration with a provider of the [`tls-certificates` charm interface](https://charmhub.io/integrations/tls-certificates) using the Landscape Server charm's `load-balancer-certificates` relation endpoint.

The TLS certificates are used by the internal HAProxy instances for secure HTTPS connections.

### Available TLS certificate providers

**For testing/development:**
- [`self-signed-certificates`](https://charmhub.io/self-signed-certificates) - Generates self-signed certificates (not trusted by browsers/clients)

**For production:**
- [`lego`](https://charmhub.io/lego) - Obtains certificates from Let's Encrypt or other ACME providers
- [`manual-tls-certificates`](https://charmhub.io/manual-tls-certificates) - Use custom CA certificates
- Any charm that provides the `tls-certificates` interface

For deployment examples and configuration, see {ref}`how-to-juju-ha-installation` and {ref}`how-to-migrate-to-26-04-charm`.

## K8s Operators

Landscape Server is currently only distributed as a machine (VM) charm and cannot be directly integrated with any version of K8s Charmed Operators, such as the HAProxy K8s operator or the Charmed PostgreSQL K8s operator.

```{note}
This feature is available in Landscape 26.04 LTS beta+.
```

## Ingress Configurator charm

Starting with the 26.04 beta version of the Landscape Server charm, the Ingress Configurator charm can be used to integrate Landscape Server with external load balancers that provide the `haproxy-route` interface, such as the new HAProxy charm. These integrations are **optional** and provide advanced routing capabilities beyond the built-in internal HAProxy.

There are two deployment approaches for external load balancers:

### LBaaS (Load Balancer as a Service) - Cross-Model Relations

For enterprise deployments, you can deploy HAProxy in a separate Juju model and use cross-model relations (offers/consumes) to connect it to Landscape Server. This provides:
- Separate lifecycle management for load balancer infrastructure
- Ability to share a load balancer across multiple applications/models
- Better isolation of infrastructure concerns

**Architecture:**
```
Client → HAProxy (lbaas model)
  → [Cross-model relation]
  → Ingress Configurators (landscape model)
  → Internal HAProxy (on each Landscape Server unit)
  → Landscape Services
```

See the "External Load Balancer with Cross-Model Integration (LBaaS)" section in {ref}`how-to-juju-ha-installation` for complete setup.

### Configuration

If you use external load balancers via Ingress Configurator, configure the following options:

**Landscape Server charm configuration:**

| Configuration Option             | Value                              |
| -------------------------------- | ---------------------------------- |
| `enable_hostagent_messenger`     | `True`                             |
| `enable_ubuntu_installer_attach` | `True`                             |
| `root_url`                       | `https://your-domain.example.com/` |
| `redirect_https`                 | `none`                             |

**Ingress Configurator charm configuration:**

| Relation/Service            | Configuration Option         | Value                     |
| --------------------------- | ---------------------------- | ------------------------- |
| **Hostagent Messenger**     | `external-grpc-port`         | `6554`                    |
|                             | `hostname`                   | `your-domain.example.com` |
|                             | `backend-protocol`           | `https`                   |
| **Ubuntu Installer Attach** | `external-grpc-port`         | `50051`                   |
|                             | `hostname`                   | `your-domain.example.com` |
|                             | `backend-protocol`           | `https`                   |
| **HTTP Ingress**            | `paths`                      | `/`                       |
|                             | `hostname`                   | `your-domain.example.com` |
|                             | `header-rewrite-expressions` | `X-Forwarded-Proto:https` |
|                             | `allow-http`                 | `true`                    |

```{important}
The Ingress Configurator integration for external load balancers (such as a dedicated HAProxy deployment) is optional. The internal HAProxy on each Landscape Server unit already handles load balancing without requiring external load balancers. Use the Ingress Configurator integration only when you need dedicated infrastructure management, advanced routing, or integration with existing load balancer systems.
```

- [Ingress Configurator on Charmhub](https://charmhub.io/ingress-configurator)

## HAProxy

The relationship between Landscape Server and HAProxy varies significantly between Landscape versions:

**Landscape 26.04 LTS beta+:**
- HAProxy is bundled **internally** within each Landscape Server unit
- Cannot be directly integrated with the HAProxy charm
- Each Landscape Server unit runs its own HAProxy instance for load balancing

**Before 26.04:**
- Requires the external HAProxy charm for load balancing
- Uses the `latest/x` channel
- HAProxy units sit in front of Landscape Server units
- Cannot be integrated with the `2.8/x` channels of the HAProxy charm

**External load balancer integration (optional for Landscape 26.04 LTS beta+):**
- Must use Ingress Configurator charms as an intermediary to integrate with external HAProxy
- See the LBaaS section in {ref}`how-to-juju-ha-installation` for complete setup

For migrating from older deployments to the internal HAProxy architecture, see {ref}`how-to-migrate-to-26-04-charm`.

- [HAProxy on Charmhub](https://charmhub.io/haproxy)
- [Ingress Configurator on Charmhub](https://charmhub.io/ingress-configurator)

## Charmed PostgreSQL

PostgreSQL charm compatibility varies by Landscape Server version:

**Landscape 26.04 LTS beta+:**
- Compatible with PostgreSQL 14+ using the modern `database` interface
- Landscape Server integrates using the `database` relation endpoint: `landscape-server:database` → `postgresql:database`
- It is recommended to use PostgreSQL 16 for new deployments

**Before 26.04:**
- Compatible with PostgreSQL 14 using the legacy `pgsql` interface
- Landscape Server integrates using the `db` relation endpoint: `landscape-server:db` → `postgresql:db-admin`
- Cannot use PostgreSQL 16 due to interface incompatibility

- [Charmed PostgreSQL VM on Charmhub](https://charmhub.io/postgresql)

## RabbitMQ Server

RabbitMQ Server integration varies by Landscape Server version:

**Landscape 25.10+:**
- Uses separate inbound and outbound AMQP relation endpoints
- Relations:
  - `landscape-server:inbound-amqp` ↔ `rabbitmq-server`
  - `landscape-server:outbound-amqp` ↔ `rabbitmq-server`

**Before 25.10:**
- Uses a single `amqp` relation endpoint
- Relation: `landscape-server:amqp` ↔ `rabbitmq-server:amqp`

- [RabbitMQ Server on Charmhub](https://charmhub.io/rabbitmq-server)
