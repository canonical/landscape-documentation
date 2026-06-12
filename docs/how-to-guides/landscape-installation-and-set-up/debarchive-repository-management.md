---
myst:
  html_meta:
    description: "Set up Landscape Deb Archive alongside a working Landscape Server installation. Step-by-step guide for installing and configuring the landscape-debarchive snap."
---

(how-to-debarchive-repository-management)=
# How to set up Deb Archive with Landscape

This guide walks you through installing and configuring the `landscape-debarchive` snap alongside an existing {ref}`manual <how-to-manual-installation>` or {ref}`quickstart <how-to-quickstart-installation>` installation of Landscape Server. By the end, you'll have the Deb Archive service running and accessible through your existing reverse proxy, enabling repository management from the Landscape web portal.

Deb Archive was introduced in **Landscape 26.04 LTS**.

## Prerequisites

You need one of the following Landscape Server installations:

- A {ref}`quickstart <how-to-quickstart-installation>` installation of `landscape-server-quickstart`
- A {ref}`manual <how-to-manual-installation>` installation of `landscape-server`

For Quickstart installations, you need administrative access to the Landscape Server machine.

For Manual installations, you need:

- Access to the PostgreSQL database server used by Landscape
- Administrative (root) access to the application server

## Install the landscape-debarchive snap

Install the snap on the same machine as the Landscape application server. 

- For Quickstart installations, this is the same machine as your Landscape server.
- For Manual installations, this is the Landscape application server.

```bash
sudo snap install landscape-debarchive --channel=latest/beta
```

The snap installs as a daemon that will start automatically. It will fail to connect to the database until the remaining configuration steps are completed.

## Create the Deb Archive database

The Deb Archive service requires its own database in the PostgreSQL cluster already used by Landscape Server.

- For Quickstart installations, run the following commands on the Landscape Server machine.
- For Manual installations, run the commands on the PostgreSQL database server.

Create a dedicated database user for Deb Archive, replacing `<PASSWORD>` with a strong password of your choice. The `--pwprompt` flag will prompt you to enter the password securely:

```bash
sudo -u postgres createuser --pwprompt landscape_debarchive
```

Create the database, owned by the new user. If the database already exists, you can skip the `createdb` step and just ensure the user has the necessary privileges.

```bash
sudo -u postgres createdb --owner=landscape_debarchive landscape-standalone-debarchive
```

Grant the required privileges:

```bash
sudo -u postgres psql -d landscape-standalone-debarchive -c "GRANT USAGE, CREATE ON SCHEMA public TO landscape_debarchive;"
```

For **Manual installations** where the PostgreSQL server is on a separate host, also update `/etc/postgresql/<VERSION>/main/pg_hba.conf` on the database server to allow the new user to connect from the application server:

```text
host landscape-standalone-debarchive landscape_debarchive <IP-OF-APP>/32 scram-sha-256
```

Then reload PostgreSQL:

```bash
sudo systemctl reload postgresql
```

The Deb Archive service automatically applies its schema on first successful connection. No manual schema import is needed.

## Configure the Deb Archive snap to connect to the database

Configure the snap with the database name, user, and password you created in the previous step. Replace `<PASSWORD>` with the password you set for `landscape_debarchive`:

```bash
sudo snap set landscape-debarchive \
    deb.archive.database.name=landscape-standalone-debarchive \
    deb.archive.database.user=landscape_debarchive \
    deb.archive.database.password=<PASSWORD>
```

```{note}
**Manual installations**: Additionally, the Deb Archive snap must be able to read `/etc/landscape/service.conf`. If this file isn't on on the machine you're installing Deb Archive on, you'll need to manually copy it to that machine.
```

```{note}
The snap also supports SSL connections to the database. If your PostgreSQL server requires SSL, set `deb.archive.database.ssl` to the appropriate SSL mode (e.g. `require`) and ensure the snap can access any necessary certificates. Set the SSL cert, key, and root cert as needed with the `deb.archive.database.ssl-cert`, `deb.archive.database.ssl-key`, and `deb.archive.database.ssl-root-cert` settings, respectively.
```

### (Optional) Override default settings with `snap set`

Quickstart installations use the default configurations and generally don't require additional setup. Skip this section unless you've customized your database configuration.

For Manual installations, if your PostgreSQL server is **not** at the default location (`localhost:5432`), or you need to override any other defaults, use `snap set` to configure the snap directly.

The available settings and their defaults are:

