---
myst:
  html_meta:
    description: "Set up RabbitMQ on a separate Ubuntu 22.04 LTS or Ubuntu 24.04 LTS machine and connect a manually installed Landscape Server 26.04 LTS on Ubuntu 26.04 LTS to it."
---

(how-to-configure-remote-rabbitmq)=
# How to use a remote RabbitMQ server

Landscape requires RabbitMQ 3.x. Ubuntu 26.04 LTS (Resolute) ships RabbitMQ 4.x, which Landscape doesn't support. If you {ref}`install Landscape 26.04 LTS manually <how-to-manual-installation>` on an Ubuntu 26.04 LTS application server, RabbitMQ must run on a separate machine with Ubuntu 22.04 LTS or Ubuntu 24.04 LTS.

This guide describes how to set up RabbitMQ on that separate machine and how to configure Landscape Server to connect to it. In this guide:

- The **RabbitMQ server** is the Ubuntu 22.04 LTS or Ubuntu 24.04 LTS machine that runs RabbitMQ.
- The **application server** is the Ubuntu 26.04 LTS machine that runs the Landscape Server services.

## Network requirements

- The application server must be able to resolve and reach the RabbitMQ server.
- The RabbitMQ server must accept TCP connections from the application server on the AMQP port. The default AMQP port is `5672`.

For more information on the ports that Landscape components use, see {ref}`reference-internal-network-requirements`.

## Install and configure the RabbitMQ server

Run the following steps on the RabbitMQ server.

### Install RabbitMQ

Install the RabbitMQ package from the Ubuntu archive:

```bash
sudo apt update
sudo apt install rabbitmq-server
```

```{note}
You may want to change the default timeout of 30 minutes in RabbitMQ. See {ref}`how-to-configure-rabbitmq`.
```

### Create the Landscape user and virtual hosts

Landscape Server uses two RabbitMQ virtual hosts: `landscape` and `landscape-hostagent`. Create a `landscape` user and give it permissions on both virtual hosts. Replace `<PASSWORD>` with a strong password of your choice. You'll need it later when you configure the application server.

```bash
sudo rabbitmqctl add_user landscape <PASSWORD>
sudo rabbitmqctl add_vhost landscape
sudo rabbitmqctl set_permissions -p landscape landscape ".*" ".*" ".*"
sudo rabbitmqctl add_vhost landscape-hostagent
sudo rabbitmqctl set_permissions -p landscape-hostagent landscape ".*" ".*" ".*"
```

### Listen on the network interface

RabbitMQ must listen on a network interface that the application server can reach, not only on the loopback interface (`127.0.0.1`).

Open `/etc/rabbitmq/rabbitmq-env.conf`. If it contains `NODE_IP_ADDRESS=127.0.0.1`, remove that line or comment it out to listen on all interfaces. Alternatively, set `NODE_IP_ADDRESS` to the IP address of the RabbitMQ server interface that the application server connects to. For example:

```ini
NODE_IP_ADDRESS=192.168.122.200
```

Restart RabbitMQ:

```bash
sudo systemctl restart rabbitmq-server
```

Confirm that RabbitMQ listens on the expected address and port:

```bash
sudo ss -tlnp | grep 5672
```

### Allow connections through the firewall

If a firewall runs on the RabbitMQ server, allow connections from the application server to the AMQP port. For example, with `ufw`, replace `<IP-OF-APP>` with the IP address of the application server:

```bash
sudo ufw allow from <IP-OF-APP> to any port 5672 proto tcp
```

Only expose the AMQP port to the machines that run Landscape Server services.

## Configure Landscape Server to use the RabbitMQ server

Run the following steps on the application server.

### Install Landscape Server without RabbitMQ

On the Ubuntu 26.04 LTS application server, don't install the `rabbitmq-server` package. Install Landscape Server and Apache only:

```bash
sudo apt-get install landscape-server apache2
```

For the full installation procedure, see {ref}`how-to-manual-installation`.

### Configure the `[broker]` section

Edit the `[broker]` section of `/etc/landscape/service.conf`:

- `host`: the hostname or IP address of the RabbitMQ server.
- `port`: the AMQP port of the RabbitMQ server. The default is `5672`.
- `user`: the RabbitMQ user you created, `landscape`.
- `password`: the password you chose for the `landscape` RabbitMQ user.
- `vhost`: the main virtual host, `landscape`.
- `hostagent_virtual_host`: the virtual host for the hostagent services, `landscape-hostagent`.

For example:

```ini
[broker]
host = rabbitmq.example.com
port = 5672
user = landscape
password = <PASSWORD>
vhost = landscape
hostagent_virtual_host = landscape-hostagent
```

Keep any other settings that already exist in the `[broker]` section. For a description of each setting, see {ref}`reference-service-conf`.

### Restart Landscape Server

If Landscape Server is already set up, restart the Landscape services to apply the changes:

```bash
sudo lsctl restart
```

If you're doing a new installation, return to [Configure database and broker access](/how-to-guides/landscape-installation-and-set-up/manual-installation.md#configure-database-and-broker-access) in the manual installation guide and complete the remaining settings in `/etc/landscape/service.conf`. You've already configured `[broker]`. Then continue with the manual installation steps. After you [start the Landscape services](/how-to-guides/landscape-installation-and-set-up/manual-installation.md#start-landscape-services), return here to [verify the connection](#verify-the-connection).

## Verify the connection

From the application server, check that the RabbitMQ port is reachable. Replace `<RABBITMQ-HOST>` with the hostname or IP address of the RabbitMQ server:

```bash
nc -zv <RABBITMQ-HOST> 5672
```

After the Landscape services start, check on the RabbitMQ server that the `landscape` user has open connections from the application server:

```bash
sudo rabbitmqctl list_connections user vhost peer_host state
```

If there are no connections, check the Landscape Server logs in `/var/log/landscape-server/` on the application server. For more information, see {ref}`reference-logs`.
