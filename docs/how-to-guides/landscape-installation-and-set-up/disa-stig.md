(howto-install-disa-stig-compliant)=

# How to install Landscape in compliance with the DISA STIG

This guide provides an overview of how to install Landscape in a DISA STIG compliant environment. DISA STIG is a set of technical security guidelines used by the U.S. Department of Defense.

## Prepare for installation

Ensure you meet the following requirements before installing Landscape:

* Ubuntu Server install media for the version of Ubuntu (Jammy 22.04 or Noble 24.04)
* Ubuntu Pro subscription
* Server X509 certificates and keys, signed by a DoD Certificate Authority, and issued for the FQDN hostname of the application server, database server, and message queuing server.
* DISA STIG compliant Ubuntu system with the FIPS OpenSSL package installed and with FIPS enabled for all Landscape nodes.
* Limits on directory sizes

### Limiting `/etc` and `/var` directory sizes

Each of the directories below store files related to the configuration, state, and logs of the Landscape Server and its dependent services. The directories for those services can be created in advance in a way that limits the amount of data they may contain. The table below recommends sizes for each directory but can be adjusted to suit your deployment requirements.

| directory  | recommended size |
|------------|--------------:|
| /etc/apache2/ | 50MB |
| /etc/landscape/ | 50MB |
| /etc/postgresql/ | 50MB |
| /etc/postgresql-common/ | 50MB |
| /etc/rabbitmq/ | 50MB |
| /var/lib/apache2/ | 10GB |
| /var/lib/landscape-server/ | 10GB |
| /var/lib/postgresql/ | 10GB |
| /var/lib/rabbitmq/ | 10GB |
| /var/log/apache2/ | 10GB |
| /var/log/landscape-server/ | 10GB |
| /var/log/postgresql/ | 10GB |
| /var/log/rabbitmq/ | 10GB |

Every directory listed above must be configured in advance of installing Landscape Server for size limits to be enforced.

If you are using Landscape Server for repository mirroring, packages will be downloaded to the `/var/lib/landscape/landscape-repository/` directory. Consider limiting the size of that directory based on the size of the pockets in each repository mirror.

The method used to limit the size of these directories depends on the environment Landscape Server is deployed to.

#### Deployment using LXD containers

Here is an example for limiting the size of the `/var/log/landscape-server/` directory to 10GB by creating a volume in an LXD storage pool and attaching it to the LXD container in which Landscape Server will be installed. For this example, that container is assumed to be named `landscape-server-container`.

1. Create a volume from the `default` storage pool (named `landscape_server_log` in this example). The storage pools for each directory must have unique names.

    ```bash
    lxc storage volume create default landscape_server_log
    ```

1. Limit the volume to 10GB.

    ```bash
    lxc storage volume set default landscape_server_log size=10GB
    ```

1. Create the log directory in the container, and attach the volume to it.

    ```bash
    lxc exec landscape-server-container -- sudo mkdir -p /var/log/landscape-server
    lxc storage volume attach default landscape_server_log landscape-server-container /var/log/landscape-server
    ```

Repeat the above process for each directory that requires limits, creating a new volume of the required size for each directory.

#### Non-containerized deployment

In non-containerized deployments, loop devices can be used to limit directory sizes. Here is an example to create a 10GB `ext4` formatted loop device mounted to the `/var/log/landscape-server` directory.

1. Create the image file.

    ```bash
    sudo dd if=/dev/zero of=/root/landscape-server-log.img bs=10G count=1
    ```

1. Format the device as an `ext4` filesystem.

    ```bash
    sudo mkft.ext4 /root/landscape-server-log.img
    ```

1. Mount it at `/var/log/landscape-server`.

    ```bash
    sudo mkdir -p /var/log/landscape-server
    sudo mount -o loop /root/landscape-server-log.img /var/log/landscape-server
    ```

1. Make the mount persistent by adding the line below to `/etc/fstab`

    ```text
    /root/landscape-server-log.img /var/log/landscape-server ext4 loop 0 2
    ```

Repeat the above process for each directory that requires limits, creating a new loop device of the required size for each directory.

## Install service dependencies

You need to install PostgreSQL, RabbitMQ, and Apache.

### Install PostgreSQL and required libraries

Run one of the following commands to install the database software.

For an Ubuntu 22.04 (`jammy`) database server:

```bash
sudo apt update
sudo apt install postgresql postgresql-14 postgresql-14-debversion postgresql-plpython3-14 postgresql-contrib postgresql-client-14 postgresql-client-common postgresql-common postgresql-14-pgaudit postgresql-14-pgauditlogtofile pgbackrest
```

For an Ubuntu 24.04 (`noble`) database server:

```bash
sudo apt update
sudo apt install postgresql postgresql-16 postgresql-16-debversion postgresql-plpython3-16 postgresql-contrib postgresql-client-16 postgresql-client-common postgresql-common postgresql-16-pgaudit postgresql-16-pgauditlogtofile pgbackrest postgresql-16-set-user
```

### Install RabbitMQ

Run the following to install RabbitMQ.

```bash
sudo apt update
sudo apt install rabbitmq-server
```

### Install Apache

Run the following to install Apache.

```bash
sudo apt update
sudo apt install apache2
```

## Requirements for certificates

Several certificates are necessary for mTLS between services and Landscape. This section describes the recommended permissions for these certificates and gives suggested locations. The rest of the guide uses these recommended paths.

### CA certificate and CRL

You need the CA certificate used to sign the other certificates.

```bash
sudo chown root:root /etc/ca-certificates.crt
sudo chmod 444 /etc/ca-certificates.crt
```

You'll also need the CRL file to revoke certificates.

```bash
sudo chown root:root /etc/crl.crl
sudo chmod 444 /etc/crl.crl
```

### Certificates for PostgreSQL

**Ubuntu 22.04 (Jammy) database server**

For an Ubuntu 22.04 database server, you'll need three certificates and their corresponding keys:

* Client authentication certificate for the `landscape` PostgreSQL user. The common name must be `landscape`. The SAN must contain the DNS or IP address of the Landscape server.

    ```bash
    sudo chown landscape:landscape /etc/landscape/postgres_client.pem
    sudo chown landscape:landscape /etc/landscape/postgres_client.key
    sudo chmod 444 /etc/landscape/postgres_client.pem
    sudo chmod 400 /etc/landscape/postgres_client.key
    ```

