---
myst:
  html_meta:
    description: "Migrate to Landscape 26.04 LTS (charm)."
---

(how-to-migrate-to-26-04-charm)=
# How to migrate to Landscape 26.04 LTS (charm)

```{note}
The Landscape Server charm for 26.04 is available in the `26.04/stable` channel. See the {ref}`reference-release-notes-26-04-lts` for details on our changes introduced in 26.04. Note the recommendations for repository management users.
```

This guide explains how to migrate from an older Landscape Server charm deployment (pre-26.04) to the 26.04 LTS version with an external HAProxy charm using the `haproxy-route` interface.

You can follow the manual `juju integrate` steps below, or use the {ref}`Landscape Scalable Terraform product module <how-to-terraform-juju-deployment>` (see its {ref}`module reference <reference-landscape-product-modules-landscape-scalable>`) to manage the migration as code instead.

## Architectural changes

The 26.04 version introduces significant architectural changes:

| Aspect                   | Landscape 26.04 LTS                                                                         | Pre-26.04                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Load balancing**       | External HAProxy charm (`haproxy` at `2.8/stable`, `haproxy-route` interface)                     | External HAProxy charm (`reverseproxy` interface)            |
| **PostgreSQL interface** | Modern `postgresql_client` interface (PostgreSQL 14+)                                                      | Legacy `pgsql` interface (PostgreSQL 14)                     |
| **PostgreSQL relation**  | `landscape-server:database` → `postgresql:database`                                               | `landscape-server:db` → `postgresql:db-admin`                |
| **RabbitMQ relation**    | `landscape-server:inbound-amqp` and `landscape-server:outbound-amqp` → `rabbitmq-server` (25.10+) | `landscape-server:amqp` → `rabbitmq-server:amqp` (pre-25.10) |
| **HAProxy relation**     | `landscape-server:*-haproxy-route` → `haproxy:haproxy-route` (8 route endpoints)                  | `landscape-server:website` → `haproxy:reverseproxy`          |
| **TLS certificates**     | `haproxy:certificates` → TLS provider (e.g., `self-signed-certificates`, `lego`)                  | HAProxy self-signed or manual config                         |
| **Access method**        | HAProxy unit IP or `root_url`                                                                     | HAProxy unit IP                                              |
| **HA capabilities**      | HAProxy units for load balancing                                                                  | HAProxy units for load balancing                             |

## Migration steps

### Step 1: Backup your database

Before making any changes, back up your Landscape database following the backup procedures in {ref}`how-to-back-up-restore-tear-down-charmed-deployment`.

### Step 2: Remove incompatible relations

Remove the older HAProxy relation:

```bash
juju remove-relation landscape-server:website haproxy:reverseproxy
```

```{note}
The legacy `website` relation (`reverseproxy` interface) is still available for backwards compatibility, but is deprecated. Support will be removed in Landscape 26.10, so it is recommended to complete this migration to the `haproxy-route` interface rather than continuing to rely on the legacy relation.
```

**For deployments older than 25.10 only:**

Remove the older RabbitMQ relation:

```bash
juju remove-relation landscape-server:amqp rabbitmq-server:amqp
```

```{note}
If you're migrating from 25.10 or later, you already have the `inbound-amqp` and `outbound-amqp` relations.
```

### Step 3: Deploy HAProxy and TLS certificates provider

Deploy the HAProxy charm and a TLS certificates provider before refreshing the charm. This gives them time to become active while other operations proceed.

````{important}
If your existing HAProxy application is not running on Ubuntu 24.04 LTS, remove the application and redeploy it on the `2.8/stable` channel. The `2.8/stable` HAProxy charm runs on Ubuntu 24.04 LTS, and `juju refresh` does not change the base of existing units.
```sh
juju remove-application haproxy
juju deploy haproxy --channel 2.8/stable
```
````

First, deploy the HAProxy charm:

```bash
juju deploy haproxy --channel 2.8/stable
```

Alternatively, if you still have HAProxy deployed from the `latest/x` track, you can simply refresh it to the `2.8/stable` channel:

```sh
juju refresh haproxy --channel 2.8/stable
```

**For testing/development with self-signed certificates:**

```bash
juju deploy self-signed-certificates
juju integrate haproxy:certificates self-signed-certificates:certificates
juju integrate haproxy:receive-ca-certs self-signed-certificates:send-ca-cert
```

**For production with Let's Encrypt:**

For production deployments that use Let's Encrypt, follow the [lego charm documentation](https://charmhub.io/lego) to deploy and configure the `lego` charm for your environment. After deploying `lego`, integrate it with HAProxy:

```bash
juju integrate haproxy:certificates lego:certificates
juju integrate haproxy:receive-ca-certs lego:send-ca-cert
```

**For custom CA certificates:**

