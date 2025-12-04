(explanation-charm-compatibility)=

# Landscape Server charm integration compatibility

The [Landscape Server charm](https://charmhub.io/landscape-server) can be deployed with Juju when integrated with at least the following charms:

- `haproxy`
- `postgresql`
- `rabbitmq-server`

For a recommended charm bundle configuration and more information about deploying Landscape Server with Juju, see {ref}`How to install Landscape Server with Juju <how-to-juju-installation>`.

Compatibility with a Landscape Server charm revision is limited to specific revisions and channels of the required charms. Incompatibility can occur if the charm’s base (e.g., `ubuntu@24.04`), architecture (e.g., `amd64`), or interfaces change.

```{tip}
Learn more about [Juju integrations](https://canonical.com/juju/integrations).
```

## K8s Operators

Landscape Server is currently only distributed as a machine (VM) charm and cannot be directly integrated with any version of K8s Charmed Operators, such as the HAProxy K8s operator or the Charmed PostgreSQL K8s operator.

## HAProxy

The Landscape Server charm can be integrated to any of the `latest/x` channels of the HAProxy charm. However, it cannot yet be related to any of the `2.8/x` channels of the HAProxy charm due to a complete rewrite of the charm and its interfaces.

- [HAProxy on Charmhub](https://charmhub.io/haproxy)

## Charmed PostgreSQL

The Landscape Server charm can be integrated to any of the `latest/x` or `14/x` channels of the PostgreSQL charm. However, it cannot yet be related to any of the `16/x` channels of the PostgreSQL charm due to the charm interface being restructured.

- [Charmed PostgreSQL VM on Charmhub](https://charmhub.io/postgresql)

## RabbitMQ Server

There are no charm integration incompatibilities between the Landscape Server charm and the RabbitMQ Server charm.

- [RabbitMQ Server on Charmhub](https://charmhub.io/rabbitmq-server)
