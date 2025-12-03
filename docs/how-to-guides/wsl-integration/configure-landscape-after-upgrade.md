(how-to-wsl-configure-landscape-after-upgrade)=
# How to configure WSL-related services after upgrading Landscape

```{note}
This guide is only for upgrades from **Landscape 23.10** or earlier. Note that the WSL integration is still a beta feature in Landscape and not widely available yet.
```

This guide describes how to configure WSL-related services if you've upgraded from an older version of Landscape (23.10 or earlier). If this is your first time installing Landscape, you don’t need to perform these steps.

## Update the `service.conf` file

Open the `service.conf` file located in the `/etc/landscape` directory and add:

```bash
[broker]
hostagent_virtual_host = landscape-hostagent
hostagent_task_queue = landscape-server-hostagent-task-queue

[hostagent-message-consumer]
threads = 1
stores = main account-1

[features]
enable-wsl-child-instance-profiles = true
```

## Update your Apache config

Open your Apache config (commonly located in `/etc/apache2/sites-available/{hostname}.conf`) and add the following at the end:

```bash
Listen 6554

<VirtualHost *:6554>
  ServerName ${hostname}
  ServerAdmin webmaster@${hostname}

  ErrorLog /var/log/apache2/landscape_error.log
  CustomLog /var/log/apache2/landscape_access.log combined

  SSLEngine On
  SSLCertificateFile ${ssl_certificate_crt}
  SSLCertificateKeyFile ${ssl_certificate_key}
  # Disable to avoid POODLE attack
  SSLProtocol all -SSLv3 -SSLv2 -TLSv1
  SSLHonorCipherOrder On
  SSLCompression Off
  SSLCipherSuite EECDH+AESGCM+AES128:EDH+AESGCM+AES128:EECDH+AES128:EDH+AES128:ECDH+AESGCM+AES128:aRSA+AESGCM+AES128:ECDH+AES128:DH+AES128:aRSA+AES128:EECDH+AESGCM:EDH+AESGCM:EECDH:EDH:ECDH+AESGCM:aRSA+AESGCM:ECDH:DH:aRSA:HIGH:!MEDIUM:!aNULL:!NULL:!LOW:!3DES:!DSS:!EXP:!PSK:!SRP:!CAMELLIA:!DHE-RSA-AES128-SHA:!DHE-RSA-AES256-SHA:!aECDH
  # If you have either an SSLCertificateChainFile or, a self-signed CA signed certificate
  # uncomment the line below.
  # Note: Some versions of Apache will not accept the SSLCertificateChainFile
  # directive. Try using SSLCACertificateFile instead
  # SSLCertificateChainFile /etc/ssl/certs/landscape_server_ca.crt
 
  ProxyPass / h2c://localhost:50052/
  ProxyPassReverse / http://localhost:50052/
</VirtualHost>
```

Then enable `proxy_http2`:

```bash
sudo a2enmod proxy_http2
```
You can see a full Apache config example with details in our {ref}`how to configure the web server <how-to-heading-manual-install-configure-web-server>` guide.

## Add a virtual host to RabbitMQ

Add a new virtual host to RabbitMQ:

```bash
sudo rabbitmqctl add_vhost landscape-hostagent
sudo rabbitmqctl set_permissions -p landscape-hostagent landscape ".*" ".*" ".*"
```

The `".*"` characters in the `set_permissions` command are regular expressions that match any character. They grant all permissions (configure, write, read) on all resources (exchanges, queues, bindings, etc.) to the `landscape` user for the `landscape-hostagent` virtual host.

## Restart the services

Restart the Landscape services:

```bash
sudo service landscape-hostagent-messenger restart
sudo service landscape-hostagent-consumer restart
```

Now, you're ready to use WSL with Landscape. See {ref}`how-to-register-wsl-hosts`.
