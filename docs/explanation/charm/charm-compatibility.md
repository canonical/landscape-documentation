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
- `haproxy` (at `2.8/stable`, via `haproxy-route` interface)
- A TLS certificates provider integrated with HAProxy (e.g., `self-signed-certificates`, `lego`)
- `landscape-debarchive` (for Deb Archive repository management)
- `landscape-task-handler` (for task processing)

**Before Landscape 26.04:**
- `haproxy` (via `reverseproxy` interface)

For a recommended charm bundle configuration and more information about deploying Landscape Server with Juju, see {ref}`how-to-juju-installation` and {ref}`how-to-juju-ha-installation`.

Compatibility with a Landscape Server charm revision is limited to specific revisions and channels of the required charms. Incompatibility can occur if the charm's base (e.g., `ubuntu@24.04`), architecture (e.g., `amd64`), or interfaces change.

```{tip}
Learn more about [Juju integrations](https://canonical.com/juju/integrations).
```

## Deployment architectures

The Landscape Server charm supports two deployment architectures:

**Landscape 26.04 LTS beta+ (recommended):**
- External HAProxy charm (`2.8/stable`) for load balancing, using the `haproxy-route` interface
- PostgreSQL 14+ with modern `database` interface
- TLS certificates via a `tls-certificates` interface provider integrated with HAProxy
- `landscape-debarchive` charm for Deb Archive repository management
- `landscape-task-handler` charm for task processing

```{include} /reuse/charm-ha-architecture-2604.md
```

**Before 26.04:**
- External HAProxy charm for load balancing, using the `reverseproxy` interface
- PostgreSQL ≥ 14 with legacy `pgsql` interface

```{include} /reuse/charm-ha-architecture-pre-2604.md
```

For migration from older deployments to 26.04 beta+, see {ref}`how-to-migrate-to-26-04-charm`.

## Required integrations by version

| Charm                         | Landscape 26.04 LTS beta+                                            | Before 26.04                                    |
| ----------------------------- | -------------------------------------------------------------------- | ----------------------------------------------- |
| **PostgreSQL**                | Required (PostgreSQL 14+, `database` interface)                      | Required (PostgreSQL 14, `pgsql` interface)     |
| **RabbitMQ Server**           | Required                                                             | Required                                        |
| **HAProxy**                   | Required (`2.8/x`, `haproxy-route` interface)                        | Required (`latest/x`, `reverseproxy` interface) |
| **TLS Certificates Provider** | Required (integrated with HAProxy, e.g., `self-signed-certificates`) | Not used                                        |
| **landscape-debarchive**      | Required (Deb Archive repository management)                         | Not available                                   |
| **landscape-task-handler**    | Required (task processing)                                           | Not available                                   |

## TLS certificates charm interface

Starting with the 26.04 beta version, TLS is managed by the HAProxy charm. The HAProxy charm integrates with a provider of the [`tls-certificates` charm interface](https://charmhub.io/integrations/tls-certificates) to obtain certificates for HTTPS connections.

### Available TLS certificate providers

**For testing/development:**
- [`self-signed-certificates`](https://charmhub.io/self-signed-certificates) - Generates self-signed certificates (not trusted by browsers/clients)

**For production:**
- [`lego`](https://charmhub.io/lego) - Obtains certificates from Let's Encrypt or other ACME providers
- [`manual-tls-certificates`](https://charmhub.io/manual-tls-certificates) - Use custom CA certificates
- Any charm that provides the `tls-certificates` interface

Integrate TLS with HAProxy (not with `landscape-server` directly):

```bash
juju integrate haproxy:certificates <tls-provider>:certificates
```

For deployment examples and configuration, see {ref}`how-to-juju-ha-installation` and {ref}`how-to-migrate-to-26-04-charm`.

## K8s Operators

Landscape Server is currently only distributed as a machine (VM) charm and cannot be directly integrated with any version of K8s Charmed Operators, such as the HAProxy K8s operator or the Charmed PostgreSQL K8s operator.

## HAProxy

The relationship between Landscape Server and HAProxy varies significantly between Landscape versions:

**Landscape 26.04 LTS beta+:**
- Requires the HAProxy charm at `2.8/stable`
- Integrates via 8 `haproxy-route` relation endpoints directly from landscape-server to haproxy
- HAProxy handles TLS termination and load balancing
- Cannot be integrated with the `latest/x` channels of the HAProxy charm (different interface)

**Before 26.04:**
- Requires the external HAProxy charm at `latest/x`
- Integrates via the `reverseproxy` interface: `landscape-server:website` → `haproxy:reverseproxy`
- Cannot be integrated with the `2.8/x` channels of the HAProxy charm

**LBaaS (Load Balancer as a Service) - cross-model HAProxy:**
- Deploy HAProxy in a separate Juju model and use cross-model relations
- Landscape Server integrates directly with the cross-model HAProxy via `haproxy-route` endpoints
- See {ref}`heading-lbaas-installation` for complete setup

For migrating from older deployments to the new HAProxy architecture, see {ref}`how-to-migrate-to-26-04-charm`.

- [HAProxy on Charmhub](https://charmhub.io/haproxy)

## Charmed PostgreSQL

PostgreSQL charm compatibility varies by Landscape Server version:

**Landscape 26.04 LTS beta+:**
- Compatible with PostgreSQL 14+ using the modern `database` interface
- Landscape Server integrates using the `database` relation endpoint: `landscape-server:database` → `postgresql:database`
- It is recommended to use PostgreSQL 16 for new deployments
- Supports [PgBouncer](https://charmhub.io/pgbouncer) as a connection pooler via the `database` relation endpoint; see {ref}`explanation-pgbouncer-integration`

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
