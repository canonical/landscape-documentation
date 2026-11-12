---
myst:
  html_meta:
    description: "Harden Landscape deployment security with TLS certificates, network restrictions, and secure client configurations."
---

(how-to-harden-deployment)=

# How to harden your Landscape deployment

You have many options when hardening your Landscape deployment.

## Harden the network

The only application in your Landscape server deployment that should be exposed to incoming external traffic is the reverse proxy, which is either HAProxy or Apache. The reverse proxy listens on these frontend ports:

* **80** and **443**: HTTP and HTTPS traffic, respectively.
* **6554** (optional): gRPC over HTTP/2 traffic for the Hostagent Messenger service. Expose it only when that service is enabled.

For more details on networking, see {ref}`reference-internal-network-requirements`.

Landscape's gRPC services currently support only unencrypted HTTP/2 (h2c). External clients reach the gRPC frontends using HTTP/2 over TLS; TLS terminates at the reverse proxy, which then forwards the traffic to the backend services over h2c. Because these backend connections aren't TLS, the backend services don't negotiate ALPN, so their ports must remain internal.

If you're using Landscape's repository mirroring features, Landscape Server may need outgoing network access depending on the location of the repositories you're pulling from.

Port 80 is only needed for Landscape's repository mirroring features. If you don't use these features, then you don't need to expose Port 80. In this case, you would configure your Landscape clients to use HTTPS for all traffic:

1. Edit `/etc/landscape/client.conf` to ensure that the entries for `url`, `package_hash_id_url`, and `ping_url` all start with `https` instead of `http`
1. Restart Landscape Client: `sudo systemctl restart landscape-client`

The other applications in your deployment only require enough network access to communicate with each other. Using the default configuration, these applications use the following ports for incoming traffic:

* Landscape server: 8070-9100 (inclusive) and 50051
* PostgreSQL: 5432
* RabbitMQ server: 5672 for unencrypted TCP

Landscape doesn't listen on every port in the 8070-9100 range. For services configured with a base port, additional instances use successive ports starting at that base port, so the exact ports depend on your deployment. Make sure the ports in use are exposed for internal traffic between the applications. **None of these ports should be exposed to external traffic.**

## Secure external traffic

For more security, configure HAProxy or Apache with a TLS certificate. LetsEncrypt provides an easy way to create one: use it with HAProxy by following the {ref}`Juju HA installation guide <how-to-header-configure-haproxy-with-ssl-cert>`, or with Apache by acquiring the certificate the same way and installing it as described in the {ref}`configure web server <how-to-heading-manual-install-configure-web-server>` section of the manual installation guide. You can also use a self-signed certificate, but you'll then need to manually distribute it to any Landscape clients you want to register.

### Restrict TLS versions and cipher suites

A TLS certificate encrypts traffic, but on its own it still lets the reverse proxy negotiate old protocol versions and weak cipher suites. You can configure your proxy to disable older versions.

**Apache**

Apache is the reverse proxy for {ref}`Quickstart <how-to-quickstart-installation>` and most {ref}`Manual <how-to-manual-installation>` installations of Landscape. Its virtual host configuration is at `/etc/apache2/sites-available/landscape.conf`. In each TLS virtual host (each `<VirtualHost>` block with `SSLEngine On`), set these directives, replacing the installer's defaults:

```apache
SSLProtocol all -SSLv3 -SSLv2 -TLSv1 -TLSv1.1
SSLHonorCipherOrder On
SSLCompression Off
SSLCipherSuite HIGH:!aNULL:!NULL:!3DES:!DSS:!EXP:!PSK:!SRP:!MD5:!SHA:!CBC:!CAMELLIA
```

This disables the older SSL and TLS 1.0/1.1 protocols and restricts the TLS 1.2 cipher suites. It doesn't affect TLS 1.3 ciphers, which Apache [configures separately](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html#sslciphersuite). Then test and reload:

```bash
sudo apache2ctl -t
sudo systemctl reload apache2.service
```

**HAProxy**

For pre-26.04 {ref}`Juju <how-to-juju-ha-installation>` deployments, the classic `haproxy` charm exposes bind options for this:

```bash
juju config haproxy global_default_bind_options='no-sslv3 no-tlsv10 no-tlsv11'
juju config haproxy global_default_bind_ciphers='HIGH:!aNULL:!NULL:!3DES:!DSS:!EXP:!PSK:!SRP:!MD5:!SHA:!CBC:!CAMELLIA'
```

This disables SSL 3.0 and TLS 1.0/1.1 and restricts the TLS 1.2 cipher suites, but doesn't affect TLS 1.3. Then restart HAProxy on each unit to apply the change:

```bash
juju exec --application haproxy "sudo systemctl restart haproxy.service"
```

