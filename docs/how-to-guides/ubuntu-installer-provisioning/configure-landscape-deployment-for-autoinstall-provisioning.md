(how-to-ubuntu-installer-provisioning-deployment-configuration)=
# How to configure a Landscape deployment for autoinstall provisioning

Recent releases of the Ubuntu installer (24.04+) can use Landscape to serve an autoinstall file.
Your Landscape account must use OIDC authentication.

```{note}
This feature is available from Landscape server `25.10~beta.4` onwards.
```

## Install the `landscape-ubuntu-installer-attach` package

Landscape requires an additional service for the Ubuntu installer attach experience.

```sh
sudo add-apt-repository ppa:landscape/self-hosted-beta
sudo apt update
sudo apt install landscape-ubuntu-installer-attach
```

## Configure the proxy

Landscape requires the `X-FQDN` header to be set in order to properly configure the autoinstall files.

For example, if using HAProxy, include the following in `/etc/haproxy/haproxy.cfg`:

```text
frontend haproxy-0-grpc-ubuntu-installer
    bind 0.0.0.0:50051 ssl crt /var/lib/haproxy/default.pem alpn h2
    acl host_found hdr(host) -m found
    http-request set-var(req.full_fqdn) hdr(authority) if !host_found
    http-request set-var(req.full_fqdn) hdr(host) if host_found
    http-request set-header X-FQDN %[var(req.full_fqdn)]
    default_backend landscape-ubuntu-installer-attach-messenger

backend landscape-ubuntu-installer-attach-messenger
    mode http
    server landscape-ubuntu-installer-attach-messenger-0-0 localhost:53354 proto h2
```

- The installer expects the service to be available at port `50051` on the proxy.
- Port `53354` is the default port for the `ubuntu-installer-attach` service.

## Enable the feature

Set the feature flag in your `service.conf`:

```ini
[features]
[...]
enable-employee-management = true
```

## Verify the connection

```sh
curl -i https://<Landscape server host>:50051
```

```text
HTTP/2 200 
content-type: application/grpc
grpc-status: 2
grpc-message: Bad method header
```

Ensure that your server can be reached using HTTPS, and that the certificate is verifiable without additional flags.
The Ubuntu installer expects a valid SSL certificate that is signed by a known CA.