* Client authentication certificate for the `landscape_superuser` PostgreSQL user. The common name must be `landscape_superuser`. The SAN must contain the DNS or IP address of the Landscape server.

    ```bash
    sudo chown landscape:landscape /etc/landscape/postgres_client_superuser.pem
    sudo chown landscape:landscape /etc/landscape/postgres_client_superuser.key
    sudo chmod 444 /etc/landscape/postgres_client_superuser.pem
    sudo chmod 400 /etc/landscape/postgres_client_superuser.key
    ```

* Server authentication certificate. The SAN must contain the DNS or IP address of the database server.

    ```bash
    sudo chown postgres:postgres /etc/postgresql/postgres_server.pem
    sudo chown postgres:postgres /etc/postgresql/postgres_server.key
    sudo chmod 444 /etc/postgresql/postgres_server.pem
    sudo chmod 400 /etc/postgresql/postgres_server.key
    ```

**Ubuntu 24.04 (Noble) database server**

For an Ubuntu 24.04 database server, you'll need four certificates and their corresponding keys:

* Client authentication certificate for the `landscape` PostgreSQL user. The common name must be `landscape`. The SAN must contain the DNS or IP address of the Landscape server.

    ```bash
    sudo chown landscape:landscape /etc/landscape/postgres_client.pem
    sudo chown landscape:landscape /etc/landscape/postgres_client.key
    sudo chmod 444 /etc/landscape/postgres_client.pem
    sudo chmod 400 /etc/landscape/postgres_client.key
    ```

* Client authentication certificate for the `landscape_superuser` PostgreSQL user. The common name must be `landscape_superuser`. The SAN must contain the DNS or IP address of the Landscape server.

    ```bash
    sudo chown landscape:landscape /etc/landscape/postgres_client_superuser.pem
    sudo chown landscape:landscape /etc/landscape/postgres_client_superuser.key
    sudo chmod 444 /etc/landscape/postgres_client_superuser.pem
    sudo chmod 400 /etc/landscape/postgres_client_superuser.key
    ```

* Client authentication certificate for the `landscape_maintenance` PostgreSQL user. The common name must be `landscape_maintenance`. The SAN must contain the DNS or IP address of the Landscape server.

    ```bash
    sudo chown landscape:landscape /etc/landscape/postgres_client_maintenance.pem
    sudo chown landscape:landscape /etc/landscape/postgres_client_maintenance.key
    sudo chmod 444 /etc/landscape/postgres_client_maintenance.pem
    sudo chmod 400 /etc/landscape/postgres_client_maintenance.key
    ```

* Server authentication certificate. The SAN must contain the DNS or IP address of the database server.

    ```bash
    sudo chown postgres:postgres /etc/postgresql/postgres_server.pem
    sudo chown postgres:postgres /etc/postgresql/postgres_server.key
    sudo chmod 444 /etc/postgresql/postgres_server.pem
    sudo chmod 400 /etc/postgresql/postgres_server.key
    ```

### Certificates for RabbitMQ

For RabbitMQ, you'll need two certificates and their corresponding keys:

* Client authentication certificate for the `landscape` RabbitMQ user. The common name must be `landscape`. The SAN must contain the DNS or IP address of the Landscape server. Additionally, the CDP must be an `http` link to the CRL file.

    ```bash
    sudo chown landscape:landscape /etc/landscape/rabbitmq_client.pem
    sudo chown landscape:landscape /etc/landscape/rabbitmq_client.key
    sudo chmod 444 /etc/landscape/rabbitmq_client.pem
    sudo chmod 400 /etc/landscape/rabbitmq_client.key
    ```

* Server authentication certificate. The SAN must contain the DNS or IP address of the RabbitMQ server.

    ```bash
    sudo chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq_server.pem
    sudo chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq_server.key
    sudo chmod 444 /etc/rabbitmq/rabbitmq_server.pem
    sudo chmod 400 /etc/rabbitmq/rabbitmq_server.key
    ```

### Certificates for Apache

For Apache, you'll need one certificate and its corresponding key:

* Server authentication certificate. The common name must be the `root_url` of your Landscape instance. The SAN must contain the DNS or IP address of the Apache server and the `root_url` of your Landscape instance.

    ```bash
    sudo chown root:root /etc/apache2/apache_server.pem
    sudo chown root:root /etc/apache2/apache_server.key
    sudo chmod 444 /etc/apache2/apache2_server.pem
    sudo chmod 400 /etc/apache2/apache2_server.key
    ```

## Harden PostgreSQL

Use the following steps to harden the PostgreSQL service.

### Configure PostgreSQL user authentication

PostgreSQL must be configured to allow the Landscape application server to access the database server. Landscape uses several users for access, so all users must be added.

Edit the file `/etc/postgresql/<VERSION>/main/pg_hba.conf` (replace `<VERSION>` with your PostgreSQL version, i.e., `/etc/postgresql/14/main/pg_hba.conf` for Jammy and `/etc/postgresql/16/main/pg_hba.conf` for Noble) and add:

```ini
hostssl all landscape,landscape_maintenance,landscape_superuser <LANDSCAPE_IP_ADDRESS>/32 cert
```

Replace `<LANDSCAPE_IP_ADDRESS>` with the IP address of the server hosting Landscape services. You may also specify a network address using CIDR notation if needed.

You should also remove the lines that refer to `scram-sha-256` or other password configurations.

### Configure database settings

Edit `/etc/postgresql/<VERSION>/main/postgresql.conf` (replace `<VERSION>` with your PostgreSQL version, i.e., `/etc/postgresql/14/main/pg_hba.conf` for Jammy and `/etc/postgresql/16/main/pg_hba.conf` for Noble) to apply the following settings:

1. Limit the allowed connections.

    ```ini
    listen_addresses = 'localhost,<POSTGRES_IP_ADDRESS>'
    ```

    Replace `<POSTGRES_IP_ADDRESS>` with the IPv4 or IPv6 address of the database server.

1. Ensure `max_prepared_transactions` is the same as `max_connections`:

    ```ini
    max_connections = 400
    max_prepared_transactions = 400
    ```

1. Enable SSL with FIPS-compliant ciphers and EC curves.

    ```ini
    ssl = on

    ssl_cert_file = '/etc/postgresql/postgres_server.pem'
    ssl_key_file = '/etc/postgresql/postgres_server.key'
    ssl_ca_file = '/etc/ca-certificates.crt'
    ssl_crl_file = '/etc/crl.crl'

    ssl_ciphers = 'TLS_AES_256_GCM_SHA384,TLS_AES_128_GCM_SHA256,ECDHE-RSA-AES256-GCM-SHA384,ECDHE-RSA-AES128-GCM-SHA256,ECDHE-ECDSA-AES256-GCM-SHA384,ECDHE-ECDSA-AES128-GCM-SHA256'
    ssl_prefer_server_ciphers = on
    ssl_ecdh_curve = 'secp384r1' # for CNSA Suite B up to Top Secret
    ssl_min_protocol_version = 'TLSv1.2'
    ```