```{note}
Landscape 26.04 LTS and later use a different HAProxy charm, from the `2.8/stable` channel, that doesn't expose these options, so these steps apply only to pre-26.04 deployments. For that charm, see its [security documentation](https://canonical.com/juju/docs/haproxy-charm/latest/explanation/security/) for maintained guidance.
```

**Verify the result**

From a machine that can reach the reverse proxy, scan it with `nmap` (`sudo apt install nmap`) to confirm the offered protocols and ciphers. If your deployment exposes port 6554, include it in the scan as well by using `-p 443,6554`.

```bash
nmap --script ssl-enum-ciphers -p 443 <LANDSCAPE_HOST>
```

TLS 1.0 and TLS 1.1 should no longer appear.

(how-to-harden-deployment-secure-email-traffic)=
## Secure email traffic

If your deployment {ref}`relays Landscape's outgoing email notifications through Postfix <how-to-configure-postfix>`, you can require a minimum TLS version for those outgoing connections.

Landscape's Postfix configuration acts as an SMTP client that relays mail to an external SMTP provider. The Postfix guide already sets `smtp_tls_security_level=encrypt`, which requires TLS for outgoing mail. To also require a minimum protocol version and restrict the cipher suites, set the mandatory client parameters:

```bash
sudo postconf -e 'smtp_tls_mandatory_protocols=>=TLSv1.2'
sudo postconf -e 'smtp_tls_mandatory_ciphers=high'
sudo postconf -e 'smtp_tls_mandatory_exclude_ciphers=aNULL, MD5, SHA, CBC, CAMELLIA'
```

These `smtp_tls_mandatory_*` settings apply when TLS is mandatory, that is, when `smtp_tls_security_level` is `encrypt` or higher. The `>=TLSv1.2` syntax requires Postfix 3.6 or later, which is the version shipped with Ubuntu 22.04 LTS and later releases. These settings restrict the protocols and cipher suites Postfix uses when it connects to your SMTP provider; they do not configure Postfix to accept incoming SMTP connections.

Reload Postfix to apply the change:

```bash
sudo postfix reload
```

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

(how-to-harden-deployment-secure-gpg-keys)=
## Secure your GPG keys

**Select your Landscape Server version:**

`````{tab-set}

````{tab-item} Landscape Server 26.04 LTS and later

In Landscape Server 26.04 LTS and later, you don't upload a single GPG key to Landscape Server. Instead, you provide GPG keys directly on the mirrors and publications that use them:

- **Verification keys** are attached to a {ref}`mirror <how-to-heading-create-new-mirror>`. For a third-party repository that doesn't preserve the upstream signing key, provide the ASCII-armored public key in the mirror's **Verification GPG key** field. Landscape uses this key to validate the upstream repository's signature when it syncs the mirror.
- **Signing keys** are attached to a {ref}`publication <how-to-heading-create-new-publication>`. To sign (or resign) the release files of a published repository, provide the ASCII-armored GPG private key in the publication's **Signing GPG key** field. Registered clients use the corresponding public key to validate these signatures.

Keep the following in mind when managing these keys:

- Do not reuse an existing key for signing—generate a new key for this purpose.
- Because signing is automated, the signing private key must **not** be secured with a passphrase.
- If you suspect a signing key has been compromised, generate a new key, update the affected publications to use it, and republish. Distribute the new verification (public) key to any registered clients that don't already have it in their keyring, then delete the compromised key.
````

````{tab-item} Landscape Server 25.10 and earlier

If you use Landscape's repository management features, you'll need to {ref}`upload a GPG key to Landscape Server <how-to-heading-create-import-gpg-key>`. Do not reuse an existing key—you should generate a new key for this purpose.

This GPG private key is used to sign repository package indices. The public key is used by registered clients to validate these signatures. Because the use of the private key is automated, it's required that the key is **not** secured with a passphrase.

If for any reason you suspect that the key has been compromised, create a new key, upload it to Landscape, and edit your repository mirrors to use the new key. Landscape will re-sign your repository using the new key. You should then delete the previously-used key.
````

`````

## Harden Ubuntu

To harden your deployment, you also need to harden the Ubuntu installations that Landscape is deployed on. The best way to ensure your Ubuntu installations are hardened is to make them compliant with security benchmarks.

Ubuntu LTS releases with Ubuntu Pro can take advantage of the [Ubuntu Security Guide](https://ubuntu.com/security/certifications/docs) to ensure they are secure.

## Harden Juju

If you used Juju to deploy Landscape, you can follow [Juju's hardening guide](https://documentation.ubuntu.com/juju/3.6/howto/manage-your-juju-deployment/harden-your-juju-deployment/#harden-your-deployment) to harden the Juju aspects of your deployment.
