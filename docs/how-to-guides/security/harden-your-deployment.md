---
myst:
  html_meta:
    description: "Harden Landscape deployment security with TLS certificates, network restrictions, secure client configurations, and mTLS. Configure secure services and access controls."
---

(how-to-harden-deployment)=

# How to harden your Landscape deployment

You have many options when hardening your Landscape deployment.

## Harden the network

The only application in your Landscape server deployment that should be exposed to incoming external traffic is the reverse proxy, which is either HAProxy or Apache. The reverse proxies listen on ports 80 and 443 for HTTP and HTTPS traffic, respectively.

If you're using Landscape's repository mirroring features, Landscape Server may need outgoing network access depending on the location of the repositories you're pulling from.

Port 80 is only needed for Landscape's repository mirroring features. If you don't use these features, then you don't need to expose Port 80. In this case, you would configure your Landscape clients to use HTTPS for all traffic:

1. Edit `/etc/landscape/client.conf` to ensure that the entries for `url`, `package_hash_id_url`, and `ping_url` all start with `https` instead of `http`
1. Restart Landscape client: `sudo systemctl restart landscape-client`

The other applications in your deployment only require enough network access to communicate with each other. Using the default configuration, applications listen on these ports for incoming traffic:

* Landscape server: 6554, and 8080-9100, inclusive
* PostgreSQL: 5432
* RabbitMQ server: 5672 for unencrypted TCP or 5671 for TLS-encrypted TCP

Make sure these ports are exposed for internal traffic between the applications. **None of these ports should be exposed to external traffic.**

## Secure external traffic

For more security, you should configure HAProxy or Apache with a TLS certificate. LetsEncrypt provides an easy way to create a certificate, and you can use LetsEncrypt with HAProxy by following the directions in the {ref}`Juju HA installation guide for Landscape <how-to-header-configure-haproxy-with-ssl-cert>`.

