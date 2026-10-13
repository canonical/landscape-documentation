(reference-charm-haproxy-route-endpoints)=

# HAProxy route endpoints

The Landscape Server charm exposes six HTTP route endpoints and the optional Ubuntu Installer Attach endpoint using the `haproxy-route` interface, and the optional Hostagent Messenger endpoint using `haproxy-route-tcp`. Integrate the endpoints with the HAProxy charm (`2.8/stable`). The optional endpoints are needed only when the corresponding service is enabled.

## Relation endpoints

| Endpoint                                | Service                   | URL paths                        | Protocol | Default backend port(s)                    |
| --------------------------------------- | ------------------------- | -------------------------------- | -------- | ------------------------------------------ |
| `appserver-haproxy-route`               | Landscape app server      | `/`, `/hash-id-databases`        | HTTP     | `appserver_base_port` (default `8080`)     |
| `pingserver-haproxy-route`              | Ping server               | `/ping`                          | HTTP     | `pingserver_base_port` (default `8070`)    |
| `message-server-haproxy-route`          | Message server            | `/message-system`, `/attachment` | HTTP     | `message_server_base_port` (default `8090`) |
| `api-haproxy-route`                     | REST API                  | `/api`                           | HTTP     | `api_base_port` (default `9080`)           |
| `package-upload-haproxy-route`          | Package upload            | `/upload`                        | HTTP     | `package_upload_base_port` (default `9100`) |
| `repository-haproxy-route`              | Repository mirror         | `/repository`                    | HTTP     | `appserver_base_port` (default `8080`)     |
| `hostagent-messenger-haproxy-route`     | Host agent gRPC messenger | (gRPC)                           | gRPC     | `hostagent_server_base_port` (default `50052`) |
| `ubuntu-installer-attach-haproxy-route` | Ubuntu Installer Attach   | (gRPC)                           | gRPC (HTTPS) | `ubuntu_installer_attach_base_port` (default `53354`) |

Backend ports are configurable via the charm config options shown above (e.g. `juju config landscape-server appserver_base_port=8080`). For multi-worker services (`appserver`, `pingserver`, `message-server`, `api`), the charm allocates one port per worker starting at the base port — e.g., with `worker_counts=2` and `appserver_base_port=8080`, ports `8080` and `8081` are used. Metrics paths (e.g. `/ping/metrics`, `/api/metrics`) are denied on all endpoints.

## Integration

Integrate the six HTTP endpoints with the HAProxy charm:

```bash
juju integrate landscape-server:appserver-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:pingserver-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:message-server-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:api-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:package-upload-haproxy-route haproxy:haproxy-route
juju integrate landscape-server:repository-haproxy-route haproxy:haproxy-route
```

The Hostagent Messenger and Ubuntu Installer Attach services are optional and disabled by default. If you enable the Hostagent Messenger service, integrate its endpoint with HAProxy's `haproxy-route-tcp` endpoint:

```bash
juju integrate landscape-server:hostagent-messenger-haproxy-route haproxy:haproxy-route-tcp
```

If you enable the Ubuntu Installer Attach service, integrate its endpoint with HAProxy's `haproxy-route` endpoint. HAProxy negotiates ALPN `h2` on the external port and re-encrypts traffic to the backend, so you must also provide TLS certificates to the Landscape Server units and make HAProxy trust the issuing CA, using the same TLS certificates provider for both:

```bash
juju integrate landscape-server:certificates <tls-provider>:certificates
juju integrate haproxy:receive-ca-certs <tls-provider>:send-ca-cert
juju integrate landscape-server:ubuntu-installer-attach-haproxy-route haproxy:haproxy-route
```

For more information, see {ref}`how-to-ubuntu-installer-configure-landscape-deployment`.

## HTTP redirect behaviour and `redirect_https`

The `redirect_https` charm configuration option controls whether HTTP traffic is redirected to HTTPS:

| `redirect_https` value | `appserver`, `message-server`, `api`, `package-upload` | `pingserver`, `repository` |
| ---------------------- | ------------------------------------------------------ | -------------------------- |
| `default`              | HTTP redirected to HTTPS                               | HTTP allowed               |
| `none`                 | HTTP allowed                                           | HTTP allowed               |
| `all`                  | HTTP redirected to HTTPS                               | HTTP redirected to HTTPS   |

`pingserver` and `repository` always allow plain HTTP under `default` and `none` because Landscape Clients and mirrors use HTTP for those paths.

## External gRPC ports

| Endpoint                                | External port |
| --------------------------------------- | ------------- |
| `hostagent-messenger-haproxy-route`     | `6554`        |
| `ubuntu-installer-attach-haproxy-route` | `50051`       |
