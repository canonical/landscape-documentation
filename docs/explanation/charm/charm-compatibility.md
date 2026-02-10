(explanation-charm-compatibility)=

# Landscape Server charm integration compatibility

The [Landscape Server charm](https://charmhub.io/landscape-server) can be deployed with Juju when integrated with at least the following charms:

- `postgresql`
- `rabbitmq-server`

<!--TODO: update this bundle/guide too -->
For a recommended charm bundle configuration and more information about deploying Landscape Server with Juju, see {ref}`How to install Landscape Server with Juju <how-to-juju-installation>`.

Compatibility with a Landscape Server charm revision is limited to specific revisions and channels of the required charms. Incompatibility can occur if the charm’s base (e.g., `ubuntu@24.04`), architecture (e.g., `amd64`), or interfaces change.

```{tip}
Learn more about [Juju integrations](https://canonical.com/juju/integrations).
```

## TLS certificates charm interface

Starting with revision xxx, the Landscape Server charm handles load balancing internally and requires integration with a provider of the [`tls-certificates` charm interface](https://charmhub.io/integrations/tls-certificates), such as the [`self-signed-certificates-operator` charm](https://charmhub.io/self-signed-certificates), using the Landscape Server charm's `load-balancer-certificates` relation endpoint. Due to it being an interface, there are no requirements about which specific provider charm should be used with the Landscape Server charm.

<!--TODO: add link to migrating the Landscape Server charm away from the legacy HAProxy charm how-to guide-->

## K8s Operators

Landscape Server is currently only distributed as a machine (VM) charm and cannot be directly integrated with any version of K8s Charmed Operators, such as the HAProxy K8s operator or the Charmed PostgreSQL K8s operator.

## Ingress Configurator charm

The Ingress Configurator charm is used to integrate Landscape Server with external load balancers that are providers of the `haproxy-route` interface. These integrations are optional. If you use them, configure the following services to ensure correct traffic routing:

- **Hostagent Messenger:** Requires `external-grpc-port` set to `6554`.
- **Ubuntu Installer Attach:** Requires `external-grpc-port` set to `50051`.
- **HTTP ingress:** Uses HTTP traffic on port `80`. Configure the appropriate hostname and paths. Does not require `external-grpc-port`.

These settings allow an external load balancer to correctly expose the relevant service endpoints via the `haproxy-route` relation and handle traffic routing for Landscape Server.

- [Ingress Configurator on Charmhub](https://charmhub.io/ingress-configurator)

## HAProxy

Due to the deprecation of the legacy HAProxy charm, the Landscape Server charm now installs HAProxy on each unit to handle load balancing. This means that newer versions of the Landscape Server charm are now incompatible with the legacy HAProxy charm:

<!--TODO: Update with real revision numbers once released -->
```{list-table}
   :header-rows: 1

* - Landscape Server charm revision
  - HAProxy charm compatibility
* - < xxx
  - Compatible with `latest/x` channels
* - ≥ xxx
  - NOT compatible with `latest/x` (HAProxy installed internally)
```

```{note}
The Landscape Server charm cannot be integrated with the `2.8/x` channels of the HAProxy charm.
```

<!--TODO: add link to how-to guide migrating the Landscape Server charm away from the legacy HAproxy charm -->

- [HAProxy on Charmhub](https://charmhub.io/haproxy)

## Charmed PostgreSQL

The Landscape Server charm can be integrated to any of the `latest/x` or `14/x` channels of the PostgreSQL charm. However, it cannot yet be related to any of the `16/x` channels of the PostgreSQL charm due to the charm interface being restructured.

- [Charmed PostgreSQL VM on Charmhub](https://charmhub.io/postgresql)

## RabbitMQ Server

There are no charm integration incompatibilities between the Landscape Server charm and the RabbitMQ Server charm.

- [RabbitMQ Server on Charmhub](https://charmhub.io/rabbitmq-server)