For deployments that use custom CA certificates, follow the [manual-tls-certificates charm documentation](https://charmhub.io/manual-tls-certificates/docs/h-getting-started?channel=1/beta) to deploy and configure the `manual-tls-certificates` charm for your environment. After deploying `manual-tls-certificates`, integrate it with HAProxy:

```sh
juju integrate haproxy:certificates manual-tls-certificates:certificates
juju integrate haproxy:receive-ca-certs manual-tls-certificates:trust_certificate
```

```{note}
For Let's Encrypt and custom CA certificates, complete certificate issuance after you integrate Landscape Server with HAProxy. HAProxy requests certificates after it receives the hostname from the Landscape Server HAProxy route integrations.
```

### Step 4: Refresh the charm

Refresh the Landscape Server charm to the 26.04 version:

```bash
juju refresh landscape-server --channel 26.04/stable
```

```{note}
`juju refresh` updates the charm revision, but it does not upgrade the installed `landscape-server` deb packages on existing units.

Set `landscape_ppa` to `ppa:landscape/self-hosted-26.04` in the charm configuration, then follow the package upgrade steps in {ref}`how-to-heading-upgrade-juju`. The 26.04 charm's `upgrade` action adds the configured PPA before it upgrades the packages, so you don't need to add it manually on each unit. You've already refreshed the charm, so skip the `juju refresh landscape-server` step at the start of that procedure.
```

Wait for the refresh to complete and the services to restart:

```bash
juju status --watch 2s
```

### Step 5: Integrate Landscape Server with HAProxy

Configure the root URL for your Landscape deployment:

```bash
juju config landscape-server root_url="https://landscape.example.com/"
```

Enable the Hostagent Messenger service:

```bash
juju config landscape-server enable_hostagent_messenger=true
```

Add the HAProxy route integrations for all Landscape Server services:

```bash
juju integrate landscape-server:appserver-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:pingserver-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:message-server-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:api-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:package-upload-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:repository-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:hostagent-messenger-haproxy-route haproxy:haproxy-route-tcp
```

```{important}
When using HAProxy charm from the `2.8/x` track, the `ssl_cert` and `ssl_key` charm configuration options for Landscape Server are unused since TLS is now managed by the HAProxy charm via the `tls-certificates` interface.
```

#### Ubuntu Installer Attach

The Ubuntu Installer Attach service requires the `landscape-ubuntu-installer-attach` package. If you are migrating from a version earlier than 25.10, enable the service after the Landscape Server package upgrade is complete.

```bash
juju config landscape-server enable_ubuntu_installer_attach=true
juju integrate landscape-server:ubuntu-installer-attach-haproxy-route haproxy:haproxy-route-tcp
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

### Step 7: Update the Landscape Server PostgreSQL relation

Remove the legacy PostgreSQL relation and add the modern `postgresql_client` relation:

```bash
juju remove-relation landscape-server:db postgresql:db-admin
juju integrate landscape-server:database postgresql:database
```

### Step 8: Update PostgreSQL (optional)

If you want to upgrade to a newer PostgreSQL version (e.g., from 14 to 16) as part of this migration, follow the backup and restore procedures in {ref}`how-to-back-up-restore-tear-down-charmed-deployment` to migrate your data to a new PostgreSQL deployment.

```{note}
PostgreSQL upgrade is optional. The 26.04 charm uses the modern `postgresql_client` interface which works with PostgreSQL 14 and above.
```

### Step 9: Deploy Debarchive and Task Handler

The 26.04 architecture also introduces two required companion charms: **Debarchive** for repository mirroring, and **Landscape Task Handler** for offloaded background task processing. Deploy them:

```bash
juju deploy landscape-debarchive --channel latest/stable --base ubuntu@24.04
juju deploy landscape-task-handler --channel latest/stable --base ubuntu@24.04 --config task-handler-snap-channel=latest/stable
```

Integrate Debarchive with Landscape Server, PostgreSQL, and HAProxy:

```bash
juju integrate landscape-server:debarchive landscape-debarchive:landscape-server
juju integrate landscape-debarchive:database postgresql:database
juju integrate landscape-debarchive:debarchive-haproxy-route haproxy:haproxy-route
```


Integrate Landscape Task Handler with Landscape Server, PostgreSQL, your TLS certificates provider, and HAProxy's gRPC route:

```bash
juju integrate landscape-task-handler:landscape-server landscape-server:task-handler
juju integrate landscape-task-handler:task-db postgresql:database
juju integrate landscape-task-handler:certificates self-signed-certificates:certificates
juju integrate landscape-task-handler:grpc-haproxy-route haproxy:haproxy-route-tcp
```

```{note}
Substitute `self-signed-certificates` above with whichever TLS provider you deployed in Step 3.
```

```{important}
The outbox component on the `landscape-server` units reaches Task Handler through this HAProxy gRPC route by hostname, not by IP. If that hostname doesn't resolve on the `landscape-server` units (for example, testing locally without a real domain), add an `/etc/hosts` entry there pointing it at the HAProxy unit's IP address. This dependency is one-directional: outbox connects to Task Handler, not the other way around.
```

Restart the Landscape Task Handler and Debarchive snaps on each unit after the integrations are complete. Repeat the following for each unit:

```bash
juju run landscape-task-handler/0 restart-snap
juju run landscape-debarchive/0 restart-snap
```


### Step 10: Verify the deployment

Check that all services are active:

```bash
juju status
```

Access Landscape via the HAProxy unit IP or your configured `root_url`. Use `juju status` to find the HAProxy unit IP address.

```{tip}
For testing access by hostname before DNS is configured, add the HAProxy unit IP (or your external HAProxy IP if using LBaaS) to `/etc/hosts` on your local machine with the hostname from your `root_url`. For example: `10.1.77.133 landscape.example.com`
```

Log in and verify:
- All computers are visible
- Activities and alerts are present
- User accounts and permissions are intact

For more information about `juju refresh`, see the [Juju documentation on charm upgrades](https://documentation.ubuntu.com/juju/3.6/howto/manage-charms/#update-a-charm).


## Additional resources

- {ref}`how-to-juju-ha-installation` - Full HA deployment guide
- {ref}`explanation-charm-compatibility` - Charm compatibility details
- {ref}`how-to-terraform-juju-deployment` - How to deploy Landscape with Terraform and Juju
- {ref}`reference-landscape-product-modules-landscape-scalable` - Terraform module reference
- [Landscape Server charm documentation](https://charmhub.io/landscape-server)
- [PostgreSQL charm documentation](https://charmhub.io/postgresql)