| Setting | Snap key | Default |
| --- | --- | --- |
| Gateway (HTTP) port | `deb.archive.server.gateway-port` | `8100` |
| Server host | `deb.archive.server.host` | `localhost` |
| Database driver | `deb.archive.database.driver` | `pgx` |
| Database name | `deb.archive.database.name` | *(empty, should be set manually)* |
| Database host | `deb.archive.database.host` | *(empty, read from service.conf)* |
| Database port | `deb.archive.database.port` | `5432` |
| Database user | `deb.archive.database.user` | *(set in previous step)* |
| Database password | `deb.archive.database.password` | *(set in previous step)* |
| Database SSL mode | `deb.archive.database.ssl` | `disable` (can be any of the [PostgreSQL SSL modes](https://www.postgresql.org/docs/current/libpq-ssl.html)) |
| Logging level | `deb.archive.logging.level` | `info` |
| Human-readable logs | `deb.archive.logging.human-readable` | `false` |
| Filesystem storage path | `deb.archive.filesystem-storage-path` | `$SNAP_COMMON/filesystem_storage` |
| Filesystem published root | `deb.archive.filesystem-published-root` | `$SNAP_COMMON/publications` |
| Pagination secret | `deb.archive.pagination.secret` | *(empty, read from service.conf)* |
| JWT secret | `deb.archive.jwt.secret` | *(empty, read from service.conf)* |

For example, to point at a database server on a different host:

```bash
sudo snap set landscape-debarchive deb.archive.database.host=10.0.1.5
```

```{note}
If a value is defined in both `service.conf` and via `snap set`, the value from `service.conf` is used.
```

If you edited `service.conf` directly, restart the service manually:

```bash
sudo snap restart landscape-debarchive
```

The snap automatically restarts when configuration changes are applied via `snap set`.

## Configure the root directory for filesystem publications

When you publish a repository to a filesystem target, Deb Archive writes the published repository tree to a location on disk. The `filesystem-published-root` setting defines the base directory that is combined with each publication target's configured path to form the full output location.

By default, the snap uses `$SNAP_COMMON/publications` (typically `/var/snap/landscape-debarchive/common/publications`) as the root. If you need published repositories written to a different location — for example, a dedicated mount point or a directory served directly by a web server — override this setting:

```bash
sudo snap set landscape-debarchive deb.archive.filesystem-published-root=/srv/published-repos
```

The directory must exist and be writable by the snap. After the setting is applied, any new filesystem publication will write its repository tree under the specified root, joined with the target path configured in the publication.

For example, if the published root is `/srv/published-repos` and a publication target has the path `myrepo/ubuntu`, the resulting published repository will be located at `/srv/published-repos/myrepo/ubuntu`.

Landscape itself does not serve filesystem publication targets. Instead, you must configure a web server to serve your packages from your filesystem. The example configurations for Apache and Nginx below illustrate how you can achieve this. Both examples configure the service to listen on port 8000 to avoid conflicts with Landscape Server.

If the published repositories should not be publicly accessible, restrict access at the web server and/or network layer (e.g. firewall rules, IP allowlists, or HTTP authentication).
### Apache

If Apache isn't already listening on port 8000, add `Listen 8000` to `/etc/apache2/ports.conf` (or another included config file) before enabling the site.

Install the file below as `/etc/apache2/sites-available/filesystem-repo.conf` and change the following values:

- `@hostname@`: The fully qualified domain name for your server.
- `@publication_target_file_path@`: The path of the local directory you chose when creating the filesystem publication target (e.g. `/srv/published-repos/myrepo/ubuntu`).

```apache
<VirtualHost *:8000>
    ServerName @hostname@

    DocumentRoot @publication_target_file_path@

    <Directory @publication_target_file_path@>
        Options +Indexes

        # Optional: Makes the directory listings look a bit cleaner
        IndexOptions FancyIndexing NameWidth=* FoldersFirst
        
        Require all granted
    </Directory>

    # Optional: Logging configuration for easier troubleshooting
    ErrorLog /var/log/apache2/repo_error.log
    CustomLog /var/log/apache2/repo_access.log combined
</VirtualHost>
```

Then enable it:

```bash
sudo a2ensite filesystem-repo.conf
```

And restart Apache:

```bash
sudo systemctl restart apache2
```

### Nginx

Create `/etc/nginx/sites-available/filesystem-repo.conf` with the following contents, then replace:

- `<YOUR_FQDN>`: The fully qualified domain name for your server.
- `<PUBLICATION_TARGET_FILE_PATH>`: The path of the local directory you chose when creating the filesystem publication target (e.g. `/srv/published-repos/myrepo/ubuntu`).

```nginx
server {
    listen 8000;
    listen [::]:8000;

    server_name <YOUR_FQDN>;

    root <PUBLICATION_TARGET_FILE_PATH>;

    location / {
        autoindex on;
        
        # Optional: Makes the directory listings look a bit cleaner
        autoindex_exact_size off;
        autoindex_localtime on;

        try_files $uri $uri/ =404;
    }

    # Optional: Logging configuration for easier troubleshooting
    access_log /var/log/nginx/repo_access.log;
    error_log /var/log/nginx/repo_error.log;
}
```

Then enable it:

```bash
sudo ln -s /etc/nginx/sites-available/filesystem-repo.conf /etc/nginx/sites-enabled/
```

And restart Nginx:

```bash
sudo systemctl restart nginx
```

## Configure the reverse proxy

You need to expose the Deb Archive service at `/debarchive` on your Landscape URL.

This requires updating your reverse proxy to forward requests to the Deb Archive service while stripping the `/debarchive` prefix.

### Apache (Quickstart and most Manual installations)

Add the following rules to the `<VirtualHost *:443>` block in `/etc/apache2/sites-available/landscape.conf` (or the appropriate configuration file for your setup).

Add these lines **before** the final catch-all `RewriteRule` at the bottom of the block (the line that starts with `RewriteRule ^/(.*) http://localhost:8080/...`):

```apache
    # Landscape Deb Archive
    RewriteRule ^/debarchive$ /debarchive/ [R=permanent]
    RewriteRule ^/debarchive/(.*) http://localhost:8100/$1 [P,L]
```

Then reload Apache:

```bash
sudo systemctl reload apache2
```

### HAProxy (some Manual installations)

If your deployment uses HAProxy, add a routing rule and backend for the Deb Archive service. Edit your HAProxy configuration (typically `/etc/haproxy/haproxy.cfg`):

In the existing `frontend` section, add:

```text
    acl is_debarchive path_beg /debarchive
    use_backend debarchive if is_debarchive
```

Add a new backend section:

```text
backend debarchive
    http-request set-path %[path,regsub(^/debarchive,/)]
    server debarchive 127.0.0.1:8100 check
```

```{note}
If the Deb Archive service runs on a different machine from HAProxy, replace `127.0.0.1` with the appropriate IP address or hostname.
```

Then reload HAProxy:

```bash
sudo systemctl reload haproxy
```

## Verify the installation

### Check the service status

Confirm the snap service is running:

```bash
sudo snap services landscape-debarchive
```

The output should show the `debarchive` service as **active**:

```text
Service                              Startup  Current  Notes
landscape-debarchive.debarchive      enabled  active   -
```

### Verify Deb Archive is reachable

Send a probe request through the reverse proxy. Replace `$LANDSCAPE_FQDN` with the FQDN of your Landscape Server, or set it as an environment variable:

```bash
curl -sk -o /dev/null -w "%{http_code}" "https://$LANDSCAPE_FQDN/debarchive/v1beta1/mirrors"
```

A response of `401` (unauthorized) confirms the Deb Archive service is reachable through the reverse proxy. Deb Archive uses the same authentication as the main Landscape Server API. You should receive a `200` response instead if you include a JWT token in the request via bearer authentication, or include a cookie from a logged-in session in the Landscape web portal.

You can also test directly against the service (bypassing the proxy) to isolate connectivity issues:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8100/v1beta1/mirrors
```

### Verify in the Landscape web portal

1. Log in to the Landscape web portal at `https://$LANDSCAPE_FQDN`
2. Navigate to the **Repository management** page
3. Confirm that you can create or add a new repository mirror

If the repository management page loads and allows you to begin adding mirrors, the Deb Archive service is fully operational.

## Troubleshooting

### Service fails to start

Check the snap logs for error details:

```bash
sudo snap logs landscape-debarchive -n 50
```

Common issues include:

- **Database connection errors**: Verify the database host, port, user, and password. Ensure the Deb Archive database exists and the configured user has access.
- **Missing secrets**: If not using the configuration shim with `service.conf`, the `deb.archive.pagination.secret` (base64url-encoded) and `deb.archive.jwt.secret` (base64-encoded) must be set.

### Health check returns an error through the proxy

- Confirm the Deb Archive gateway port matches what the proxy expects (default: `8100`)
- Test direct connectivity to `http://localhost:8100/` to determine whether the issue is with the service or the proxy configuration
- Check Apache or HAProxy error logs for rewrite or proxy errors
