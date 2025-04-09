(how-to-guides-landscape-installation-and-set-up-juju-installation)=
# How to install Landscape Server with Juju

> See also: [Landscape Server charm (Charmhub)](https://charmhub.io/landscape-server)

[note type=information]
Note: For more information on charms and bundles, visit [Charmhub](https://charmhub.io/).
[/note]

You can deploy Landscape in a scalable way with Juju.

**Contents:**
1. [Install Juju](#heading--install-juju)
1. [Deploy self-hosted Landscape Server](#heading--deploy-self-hosted-landscape-server)
1. [Access self-hosted Landscape](#heading--access-self-hosted-landscape)

## Install Juju

[Install Juju](https://canonical-juju.readthedocs-hosted.com/en/latest/user/howto/manage-juju/) as a snap with this command:

```bash
sudo snap install juju --classic
```

To learn more about Juju and to bootstrap a Juju controller, check out their [getting started](https://canonical-juju.readthedocs-hosted.com/en/latest/user/tutorial/) page.

## Deploy self-hosted Landscape Server

When deploying with Juju, you will use a Juju bundle. A bundle is an encapsulation of all of the parts needed to deploy the required services as well as associated relations and configurations that the deployment requires.


### landscape-scalable bundle

> See also: [Landscape-scalable bundle on Charmhub](https://charmhub.io/landscape-scalable)

> Also note the other bundles have been deprecated (landscape-dense and landscape-dense-maas)

**landscape-scalable** bundle is the one in which each service gets its own machine. Currently that means you will need 4 machines for Landscape, and one for the controller node. Test it out using:

```console
juju deploy landscape-scalable
```

For more detailed instructions on deploying the Landscape server with the bundle, 
refer to the [Landscape Juju High Availability Installation Guide](https://ubuntu.com/landscape/docs/juju-ha-installation).

## Access self-hosted Landscape

Once the deployment has finished, grab the address of the first `haproxy` unit and access it with your browser:

```bash
juju status haproxy
```
