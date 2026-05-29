---
myst:
    html_meta:
        description: "Configure Landscape Outbox for Landscape 26.04+ and optionally apply overrides from defaults parsed in the service.conf."
---

(how-to-configure-outbox)=
# How to configure Landscape Outbox

The {ref}`Landscape Outbox <explanation-server-architecture-outbox>` is required for Landscape 26.04 LTS and later.

The outbox snap (`landscape-outbox`) runs sand-boxed as `root` and connects to the same databases and broker as Landscape Server.

## Identify whether additional configuration is needed

By default, outbox reads database and broker settings from `/etc/landscape/service.conf`. In many deployments, the configuration read from this file is sufficient and no extra outbox configuration is needed. Additional outbox configuration is usually needed only when one or more of these are true:

- Outbox must read from a non-default `service.conf` path.
- The outbox needs to connect to the broker or database with different settings than what Landscape server uses.
- The outbox needs a configuration option that cannot be specified in the `service.conf`.

If none of these apply, stop here.

For all available keys and environment variable mappings, see {ref}`Landscape Outbox configuration reference <reference-outbox-configuration>`.

## Apply additional configuration

Use `snap set landscape-outbox ...` to set values. For example, to configure the outbox to log with human-readable log lines:

```bash
sudo snap set landscape-outbox landscape.logging.human-readable=true
```

Values set through snap configuration will override equivalent values that can be parsed from the `service.conf`. For example, to configure the outbox to connect to the broker using a specific password:

```bash
sudo snap set landscape-outbox landscape.broker.password=<SOMEPASSWORD>
```

Even if a different password is specified in the `[broker]` section of the `service.conf`, `<SOMEPASSWORD>` will be used when the outbox connects to the broker.

## Verify configuration changes

The service will automatically restart when applying configuration changes. Verify the configuration is valid by examining the logs for errors:

```bash
sudo snap services landscape-outbox
sudo snap logs landscape-outbox -n 50
```

If there are no errors, the configuration is valid.
