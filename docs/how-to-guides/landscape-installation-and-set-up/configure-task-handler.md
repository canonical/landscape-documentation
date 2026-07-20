---
myst:
  html_meta:
    description: "Configure the Landscape Task Handler charm for Landscape 26.04.1 LTS and later Juju deployments."
---

(how-to-configure-task-handler)=
# How to configure the Landscape Task Handler charm

The `landscape-task-handler-operator` charm is required for Juju-managed Landscape Server 26.04.1 LTS and later deployments. It installs, manages, and configures the `landscape-task-handler` snap.

The charm automatically manages database credentials, gRPC mTLS certificates, and HAProxy routing. In most deployments, the defaults are sufficient and no additional configuration is needed. Additional configuration is usually only needed when one or more of these are true:

- You need to tune worker behavior (concurrency, batch size, retry limits).
- You need to tune cleanup retention or scheduling.
- You need to change the snap channel or the external gRPC port.
- You need human-readable logs or a non-default log level.

If none of these apply, stop here.

For all available config options, actions, and their snap-key equivalents, see the [Charmhub documentation for landscape-task-handler](https://charmhub.io/landscape-task-handler).

## Apply configuration

Use `juju config` to set values. For example, to increase worker concurrency:

```bash
juju config landscape-task-handler-operator worker-concurrency=8
```

To change the log level:

```bash
juju config landscape-task-handler-operator log-level=debug
```

## Verify configuration changes

Confirm the charm applied the configuration and services are healthy:

```bash
juju run landscape-task-handler-operator/0 check-health
```

For more detail, inspect the snap services directly:

```bash
juju ssh landscape-task-handler-operator/0 -- sudo snap services landscape-task-handler
```

The `server` and `worker` services should show **active**.
