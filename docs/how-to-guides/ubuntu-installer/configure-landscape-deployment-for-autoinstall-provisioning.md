(how-to-ubuntu-installer-provisioning-deployment-configuration)=
# How to configure a Landscape deployment for autoinstall provisioning

The Ubuntu installer (24.04 and later) can use Landscape to serve an autoinstall file.
Your Landscape account must use OIDC authentication.

```{note}
This feature is available from Landscape server `25.10~beta.4` onwards.
```

## Background information

[Autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) is a means to automate an Ubuntu installation.
Landscape integrates with the Ubuntu installer to deliver an Autoinstall file at installation time.

## Install the `landscape-ubuntu-installer-attach` package

Landscape requires an additional service for the Ubuntu installer attach experience.

```sh
sudo add-apt-repository ppa:landscape/self-hosted-beta
sudo apt update
sudo apt install landscape-ubuntu-installer-attach
```

## Configure the proxy

This feature uses gRPC and requires an upstream proxy to perform HTTP/2 and TLS termination.

- The installer expects the service to be available at port `50051` on the proxy.
- The installer uses HTTPS by default
- Port `53354` is the default port for the `ubuntu-installer-attach` service.

For example, if using HAProxy, include the following in `/etc/haproxy/haproxy.cfg`:

```text
frontend haproxy-0-grpc-ubuntu-installer
    bind 0.0.0.0:50051 ssl crt /var/lib/haproxy/default.pem alpn h2
    default_backend landscape-ubuntu-installer-attach-messenger

backend landscape-ubuntu-installer-attach-messenger
    mode http
    server landscape-ubuntu-installer-attach-messenger-0-0 localhost:53354 proto h2
```

### (Optional) Configure the X-FQDN header

```{note}
This is only useful for multitenant deployments.
If you are using self-hosted, you can disregard this.
```

For multitenant deployments, Landscape requires an `X-FQDN` header to disambiguate the tenant.

For example, if using HAProxy, include the following in `/etc/haproxy/haproxy.cfg`:

```text
frontend haproxy-0-grpc-ubuntu-installer
    bind 0.0.0.0:50051 ssl crt /var/lib/haproxy/default.pem alpn h2
    default_backend landscape-ubuntu-installer-attach-messenger
    acl host_found hdr(host) -m found
    http-request set-var(req.full_fqdn) hdr(authority) if !host_found
    http-request set-var(req.full_fqdn) hdr(host) if host_found
    http-request set-header X-FQDN %[var(req.full_fqdn)]
```

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
