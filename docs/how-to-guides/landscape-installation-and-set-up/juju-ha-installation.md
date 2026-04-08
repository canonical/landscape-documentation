---
myst:
  html_meta:
    description: "Configure high-availability Landscape deployments with Juju and the landscape-scalable bundle. Deploy with HAProxy, RabbitMQ, PostgreSQL, and multiple units."
---

(how-to-juju-ha-installation)=
# How to install and configure Landscape for high-availability deployments

> See also: [Juju documentation](https://juju.is/docs/juju)

You can create a scalable, high availability (HA) deployment of Landscape Server by using Juju and the [Landscape Scalable](https://charmhub.io/landscape-scalable) charm bundle. The result is a Juju-managed deployment of Landscape Server and the other services it depends on.

```{important}
This guide covers both the **26.04 beta+ deployment approach** and the older **pre-26.04 deployment approach**. The 26.04 beta version integrates directly with the external HAProxy charm (`2.8/edge`) using the `haproxy-route` interface, replacing the older `reverseproxy` interface. For new deployments, use the 26.04 beta+ approach. For existing deployments, see {ref}`how-to-migrate-to-26-04-charm`.
```

## Architecture overview

### 26.04 beta+ architecture (recommended)

Starting with the 26.04 beta version, Landscape Server uses the following architecture:

- **Landscape Server units** for the application
- **HAProxy** charm (`2.8/edge`) for load balancing via the `haproxy-route` interface
- **PostgreSQL 14+** for the database (using the modern `database` interface)
- **RabbitMQ Server** for message queuing
- **Self-signed certificates** charm (or other TLS provider) integrated with HAProxy

HAProxy sits in front of all Landscape Server units and routes traffic to the appropriate service endpoints.

```{include} /reuse/charm-ha-architecture-2604.md
```

### Before 26.04

The older approach uses:

- **External HAProxy charm** for load balancing
- **PostgreSQL 14** for the database (using the legacy `pgsql` interface)
- **RabbitMQ Server** for message queuing
- **Separate HAProxy units** for traffic management

```{include} /reuse/charm-ha-architecture-pre-2604.md
```

## Prerequisites

Before you can deploy the Landscape Scalable charm bundle, you need to:

  1. [Install the Juju client](https://juju.is/docs/juju/install-and-manage-the-client)
  1. [Add a machine cloud to Juju](https://juju.is/docs/juju/manage-clouds)

These steps lay the groundwork for using Juju to deploy [machine charms](https://juju.is/charms-architecture).

Machine charms are Juju-managed applications deployed on bare-metal servers, virtual machines, or system containers such as [LXD](https://canonical.com/lxd). Landscape is only one of many charms that can be deployed from [Charmhub](https://charmhub.io/) and managed by Juju. Juju handles installing the applications and configuring them to work together.

```{note}
For improved database performance and scalability in high-load deployments, consider using PgBouncer as a connection pooler between Landscape Server and PostgreSQL. PgBouncer integrates via the Landscape Server charm's `database` relation endpoint, which uses the underlying `postgresql_client` interface. This requires recent Landscape Server charm revisions with `postgresql_client` support. See {ref}`explanation-pgbouncer-integration` for more information.
```

## Deployment approach selection

Choose the appropriate deployment approach based on your needs:

- **For new deployments:** Use the 26.04 beta+ approach (recommended)
- **For existing deployments:** Continue with the older approach or migrate using {ref}`how-to-migrate-to-26-04-charm`

---

## 26.04 beta+ deployment (recommended)

This section covers deploying Landscape Server with the external HAProxy charm introduced in version 26.04 beta.

### Create a Juju model

```bash
juju add-model landscape-ha
```

### Deploy with a custom bundle file

For the 26.04 beta+ deployment, you'll create a custom bundle file that includes all the necessary components.

#### Step 1: Create the bundle file

Create a file named `landscape-ha-26.04.yaml` with the following content:

```yaml
description: Landscape Scalable
applications:
  postgresql:
    channel: 16/stable
    charm: ch:postgresql
    num_units: 3
    options:
      plugin_plpython3u_enable: true
      plugin_ltree_enable: true
      plugin_intarray_enable: true
      plugin_debversion_enable: true
      plugin_pg_trgm_enable: true
      experimental_max_connections: 500
    base: ubuntu@24.04

  rabbitmq-server:
    channel: latest/edge
    charm: ch:rabbitmq-server
    num_units: 3
    options:
      consumer-timeout: 259200000

  landscape-server:
    charm: ch:landscape-server
    channel: 26.04/beta
    num_units: 3
    options:
      landscape_ppa: ppa:landscape/self-hosted-26.04
      min_install: True
      root_url: https://landscape.local/
    base: ubuntu@24.04

  haproxy:
    charm: ch:haproxy
    channel: 2.8/edge
    num_units: 1
    constraints: arch=amd64

  self-signed-certificates:
    charm: ch:self-signed-certificates
    channel: 1/stable
    num_units: 1
    constraints: arch=amd64

relations:
  - [landscape-server:inbound-amqp, rabbitmq-server]
  - [landscape-server:outbound-amqp, rabbitmq-server]
  - [landscape-server:database, postgresql:database]
  - [haproxy:certificates, self-signed-certificates:certificates]
  - [haproxy:receive-ca-certs, self-signed-certificates:send-ca-cert]
  - [landscape-server:appserver-haproxy-route, haproxy:haproxy-route]
  - [landscape-server:pingserver-haproxy-route, haproxy:haproxy-route]
  - [landscape-server:message-server-haproxy-route, haproxy:haproxy-route]
  - [landscape-server:api-haproxy-route, haproxy:haproxy-route]
  - [landscape-server:package-upload-haproxy-route, haproxy:haproxy-route]
  - [landscape-server:repository-haproxy-route, haproxy:haproxy-route]
  - [landscape-server:hostagent-messenger-haproxy-route, haproxy:haproxy-route]
  - [landscape-server:ubuntu-installer-attach-haproxy-route, haproxy:haproxy-route]
```

```{note}
This bundle uses PostgreSQL 16 and the new `database` interface. Adjust the `root_url` option to match your domain name.
```

#### Step 2: Deploy the bundle

```bash
juju deploy ./landscape-ha-26.04.yaml
```

#### Step 3: Monitor the deployment

Watch the deployment progress:

```bash
juju status --watch 3s
```

Once everything is installed and settled, the `Status` for every application will be `active`:

```text
Model         Controller  Cloud/Region    Version  SLA          Timestamp
landscape-ha  lxd         localhost/lxd   3.5.5    unsupported  10:30:00+00:00

App                       Version  Status  Scale  Charm                      Channel     Rev  Base
haproxy                            active      1  haproxy                    2.8/edge     50  ubuntu@24.04
landscape-server          26.04    active      3  landscape-server           26.04/beta   150  ubuntu@24.04
postgresql                16.4     active      3  postgresql                 16/stable    500  ubuntu@24.04
rabbitmq-server           3.9.27   active      3  rabbitmq-server            latest/edge  200  ubuntu@22.04
self-signed-certificates           active      1  self-signed-certificates   1/stable      12  ubuntu@24.04
```

#### Step 4: Configure license file

Set your Landscape license:

```sh
juju config landscape-server "license_file=$(cat your-license-file)"
```

#### Step 5: Access Landscape

Access Landscape via the HAProxy unit IP or your configured `root_url`. Use `juju status` to find the HAProxy unit IP address.

### Optional: Replace self-signed certificates with a valid certificate

If you deployed the example bundle above, it includes self-signed certificates (suitable for testing). For production, replace them with a valid certificate, such as one from Let's Encrypt:

```bash
juju remove-application self-signed-certificates

juju deploy lego --channel 4/stable
juju config lego server="https://acme-v02.api.letsencrypt.org/directory"
juju config lego email="admin@example.com"
juju config lego plugin="http"

juju integrate haproxy:certificates lego:certificates
juju integrate haproxy:receive-ca-certs lego:send-ca-cert
```

**Prerequisites:**
- Domain in `root_url` must resolve to the HAProxy unit IP
- Port 80 must be accessible for ACME HTTP-01 challenge validation
- Valid email for certificate notifications

For more details, see the [lego charm documentation](https://charmhub.io/lego/docs/getting-started-with-lego-http01).

(heading-lbaas-installation)=
### Optional: External Load Balancer with Cross-Model Integration (LBaaS)

For production deployments requiring an external load balancer in a separate infrastructure layer, you can deploy HAProxy in a **separate Juju model** and connect it to Landscape Server using cross-model relations (also known as LBaaS - Load Balancer as a Service).

This approach is useful when:
- You want to manage your load balancer infrastructure separately from application deployments
- You need a dedicated load balancer shared across multiple applications
- You want to isolate load balancer lifecycle from application lifecycle

#### Step 1: Create a separate model for the load balancer

```bash
juju add-model lbaas
juju switch lbaas
```

#### Step 2: Deploy HAProxy and TLS certificates in the LBaaS model

Deploy HAProxy:

```sh
juju deploy haproxy --channel 2.8/edge
juju expose haproxy
```

Deploy the TLS certificates provider:

```sh
juju deploy lego --channel 4/stable
juju config lego server="https://acme-v02.api.letsencrypt.org/directory"
juju config lego email="admin@example.com"
juju config lego plugin="http"
```

Wait for both applications to become active:

```sh
juju wait-for application haproxy --query='status=="active"'
juju wait-for application lego --query='status=="active"'
```

Integrate HAProxy with the TLS certificates provider:

```sh
juju integrate haproxy:certificates lego:certificates
juju integrate haproxy:receive-ca-certs lego:send-ca-cert
```

#### Step 3: Create a cross-model offer

```sh
juju offer haproxy:haproxy-route
```

This creates an offer that can be consumed from other Juju models.

#### Step 4: Consume the HAProxy offer and integrate Landscape Server

Switch back to your Landscape Server model:

```sh
juju switch landscape-ha
```

Consume the HAProxy offer from the lbaas model:

```sh
juju consume admin/lbaas.haproxy lbaas-haproxy
```

Integrate Landscape Server's route endpoints directly with the external HAProxy:

```sh
juju integrate landscape-server:appserver-haproxy-route lbaas-haproxy:haproxy-route
juju integrate landscape-server:pingserver-haproxy-route lbaas-haproxy:haproxy-route
juju integrate landscape-server:message-server-haproxy-route lbaas-haproxy:haproxy-route
juju integrate landscape-server:api-haproxy-route lbaas-haproxy:haproxy-route
juju integrate landscape-server:package-upload-haproxy-route lbaas-haproxy:haproxy-route
juju integrate landscape-server:repository-haproxy-route lbaas-haproxy:haproxy-route
juju integrate landscape-server:hostagent-messenger-haproxy-route lbaas-haproxy:haproxy-route
juju integrate landscape-server:ubuntu-installer-attach-haproxy-route lbaas-haproxy:haproxy-route
```

Wait for the deployment to complete:

```sh
juju wait-for application landscape-server --query='status=="active"'
```

#### Step 5: Configure DNS and access

Get the HAProxy public IP address:

```sh
juju switch lbaas
juju status haproxy --format=json | jq -r '.applications.haproxy.units | to_entries[0].value["public-address"]'
```

Configure your DNS to point your hostname (matching `root_url`) to this IP address.

Access Landscape via: `https://landscape.example.com/`

```{mermaid}
flowchart TD
    Client([Client])
    subgraph lbaas[Juju model: lbaas]
        HAProxy["HAProxy<br/>2.8/edge"]
        TLS[lego / TLS provider]
    end
    subgraph landscape-ha[Juju model: landscape-ha]
        LS0[landscape-server/0]
        LS1[landscape-server/1]
        LS2[landscape-server/2]
        PG[(PostgreSQL)]
        RMQ[RabbitMQ Server]
    end
    TLS -- certificates --> HAProxy
    Client -- HTTPS --> HAProxy
    HAProxy -- "haproxy-route (cross-model)" --> LS0
    HAProxy -- "haproxy-route (cross-model)" --> LS1
    HAProxy -- "haproxy-route (cross-model)" --> LS2
    LS0 & LS1 & LS2 --- PG
    LS0 & LS1 & LS2 --- RMQ
```

## Pre-26.04 deployment

```{warning}
This deployment approach is **deprecated**. For new deployments, use the 26.04 beta+ approach described above. For existing deployments, consider migrating using {ref}`how-to-migrate-to-26-04-charm`.
```

This section covers the older deployment approach using the external HAProxy charm. This approach is maintained for existing deployments only.

### Deploy the charm bundle

You can deploy the Landscape Scalable charm bundle using one of two main methods. The methods are:

  1. Deploy the bundle with the default configuration, then customize the configuration
  1. Download the bundle configuration, customize it, then deploy it

This guide describes both methods.

### Option 1: Deploy with the default configuration

Once you have a Juju machine cloud configured, deploying the charm bundle with the default configuration is relatively straightforward.

#### Step 1: Create a Juju model

```bash
juju add-model landscape-self-hosted
```

#### Step 2: Deploy `landscape-scalable`

You can deploy the `landscape-scalable` charm bundle directly.

```bash
juju deploy landscape-scalable
```

It will take some time for the bundle to finish deploying. You can watch the deployment progress with `juju status`:

```bash
juju status --watch 3s
```

`--watch` refreshes the status periodically. This example is set to refresh every three seconds.

You can also check the status at any time without `--watch`:

```bash
juju status
```

At first, the `juju status` output will indicate that all units are waiting for machines to become available:

```text
Model                  Controller           Cloud/Region         Version  SLA          Timestamp
landscape-self-hosted  localhost-localhost  localhost/localhost  3.5.5    unsupported  15:12:31-08:00

App               Version  Status   Scale  Charm             Channel        Rev  Exposed  Message
haproxy                    waiting    0/1  haproxy           latest/stable   75  yes      waiting for machine
landscape-server           waiting    0/1  landscape-server  latest/stable  124  no       waiting for machine
postgresql                 waiting    0/1  postgresql        14/stable      468  no       waiting for machine
rabbitmq-server            waiting    0/1  rabbitmq-server   3.9/stable     188  no       waiting for machine

Unit                Workload  Agent       Machine  Public address  Ports  Message
haproxy/0           waiting   allocating  0                               waiting for machine
landscape-server/0  waiting   allocating  1                               waiting for machine
postgresql/0        waiting   allocating  2                               waiting for machine
rabbitmq-server/0   waiting   allocating  3                               waiting for machine

Machine  State    Address  Inst id  Base          AZ  Message
0        pending           pending  ubuntu@22.04
1        pending           pending  ubuntu@22.04
2        pending           pending  ubuntu@22.04
3        pending           pending  ubuntu@22.04
```

Once everything is installed and settled, the `Status` for every application will be `active`:

```text
Model                  Controller           Cloud/Region         Version  SLA          Timestamp
landscape-self-hosted  localhost-localhost  localhost/localhost  3.5.5    unsupported  15:28:30-08:00

App               Version  Status  Scale  Charm             Channel        Rev  Exposed  Message
haproxy                    active      1  haproxy           latest/stable   75  yes      Unit is ready
landscape-server           active      1  landscape-server  latest/stable  124  no       Unit is ready
postgresql        14.12    active      1  postgresql        14/stable      468  no
rabbitmq-server   3.9.27   active      1  rabbitmq-server   3.9/stable     188  no       Unit is ready

Unit                 Workload  Agent  Machine  Public address  Ports           Message
haproxy/0*           active    idle   0        10.76.244.244   80,443/tcp      Unit is ready
landscape-server/0*  active    idle   1        10.76.244.6                     Unit is ready
postgresql/0*        active    idle   2        10.76.244.26    5432/tcp        Primary
rabbitmq-server/0*   active    idle   3        10.76.244.71    5672,15672/tcp  Unit is ready

Machine  State    Address        Inst id        Base          AZ  Message
0        started  10.76.244.244  juju-dded29-0  ubuntu@22.04      Running
1        started  10.76.244.6    juju-dded29-1  ubuntu@22.04      Running
2        started  10.76.244.26   juju-dded29-2  ubuntu@22.04      Running
3        started  10.76.244.71   juju-dded29-3  ubuntu@22.04      Running
```

#### Step 3: Add application units

The following commands add two units each of Landscape Server, HAProxy, PostgreSQL, and RabbitMQ. Execute them to create your high availability deployment with three units of each service.

```bash
juju add-unit landscape-server -n 2
juju add-unit haproxy -n 2
juju add-unit postgresql -n 2
juju add-unit rabbitmq-server -n 2
```

The charms for each application handle relationships between the units. The unit indicated with an asterisk (`*`) in the `juju status` output is the current leader unit.

After the new units are given machines and the charm installation and setup is complete, the result is a high availability deployment:

```text
Model                  Controller           Cloud/Region         Version  SLA          Timestamp
landscape-self-hosted  localhost-localhost  localhost/localhost  3.5.5    unsupported  15:49:11-08:00

App               Version  Status  Scale  Charm             Channel        Rev  Exposed  Message
haproxy                    active      3  haproxy           latest/stable   75  yes      Unit is ready
landscape-server           active      3  landscape-server  latest/stable  124  no       Unit is ready
postgresql        14.12    active      3  postgresql        14/stable      468  no
rabbitmq-server   3.9.27   active      3  rabbitmq-server   3.9/stable     188  no       Unit is ready

Unit                 Workload  Agent  Machine  Public address  Ports           Message
haproxy/0*           active    idle   0        10.76.244.244   80,443/tcp      Unit is ready
haproxy/1            active    idle   6        10.76.244.204   80,443/tcp      Unit is ready
haproxy/2            active    idle   7        10.76.244.41    80,443/tcp      Unit is ready
landscape-server/0*  active    idle   1        10.76.244.6                     Unit is ready
landscape-server/1   active    idle   4        10.76.244.192                   Unit is ready
landscape-server/2   active    idle   5        10.76.244.237                   Unit is ready
postgresql/0*        active    idle   2        10.76.244.26    5432/tcp        Primary
postgresql/1         active    idle   8        10.76.244.43    5432/tcp
postgresql/2         active    idle   9        10.76.244.32    5432/tcp
rabbitmq-server/0*   active    idle   3        10.76.244.71    5672,15672/tcp  Unit is ready and clustered
rabbitmq-server/1    active    idle   10       10.76.244.98    5672,15672/tcp  Unit is ready and clustered
rabbitmq-server/2    active    idle   11       10.76.244.71    5672,15672/tcp  Unit is ready and clustered

Machine  State    Address        Inst id         Base          AZ  Message
0        started  10.76.244.244  juju-dded29-0   ubuntu@22.04      Running
1        started  10.76.244.6    juju-dded29-1   ubuntu@22.04      Running
2        started  10.76.244.26   juju-dded29-2   ubuntu@22.04      Running
3        started  10.76.244.71   juju-dded29-3   ubuntu@22.04      Running
4        started  10.76.244.192  juju-dded29-4   ubuntu@22.04      Running
5        started  10.76.244.237  juju-dded29-5   ubuntu@22.04      Running
6        started  10.76.244.204  juju-dded29-6   ubuntu@22.04      Running
7        started  10.76.244.41   juju-dded29-7   ubuntu@22.04      Running
8        started  10.76.244.43   juju-dded29-8   ubuntu@22.04      Running
9        started  10.76.244.32   juju-dded29-9   ubuntu@22.04      Running
10       started  10.76.244.98   juju-dded29-10  ubuntu@22.04      Running
11       started  10.76.244.71   juju-dded29-11  ubuntu@22.04      Running
```

You now have Landscape Server set up for a high-availability deployment. Next, you need to set up your clients by {ref}`installing the Landscape Client charm <how-to-install-landscape-client>` on each client, and configuring them with [the `juju config` command](https://juju.is/docs/juju/juju-config). You may also need to change your SSL certificate configuration. See the {ref}`how-to-header-configure-haproxy-with-ssl-cert` section in this guide for more information.

### Option 2: Customize the configuration before deployment

If you would rather do all of your configuration up-front and then let Juju orchestrate everything during deployment, you can download the charm bundle's YAML file and customize it.

#### Step 1: Download the `landscape-scalable` charm bundle

```bash
juju download landscape-scalable
```

You'll get output similar to:

```text
Fetching bundle "landscape-scalable" revision 37 using "stable" channel and base "amd64/ubuntu/22.04"
Install the "landscape-scalable" bundle with:
    juju deploy ./landscape-scalable_r37.bundle
```

Then, unzip it:

```bash
unzip ./landscape-scalable_r37.bundle
```

You'll get output similar to:

```text
Archive:  ./landscape-scalable_r37.bundle
  inflating: bundle.yaml
  inflating: README.md
  inflating: manifest.yaml
```

#### Step 2: Edit the `bundle.yaml` file

You need to increase the `num_units` for each application to turn your deployment into a high availability deployment. In this example, we set each service to `num_units: 3`. This means there will be three units of each Landscape Server, HAProxy, PostgreSQL, and RabbitMQ.

```yaml
description: Landscape Scalable
name: landscape-scalable
series: jammy
docs: https://discourse.charmhub.io/t/landscape-charm-bundles/10638
applications:
  haproxy:
    charm: ch:haproxy
    channel: stable
    revision: 75
    num_units: 3
    expose: true
    options:
      default_timeouts: queue 60000, connect 5000, client 120000, server 120000
      global_default_bind_options: no-tlsv10
      services: ""
      ssl_cert: SELFSIGNED
  landscape-server:
    charm: ch:landscape-server
    channel: stable
    revision: 124
    num_units: 3
    constraints: mem=4096
    options:
      landscape_ppa: ppa:landscape/self-hosted-24.04
  postgresql:
    charm: ch:postgresql
    channel: 14/stable
    revision: 468
    num_units: 3
    options:
      plugin_plpython3u_enable: true
      plugin_ltree_enable: true
      plugin_intarray_enable: true
      plugin_debversion_enable: true
      plugin_pg_trgm_enable: true
      experimental_max_connections: 500
    constraints: mem=2048
  rabbitmq-server:
    charm: ch:rabbitmq-server
    channel: 3.9/stable
    revision: 188
    num_units: 3
    options:
      consumer-timeout: 259200000
relations:
    - [landscape-server, rabbitmq-server]
    - [landscape-server, haproxy]
    - [landscape-server:db, postgresql:db-admin]
```

#### Step 3: Deploy the `bundle.yaml` file

```bash
juju deploy ./bundle.yaml
```

It will take some time for the bundle to finish deploying, you can watch the deployment progress with `juju status`:

```bash
juju status --watch 3s
```

`--watch` refreshes the status periodically. This example is set to refresh every three seconds.

You can also check the status at any time without `--watch`:

```bash
juju status
```

At first, the `juju status` output will indicate that all units are waiting for machines to become available:

```text
Model                  Controller           Cloud/Region         Version  SLA          Timestamp
landscape-self-hosted  localhost-localhost  localhost/localhost  3.5.5    unsupported  16:20:40-08:00

App               Version  Status   Scale  Charm             Channel        Rev  Exposed  Message
haproxy                    waiting    0/3  haproxy           latest/stable   75  yes      waiting for machine
landscape-server           waiting    0/3  landscape-server  latest/stable  124  no       waiting for machine
postgresql                 waiting    0/3  postgresql        14/stable      468  no       waiting for machine
rabbitmq-server            waiting    0/3  rabbitmq-server   3.9/stable     188  no       waiting for machine

Unit                Workload  Agent       Machine  Public address  Ports  Message
haproxy/0           waiting   allocating  0                               waiting for machine
haproxy/1           waiting   allocating  1                               waiting for machine
haproxy/2           waiting   allocating  2                               waiting for machine
landscape-server/0  waiting   allocating  3                               waiting for machine
landscape-server/1  waiting   allocating  4                               waiting for machine
landscape-server/2  waiting   allocating  5                               waiting for machine
postgresql/0        waiting   allocating  6                               waiting for machine
postgresql/1        waiting   allocating  7                               waiting for machine
postgresql/2        waiting   allocating  8                               waiting for machine
rabbitmq-server/0   waiting   allocating  9                               waiting for machine
rabbitmq-server/1   waiting   allocating  10                              waiting for machine
rabbitmq-server/2   waiting   allocating  11                              waiting for machine

Machine  State    Address  Inst id  Base          AZ  Message
0        pending           pending  ubuntu@22.04
1        pending           pending  ubuntu@22.04
2        pending           pending  ubuntu@22.04
3        pending           pending  ubuntu@22.04
4        pending           pending  ubuntu@22.04
5        pending           pending  ubuntu@22.04
6        pending           pending  ubuntu@22.04
7        pending           pending  ubuntu@22.04
8        pending           pending  ubuntu@22.04
9        pending           pending  ubuntu@22.04
10       pending           pending  ubuntu@22.04
11       pending           pending  ubuntu@22.04
```

Once everything is installed and settled, the `Status` for every application will be `active`:

```text
Model                  Controller           Cloud/Region         Version  SLA          Timestamp
landscape-self-hosted  localhost-localhost  localhost/localhost  3.5.5    unsupported  16:30:52-08:00

App               Version  Status   Scale  Charm             Channel        Rev  Exposed  Message
haproxy                    waiting      3  haproxy           latest/stable   75  yes      Unit is ready
landscape-server           waiting      3  landscape-server  latest/stable  124  no       Unit is ready
postgresql                 waiting      3  postgresql        14/stable      468  no
rabbitmq-server            waiting      3  rabbitmq-server   3.9/stable     188  no       Unit is ready

Unit                 Workload  Agent  Machine  Public address  Ports           Message
haproxy/0*           active    idle   0        10.76.244.87    80,443/tcp      Unit is ready
haproxy/1            active    idle   1        10.76.244.102   80,443/tcp      Unit is ready
haproxy/2            active    idle   2        10.76.244.250   80,443/tcp      Unit is ready
landscape-server/0*  active    idle   3        10.76.244.17                    Unit is ready
landscape-server/1   active    idle   4        10.76.244.212                   Unit is ready
landscape-server/2   active    idle   5        10.76.244.170                   Unit is ready
postgresql/0*        active    idle   6        10.76.244.112   5432/tcp        Primary
postgresql/1         active    idle   7        10.76.244.166   5432/tcp
postgresql/2         active    idle   8        10.76.244.165   5432/tcp
rabbitmq-server/0*   active    idle   9        10.76.244.14    5672,15672/tcp  Unit is ready and clustered
rabbitmq-server/1    active    idle   10       10.76.244.237   5672,15672/tcp  Unit is ready and clustered
rabbitmq-server/2    active    idle   11       10.76.244.179   5672,15672/tcp  Unit is ready and clustered

Machine  State    Address        Inst id         Base          AZ  Message
0        started  10.76.244.87   juju-be1fab-0   ubuntu@22.04      Running
1        started  10.76.244.102  juju-be1fab-1   ubuntu@22.04      Running
2        started  10.76.244.250  juju-be1fab-2   ubuntu@22.04      Running
3        started  10.76.244.17   juju-be1fab-3   ubuntu@22.04      Running
4        started  10.76.244.212  juju-be1fab-4   ubuntu@22.04      Running
5        started  10.76.244.170  juju-be1fab-5   ubuntu@22.04      Running
6        started  10.76.244.112  juju-be1fab-6   ubuntu@22.04      Running
7        started  10.76.244.166  juju-be1fab-7   ubuntu@22.04      Running
8        started  10.76.244.165  juju-be1fab-8   ubuntu@22.04      Running
9        started  10.76.244.14   juju-be1fab-9   ubuntu@22.04      Running
10       started  10.76.244.237  juju-be1fab-10  ubuntu@22.04      Running
11       started  10.76.244.179  juju-be1fab-11  ubuntu@22.04      Running
```

You now have Landscape Server set up for a high-availability deployment. Next, you need to set up your clients by {ref}`installing the Landscape Client charm <how-to-install-landscape-client>` on each client, and configuring them with [the `juju config` command](https://juju.is/docs/juju/juju-config). You may also need to change your SSL certificate configuration. See the {ref}`how-to-header-configure-haproxy-with-ssl-cert` section in this guide for more information.

(how-to-header-configure-haproxy-with-ssl-cert)=
## Configure SSL certificates (pre-26.04 deployments only)

```{warning}
This section applies **only to pre-26.04 deployments** using the external HAProxy charm. For 26.04 beta+ deployments, see the TLS certificates configuration in the 26.04 deployment section above.
```

### For pre-26.04 deployments with external HAProxy charm

The older HAProxy charm uses self-signed SSL certificates by default. Landscape Clients and your browser won't trust this certificate.

**Option 1: Manual certificate configuration**

If you have a valid SSL certificate:

```bash
juju config haproxy ssl_cert="$(base64 fullchain.pem)" ssl_key="$(base64 privkey.pem)"
```

**Option 2: Let's Encrypt with certbot**

If your Landscape instance has a public IP and your FQDN resolves to it:

```bash
# On a machine with port 80 accessible
sudo certbot certonly --standalone -d $FQDN --non-interactive --agree-tos --email admin@example.com
```

This produces `fullchain.pem` and `privkey.pem` files:

```bash
juju config haproxy ssl_cert="$(base64 /etc/letsencrypt/live/$FQDN/fullchain.pem)" \
  ssl_key="$(base64 /etc/letsencrypt/live/$FQDN/privkey.pem)"
```

```{note}
Certificate renewal must be handled manually for pre-26.04 deployments. Consider migrating to 26.04 beta+ for automatic certificate management via the `tls-certificates` interface.
```
