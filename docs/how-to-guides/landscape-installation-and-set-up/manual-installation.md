(how-to-manual-installation)=
# How to install Landscape manually

```{note}
If you have an Ubuntu Pro subscription, we recommend you attach your Pro token for easy access to your Pro services. For more information, see {ref}`how-to-attach-ubuntu-pro` and {ref}`how-to-ubuntu-pro-enable-landscape`.
```

This is the baseline deployment recommendation we have for Landscape Server when Juju is not used. At a minimum, you need two machines: the database server and application server.

For a manual installation of Landscape 24.04 LTS:

 * **Database server**: runs Ubuntu 22.04 LTS ("jammy") or Ubuntu 24.04 ("noble"), with the versions of PostgreSQL that are in the Ubuntu archives for Jammy and Noble. Jammy uses PostgreSQL 14 and Noble uses PostgreSQL 16.
 * **Application server**: runs Ubuntu 22.04 LTS ("jammy") or Ubuntu 24.04 ("noble") and hosts the Landscape services

 You'll also need {ref}`certain PostgreSQL extensions <how-to-header-install-postgresql>` to setup Landscape. If you're using a managed PostgreSQL solution, check with your provider to make sure these extensions are available.

This is a long document. If you want a quick installation that just works, but doesn't scale to a large number of machines, then install the `landscape-server-quickstart` package. For more information, visit {ref}`how-to-quickstart-installation`.

## Prepare for the installation

What you will need:

 * Ubuntu server install media for the version of Ubuntu you're using
 * An Ubuntu Pro subscription
 * Server X509 certificate and key, signed by a publicly known Certificate Authority, and issued for the FQDN hostname of the application server.
 * Custom (internal) CAs can be used, but this process isn't documented here in depth because many parts of that process take place outside of Landscape. Administrators deploying custom CAs generally know what needs to be done, but there is some guidance throughout this document.

## Install the database server

After having installed the basic server profile of Ubuntu Server, we need to install the PostgreSQL database and configure it for use by Landscape. Please follow these steps:

(how-to-header-install-postgresql)=
### Install PostgreSQL and required libraries

Run one of the following commands to install the database software.

For an Ubuntu 22.04 ("jammy") database server:
```
sudo apt install postgresql postgresql-14-debversion postgresql-plpython3-14 postgresql-contrib
```

For an Ubuntu 24.04 ("noble") database server:
```
sudo apt install postgresql postgresql-16-debversion postgresql-plpython3-16 postgresql-contrib
```

### Create a superuser Landscape can use

Landscape needs a database superuser in order to create the lower privilege users it needs to perform routine tasks and access the data, as well as alter the database schema whenever needed:
```
sudo -u postgres createuser --createdb --createrole --superuser --pwprompt landscape_superuser
```

You should use a strong password.

```{note}
**Warning!** Do not use an `@` symbol in the password.
```

If this database is to be shared with other services, it's recommended that another cluster is created instead for those services (or for Landscape). Please refer to the PostgreSQL documentation in that case.

### Configure PostgreSQL

We now need to allow the application server to access this database server. Landscape uses several users for this access, so we need to allow them all. Edit the `/etc/postgresql/<version>/main/pg_hba.conf` file (where `<version>` is the installed version of postgres for example `/etc/postgresql/12/...`) and add the following to the end:
```
host all landscape,landscape_maintenance,landscape_superuser <IP-OF-APP> md5
```
Replace `<IP-OF-APP>` with the IP address of the application server, followed by `/32`. Alternatively, you can specify the network address using the CIDR notation. Some examples of valid values:

 * `192.168.122.199/32`: the IP address of the APP server
 * `192.168.122.0/24`: a network address

Now come changes to the main PostgreSQL configuration file. Edit `/etc/postgresql/<version>/main/postgresql.conf` and:

 * Find the `listen_addresses` parameter, which is probably commented, and change it to:
```
listen_addresses = '*'
```
 * Set `max_prepared_transactions` to the same value as `max_connections`. For example:
```
max_connections = 400
...
max_prepared_transactions = 400
```
Finally, restart the database service:
```
sudo systemctl restart postgresql
```

### Tune PostgreSQL

