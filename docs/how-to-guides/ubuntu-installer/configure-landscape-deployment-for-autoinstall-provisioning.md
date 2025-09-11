(how-to-ubuntu-installer-configure-landscape-deployment)=
# How to configure your Landscape deployment to provision workstations with Autoinstall via the Ubuntu installer

The Ubuntu installer (24.04 and later) can use Landscape to serve an autoinstall file. Your Landscape account must use OIDC authentication.

```{note}
This feature is available from Landscape server `25.10~beta.4` onwards.
```

## Background information

[Autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) is a means to automate an Ubuntu installation. Landscape integrates with the Ubuntu installer to deliver an Autoinstall file at installation time.

> See also: [Ubuntu installation (Subiquity) documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/index.html)

## Install the `landscape-ubuntu-installer-attach` package

Landscape requires an additional service for the Ubuntu installer attach experience. This example uses the Landscape Beta PPA.

```sh
sudo add-apt-repository ppa:landscape/self-hosted-beta
sudo apt update
sudo apt install landscape-ubuntu-installer-attach
```

## Configure the proxy

This feature uses gRPC and requires an upstream proxy to perform HTTP/2 and TLS termination.

### Requirements

- The installer connects to the proxy on port 50051.
- The installer connects using HTTPS.
- The `ubuntu-installer-attach` service listens on port 53354 by default.

### Example configuration (HAProxy)

For example, if you're using HAProxy, add the following to `/etc/haproxy/haproxy.cfg`:

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
This is only useful for multi-tenant deployments.
If you are using self-hosted, you can disregard this.
```

For multi-tenant deployments, Landscape requires an `X-FQDN` header to disambiguate the tenant.

You'll need to configure this X-FQDN in your proxy settings. For example, if you're using HAProxy, add the following to `/etc/haproxy/haproxy.cfg`:

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

Set the following configuration in your `service.conf`:

```ini
[features]
[...]
employee_management = true
```

## Verify the connection

You should verify the connection to ensure that your server can be reached using HTTPS, and that the certificate is verifiable without additional flags. The Ubuntu installer expects a valid SSL certificate that is signed by a known CA.

For example:

```sh
curl -i https://<LANDSCAPE_SERVER_HOST>:50051
```

Sample output:

```text
HTTP/2 200 
content-type: application/grpc
grpc-status: 2
grpc-message: Bad method header
```