You can use LetsEncrypt with Apache by following the same directions to acquire the certificate, then install it by following the [configure web server](/how-to-guides/landscape-installation-and-set-up/manual-installation.md#configure-web-server) section of the manual installation guide.

You can also use a self-signed certificate with HAProxy or Apache. If you use one, you'll need to manually distribute the certificate to any Landscape clients that you want to register.

## Secure the Landscape user

Landscape Server runs all of its services as the service account `landscape`. `landscape`'s home directory is `/var/lib/landscape`.

The `landscape` user should not be granted write permission to any other directories other than `/var/lib/landscape` and `/tmp`.

## Harden Landscape Client

Landscape Client runs _some_ of its services as `root`. This is because some management activities, such as package management, require root privileges.

If you use Landscape's script execution features, you can restrict what users Landscape can run scripts as by editing the `script_users` setting in `/etc/landscape/client.conf`.

If you want to further restrict Landscape Client's access to the system, configure it to run in "Monitor-only" mode:

1. Add the line `monitor_only = True` to `/etc/landscape/client.conf`
1. Create or edit the file `/etc/default/landscape-client` to include `DAEMON_USER=landscape`
1. Restart Landscape Client: `sudo systemctl restart landscape-client`

Keep in mind that management features will be unavailable in Monitor-only mode.

## Secure your GPG keys

If you use Landscape's repository management features, you'll need to [upload a GPG key to Landscape Server](/how-to-guides/repository-mirrors/manage-repositories-in-the-web-portal.md#create-and-import-the-gpg-key). Do not reuse an existing key—you should generate a new key for this purpose.

This GPG private key is used to sign repository package indices. The public key is used by registered clients to validate these signatures. Because the use of the private key is automated, it's required that the key is **not** secured with a passphrase.

If for any reason you suspect that the key has been compromised, create a new key, upload it to Landscape, and edit your repository mirrors to use the new key. Landscape will re-sign your repository using the new key. You should then delete the previously-used key.

## Harden Ubuntu

To harden your deployment, you also need to harden the Ubuntu installations that Landscape is deployed on. The best way to ensure your Ubuntu installations are hardened is to make them compliant with security benchmarks.

Ubuntu LTS releases with Ubuntu Pro can take advantage of the [Ubuntu Security Guide](https://ubuntu.com/security/certifications/docs) to ensure they are secure.

## Harden Juju

If you used Juju to deploy Landscape, you can follow [Juju's hardening guide](https://documentation.ubuntu.com/juju/3.6/howto/manage-your-juju-deployment/harden-your-juju-deployment/#harden-your-deployment) to harden the Juju aspects of your deployment.

## TLS and mTLS in Landscape

The transport-layer security (TLS) protocol secures communication by requiring the server to present a certificate and private key. With mutual TLS (mTLS), clients must also present a certificate issued by the same certificate authority (CA), so both sides authenticate each other.

Landscape can be configured to use basic TLS or mTLS for its internal services, and for connections to external services like RabbitMQ and HashiCorp Vault.

### CA Certificate

The CA certificate is used by servers and clients in Landscape to identify who the certificates were issued by. mTLS insists that both the client and the server present valid TLS credentials issued by the same CA. However, if a TLS server is using self-signed credentials, a client may connect to it by saving the CA certificate in its system CA bundle, or by presenting it when it attempts to connect.

To set up TLS or mTLS, you will need the CA certificate used to sign your certificates. Ensure it has the following permissions:

```sh
sudo chmod 644 /path/to/ca/ca-cert.pem
sudo chown root:root /path/to/ca/ca-cert.pem
```

### RabbitMQ

To enable TLS, obtain TLS credentials for the RabbitMQ server and provide their paths in `/etc/rabbitmq/rabbitmq.conf`, along with other required fields:

```ini
listeners.ssl.default = 5671
ssl_options.certfile = /path/to/rabbitmq/server-cert.pem
ssl_options.keyfile = /path/to/rabbitmq/server-key.pem
ssl_options.verify = verify_none
ssl_options.fail_if_no_peer_cert = false
```

Make sure the TLS credential files are owned by the `rabbitmq` user:

```sh
sudo chown rabbitmq:rabbitmq /path/to/rabbitmq/server-cert.pem /path/to/rabbitmq/server-key.pem
sudo chmod 600 /path/to/rabbitmq/server-key.pem
sudo chmod 644 /path/to/rabbitmq/server-cert.pem
```

To have the RabbitMQ server enforce mTLS, add the following fields to the config:

```ini
ssl_options.cacertfile = /path/to/ca/ca-cert.pem
auth_mechanisms.1 = EXTERNAL
ssl_cert_login_from = common_name
```

Then, add the following options: `ssl_options.verify` and `ssl_options.fail_if_no_peer_cert`:

```ini
ssl_options.verify = verify_peer
ssl_options.fail_if_no_peer_cert = true
```

Edit `/etc/rabbitmq/enabled_plugins`:

```ini
[rabbitmq_auth_mechanism_ssl].
```

Finally, restart RabbitMQ:

```sh
sudo systemctl restart rabbitmq-server
```

Landscape connects to RabbitMQ via the credentials defined in the `[broker]` section of your `service.conf` file, and it can connect via TLS or mTLS.

If RabbitMQ is listening using TLS, add the following field to the `[broker]` section:

```ini
[broker]
ssl_client_ca_cert = /path/to/ca/ca-cert.pem
```

If RabbitMQ is enforcing mTLS, delete the `password` field from the section if present and provide the paths to a TLS credential pair to enable certificate-based authentication:

```ini
[broker]
ssl_client_cert = /path/to/broker/client-cert.pem
ssl_client_private_key = /path/to/broker/client-key.pem
```

Ensure the broker credentials are owned by the `landscape` user:

```sh
sudo chown landscape:landscape /path/to/broker/client-cert.pem /path/to/broker/client-key.pem
sudo chmod 600 /path/to/broker/client-key.pem
sudo chmod 644 /path/to/broker/client-cert.pem
```

Restart Landscape:

```sh
sudo lsctl restart
```

### Landscape services

The following Landscape services can be configured to use TLS or mTLS:

- `landscape-async-frontend`
- `landscape-secrets-service`

Each service can have its own server certificate and can be configured to require clients to authenticate via their own TLS credentials.
The `secrets-service` can additionally be configured to connect to HashiCorp Vault as a client via TLS or mTLS.

#### Async Frontend

The `async-frontend` service can listen using TLS or mTLS for incoming connections.

Obtain a TLS server certificate and private key pair, and add the paths in the `[async_frontend]` section in `service.conf`:

```ini
ssl_server_cert = /path/to/async_frontend/server-cert.pem
ssl_server_private_key = /path/to/async_frontend/server-key.pem
```

Set ownership and permissions:

```sh
sudo chown landscape:landscape /path/to/async_frontend/server-cert.pem /path/to/async_frontend/server-key.pem
sudo chmod 600 /path/to/async_frontend/server-key.pem
sudo chmod 644 /path/to/async_frontend/server-cert.pem
```

To further enable mTLS, you must also provide the path to the CA cert:

```ini
ssl_server_ca_cert = /path/to/ca/ca-cert.pem
```

Restart Landscape:

```sh
sudo lsctl restart
```

#### Secrets Service (with HashiCorp Vault)

The `secrets-service` can listen using TLS or mTLS for incoming connections, and it can connect to a Vault server using TLS or mTLS. See HashiCorp's guide on [hardening your Vault server](https://developer.hashicorp.com/vault/docs/concepts/production-hardening).

Update the `vault_url` field in the `[secrets]` section of your `service.conf`, and make sure both URLs are using HTTPS:

```ini
[secrets]
service_url = https://localhost:26155
vault_url = https://localhost:8200
```

If the Vault server is listening with TLS, you must also provide the `secrets-service` with paths to the CA certificate used by Vault:

```ini
ssl_client_ca_cert = /path/to/vault/vault-ca.pem
```

To make the service itself listen using TLS, append the paths to a TLS credential pair:

```ini
ssl_server_private_key = /path/to/secrets/server-key.pem
ssl_server_cert        = /path/to/secrets/server-cert.pem
```

To connect to a Vault server that is enforcing mTLS, obtain or generate client TLS credentials issued by the same CA and append them to the section:

```ini
ssl_client_private_key = /path/to/client/client-key.pem
ssl_client_cert = /path/to/client/client-cert.pem
```

To make the Secrets Service listen using mTLS, you must also include the path to the CA cert:

```ini
ssl_server_ca_cert = /path/to/ca/ca-cert.pem
```

Set ownership and permissions:

```sh
sudo chown landscape:landscape /path/to/secrets/server-cert.pem /path/to/secrets/server-key.pem
sudo chmod 600 /path/to/secrets/server-key.pem
sudo chmod 644 /path/to/secrets/server-cert.pem
```

Restart Landscape:

```sh
sudo lsctl restart
```
