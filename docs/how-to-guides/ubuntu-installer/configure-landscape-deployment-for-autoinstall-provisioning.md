(how-to-ubuntu-installer-configure-landscape-deployment)=
# How to configure your Landscape deployment to provision workstations with Autoinstall via the Ubuntu installer

The Ubuntu installer (26.04 and later) can use Landscape to serve an autoinstall file. Your Landscape account must use OIDC authentication.

```{note}
This feature is available from Landscape server `25.10~beta.4` onwards.
```

```{note}
This feature is available on self-hosted and **select accounts on SaaS**. It is not generally available to all SaaS accounts.
```

## Background information

[Autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) is a means to automate an Ubuntu installation. Landscape integrates with the Ubuntu installer to deliver an Autoinstall file at installation time.

See the [Ubuntu installation (Subiquity) documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/index.html) for more information.

## On a Juju deployment

```{note}
This action is available on charm revision 189 and later.
```

Enable the service for a Landscape unit with the Juju action:

```sh
juju run landscape-server/<N> enable-ubuntu-installer-attach
```

If you have multiple Landscape server units, you can enable the service on each unit:

```sh
juju run landscape-server/0 enable-ubuntu-installer-attach
juju run landscape-server/1 enable-ubuntu-installer-attach
juju run landscape-server/2 enable-ubuntu-installer-attach
...
juju run landscape-server/<N> enable-ubuntu-installer-attach
```

You'll need to provide additional configuration to the Landscape server units to enable
the feature and set minimal service configuration:

```sh
juju config landscape-server additional_service_config='[ubuntu_installer_attach]
stores = main account-1
threads = 1
base_port = 53354
[features]
employee_management = true
'
```

To disable the service on a unit, run the following Juju action:

```sh
juju run landscape-server/<N> disable-ubuntu-installer-attach
```

## On a manual install

### Install the `landscape-ubuntu-installer-attach` package

Landscape requires an additional service for the Ubuntu installer attach experience. This example uses the Landscape Beta PPA.

```sh
sudo add-apt-repository ppa:landscape/self-hosted-beta
sudo apt update
sudo apt install landscape-ubuntu-installer-attach
```

### Set configuration

In your `service.conf`, include the following section if not already present:

```ini
[ubuntu_installer_attach]
stores = main account-1
threads = 1
base_port = 53354
```

Include the following configuration in the `[features]` section of your `service.conf`:

```ini
[features]
employee_management = true
```

### Configure the proxy

This feature uses gRPC and requires an upstream proxy to perform HTTP/2 and TLS termination.

#### Requirements

- The installer connects to the proxy on port 50051.
- The installer connects using HTTPS.
- The `landscape-ubuntu-installer-attach` service listens on port 53354 by default.

#### Example configuration (HAProxy)

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