It is strongly recommended to fine tune this PostgreSQL installation according to the hardware of the server. Keeping the default settings (especially of `max_connections`) is known to be problematic.  For more information, visit [PostgreSQL's guide on tuning your PostgreSQL server](https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server).

#### Landscape-specific tips for tuning PostgreSQL

The following parameters at a minimum should be touched:

* [`shared_buffers`](http://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-SHARED-BUFFERS)
* [`effective_cache_size`](https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-EFFECTIVE-CACHE-SIZE)
* [`wal_buffers`](http://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-BUFFERS)
* [`max_connections`](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-MAX-CONNECTIONS)

A good starting value for `max_connections` is 200, even on modest hardware. As your needs grow, this number should be adjusted and re-evaluated carefully. It may be helpful to use a tuning tool like [pgtune](https://pgtune.leopard.in.ua/).

When you adjust `max_connections`, you are likely to overrun shared memory allowed by the kernel (per process) and may need to increase the [`SHMMAX`](https://www.postgresql.org/docs/current/kernel-resources.html#SYSVIPC) parameter.

If the tuning changed the value of `max_connections`, make sure you also change `max_prepared_transactions` to the same value.

## Install the application server

The application server will host the following Landscape services:

 * application server
 * message server
 * ping server
 * job handler
 * async-frontend
 * combo loader
 * api server
 * package upload service
 * package search

Additionally, other services needed by Landscape will also be running on this machine, such as:

 * apache
 * rabbitmq-server

### Add the Landscape package archive

Landscape is distributed in a public PPA. You can add it to the system with these commands, replacing `{LANDSCAPE_PPA}` with the appropriate repository:
```
sudo add-apt-repository {LANDSCAPE_PPA}
sudo apt-get update
```
   - `{LANDSCAPE_PPA}`: The PPA for the specific Landscape installation you’re using. The PPA for the most recent Landscape LTS is: `ppa:landscape/self-hosted-24.04`.  The PPA for Landscape's stable rolling release is: `ppa:landscape/latest-stable`. We recommend using an LTS for production deployments.

### Install the server package

Install the server package and its dependencies:
```
sudo apt-get install landscape-server rabbitmq-server apache2
```

### Install the license file

If you were given a license file, copy it to `/etc/landscape/license.d`:
```
sudo cp license.txt /etc/landscape/license.d
```
Make sure it's readable by the `landscape` user and root.

If you have no such file, Landscape will manage machines with Ubuntu Pro subscriptions associated with them.

### Configure rabbitmq

```{note}
If you're installing Landscape on Jammy 22.04 or later, you may want to change the default timeout of 30 minutes in RabbitMQ. For more information, see {ref}`how-to-configure-rabbitmq`.
```

Just run the following commands, replacing `<password>` with a password of your choice. It will be needed later.
```
sudo rabbitmqctl add_user landscape <password>
sudo rabbitmqctl add_vhost landscape
sudo rabbitmqctl set_permissions -p landscape landscape ".*" ".*" ".*"
sudo rabbitmqctl add_vhost landscape-hostagent
sudo rabbitmqctl set_permissions -p landscape-hostagent landscape ".*" ".*" ".*"
```

To make rabbitmq listen only on the loopback interface (127.0.0.1), edit the file `/etc/rabbitmq/rabbitmq-env.conf` with the following content:
```
NODE_IP_ADDRESS=127.0.0.1
```

Then restart it:
```
sudo systemctl restart rabbitmq-server
```

### Configure database and broker access

We now need to make some configuration changes to the `/etc/landscape/service.conf` file to tell Landscape how to use some other services:

Please make the following changes:

Section `[stores]`:

 * `host`: the IP or hostname of the database server.  If not the default PostgreSQL port (5432), add a :NNNN port definition after the hostname (e.g., 10.0.1.5:3232)
 * Ensure a strong password is set for user landscape (this differs from landscape_superuser password from earlier and will be created when setup script is executed) 

Section `[broker]`:

 * Replace the `password` value with the password chosen above when configuring rabbitmq

Section `[schema]`:

 * Change the value of `store_user` to the landscape super user we created above during the DB installation
 * Add an entry for `store_password` with the password that was chosen in that same step

Section `[landscape]`:

* Add an entry for `secret-token` and set it as a random string. You can set any string you want, but it should be reasonably long. You can use `openssl` to create a random string. For example, `openssl rand -base64 128 | tr -d '\n'`.

If you want the services to allow only certain interfaces, you can set `allowed_interfaces` in each of the services listed in the configuration file. These must be space-separated IP addresses or hostnames.

### Run the Landscape setup script

This script will bootstrap the databases Landscape needs to work and setup the remaining of the configuration:
```
sudo setup-landscape-server
```

```{note}
Depending on the hardware, this may take several minutes to complete
```

### Configure Landscape services and schema upgrades

We need to enable the Landscape services now. Please edit `/etc/default/landscape-server` and change the `RUN_ALL` line to `yes`:
```
# To run all Landscape services set this to "yes"
RUN_ALL="yes"
```
```{note}
If more performance and availability are needed out of Landscape Server, it's possible to spread out the services amongst several machines. In that case, for example, one could run message servers in one machine, application servers in another one, etc.
```

The message, application and ping services can be configured to run multiple instances. If your hardware has several cores and enough memory (4Gb or more), running two or more of each will improve performance. To run multiple instances of a service, just set the value in the respective `RUN_` line to the number of instances. For example, if you want to run two message servers, just set:
```
RUN_MSGSERVER="2"
```

```{note}
In order to take advantage of this multiple-instances setting, you need to configure some sort of load balancer or proxy. See the `README.multiple-services` file in the `landscape-server` package documentation directory for an example using Apache's `proxy_loadbalancer` module.
```

In that same file, the `UPGRADE_SCHEMA` option needs to be reviewed. If set to `yes`, whenever the package `landscape-server` is updated it will attempt to update the database schema too. It is a very convenient setting, but please think about the following before enabling it:

 * schema updates can take several minutes
 * if the package is updated while the database is offline, or unreachable, the update will fail
 * you should have a backup of the database before updating the package

Without this setting enabled, a package update might result in services that won't start anymore because of a needed schema change. In that case:

 * stop all the Landscape services
 * backup your database
 * Update the schema on the application server:
```
sudo setup-landscape-server
```
 * start all Landscape services again

(how-to-heading-manual-install-configure-web-server)=
### Configure web server

Landscape uses Apache to, among other things, redirect requests to each service and provide SSL support. The usual way to do this in Ubuntu is to create a Virtual Host for Landscape.

Below is a suggested configuration file that does just that. Install it as `/etc/apache2/sites-available/landscape.conf` and change the following values:

 * `@hostname@`: the FQDN of the hostname the clients (browser and machines) will use to connect to Landscape Server. This is what will be in the URL, and it needs to be resolvable via DNS. For example, `lds.example.com`
 * `@certfile@`: the full filesystem path to where the SSL certificate for this server is installed. For example, `/etc/ssl/certs/landscape_server.pem`
 * `@keyfile@`: the full filesystem path to where the corresponding private key of that certificate is installed. For example, `/etc/ssl/private/landscape_server.key`

If you are using a custom certificate authority for your SSL certificate, then you **MUST** put the CA public certificate in the file `/etc/ssl/certs/landscape_server_ca.crt` and uncomment the `SSLCertificateChainFile /etc/ssl/certs/landscape_server_ca.crt` line.

 Make sure the user apache runs as can read those files! Also, make sure the private key can only be read by root and that same apache user.

```
<VirtualHost *:80>

    # This Hostname is the HTTP/1.1 hostname that users and Landscape clients will access
    # It must be the same as your SSL Certificate's CommonName
    # And the DNS Hostname for this machine
    # It is not recommended that you use an IP address here...
    ServerName @hostname@
    ServerAdmin webmaster@@hostname@
    ErrorLog /var/log/apache2/landscape_error.log
    CustomLog /var/log/apache2/landscape_access.log combined
    DocumentRoot /opt/canonical/landscape/canonical/landscape

    # Set a Via header in outbound requests to the proxy, so proxied apps can
    # know who the actual client is
    ProxyVia on
    ProxyTimeout 10

    <Directory "/">
      Options +Indexes
      Order deny,allow
      Allow from all
      Require all granted
      Satisfy Any
      ErrorDocument 403 /offline/unauthorized.html
      ErrorDocument 404 /offline/notfound.html
    </Directory>

    Alias /offline /opt/canonical/landscape/canonical/landscape/offline
    Alias /static /opt/canonical/landscape/canonical/static
    Alias /repository /var/lib/landscape/landscape-repository


    <Location "/repository">
      Order deny,allow
      Deny from all
      ErrorDocument 403 default
      ErrorDocument 404 default
    </Location>
   <LocationMatch "/repository/[^/]+/[^/]+/(dists|pool)/.*">
     Allow from all
   </LocationMatch>
   <Location "/icons">
        Order allow,deny
        Allow from all
   </Location>
   <Location "/ping">
        Order allow,deny
        Allow from all
    </Location>

    <Location "/message-system">
        Order allow,deny
        Allow from all
    </Location>

   <Location "/static">
      Header always append X-Frame-Options SAMEORIGIN
   </Location>

   <Location "/r">
      FileETag none
      ExpiresActive on
      ExpiresDefault "access plus 10 years"
      Header append Cache-Control "public"
   </Location>

    RewriteEngine On

    RewriteRule ^/r/([^/]+)/(.*) /$2

    RewriteRule ^/ping$ http://localhost:8070/ping [P]

    RewriteCond %{REQUEST_URI} !^/icons
    RewriteCond %{REQUEST_URI} !^/static/
    RewriteCond %{REQUEST_URI} !^/offline/
    RewriteCond %{REQUEST_URI} !^/repository/
    RewriteCond %{REQUEST_URI} !^/message-system

    # Replace the @hostname@ with the DNS hostname for this machine.
    # If you change the port number that Apache is providing SSL on, you must change the
    # port number 443 here.
    RewriteRule ^/(.*) https://@hostname@:443/$1 [R=permanent]
</VirtualHost>

<VirtualHost *:443>
    ServerName @hostname@
    ServerAdmin webmaster@@hostname@

    ErrorLog /var/log/apache2/landscape_error.log
    CustomLog /var/log/apache2/landscape_access.log combined

    DocumentRoot /opt/canonical/landscape/canonical/landscape

    SSLEngine On
    SSLCertificateFile @certfile@
    SSLCertificateKeyFile @keyfile@
    # If you have either an SSLCertificateChainFile or, a self-signed CA signed certificate
    # uncomment the line below.
    # Note: Some versions of Apache will not accept the SSLCertificateChainFile directive.
    # Try using SSLCACertificateFile instead in that case.
    # SSLCertificateChainFile /etc/ssl/certs/landscape_server_ca.crt
    # Disable to avoid POODLE attack
    SSLProtocol all -SSLv3 -SSLv2 -TLSv1
    SSLHonorCipherOrder On
    SSLCompression Off
    SSLCipherSuite EECDH+AESGCM+AES128:EDH+AESGCM+AES128:EECDH+AES128:EDH+AES128:ECDH+AESGCM+AES128:aRSA+AESGCM+AES128:ECDH+AES128:DH+AES128:aRSA+AES128:EECDH+AESGCM:EDH+AESGCM:EECDH:EDH:ECDH+AESGCM:aRSA+AESGCM:ECDH:DH:aRSA:HIGH:!MEDIUM:!aNULL:!NULL:!LOW:!3DES:!DSS:!EXP:!PSK:!SRP:!CAMELLIA:!DHE-RSA-AES128-SHA:!DHE-RSA-AES256-SHA:!aECDH

    # Try to keep this close to the storm timeout. Not less, maybe slightly
    # more
    ProxyTimeout 305

    <Directory "/">
      Options -Indexes
      Order deny,allow
      Allow from all
      Require all granted
      Satisfy Any
      ErrorDocument 403 /offline/unauthorized.html
      ErrorDocument 404 /offline/notfound.html
    </Directory>

    <Location "/ajax">
      Order allow,deny
      Allow from all
    </Location>

    Alias /offline /opt/canonical/landscape/canonical/landscape/offline
    Alias /config /opt/canonical/landscape/apacheroot
    Alias /hash-id-databases /var/lib/landscape/hash-id-databases

    ProxyRequests off
    <Proxy *>
       Order deny,allow
       Allow from all
       ErrorDocument 403 /offline/unauthorized.html
       ErrorDocument 500 /offline/exception.html
       ErrorDocument 502 /offline/unplanned-offline.html
       ErrorDocument 503 /offline/unplanned-offline.html
    </Proxy>

    ProxyPass /robots.txt !
    ProxyPass /favicon.ico !
    ProxyPass /offline !
    ProxyPass /static !

    ProxyPreserveHost on


   <Location "/r">
      FileETag none
      ExpiresActive on
      ExpiresDefault "access plus 10 years"
      Header append Cache-Control "public"
   </Location>

   <Location "/static">
      Header always append X-Frame-Options SAMEORIGIN
   </Location>

    RewriteEngine On

    RewriteRule ^/.*\+\+.* / [F]
    RewriteRule ^/r/([^/]+)/(.*) /$2

    # See /etc/landscape/service.conf for a description of all the
    # Landscape services and the ports they run on.
    # Replace the @hostname@ with the DNS hostname for this machine.
    # If you change the port number that Apache is providing SSL on, you must change the
    # port number 443 here.
    RewriteRule ^/message-system http://localhost:8090/++vh++https:@hostname@:443/++/ [P,L]

    RewriteRule ^/ajax http://localhost:9090/ [P,L]
    RewriteRule ^/combo(.*) http://localhost:8080/combo$1 [P,L]
    RewriteRule ^/api/(.*) http://localhost:9080/api/$1 [P,L]
    RewriteRule ^/attachment/(.*) http://localhost:8090/attachment/$1 [P,L]
    RewriteRule ^/upload/(.*) http://localhost:9100/$1 [P,L]
    RewriteRule ^/(new_dashboard.*) http://localhost:8080/$1 [P,L]
    RewriteRule ^/(assets.*) http://localhost:8080/$1 [P,L]

    RewriteCond %{REQUEST_URI} !^/robots.txt$
    RewriteCond %{REQUEST_URI} !^/favicon.ico$
    RewriteCond %{REQUEST_URI} !^/offline/
    RewriteCond %{REQUEST_URI} !^/(r/[^/]+/)?static/
    RewriteCond %{REQUEST_URI} !^/config/
    RewriteCond %{REQUEST_URI} !^/hash-id-databases/

    # Replace the @hostname@ with the DNS hostname for this machine.
    # If you change the port number that Apache is providing SSL on, you must change the
    # port number 443 here.
    RewriteRule ^/(.*) http://localhost:8080/++vh++https:@hostname@:443/++/$1 [P]

    <Location /message-system>
      Order allow,deny
      Allow from all
    </Location>

    <Location />
        # Insert filter
        SetOutputFilter DEFLATE

        # Don't compress images or .debs
        SetEnvIfNoCase Request_URI \
        \.(?:gif|jpe?g|png|deb)$ no-gzip dont-vary

        # Make sure proxies don't deliver the wrong content
        Header append Vary User-Agent env=!dont-vary
    </Location>

</VirtualHost>

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
We now need to enable some modules:
```
for module in rewrite proxy_http ssl headers expires proxy_http2; do sudo a2enmod $module; done
```
Unless you require it and take necessary steps to secure that endpoint, it is recommended to disable mod-status:
```
sudo a2dismod status
```
Disable the default http vhost:
```
sudo a2dissite 000-default
```
Finally we can enable the new site:
```
sudo a2ensite landscape.conf
sudo systemctl restart apache2.service
```

### Start Landscape services

Just run the helper script `lsctl`:
```
sudo lsctl restart
```

### Create the first user

The first user that is created in Landscape automatically becomes the administrator of the "standalone" account. To create it, please go to https://\<servername\> and fill in the requested information.

### Configure the first client

On the client machine, install `landscape-client`.

```text
sudo apt update && sudo apt install -y landscape-client
```

If you are using the self-signed certificate on your Landscape Server, download your self-signed certificate from Landscape Server to the client machine with this command:

```
echo -n | openssl s_client -connect LANDSCAPE-SERVER-IP:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | sudo tee /etc/landscape/server.pem
```

To configure the Landscape Client package, run:
```
sudo landscape-config --computer-title "My First Computer" --account-name standalone --url https://<servername>/message-system --ping-url http://<servername>/ping
```

If you used a custom CA, you will need to pass the `--ssl-public-key` parameter pointing to the CA file so that the client can recognize the issuer of the server certificate.

You can now accept your client in the Landscape UI, and it will begin to upload data.

### (Optional) Add an email alias

You can configure Postfix to handle Landscape Server email notifications and alerts. To ensure that important system emails get attention, we recommend you also add an alias for Landscape on your local environment. For details, see {ref}`how-to-configure-postfix`.

