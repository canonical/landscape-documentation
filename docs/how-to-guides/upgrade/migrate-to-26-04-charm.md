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
| **PostgreSQL interface** | Modern `database` interface (PostgreSQL 14+)                                                      | Legacy `pgsql` interface (PostgreSQL 14)                     |
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

```bash
juju deploy lego --channel 4/stable
juju config lego server="https://acme-v02.api.letsencrypt.org/directory"
juju config lego email="admin@example.com"
juju config lego plugin="http"
juju integrate haproxy:certificates lego:certificates
juju integrate haproxy:receive-ca-certs lego:send-ca-cert
```

**Prerequisites for Let's Encrypt HTTP-01 challenge:**
- Domain in `root_url` must resolve to the HAProxy unit IP
- Port 80 must be accessible for ACME HTTP-01 challenge validation
- Valid email address for certificate notifications

See the [lego charm documentation](https://charmhub.io/lego) for DNS-01 challenge configuration.

**For custom CA certificates:**

```{tip}
See the [manual-tls-certificates charm documentation](https://charmhub.io/manual-tls-certificates/docs/h-getting-started?channel=1/beta) for more details and a tutorial on creating and using a custom CA.
```

To use custom CA certificates, deploy the `manual-tls-certificates` charm.

```bash
juju deploy manual-tls-certificates --channel 1/beta
```

Then, integrate it with HAProxy twice to provide the TLS certificates and trust the signing CA:

```sh
juju integrate manual-tls-certificates:certificates haproxy:certificates
juju integrate manual-tls-certificates:trust_certificate haproxy:receive-ca-certs
```

Now, ensure you have a CA certificate and private key available locally. You can use any existing CA (such as your organisation's internal CA or corporate PKI). If you don't already have a CA, the following example shows how to generate one with OpenSSL:

1. Create a directory to store the certificates:

   ```sh
   mkdir certs
   ```

1. Generate a private key:

   ```sh
   openssl genrsa -out certs/ca.key 2048
   ```

1. Generate a self-signed CA certificate:

   ```sh
   openssl req -new -x509 -days 3650 -key certs/ca.key -out certs/ca.crt -subj "/C=US/CN=landscape.example.com"
   ```

After integrating the charm, HAProxy will make a Certificate Signing Request (CSR) that we can extract via the `get-outstanding-certificate-requests` action, and use to create a signed TLS certificate. For example:

```sh
juju run manual-tls-certificates/0 get-outstanding-certificate-requests --format=json | jq '.manual-tls-certificates/0.results.result' | jq '.[0].csr' > certs/client.csr
```

```{note}
The outstanding certificate requests are grouped by the `relation-id`; if there are multiple requests (i.e., multiple consumers of the manual TLS certificates), use `juju show-unit manual-tls-certificates/0` to identify the correct ID.

If the machine ID of the manual TLS certificates charm is not 0, adjust the above and following commands with the correct ID. Use `juju status` to identify the Juju machine ID of the manual TLS certificates charm.
```

Then, sign the CSR with your CA. For example, with OpenSSL:

```sh
openssl x509 -req -in certs/client.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/client.crt -days 365 -sha256
```

Then, use the `provide-certificate` action on the `manual-tls-certificates` charm to provide the signed certificate, your CA certificate, and the original CSR:

```sh
juju run manual-tls-certificates/0 provide-certificate \
  certificate="$(base64 -w0 certs/client.crt)" \
  ca-certificate="$(base64 -w0 certs/ca.crt)" \
  certificate-signing-request="$(base64 -w0 certs/client.csr)"
```

Now, HAProxy is using the custom CA for TLS connections. You can verify HAProxy received the new TLS certificates using the `get-certificates` action on the HAProxy charm by providing the hostname of the configured Landscape Server root URL, for example:

```sh
juju run haproxy/0 get-certificate hostname=landscape.example.com --format=json | jq -r '.["haproxy/0"].["results"].certificate' > cert.pem
openssl x509 -in cert.pem -noout -text
```

```{note}
If the machine ID of the HAProxy charm is not 0, adjust the above command with the correct ID. Use `juju status` to identify the Juju machine ID of the HAProxy charm.
```

### Step 4: Refresh the charm

Refresh the Landscape Server charm to the 26.04 version:

```bash
juju refresh landscape-server --channel 26.04/stable
```

```{note}
`juju refresh` updates the charm revision, but it does not upgrade the installed `landscape-server` deb packages on existing units.

The landscape-server charm only adds the PPA source during installation, so you will need to manually update this PPA on each of the landscape-server units.
```

Wait for the refresh to complete and the services to restart:

```bash
juju status --watch 2s
```

### Step 5: Integrate Landscape Server with HAProxy

Add the HAProxy route integrations for all Landscape Server services:

```bash
juju integrate landscape-server:appserver-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:pingserver-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:message-server-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:api-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:package-upload-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:repository-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:hostagent-messenger-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:ubuntu-installer-attach-haproxy-route haproxy:haproxy-route
```

```{important}
When using HAProxy charm from the `2.8/x` track, the `ssl_cert` and `ssl_key` charm configuration options for Landscape Server are unused since TLS is now managed by the HAProxy charm via the `tls-certificates` interface.
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
PostgreSQL upgrade is optional. The 26.04 charm uses the modern `database` interface which works with PostgreSQL 14 and above.

The legacy `db` endpoint (legacy `pgsql` interface) is still supported for backwards compatibility but only works with PostgreSQL 14. It is recommended to migrate to the modern `database` interface since Charmed PostgreSQL 16+ does not support the legacy interface.
```

### Step 8: Verify the deployment

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

## Additional resources

- {ref}`how-to-juju-ha-installation` - Full HA deployment guide
- {ref}`explanation-charm-compatibility` - Charm compatibility details
- {ref}`how-to-terraform-juju-deployment` - How to deploy Landscape with Terraform and Juju
- {ref}`reference-landscape-product-modules-landscape-scalable` - Terraform module reference
- [Landscape Server charm documentation](https://charmhub.io/landscape-server)
- [PostgreSQL charm documentation](https://charmhub.io/postgresql)
