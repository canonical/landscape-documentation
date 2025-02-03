(how-to-guides-landscape-installation-and-set-up-juju-installation)=
# How to install Landscape Server with Juju

> See also: [Landscape Server charm (Charmhub)](https://charmhub.io/landscape-server)

```{note}
Note: For more information on charms and bundles, visit [Charmhub](https://charmhub.io/).
```

You can deploy Landscape in a scalable way with Juju.

## Install Juju

[Install Juju](https://juju.is/docs/olm/installing-juju) as a snap with this command:

```bash
sudo snap install juju --classic
```

To learn more about Juju and to bootstrap a Juju controller, check out their [getting started](https://juju.is/docs/juju/get-started-with-juju) page.

## Deploy self-hosted Landscape Server

When deploying with Juju, you will use a Juju bundle. A bundle is an encapsulation of all of the parts needed to deploy the required services as well as associated relations and configurations that the deployment requires. When deploying Landscape Server using Juju, there are three different methods you can use. Select the one that meets the needs for your environment.

### landscape-dense-maas bundle

> See also: [Landscape-dense-maas bundle on Charmhub](https://charmhub.io/landscape-dense-maas)

If you have a [MAAS](https://maas.io) server, you can take advantage of containers and use the `landscape-dense-maas` bundle:

```console
juju deploy landscape-dense-maas
```

This will deploy Landscape on just one node using LXD containers for all services.

### landscape-scalable bundle

> See also: [Landscape-scalable bundle on Charmhub](https://charmhub.io/landscape-scalable)

**landscape-scalable** each service gets its own machine. Currently that means you will need 4 machines for Landscape, and one for the controller node:

```console
juju deploy landscape-scalable
```

### landscape-dense bundle

> See also: [Landscape-dense bundle on Charmhub](https://charmhub.io/landscape-dense)

**landscape-dense** is quite similar to the `landscape-dense-maas` deployment, but it installs the `haproxy` service directly on the machine without a container. All the other services use a container:

```console
juju deploy landscape-dense
```

This is useful for the cases where the LXD containers don't get externally routable IP addresses.

## Configure an SSL cert on HAProxy

### Create a SSL certificate with LetsEncrypt

If your Landscape instance has a public IP, and your FQDN resolves to that public IP, run the following code to get a valid SSL certificate from LetsEncrypt. Replace `<EMAIL@EXAMPLE.COM>` with an email address where certificate renewal reminders can be sent.

```bash
sudo certbot certonly --standalone -d $FQDN --non-interactive --agree-tos --email <EMAIL@EXAMPLE.COM>
```

This will produce a `fullchain.pem` and `privkey.pem` file which you need for HAProxy SSL termination.

### Configure HAProxy with the certificate

Use the following commands to configure HAProxy with the generated certificate.

```bash
juju config haproxy ssl_cert="$(base64 fullchain.pem)"
juju config haproxy ssl_key="$(base64 privkey.pem)"
```

## Access self-hosted Landscape

Once the deployment has finished, grab the address of the first `haproxy` unit and access it with your browser:

```bash
juju status haproxy
```