1. Configure logging and `pgaudit` (adjust `local1` to an available syslog facility):

    ```ini
    log_destination = 'syslog'
    logging_collector = on
    log_directory = '/var/log/postgresql'
    log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
    log_file_mode = 0600
    log_rotation_age = 1d
    log_rotation_size = 10MB
    log_truncate_on_rotation = on

    syslog_facility = 'local1'
    syslog_ident = 'postgres'
    syslog_sequence_numbers = on
    syslog_split_messages = on

    log_min_messages = warning
    log_min_error_statement = error

    debug_print_parse = off
    debug_print_rewritten = off
    debug_print_plan = off
    debug_pretty_print = on

    log_connections = on
    log_disconnections = on
    log_error_verbosity = default
    log_hostname = off
    log_line_prefix = 'user=%u,db=%d,app=%a,client=%h'
    log_statement = 'ddl'
    log_replication_commands = on
    log_timezone = 'Etc/UTC'

    shared_preload_libraries = 'pgaudit'

    pgaudit.log_catalog = 'on'
    pgaudit.log_level = 'log'
    pgaudit.log_parameter = 'on'
    pgaudit.log_relation = 'on'
    pgaudit.log_statement_once = 'off'
    pgaudit.log = 'all, -misc'
    ```

1. Invalidate session identifiers for user logout and session termination to prevent replay attacks, MITM attacks, and session hijacking:

    ```ini
    client_min_messages = error
    row_security = on
    statement_timeout = 10000    # milliseconds

    tcp_keepalives_idle = 10     # seconds
    tcp_keepalives_interval = 10 # seconds
    tcp_keepalives_count = 10
    ```

### Set permissions for PostgreSQL files

Set secure permissions for the certificates and PostgreSQL configuration files. `<VERSION>` should be either `14` or `16` depending on whether you are on Jammy or Noble.

```bash
export VERSION=<VERSION>
sudo chmod 600 /etc/postgresql/$VERSION/main/postgresql.conf
sudo chmod 600 /etc/postgresql/$VERSION/main/pg_hba.conf
sudo chown postgres:postgres /etc/postgresql/$VERSION/main/postgresql.conf
sudo chown postgres:postgres /etc/postgresql/$VERSION/main/pg_hba.conf
```

### Configure `rsyslog` for PostgreSQL

Configure logging and auditing with `rsyslog` to support remote log transport to a SIEM for enterprise visibility:

```{note}
For STIG compliance, `rsyslog` should not run as the root user. Instead, it must run under the disabled, deprivileged `syslog` service account.
```

1. Set permissions on the PostgreSQL log file:

    ```bash
    sudo touch /var/log/postgresql/postgresql.log
    sudo chown syslog:postgres /var/log/postgresql/postgresql.log
    sudo chmod 640 /var/log/postgresql/postgresql.log
    ```

1. Create the `rsyslog` configuration file `/etc/rsyslog.d/10-postgresql.conf` with the following contents:

    ```ini
    # Local facility for PostgreSQL
    if $msg contains ['package.name', 'package.version'] then stop

    $CreateDirs on
    $DirGroup postgres
    $DirOwner root
    $FileGroup postgres
    $FileOwner syslog
    $DirCreateMode 1775
    $FileCreateMode 0640
    $FileOwner syslog
    $FileGroup syslog
    local1.*          /var/log/postgresql/postgresql.log
    ```

    ```{note}
    If you provided a different facility than `local1` in the above PostgreSQL configuration for `syslog_facility`, adjust `local1.*` to match the new facility.
    ```

1. Set permissions for the `rsyslog` configuration file:

    ```bash
    sudo chmod 644 /etc/rsyslog.d/10-postgresql.conf
    ```

1. Restart the `rsyslog` service:

    ```bash
    sudo systemctl restart rsyslog
    ```

### Disable command history

To prevent sensitive commands from being stored in shell history for all users:

```bash
sudo sh -c "echo 'PSQL_HISTORY=/dev/null' >> /etc/environment"
```

### Configure `postgres` user access

Ensure administrators have access to manage PostgreSQL securely:

```bash
sudo groupadd dba
sudo sh -c "echo '%dba ALL=(postgres) PASSWD: ALL' > /etc/sudoers.d/postgres"
sudo chmod 600 /etc/sudoers.d/postgres
sudo usermod -a -G dba <USERNAME>
```

Replace `<USERNAME>` with the system user that will have administrative privileges.

### Configure `pgBackRest`

