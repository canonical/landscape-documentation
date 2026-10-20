---
myst:
  html_meta:
    description: "Configure a Juju deployment of Landscape for WSL. Enable the Hostagent Messenger service and serve it over HTTPS through HAProxy."
---

(how-to-wsl-configure-juju-deployment)=
# How to configure a Juju deployment of Landscape for WSL

Ubuntu Pro for WSL connects to the Hostagent Messenger service of Landscape Server on port 6554. This guide describes how to enable this service on a Landscape Server charm deployment, and how to route it through HAProxy.

## Enable the service

Enable the service by setting `enable_hostagent_messenger` to `true`:

```sh
juju config landscape-server enable_hostagent_messenger=true
```

## Integrate with HAProxy and a TLS certificates provider

```{note}
`hostagent-messenger-haproxy-route` uses the `haproxy-route` interface over HTTPS. The `haproxy-route-tcp` interface isn't supported for this endpoint, because it doesn't negotiate ALPN. If you already integrated the endpoint with `haproxy:haproxy-route-tcp`, see {ref}`how-to-wsl-juju-upgrade`.
```

Ubuntu Pro for WSL uses gRPC, which requires HTTP/2 to be negotiated with ALPN (`h2`) during the TLS handshake. To support this, the charm and HAProxy work together:

- The `landscape-hostagent-messenger` service on each Landscape Server unit serves TLS itself, using a certificate that the charm requests from a TLS certificates provider through the `certificates` relation.
- The `hostagent-messenger-haproxy-route` endpoint uses the `haproxy-route` interface with the HTTPS protocol and external gRPC port `6554`. HAProxy negotiates ALPN `h2` with Ubuntu Pro for WSL on port 6554, and re-encrypts the traffic to the backend while verifying the backend certificate.
- HAProxy must trust the certificate authority (CA) that signed the Landscape Server unit certificates.

Use the same TLS certificates provider for HAProxy and Landscape Server. This example uses `self-signed-certificates`, which is only suitable for testing. If you already deployed a provider for HAProxy (see {ref}`how-to-migrate-to-26-04-charm`), reuse it.

```sh
juju integrate landscape-server:certificates self-signed-certificates:certificates
juju integrate haproxy:receive-ca-certs self-signed-certificates:send-ca-cert
juju integrate landscape-server:hostagent-messenger-haproxy-route haproxy:haproxy-route
```

If you use a different provider, substitute it in the first two commands, using the endpoint names that provider documents. For example, `manual-tls-certificates` provides `trust_certificate` instead of `send-ca-cert`.

```{important}
The `haproxy:receive-ca-certs` integration is required. Without it, HAProxy can't verify the Landscape Server unit certificates and marks the Hostagent Messenger backend as `DOWN`.
```

The certificate that HAProxy presents on port 6554 must be trusted by the Windows machines. Ubuntu Pro for WSL uses the Windows certificate stores, or the certificate set in `ssl_public_key` of its Landscape configuration. See {ref}`how-to-register-wsl-hosts`.

## Disable the service

Disable the service by setting `enable_hostagent_messenger` to `false`:

```sh
juju config landscape-server enable_hostagent_messenger=false
```

(how-to-wsl-juju-upgrade)=
## Switch an existing deployment to `haproxy-route`

Earlier charm revisions integrated `landscape-server:hostagent-messenger-haproxy-route` with `haproxy:haproxy-route-tcp`. HAProxy doesn't negotiate ALPN on that interface, so Ubuntu Pro for WSL can only connect if the `GRPC_ENFORCE_ALPN_ENABLED` environment variable is set to `false` for its agent.

The current charm replaces that relation with `haproxy-route` over HTTPS. It doesn't keep the `haproxy-route-tcp` relation, and Juju refuses to refresh the charm while that relation exists. Remove the old relation first, then refresh and create the new relations:

1. Remove the old relation:

   ```sh
   juju remove-relation landscape-server:hostagent-messenger-haproxy-route haproxy:haproxy-route-tcp
   ```

1. Refresh the charm, then upgrade the packages as described in {ref}`how-to-heading-upgrade-juju`:

   ```sh
   juju refresh landscape-server --channel 26.04/stable
   ```

1. Integrate `landscape-server:certificates` with your TLS certificates provider, and integrate `haproxy:receive-ca-certs` with the same provider, as shown above.
1. Integrate the endpoint with `haproxy:haproxy-route`:

   ```sh
   juju integrate landscape-server:hostagent-messenger-haproxy-route haproxy:haproxy-route
   ```

1. Verify the connection as described in {ref}`how-to-wsl-verify-juju`.

Windows machines can't reach Landscape on port 6554 between removing the old relation and the new one becoming active. They reconnect automatically afterwards. If you use an external HAProxy through a cross-model offer, integrate with the offered `haproxy-route` endpoint instead.

(how-to-wsl-verify-juju)=
## Verify the deployment

Check that HAProxy negotiates ALPN `h2` on port 6554. The output should include `ALPN protocol: h2`:

```sh
openssl s_client -alpn h2 -connect <LANDSCAPE_SERVER_HOST>:6554 </dev/null 2>/dev/null | grep "ALPN protocol"
```

Then register a Windows machine as described in {ref}`how-to-register-wsl-hosts`.

## Troubleshoot

- **The output has no `ALPN protocol: h2` line:** the endpoint might still be integrated with `haproxy:haproxy-route-tcp`. Run `juju status --relations` to check, and follow {ref}`how-to-wsl-juju-upgrade`.
- **The HAProxy backend is `DOWN`:** HAProxy can't verify the Landscape Server unit certificates. Confirm that `landscape-server:certificates` and `haproxy:receive-ca-certs` are integrated with the same provider, and that `enable_hostagent_messenger` is `true`.
- **Ubuntu Pro for WSL rejects the certificate:** the certificate on port 6554 isn't signed by a CA in the Windows certificate stores, and isn't set in `ssl_public_key`.
