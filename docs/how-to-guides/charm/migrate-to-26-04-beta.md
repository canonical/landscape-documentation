---
myst:
  html_meta:
    description: "Migrate to the 26.04 beta version of the Landscape Server charm."
---

(how-to-migrate-to-26-04-charm)=
# How to migrate to the 26.04 beta version of the charm

This guide explains how to migrate from an older Landscape Server charm deployment (pre-26.04) to the 26.04 LTS beta+ version with internal HAProxy.

## Architectural changes

The 26.04 beta version introduces significant architectural changes:

| Aspect                   | Landscape 26.04 LTS beta+                                                                               | Pre-26.04                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Load balancing**       | Internal HAProxy on each unit                                                                           | External HAProxy charm                                       |
| **PostgreSQL interface** | Modern `database` interface (PostgreSQL 14+)                                                            | Legacy `pgsql` interface (PostgreSQL 14)                     |
| **PostgreSQL relation**  | `landscape-server:database` → `postgresql:database`                                                     | `landscape-server:db` → `postgresql:db-admin`                |
| **RabbitMQ relation**    | `landscape-server:inbound-amqp` and `landscape-server:outbound-amqp` → `rabbitmq-server` (25.10+)       | `landscape-server:amqp` → `rabbitmq-server:amqp` (pre-25.10) |
| **HAProxy relation**     | **None** (internal HAProxy, no external charm needed)                                                   | `landscape-server:website` → `haproxy:reverseproxy`          |
| **TLS certificates**     | `landscape-server:load-balancer-certificates` → TLS provider (e.g., `self-signed-certificates`, `lego`) | HAProxy self-signed or manual config                         |
| **Access method**        | Any Landscape Server unit IP or `root_url`                                                              | HAProxy unit IP                                              |
| **HA capabilities**      | Each Landscape Server unit handles traffic                                                              | HAProxy units for load balancing                             |

## Migration steps

### Step 1: Backup your database

Before making any changes, back up your Landscape database following the backup procedures in {ref}`how-to-back-up-restore-tear-down-charmed-deployment`.

### Step 2: Remove incompatible relations

Remove the older HAProxy relation:

```bash
juju remove-relation landscape-server:website haproxy:reverseproxy --force
```

**For deployments older than 25.10 only:**

Remove the older RabbitMQ relation:

```bash
juju remove-relation landscape-server:amqp rabbitmq-server:amqp --force
```

```{note}
If you're migrating from 25.10 or later, you already have the `inbound-amqp` and `outbound-amqp` relations.
```

### Step 3: Deploy TLS certificates provider

Deploy the TLS certificates provider before refreshing the charm. This gives it time to become active while other operations proceed.

**For testing/development with self-signed certificates:**

```bash
juju deploy self-signed-certificates
```

**For production with Let's Encrypt:**

```bash
juju deploy lego --channel 4/stable
juju config lego server="https://acme-v02.api.letsencrypt.org/directory"
juju config lego email="admin@example.com"
juju config lego plugin="http"
```

**Prerequisites for Let's Encrypt HTTP-01 challenge:**
- Domain in `root_url` must resolve to a Landscape Server unit IP
- Port 80 must be accessible for ACME HTTP-01 challenge validation
- Valid email address for certificate notifications

See the [lego charm documentation](https://charmhub.io/lego) for DNS-01 challenge configuration.

**For custom CA certificates:**

```bash
juju deploy manual-tls-certificates --channel stable
juju config manual-tls-certificates ca-certificate="$(base64 -w0 ca.crt)"
juju config manual-tls-certificates certificate="$(base64 -w0 server.crt)"
juju config manual-tls-certificates private-key="$(base64 -w0 server.key)"
```

See the [manual-tls-certificates charm documentation](https://charmhub.io/manual-tls-certificates) for details.

### Step 4: Refresh the charm

Refresh the Landscape Server charm to the 26.04 beta version:

```bash
juju refresh landscape-server --channel 26.04/beta
```

Wait for the refresh to complete and the services to restart:

```bash
juju status --watch 2s
```

### Step 5: Integrate with TLS certificates provider

Integrate Landscape Server with the TLS certificates provider you deployed earlier:

```bash
juju integrate landscape-server:load-balancer-certificates self-signed-certificates:certificates
```

Or if using lego:

```bash
juju integrate landscape-server:load-balancer-certificates lego:certificates
```

Or if using manual-tls-certificates:

```bash
juju integrate landscape-server:load-balancer-certificates manual-tls-certificates:certificates
```

```{important}
The `ssl_cert` and `ssl_key` charm configuration have been removed and are no longer supported in the 26.04 beta charm. Use a provider of the `tls-certificates` interface instead.
```

### Step 6: Add new RabbitMQ relations (pre-25.10 deployments only)

```{note}
This step can be skipped on deployments on 25.10 or newer, as they will already have these relations.
```

For deployments older than 25.10, add the new separate inbound and outbound AMQP relations:

```bash
juju integrate landscape-server:inbound-amqp rabbitmq-server
juju integrate landscape-server:outbound-amqp rabbitmq-server
```

### Step 7: Update PostgreSQL (optional)

If you want to upgrade to a newer PostgreSQL version (e.g., from 14 to 16) as part of this migration, follow the backup and restore procedures in {ref}`how-to-back-up-restore-tear-down-charmed-deployment` to migrate your data to a new PostgreSQL deployment.

```{note}
PostgreSQL upgrade is optional. The 26.04 beta charm uses the modern `database` interface which works with PostgreSQL 14 and above.

The legacy `db` endpoint (legacy `pgsql` interface) is still supported for backwards compatibility but only works with PostgreSQL 14. It is recommended to migrate to the modern `database` interface since Charmed PostgreSQL 16+ does not support the legacy interface.
```

### Step 8: Remove external HAProxy

The 26.04 beta charm has an internal HAProxy service on each unit, so the external HAProxy charm is no longer needed:

```bash
juju remove-application haproxy
```

### Step 9: Verify the deployment

Check that all services are active:

```bash
juju status
```

Access Landscape via any Landscape Server unit IP or your configured `root_url`. Use `juju status` to find the landscape-server unit IP addresses.

```{tip}
For testing access by hostname before DNS is configured, add a Landscape Server unit IP (or your external HAProxy IP if using LBaaS) to `/etc/hosts` on your local machine with the hostname from your `root_url`. For example: `10.1.77.133 landscape.example.com`
```

Log in and verify:
- All computers are visible
- Activities and alerts are present
- User accounts and permissions are intact

For more information about `juju refresh`, see the [Juju documentation on charm upgrades](https://documentation.ubuntu.com/juju/3.6/howto/manage-charms/#update-a-charm).

## Additional resources

- {ref}`how-to-juju-ha-installation` - Full HA deployment guide
- {ref}`explanation-charm-compatibility` - Charm compatibility details
- [Landscape Server charm documentation](https://charmhub.io/landscape-server)
- [PostgreSQL charm documentation](https://charmhub.io/postgresql)