Set up `pgBackRest` to manage backups and restores for Landscape databases. Refer to the [official user guide](https://pgbackrest.org/user-guide.html)

### Tune PostgreSQL

It is strongly recommended to fine tune this PostgreSQL installation according to the hardware of the server. Keeping the default settings (especially of `max_connections`) is known to be problematic.  For more information, visit [PostgreSQL's guide on tuning your PostgreSQL server](https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server).

```{note}
Landscape-specific tips for tuning PostgreSQL

The following parameters at a minimum should be touched:

* [`shared_buffers`](http://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-SHARED-BUFFERS)
* [`effective_cache_size`](https://www.postgresql.org/docs/current/runtime-config-query.html#GUC-EFFECTIVE-CACHE-SIZE)
* [`wal_buffers`](http://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-WAL-BUFFERS)
* [`max_connections`](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-MAX-CONNECTIONS)

A good starting value for `max_connections` is 400, even on modest hardware. As your needs grow, this number should be adjusted and re-evaluated carefully. It may be helpful to use a tuning tool like [pgtune](https://pgtune.leopard.in.ua/).

When you adjust `max_connections`, you are likely to overrun shared memory allowed by the kernel (per process) and may need to increase the [`SHMMAX`](https://www.postgresql.org/docs/current/kernel-resources.html#SYSVIPC) parameter.

If the tuning changed the value of `max_connections`, make sure you also change `max_prepared_transactions` to the same value.
```

### Apply PostgreSQL hardening changes

Restart the PostgreSQL service to apply configuration changes:

```bash
sudo systemctl restart postgresql
```

### Sample PostgreSQL files

Click on the links to download the following sample files. Remember to replace any placeholder values with the correct ones for your configuration.

* [`/etc/postgresql/<VERSION>/main/postgresql.conf`](/assets/disa-stig/postgresql.conf)
* [`/etc/postgresql/<VERSION>/main/pg_hba.conf`](/assets/disa-stig/pg_hba.conf)
* [`/etc/rsyslog.d/10-postgresql.conf`](/assets/disa-stig/10-postgresql.conf)

## Configure PostgreSQL for Landscape

### Create database superuser and regular user

Landscape needs a database superuser to update the schema when needed:

```bash
sudo -u postgres createuser --createdb --createrole --superuser landscape_superuser
```

Landscape also needs a regular user to store and retrieve information from the database.

```bash
sudo -u postgres createuser --no-createdb --no-createrole --no-superuser landscape
```

For Ubuntu 24.04+, Landscape also needs a maintenance user which will be used to escalate permissions for schema migrations. If you are on Ubuntu 22.04 (Jammy), skip this step.

```bash
sudo -u postgres createuser --no-createdb --no-createrole --no-superuser landscape_maintenance
```

### Create databases

Landscape uses multiple databases. To create them:

```bash
sudo -u postgres createdb --owner=postgres --template=template0 --encoding=UTF8 --lc-ctype=C.UTF-8 --lc-collate=C.UTF-8 landscape-standalone-account-1
sudo -u postgres createdb --owner=postgres --template=template0 --encoding=UTF8 --lc-ctype=C.UTF-8 --lc-collate=C.UTF-8 landscape-standalone-knowledge
sudo -u postgres createdb --owner=postgres --template=template0 --encoding=UTF8 --lc-ctype=C.UTF-8 --lc-collate=C.UTF-8 landscape-standalone-main
sudo -u postgres createdb --owner=postgres --template=template0 --encoding=UTF8 --lc-ctype=C.UTF-8 --lc-collate=C.UTF-8 landscape-standalone-package
sudo -u postgres createdb --owner=postgres --template=template0 --encoding=UTF8 --lc-ctype=C.UTF-8 --lc-collate=C.UTF-8 landscape-standalone-resource-1
sudo -u postgres createdb --owner=postgres --template=template0 --encoding=UTF8 --lc-ctype=C.UTF-8 --lc-collate=C.UTF-8 landscape-standalone-session
```

(header-set-user)=

### Enable the `set_user` extension

If you are on a Noble instance, you will have the PostgreSQL `set_user` extension. This allows Landscape to escalate from a normal user to a superuser for schema migrations. To enable it:

1. Enable the extension on each database.

    ```bash
    sudo -u postgres psql landscape-standalone-account-1  -c "CREATE EXTENSION IF NOT EXISTS set_user"
    sudo -u postgres psql landscape-standalone-knowledge  -c "CREATE EXTENSION IF NOT EXISTS set_user"
    sudo -u postgres psql landscape-standalone-main       -c "CREATE EXTENSION IF NOT EXISTS set_user"
    sudo -u postgres psql landscape-standalone-package    -c "CREATE EXTENSION IF NOT EXISTS set_user"
    sudo -u postgres psql landscape-standalone-resource-1 -c "CREATE EXTENSION IF NOT EXISTS set_user"
    sudo -u postgres psql landscape-standalone-session    -c "CREATE EXTENSION IF NOT EXISTS set_user"
    ```

1. Grant execute permissions.

    ```bash
    sudo -u postgres psql landscape-standalone-account-1  -c "GRANT EXECUTE ON FUNCTION set_user_u(text) TO landscape_maintenance"
    sudo -u postgres psql landscape-standalone-knowledge  -c "GRANT EXECUTE ON FUNCTION set_user_u(text) TO landscape_maintenance"
    sudo -u postgres psql landscape-standalone-main       -c "GRANT EXECUTE ON FUNCTION set_user_u(text) TO landscape_maintenance"
    sudo -u postgres psql landscape-standalone-package    -c "GRANT EXECUTE ON FUNCTION set_user_u(text) TO landscape_maintenance"
    sudo -u postgres psql landscape-standalone-resource-1 -c "GRANT EXECUTE ON FUNCTION set_user_u(text) TO landscape_maintenance"
    sudo -u postgres psql landscape-standalone-session    -c "GRANT EXECUTE ON FUNCTION set_user_u(text) TO landscape_maintenance"
    ```

1. Disable direct login for the superuser.

    ```bash
    sudo -u postgres psql -c "ALTER USER landscape_superuser NOLOGIN"
    ```

### Limit concurrent connections

To prevent denial-of-service due to resource exhaustion, limit the number of concurrent connections for PostgreSQL users:

```bash
sudo -u postgres psql -c "ALTER USER landscape CONNECTION LIMIT 100"
sudo -u postgres psql -c "ALTER USER landscape_superuser CONNECTION LIMIT 8"
```

If you have the PostgreSQL `set_user` extension enabled, additionally set the limit for the `landscape_maintenance` user.

```bash
sudo -u postgres psql -c "ALTER USER landscape_maintenance CONNECTION LIMIT 8"
```

### Require reauthentication for privilege escalation

High governance environments require users to reauthenticate for privilege escalation. To force reauthentication for all users:

```bash
sudo -u postgres psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE user LIKE '%'"
```

## Harden RabbitMQ

RabbitMQ must be configured for the application server to access the message queueing server.

### Configure connections

Create the `/etc/rabbitmq/rabbitmq.conf` file and adjust the following parameters:

1. Enable SSL with FIPS-compliant ciphers and EC curves.

    ```ini
    listeners.tcp = none
    listeners.ssl.default = <RABBIT_IP_ADDRESS>:5671
    num_acceptors.ssl = 30
    ssl_options.cacertfile = /etc/ca-certificates.crt
    ssl_options.certfile = /etc/rabbitmq/rabbitmq_server.pem
    ssl_options.keyfile = /etc/rabbitmq/rabbitmq_server.key
    ssl_options.verify = verify_peer
    auth_mechanisms.1 = EXTERNAL
    ssl_cert_login_from = common_name

    ssl_options.fail_if_no_peer_cert = true
    ssl_options.honor_cipher_order = true
    ssl_options.honor_ecc_order = true
    ssl_options.versions.1 = tlsv1.3
    ssl_options.versions.2 = tlsv1.2
    ssl_options.ciphers.1 = TLS_AES_256_GCM_SHA384
    ssl_options.ciphers.2 = TLS_AES_128_GCM_SHA256
    ssl_options.ciphers.3 = ECDHE-ECDSA-AES256-GCM-SHA384
    ssl_options.ciphers.4 = ECDHE-RSA-AES256-GCM-SHA384
    ssl_options.ciphers.5 = ECDHE-ECDSA-AES128-GCM-SHA256
    ssl_options.ciphers.6 = ECDHE-RSA-AES128-GCM-SHA256
    ssl_options.bypass_pem_cache = true
    ssl_handshake_timeout = 5000
    ```

    Replace `<RABBIT_IP_ADDRESS>` with the RabbitMQ node's interface address.

1. Configure logging and auditing (adjust `local2` to an available syslog facility):

    ```ini
    log.syslog = true
    log.syslog.transport = tcp
    log.syslog.protocol = rfc3164
    log.syslog.host = 127.0.0.1
    log.syslog.port = 514

    log.syslog.identity = rabbitmq
    log.syslog.facility = local2

    # Log levels for logging
    log.file.level = info
    log.connection.level = info
    log.channel.level = error
    log.queue.level = error
    log.federation.level = info
    log.upgrade.level = error
    log.default.level = info

    # Log level formatting
    log.file.formatter.time_format = rfc3339_space
    log.file.formatter.level_format = lc
    log.console.formatter.plaintext.format = $time [$level] $pid $msg
    ```

1. Configure strong password hashing:

    ```ini
    password_hashing_module = rabbit_password_hashing_sha512
    ```

1. Enforce strong password complexity:

    ```ini
    credential_validator.validation_backend = rabbit_credential_validator_password_regexp
    credential_validator.regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!%*#?&]{15,}$"
    ```

1. Limit connections:

    ```ini
    channel_max = 128
    connection_max = 64
    ```

1. Secure inter-node communication

    ```ini
    distribution.listener.interface = <LISTENER_IP_ADDRESS>
    distribution.listener.port_range.min = 25672
    distribution.listener.port_range.max = 25672
    ```

    Replace `<LISTENER_IP_ADDRESS>` with the specific IP address on which the RabbitMQ listener should bind.

1. Invalidate session identifiers for user logout and session termination to prevent replay attacks, MITM attacks, and session hijacking:

    ```ini
    heartbeat = 60
    frame_max = 131072
    initial_frame_max = 4096
    channel_max = 128
    tcp_listen_options.backlog = 128
    tcp_listen_options.nodelay = true
    tcp_listen_options.exit_on_close = false

    tcp_listen_options.keepalive = true
    tcp_listen_options.send_timeout = 15000

    tcp_listen_options.buffer = 196608
    tcp_listen_options.sndbuf = 196608
    tcp_listen_options.recbuf = 196608
    ```

### Configure certificate revocation lists

Create the `/etc/rabbitmq/advanced.config` file to enable CRL checking. If your certificates do not have a CRL Distribution Point (CDP) configured to point to your CRL, skip this step.

```erlang
[
    {rabbit, [
        {ssl_listeners, [{'<RABBIT_IP_ADDRESS>',5671}]},
        {ssl_options, [
            {cacertfile, "/etc/ca-certificates.crt"},
            {certfile, "/etc/rabbitmq/rabbitmq_server.pem"},
            {keyfile, "/etc/rabbitmq/rabbitmq_server.key"},
            {verify, verify_peer},
            {fail_if_no_peer_cert, true},
            {crl_check, true},
            {crl_cache, {ssl_crl_cache, {internal, [{http, 50000}]}}}
        ]}
    ]}
].
```

Replace `<RABBIT_IP_ADDRESS>` with the RabbitMQ node's interface address.

### Configure SSL authentication

Create the `/etc/rabbitmq/enabled_plugins` file and enable SSL authentication and authorization:

```erlang
[rabbitmq_auth_mechanism_ssl].
```

### Configure RabbitMQ environment variables

Edit the `/etc/rabbitmq/rabbitmq-env.conf` file and set these environment variables:

```ini
NODE_IP_ADDRESS=127.0.0.1
NODE_PORT=5672
CONFIG_FILE=/etc/rabbitmq/rabbitmq.conf
ADVANCED_CONFIG_FILE=/etc/rabbitmq/advanced.config
```

### Configure `rabbitmq` user access

Ensure administrators have access to manage RabbitMQ securely:

```bash
sudo groupadd mq
sudo sh -c "echo '%mq ALL=(rabbitmq) PASSWD: ALL' > /etc/sudoers.d/rabbitmq"
sudo chmod 600 /etc/sudoers.d/rabbitmq
sudo usermod -a -G mq <USERNAME>
```

Replace `<USERNAME>` with the system user that will have administrative privileges.

### Set permissions for RabbitMQ files

Set secure permissions for RabbitMQ certificates and configuration files:

```bash
sudo chmod 600 /etc/rabbitmq/rabbitmq.conf
sudo chmod 600 /etc/rabbitmq/rabbitmq-env.conf
sudo chmod 600 /etc/rabbitmq/advanced.config
sudo chmod 600 /etc/rabbitmq/enabled_plugins
sudo chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.conf
sudo chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq-env.conf
sudo chown rabbitmq:rabbitmq /etc/rabbitmq/advanced.config
sudo chown rabbitmq:rabbitmq /etc/rabbitmq/enabled_plugins
```

### Configure `rsyslog` for RabbitMQ

Configure logging and auditing with `rsyslog` to support remote log transport to a SIEM for enterprise visibility:

```{note}
For STIG compliance, `rsyslog` should not run as the root user. Instead, it must run under the disabled, deprivileged `syslog` service account.
```

1. Modify the `/etc/rsyslog.conf` file and configure the TCP syslog input:

    ```ini
    # provides TCP syslog reception
    module(load="imtcp")
    input(type="imtcp" address="127.0.0.1" port="514")
    ```

1. Restrict the permissions of the RabbitMQ log file:

    ```bash
    sudo touch /var/log/rabbitmq/rabbit.log
    sudo chown syslog:rabbitmq /var/log/rabbitmq/rabbit.log
    sudo chmod 640 /var/log/rabbitmq/rabbit.log
    ```

1. Create the `rsyslog` configuration file `/etc/rsyslog.d/15-rabbitmq.conf`:

    ```ini
    # Local facility for RabbitMQ

    $CreateDirs on
    $DirGroup rabbitmq
    $DirOwner rabbitmq
    $FileGroup rabbitmq
    $FileOwner syslog
    $DirCreateMode 0755
    $FileCreateMode 0640
    local2.*            /var/log/rabbitmq/rabbit.log
    ```

    ```{note}
    If you provided a different facility than `local2` in the above RabbitMQ configuration for `syslog_facility`, adjust `local2.*` to match the new facility.
    ```

1. Restrict permissions on the configuration file:

    ```bash
    sudo chmod 644 /etc/rsyslog.d/15-rabbitmq.conf
    ```

1. Restart the `rsyslog` service:

    ```bash
    sudo systemctl restart rsyslog
    ```

### Restrict `epmd.socket`

By default, the RabbitMQ Erlang Port Mapper Daemon listens on port 4369 on all interfaces. To restrict this:

1. Edit the `/lib/systemd/system/epmd.socket` file and replace the `ListenStream` entries:

    ```ini
    ListenStream=127.0.0.1:4369
    ListenStream=[::1]:4369
    ```

    You can add additional `ListenStream` entries to allow additional interfaces. Make sure that the RabbitMQ node hostnames resolve to an IP listed here.

1. Reload the systemd daemon to apply the changes:

    ```bash
    sudo systemctl daemon-reload
    ```

1. Restart RabbitMQ and EPMD to load the new configuration:

    ```bash
    sudo systemctl stop rabbitmq-server
    sudo epmd -kill
    sudo systemctl restart epmd.socket
    sudo systemctl start rabbitmq-server
    ```

### Delete the Guest user in RabbitMQ

The default configuration of RabbitMQ installs a guest user with administrator permission and a weak password (guest).  It is highly recommended to delete the guest user with the following command:

```bash
sudo rabbitmqctl delete_user guest
```

### (Optional) Create Administrator User

To create a user for managing, vhosts, and permissions within the rabbitmq database use the following commands:

```{note}
Users in the `mq` group or with access to root can also use the `rabbitmqctl` command to accomplish the same results. Creating a user is not necessary.
```

```bash
# Supply a strong password that meets DoD requirements
sudo rabbitmqctl add_user <USERNAME>
sudo rabbitmqctl set_user_tags <USERNAME> administrator
```

Replace `<USERNAME>` with a RabbitMQ user that will have administrative privileges.

### Sample RabbitMQ files

Click on the links to download the following sample files. Remember to replace any placeholder values with the correct ones for your configuration.

* [`/etc/rabbitmq/rabbitmq.conf`](/assets/disa-stig/rabbitmq.conf)

* [`/etc/rabbitmq/rabbitmq-env.conf`](/assets/disa-stig/rabbitmq-env.conf)

* [`/etc/rabbitmq/enabled_plugins`](/assets/disa-stig/enabled_plugins)

* [`/etc/rabbitmq/advanced.config`](/assets/disa-stig/advanced.config)

* [`/etc/rsyslog.d/15-rabbitmq.conf`](/assets/disa-stig/15-rabbitmq.conf)

* [`/lib/systemd/system/epmd.socket`](/assets/disa-stig/epmd.socket)

## Configure RabbitMQ for Landscape

### Configure Landscape user in RabbitMQ

Execute the following commands to create the Landscape user and vhosts. Passing the empty string to the password set

```bash
sudo rabbitmqctl add_user landscape ""
sudo rabbitmqctl clear_password landscape
sudo rabbitmqctl add_vhost landscape
sudo rabbitmqctl set_permissions -p landscape landscape ".*" ".*" ".*"
```

```{note}
The following list details how RabbitMQ permissions are granted:

* First ".*" grants configure permission on every entity  
* Second ".*" grants write permission on every entity  
* Third ".*" grants read permission on every entity
```

## Configure the Apache web server

Landscape leverages Apache as the front-end web service to access Landscape Server. The following configuration changes are required:

### Edit Apache2 configuration

Modify the configuration file `/etc/apache2/apache2.conf`. See the sample provided here {ref}`header-sample-apache2-files`. The following modifications are changed from the default `/etc/apache2/apache2.conf` file:

* The common log format is modified to:

    ```ini
    LogFormat "%a %A %h %H %l %m %s %t %u %U \"%{Referer}i\" "
    ```

* `HTTPOnly` and `Secure` headers are added to prevent all cookies from access to client-side scripting to reduce XSS and session hijacking.
* The `Timeout` directive is set to `60` to prevent DoS attacks from indefinite session connections.
* The `TraceEnable` directive is set to `off` to prevent access to trace information.
* The `RequestReadTimeout` directive is set to `handshake=5 header=10 body=30` to prevent indefinite session hijacking.
* Session cookie protection directives are enabled to ensure cookies are encrypted before transmission:

    ```ini
    Session On
    SessionCookieName session path=/;httponly;secure;
    SessionMaxAge 600
    SessionCryptoCipher aes256
    ```

### Edit Apache2 port configuration

Modify the default configuration file `/etc/apache2/ports.conf`. See the template provided here {ref}`header-sample-apache2-files` and replace the following placeholder:

* `<LANDSCAPE_IP_ADDRESS>` : the IP address of Landscape Server. For example, `192.168.1.250`

### Edit Apache2 site configuration for Landscape

Add the configuration file `/etc/apache2/sites-available/landscape.conf`. See the template provided here {ref}`header-sample-apache2-files` and replace the following placeholders:

* `<IP_ADDRESS>` : the IP address of Landscape Server. For example, `192.168.1.250`
* `<HOSTNAME>`: the FQDN of the hostname the clients (browser and machines) will use to connect to Landscape Server. This must be resolvable via DNS. For example, `lds.example.com`
* `<CERTFILE>`: the full filesystem path to the SSL certificate for this server. For example, `/etc/apache2/apache_server.pem`
* `<KEYFILE>`: the full filesystem path to the private key corresponding to the SSL certificate. For example, `/etc/apache2/apache_server.key`
* `<CA_CERTFILE>`: the full filesystem path to the DoD CA chain file for this server. For example, `/etc/ca-certificates.crt`
* `<CRL_FILE>`: the full filesystem path to the DoD CRL file for revoked certificates. For example, `/etc/crl.crl`

### Set permissions for Apache2 files

Restrict configuration files to `640 root:root` permissions and the SSL private key to `400` permissions:

```bash
sudo chmod 640 /etc/apache2/ports.conf
sudo chmod 640 /etc/apache2/apache2.conf
sudo chmod 640 /etc/apache2/sites-available/landscape.conf
sudo chown root:root /etc/apache2/ports.conf
sudo chown root:root /etc/apache2/apache2.conf
sudo chown root:root /etc/apache2/sites-available/landscape.conf
```

### Edit general settings for Apache2

1. Enable the required modules for Apache:

    ```bash
    for module in rewrite proxy_http ssl headers expires proxy_http2 reqtimeout session session_cookie session_crypto usertrack unique_id; do sudo a2enmod $module; done
    ```

1. Disable the `mod-status` module:

    ```bash
    sudo a2dismod status
    ```

1. Disable the default HTTP vhost:

    ```bash
    sudo a2dissite 000-default
    ```

1. Enable the new site:

    ```bash
    sudo a2ensite landscape.conf
    sudo systemctl restart apache2.service
    ```

(header-sample-apache2-files)=

### Sample Apache2 files

Click on the links to download the following sample files. Remember to replace any placeholder values with the correct ones for your configuration.

* [`/etc/apache2/sites-available/landscape.conf`](/assets/disa-stig/landscape.conf)

* [`/etc/apache2/apache2.conf`](/assets/disa-stig/apache2.conf)

* [`/etc/apache2/ports.conf`](/assets/disa-stig/ports.conf)

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

Landscape is distributed in a public PPA. You can add it to the system with these commands, replacing `<LANDSCAPE_PPA>` with the appropriate repository:

```bash
sudo add-apt-repository <LANDSCAPE_PPA>
```

* `<LANDSCAPE_PPA>`: The PPA for the specific Landscape installation you’re using. The PPA for the most recent Landscape LTS is: `ppa:landscape/self-hosted-24.04`.  The PPA for Landscape's stable rolling release is: `ppa:landscape/latest-stable`. We recommend using an LTS for production deployments.

### Fix Pydantic Settings for FIPS

Landscape depends on `python3-pydantic >= 2.3.0`, but a lower version is pinned on FIPS. Create the `/etc/apt/preferences.d/landscape` file and add the following contents:

```ini
Package: python3-pydantic
Pin: release a=jammy
Pin-Priority: 511
```

### Install the server package

Install the Landscape Server package and its dependencies:

```bash
sudo apt install landscape-server
```

## Configure Landscape

(header-configure-authentication)=

### Configure Landscape authentication

Landscape does not support password-based authentication for administrators under DISA STIG compliance. Instead, you must configure one of the supported alternative authentication methods:

* {ref}`Active Directory <how-to-external-auth-active-directory>`
* {ref}`OIDC <how-to-external-auth-oidc>`
* {ref}`PAM <how-to-external-auth-pam>`

Be sure to set up and verify your chosen authentication method before proceeding with this guide.

```{note}
If your chosen method mentions setting a value in `service.conf`, ensure you use the correct environment variable instead. See {ref}`reference-service-conf` for the corresponding variables. It is recommended to put these environment variables in `/etc/environment` to ensure they are available if the system reboots.

If you encounter a step that depends on Landscape Server being installed, complete the installation first, then return to that step.
```

### Configure environment variables

We recommend setting the following environment variables:

```bash
# Disable password authentication
export LANDSCAPE_SYSTEM__ENABLE_PASSWORD_AUTHENTICATION=false
sudo sh -c "echo 'LANDSCAPE_SYSTEM__ENABLE_PASSWORD_AUTHENTICATION=false' >> /etc/environment"
```

If you're using the `set_user` extension, also set the following environment variables:

```bash
export LANDSCAPE_SCHEMA__STORE_USER=landscape_maintenance
sudo sh -c "echo 'LANDSCAPE_SCHEMA__STORE_USER=landscape_maintenance' >> /etc/environment"
export LANDSCAPE_SCHEMA__STORE_SUPERUSER=landscape_superuser
sudo sh -c "echo 'LANDSCAPE_SCHEMA__STORE_SUPERUSER=landscape_superuser' >> /etc/environment"
```

### Configure `service.conf`

Modify settings in the `/etc/landscape/service.conf` file to configure Landscape to connect to the database and message queuing services. For more details about the databases that Landscape uses, see {ref}`reference-database`.

The following changes are required in the sections below. Remove any passwords if they exist.

```ini
[api]
allowed_interfaces = localhost 127.0.0.1 ::1
base_port = 9080
mailer = queue
mailer_path = /var/lib/landscape/landscape-mail-queue
stores = main account-1 resource-1 package session session-autocommit
threads = 10

[appserver]
allowed_interfaces = localhost 127.0.0.1 ::1
base_port = 8080
blob_storage_root = /var/lib/landscape/blobs
display_consent_banner_at_each_login = true
mailer = queue
mailer_path = /var/lib/landscape/landscape-mail-queue
oops_key = DF
repository_path = /var/lib/landscape/landscape-repository
reprepro_binary = /opt/canonical/landscape/scripts/reprepro-wrapper.sh
sanitize_delay = 3600
secret_token = <SECRET_TOKEN>
stores = main account-1 resource-1 package session session-autocommit knowledge
threads = 8

[async_frontend]
allowed_interfaces = localhost 127.0.0.1 ::1
base_port = 9090

[broker]
host = localhost
port = 5671
ssl_client_cert = /etc/landscape/rabbitmq_client.pem
ssl_client_private_key = /etc/landscape/rabbitmq_client.key
ssl_client_ca_cert = /etc/ca-certificates.crt
user = landscape
vhost = landscape

[job_handler]
mailer = queue
mailer_path = /var/lib/landscape/landscape-mail-queue
stores = main account-1 resource-1 package
threads = 10

[load_shaper]

[maintenance]
mailer = queue
mailer_path = /var/lib/landscape/landscape-mail-queue
stores = main account-1 resource-1 package session session-autocommit knowledge
threads = 1

[message_server]
allowed_interfaces = localhost 127.0.0.1 ::1
base_port = 8090
oops_key = DM
stores = main account-1 resource-1 package
threads = 8

[oops]

[package_search]
allowed_interfaces = localhost 127.0.0.1 ::1
account_threshold = 0
pid_path = /var/run/landscape/landscape-package-search-1.pid
port = 9099
stores = main package resource-1

[package_upload]
allowed_interfaces = localhost 127.0.0.1 ::1
base_port = 9100
mailer = queue
mailer_path = /var/lib/landscape/landscape-mail-queue
root_url = http://localhost:9100
threads = 10

[pingserver]
allowed_interfaces = localhost 127.0.0.1 ::1
base_port = 8070
stores = main account-1 resource-1
threads = 2

[schema]
# note that you must have at least two certificates for db connections:
# one for landscape_superuser (or landscape_maintenance)
# and one for the regular landscape user
sslcert = /etc/landscape/postgres_client_superuser.pem
sslkey = /etc/landscape/postgres_client_superuser.key
sslmode = verify-full
sslrootcert = /etc/ca-certificates.crt
stores = main account-1 resource-1 package session knowledge
store_user = landscape_superuser
# if you have enabled the set_user extension, comment the line above and uncomment the lines below:
# store_user = landscape_maintenance
# store_superuser = landscape_superuser
threads = 1

[scripts]
mailer = queue
mailer_path = /var/lib/landscape/landscape-mail-queue
stores = main account-1 resource-1 package session knowledge
threads = 1

[secrets]
allowed_interfaces = localhost 127.0.0.1 ::1
service_url = http://localhost:26155

[stores]
account_1 = landscape-standalone-account-1
host = localhost
knowledge = landscape-standalone-knowledge
main = landscape-standalone-main
package = landscape-standalone-package
resource_1 = landscape-standalone-resource-1
session = landscape-standalone-session
session_autocommit = landscape-standalone-session
sslcert = /etc/landscape/postgres_client.pem
sslkey = /etc/landscape/postgres_client.key
sslmode = verify-full
sslrootcert = /etc/ca-certificates.crt
user = landscape

[system]
deployment_mode = standalone
enable_password_authentication = false
oops_path = /var/lib/landscape/landscape-oops
syslog_address = /dev/log
```

Replace `<SECRET_TOKEN>` with a random 172-character alphanumeric string. You can randomly generate one with:

```bash
tr -dc A-Za-z0-9 </dev/urandom | head -c 172; echo
```

You'll also have to generate a cookie encryption key.

```bash
sudo /opt/canonical/landscape/ensure-cookie-encryption-key
```

### Set permissions for Landscape files

Set secure permissions for Landscape certificates and configuration files:

```bash
sudo chown landscape:landscape /etc/landscape/service.conf
sudo chmod 600 /etc/landscape/service.conf
```

### Sample Landscape files

Click on the link to download the following sample file. Remember to replace any placeholder values with the correct ones for your configuration.

* [`/etc/landscape/service.conf`](/assets/disa-stig/service.conf)

### Run the Landscape setup script

This script will bootstrap the databases Landscape needs to work and setup the remaining configurations:

```bash
sudo setup-landscape-server
```

```{note}
Depending on the hardware, this may take several minutes to complete.
```

### Configure Landscape services

You need to disable the `hostagent-messenger` and `hostagent-consumer` services. These services have not been configured to support TLS communication with the client.

```bash
sudo systemctl disable landscape-hostagent-consumer.service landscape-hostagent-messenger.service
sudo systemctl mask landscape-hostagent-consumer.service landscape-hostagent-messenger.service
```

### Schema upgrades

In the `/etc/default/landscape-server` file, the `UPGRADE_SCHEMA` option needs to be reviewed. If set to `yes`, whenever the package `landscape-server` is updated, it will attempt to update the database schema too. It is a very convenient setting, but consider the following before enabling it:

* schema updates can take several minutes
* if the package is updated while the database is offline, or unreachable, the update will fail
* you should have a backup of the database before updating the package

Without this setting enabled, a package update might result in services that won't start anymore because of a needed schema change. In that case:

 1. Stop all the Landscape services
 1. Backup your database
 1. Update the schema on the application server:

    ```bash
    sudo setup-landscape-server
    ```

 1. Restart all Landscape services

## Start Landscape services

Run the script `lsctl` to start the `landscape-server` daemons:

```bash
sudo lsctl restart
```

### Configure authentication

If you skipped setting up authentication earlier in the guide, now is the time to complete those steps. See {ref}`Configure Authentication <header-configure-authentication>` for more details.

### Create the first user

The first user that's created in Landscape automatically becomes the administrator of the account. To create this first user, go to `https://<SERVER_NAME>` and complete the requested information.

## Configure the first client

On the client machine, install `landscape-client`.

```bash
sudo apt update && sudo apt install -y landscape-client  
```

Obtain an SSL certificate signed from a DoD Certificate Authority. This will usually be supplied via a Common Access Card (CAC).

To configure the Landscape Client package, run the following command. You choose the computer name.

```bash
sudo landscape-config --computer-title "<COMPUTER_NAME>" --account-name standalone --url https://<SERVER_NAME>/message-system --ping-url http://<SERVER_NAME>/ping –ssl-public-key /location/of/ca-certificates.crt  
```

You can now accept your client in the Landscape web portal, and it will begin to upload data.

## Configure firewalls

Configure the firewall to restrict inbound connections for Landscape Server. All inbound, forwarding, and outbound connections are disabled by default in a DISA STIG compliant system. You must configure the firewall for Apache, PostgreSQL, and RabbitMQ to be accessible.

To allow connections to Landscape Server, run:

```bash
ufw allow in on <INTERFACE_NAME> from <SOURCE_RANGE> to <IP_ADDRESS> port 80 proto tcp
ufw allow in on <INTERFACE_NAME> from <SOURCE_RANGE> to <IP_ADDRESS> port 443 proto tcp
ufw allow in on <INTERFACE_NAME> from <SOURCE_RANGE> to <IP_ADDRESS> port 6554 proto tcp
```

To allow connections to the PostgreSQL server, run:

```bash
ufw allow in on <INTERFACE_NAME> from <SOURCE_RANGE> to <IP_ADDRESS> port 5432 proto tcp
```

To allow connections to the RabbitMQ server, run:

```bash
ufw allow in on <INTERFACE_NAME> from <SOURCE_RANGE> to <IP_ADDRESS> port 4369 proto tcp
ufw allow in on <INTERFACE_NAME> from <SOURCE_RANGE> to <IP_ADDRESS> port 5671 proto tcp
ufw allow in on <INTERFACE_NAME> from <SOURCE_RANGE> to <IP_ADDRESS> port 25672 proto tcp
```

Where:

* `<INTERFACE_NAME` is the name of the network interface. For example, `enp0s1`.
* `<SOURCE_RANGE>` is the IP range allowed for connections. For example,`192.168.1.0/24`
* `<IP_ADDRESS>` is the IP address of Landscape Server’s Apache web server.

### (Optional) Add an email alias

You can configure Postfix to handle Landscape Server email notifications and alerts. To ensure that important system emails get attention, we recommend you also add an alias for Landscape on your local environment. For details, see {ref}`how-to-configure-postfix`.
