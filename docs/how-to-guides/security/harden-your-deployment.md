(how-to-harden-deployment)=
# How to harden your Landscape deployment

You have many options when hardening your Landscape deployment.

## Harden the network

The only application in your Landscape server deployment that should be exposed to incoming external traffic is the reverse proxy, which is either HAProxy or Apache. The reverse proxies listen on ports 80 and 443 for HTTP and HTTPS traffic, respectively.

If you're using Landscape's repository mirroring features, Landscape Server may need outgoing network access depending on the location of the repositories you're pulling from.

Port 80 is only needed for Landscape's repository mirroring features. If you don't use these
features, then you don't need to expose Port 80. In this case, you would configure your Landscape clients to use HTTPS for all traffic:

  1. Edit `/etc/landscape/client.conf` to ensure that the entries for `url`, `package_hash_id_url`,
     and `ping_url` all start with `https` instead of `http`
  1. Restart Landscape client: `sudo systemctl restart landscape-client`
  
The other applications in your deployment only require enough network access to communicate with each other. Using the default configuration, applications listen on these ports for incoming traffic:

  * Landscape server: 6554, and 8080-9100, inclusive
  * PostgreSQL: 5432
  * RabbitMQ server: 5672
  
Make sure these ports are exposed for internal traffic between the applications. **None of these ports should be exposed to external traffic.**

## Secure external traffic

For more security, you should configure HAProxy or Apache with a TLS certificate. LetsEncrypt provides an easy way to create a certificate, and you can use LetsEncrypt with HAProxy by following the directions in the [Juju HA installation guide for Landscape](/how-to-guides/landscape-installation-and-set-up/juju-ha-installation.md/#configure-haproxy-with-an-ssl-certificate).

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

If you used Juju to deploy Landscape, you can follow [Juju's hardening guide](https://juju.is/docs/juju/harden-your-deployment) to harden the Juju aspects of your deployment.