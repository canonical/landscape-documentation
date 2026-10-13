---
myst:
  html_meta:
    description: "Configure Landscape deployment for Autoinstall workstation provisioning. Enable Ubuntu installer attach service on Juju or manual deployments."
---

(how-to-ubuntu-installer-configure-landscape-deployment)=
# How to configure your Landscape deployment to provision workstations with Autoinstall via the Ubuntu installer

The Ubuntu installer (26.04 and later) can use Landscape to serve an autoinstall file. Your Landscape account must use OIDC authentication.

```{note}
This feature is available from Landscape server `25.10` onwards, and only on self-hosted deployments. It is not intended for {ref}`Quickstart <how-to-quickstart-installation>` deployments.
```

## Background information

[Autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) is a means to automate an Ubuntu installation. Landscape integrates with the Ubuntu installer to deliver an Autoinstall file at installation time.

See the [Ubuntu installation (Subiquity) documentation](https://canonical-subiquity.readthedocs-hosted.com/en/latest/index.html) for more information.

## On a Juju deployment

```{note}
This configuration is available in the `25.10/beta` channel beginning with revision 209.
```

Enable the service by setting `enable_ubuntu_installer_attach` to `true`:

```sh
juju config landscape-server enable_ubuntu_installer_attach=true
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

### Integrate with HAProxy and a TLS certificates provider

```{note}
The steps in this section require the Landscape Server `26.10` charm. The `26.04` charm exposes `ubuntu-installer-attach-haproxy-route` through the `haproxy-route-tcp` interface instead. To move a `26.04` deployment to the HTTPS route, see {ref}`how-to-ubuntu-installer-juju-upgrade`.
```

The Ubuntu installer uses gRPC, which requires HTTP/2 to be negotiated with ALPN (`h2`) during the TLS handshake. To support this, the charm and HAProxy work together:

- The `ubuntu-installer-attach` service on each Landscape Server unit serves TLS itself, using a certificate that the charm requests from a TLS certificates provider through the `certificates` relation.
- The `ubuntu-installer-attach-haproxy-route` endpoint uses the `haproxy-route` interface with the HTTPS protocol and external gRPC port `50051`. HAProxy negotiates ALPN `h2` with the installer on port 50051, and re-encrypts the traffic to the backend while verifying the backend certificate.
- HAProxy must trust the certificate authority (CA) that signed the Landscape Server unit certificates.

Use the same TLS certificates provider for HAProxy and Landscape Server. This example uses `self-signed-certificates`, which is only suitable for testing. If you already deployed a provider for HAProxy (see {ref}`how-to-migrate-to-26-04-charm`), reuse it.

```sh
juju integrate landscape-server:certificates self-signed-certificates:certificates
juju integrate haproxy:receive-ca-certs self-signed-certificates:send-ca-cert
juju integrate landscape-server:ubuntu-installer-attach-haproxy-route haproxy:haproxy-route
```

If you use a different provider, substitute it in the first two commands, using the endpoint names that provider documents (for example, `manual-tls-certificates` provides `trust_certificate` instead of `send-ca-cert`; see {ref}`how-to-migrate-to-26-04-charm`).

```{important}
The `haproxy:receive-ca-certs` integration is required. Without it, HAProxy can't verify the Landscape Server unit certificates and marks the Ubuntu Installer Attach backend as `DOWN`.
```

#### Certificate requirements

- **Public hostname:** the certificate that HAProxy presents on port 50051 is the one HAProxy manages for your Landscape hostname (through `haproxy:certificates`). It must be signed by a CA that the Ubuntu installer trusts, because the installer verifies it using its system trust store. See {ref}`how-to-ubuntu-installer-verify-connection`.
- **Backend:** the Landscape Server unit certificates only need to be trusted by HAProxy, which is why the CA must be integrated through `receive-ca-certs`. The charm configures only the server certificate and private key (`ssl_server_cert` and `ssl_server_private_key` in the `[ubuntu_installer_attach]` section of `service.conf`). It doesn't set a client CA, so clients aren't required to present certificates.

### Disable the service

Disable the service by setting `enable_ubuntu_installer_attach` to `false`:

```sh
juju config landscape-server enable_ubuntu_installer_attach=false
```

(how-to-ubuntu-installer-juju-upgrade)=
### Switch an existing deployment to the 26.10 charm

With the `26.04` charm, `landscape-server:ubuntu-installer-attach-haproxy-route` is integrated with `haproxy:haproxy-route-tcp`. In that configuration HAProxy doesn't negotiate ALPN, which gRPC clients that require HTTP/2 negotiation need. The `26.10` charm uses the `haproxy-route` interface over HTTPS instead.

1. Refresh the charm to the `26.10` track, then upgrade the packages as described in {ref}`how-to-heading-upgrade-juju`:

   ```sh
   juju refresh landscape-server --channel 26.10/stable
   ```

1. Integrate `landscape-server:certificates` with your TLS certificates provider, and integrate `haproxy:receive-ca-certs` with the same provider, as shown above.
1. Remove the old relation:

   ```sh
   juju remove-relation landscape-server:ubuntu-installer-attach-haproxy-route haproxy:haproxy-route-tcp
   ```

1. Integrate the endpoint with `haproxy:haproxy-route`:

   ```sh
   juju integrate landscape-server:ubuntu-installer-attach-haproxy-route haproxy:haproxy-route
   ```

1. Verify the connection as described in {ref}`how-to-ubuntu-installer-verify-juju`.

The installer isn't reachable on port 50051 between removing the old relation and the new one becoming active. If you use an external HAProxy through a cross-model offer, integrate with the offered `haproxy-route` endpoint instead.

(how-to-ubuntu-installer-verify-juju)=
### Verify the Juju deployment

Check that HAProxy negotiates ALPN `h2` on port 50051:

```sh
openssl s_client -alpn h2 -connect <LANDSCAPE_SERVER_HOST>:50051 </dev/null 2>/dev/null | grep "ALPN protocol"
```

Expected output:

```text
ALPN protocol: h2
```

Then follow {ref}`how-to-ubuntu-installer-verify-connection` to confirm that a gRPC client can reach the service.

### Troubleshoot

**The output has no `ALPN protocol: h2` line**

The endpoint is integrated with `haproxy:haproxy-route-tcp`, which doesn't negotiate ALPN. Run `juju status --relations` to check which HAProxy endpoint `ubuntu-installer-attach-haproxy-route` uses. To switch to `haproxy:haproxy-route`, follow {ref}`how-to-ubuntu-installer-juju-upgrade`.

**The connection fails and the HAProxy backend is `DOWN`**

HAProxy can't verify the Landscape Server unit certificates. Confirm that:

- `landscape-server:certificates` and `haproxy:receive-ca-certs` are integrated with the same TLS certificates provider.
- The `landscape-server` units have received their certificates (`juju status` shows no waiting or blocked status related to certificates).
- `enable_ubuntu_installer_attach` is `true`.

To inspect the backend state, check the HAProxy statistics or logs on the `haproxy` unit.

**The installer rejects the certificate**

The certificate on port 50051 isn't signed by a CA that the installer trusts. Use a certificate for your public hostname from a CA in the installer's trust store.

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

This feature uses gRPC and requires an upstream proxy to perform HTTP/2 and TLS termination. On a manual install, the `landscape-ubuntu-installer-attach` service listens for plaintext HTTP/2 (h2c) on the local port, which is a valid configuration for the examples below.

#### Requirements

- The installer connects to the proxy on port 50051.
- The installer connects using HTTPS.
- The `landscape-ubuntu-installer-attach` service listens on port 53354 by default.

#### Example configuration

**HAProxy**

If you're using HAProxy, add the following to `/etc/haproxy/haproxy.cfg`:

```text
frontend haproxy-0-grpc-ubuntu-installer
    bind 0.0.0.0:50051 ssl crt /var/lib/haproxy/default.pem alpn h2
    default_backend landscape-ubuntu-installer-attach-messenger

backend landscape-ubuntu-installer-attach-messenger
    mode http
    server landscape-ubuntu-installer-attach-messenger-0-0 localhost:53354 proto h2
```

**Apache**

If you're using Apache, add the following to your Apache configuration (commonly located in `/etc/apache2/sites-available/{hostname}.conf`):

```apache
Listen 50051

<VirtualHost *:50051>
  ServerName ${hostname}
  ServerAdmin webmaster@${hostname}

  Protocols h2 http/1.1

  ErrorLog /var/log/apache2/landscape_error.log
  CustomLog /var/log/apache2/landscape_access.log combined

  SSLEngine On
  SSLCertificateFile ${ssl_certificate_crt}
  SSLCertificateKeyFile ${ssl_certificate_key}
  # Disable to avoid POODLE attack
  SSLProtocol all -SSLv3 -SSLv2 -TLSv1
  SSLHonorCipherOrder On
  SSLCompression Off
  # If you have either an SSLCertificateChainFile or, a self-signed CA signed certificate
  # uncomment the line below.
  # Note: Some versions of Apache will not accept the SSLCertificateChainFile
  # directive. Try using SSLCACertificateFile instead.
  # SSLCertificateChainFile /etc/ssl/certs/landscape_server_ca.crt

  ProxyPass / h2c://localhost:53354/
  ProxyPassReverse / http://localhost:53354/
</VirtualHost>
```

Then enable `http2` (for HTTP/2 from the client) and `proxy_http2` (for HTTP/2 to the backend):

```bash
sudo a2enmod http2 proxy_http2
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

(how-to-ubuntu-installer-verify-connection)=
## Verify the connection

You should verify the connection to ensure that your server can be reached using HTTPS, and that the certificate is verifiable without additional flags. On a Juju deployment, first check ALPN negotiation as described in {ref}`how-to-ubuntu-installer-verify-juju`. The Ubuntu installer expects a valid SSL certificate that is signed by a known CA.

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
