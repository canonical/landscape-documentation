---
myst:
  html_meta:
    description: "Set up Landscape Deb Archive alongside a manual Landscape Server installation. Step-by-step guide for installing and configuring the landscape-debarchive snap."
---

(how-to-debarchive-repository-management)=
# How to set up Deb Archive with a manual Landscape Server installation

This guide walks you through installing and configuring the `landscape-debarchive` snap alongside an existing manual installation of Landscape Server. By the end, you'll have the Deb Archive service running and accessible through your existing reverse proxy, enabling repository management from the Landscape web portal.

## Prerequisites

- A working manual installation of Landscape Server (see {ref}`how-to-manual-installation`)
- Access to the PostgreSQL database server used by Landscape
- Administrative (root) access to the application server

## Install the landscape-debarchive snap

Install the snap on the same machine as the Landscape application server:

```bash
sudo snap install landscape-debarchive --channel=latest/edge
```

The snap installs as a daemon that will start automatically. It will fail to connect to the database until the remaining configuration steps are completed, which is expected.

## Create the Deb Archive database

The Deb Archive service requires its own database in the PostgreSQL cluster already used by Landscape Server. On the **database server**, create the database:

```bash
sudo -u postgres createdb landscape-standalone-debarchive
```

Grant access to the existing Landscape database users so that Deb Archive can connect:

```bash
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE \"landscape-standalone-debarchive\" TO landscape_superuser;"
sudo -u postgres psql -d landscape-standalone-debarchive -c "GRANT USAGE, CREATE ON SCHEMA public TO landscape_maintenance;"
```

```{note}
The existing `pg_hba.conf` entries for the Landscape users should already permit access to this new database. No changes to `pg_hba.conf` are required unless you have restricted access to specific database names.
```

The Deb Archive service automatically applies its schema on first successful connection. No manual schema import is needed.

## Configure the snap to read Landscape Server configuration

The `landscape-debarchive` snap includes a configuration shim that reads `/etc/landscape/service.conf` to automatically derive database connection details and secrets from the existing Landscape Server configuration. The snap's `etc-landscape` interface auto-connects, so no manual interface connection is required.

For this to work, the `[stores]` section of `/etc/landscape/service.conf` must contain a `debarchive` entry with the database name. This entry is managed by the `landscape-server` package and should already be present. Verify it exists:

```bash
grep debarchive /etc/landscape/service.conf
```

You should see a line similar to:

```ini
debarchive = landscape-standalone-debarchive
```

If the entry is missing, add `debarchive = landscape-standalone-debarchive` to the `[stores]` section of `/etc/landscape/service.conf`.

### Overriding default settings with snap set

If your PostgreSQL server is **not** at the default location (`localhost:5432`), or you need to override any other defaults, use `snap set` to configure the snap directly. The available settings and their defaults are:

| Setting | Snap key | Default |
|---|---|---|
| Gateway (HTTP) port | `deb.archive.server.gateway-port` | `8100` |
| gRPC port | `deb.archive.server.grpc-port` | `8101` |
| Server host | `deb.archive.server.host` | `localhost` |
| Database driver | `deb.archive.database.driver` | `pgx` |
| Database name | `deb.archive.database.name` | `db` |
| Database host | `deb.archive.database.host` | `localhost` |
| Database port | `deb.archive.database.port` | `5432` |
| Database user | `deb.archive.database.user` | *(empty, read from service.conf)* |
| Database password | `deb.archive.database.password` | *(empty, read from service.conf)* |
| Database SSL mode | `deb.archive.database.ssl` | `disable` |
| Logging level | `deb.archive.logging.level` | `debug` |
| Human-readable logs | `deb.archive.logging.human-readable` | `true` |
| Filesystem storage path | `deb.archive.filesystem-storage-path` | `./filesystem_storage` |
| Pagination secret | `deb.archive.pagination.secret` | *(empty, read from service.conf)* |
| JWT secret | `deb.archive.jwt.secret` | *(empty, read from service.conf)* |

For example, to point at a database server on a different host:

```bash
sudo snap set landscape-debarchive deb.archive.database.host=10.0.1.5
```

```{note}
When the configuration shim reads `/etc/landscape/service.conf`, the values from that file take precedence for the fields it maps (database name, host, user, password, and secrets). Values set via `snap set` for those fields are only used if `service.conf` is not available.
```

### Restart the service after configuration changes

The snap automatically restarts when configuration changes are applied via `snap set`. If you edited `service.conf` directly, restart the service manually:

```bash
sudo snap restart landscape-debarchive
```

## Configure the reverse proxy

The Deb Archive gateway must be exposed at the `/debarchive` path on your Landscape Server's external URL. This requires updating your reverse proxy to forward requests to the Deb Archive service while stripping the `/debarchive` prefix.

### Apache

If you followed the {ref}`manual installation guide <how-to-heading-manual-install-configure-web-server>`, your Landscape Server uses Apache. Add the following rules to the `<VirtualHost *:443>` block in `/etc/apache2/sites-available/landscape.conf` (or the appropriate configuration file for your setup).

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

### HAProxy

If your deployment uses HAProxy as the reverse proxy, add a backend and routing rule for the Deb Archive service. Edit your HAProxy configuration (typically `/etc/haproxy/haproxy.cfg`):

Add an ACL and `use_backend` directive in the existing `frontend` section:

```
    acl is_debarchive path_beg /debarchive
    use_backend debarchive if is_debarchive
```

Add a new backend section:

```
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

### Check the health endpoint

Send a health check request through the reverse proxy. Replace `$LANDSCAPE_FQDN` with the FQDN of your Landscape Server, or set it as an environment variable:

```bash
curl -sk -o /dev/null -w "%{http_code}" "https://$LANDSCAPE_FQDN/debarchive/v1/mirrors"
```

A response of `401` (unauthorized) confirms the Deb Archive service is reachable through the reverse proxy. Deb Archive uses the same authentication as the main Landscape Server API. You should receive a `200` response instead if you include a JWT token in the request via bearer authorization, or include a cookie from a logged-in session in the Landscape web portal.

You can also test directly against the service (bypassing the proxy) to isolate connectivity issues:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8100/v1/mirrors
```

### Verify in the Landscape web portal

1. Log in to the Landscape web portal at `https://$LANDSCAPE_FQDN`
2. Navigate to the **repository management** page
3. Confirm that you can create or add a new repository mirror

If the repository management page loads and allows you to begin adding mirrors, the Deb Archive service is fully operational.

## Troubleshooting

### Service fails to start

Check the snap logs for error details:

```bash
sudo snap logs landscape-debarchive -n 50
```

Common issues include:

- **Database connection errors**: Verify the database host, port, user, and password. Ensure the `landscape-standalone-debarchive` database exists and the configured user has access.
- **Missing secrets**: If not using the configuration shim with `service.conf`, the `deb.archive.pagination.secret` (base64url-encoded) and `deb.archive.jwt.secret` (base64-encoded) must be set.

### Health check returns an error through the proxy

- Confirm the Deb Archive gateway port matches what the proxy expects (default: `8100`)
- Test direct connectivity to `http://localhost:8100/` to determine whether the issue is with the service or the proxy configuration
- Check Apache or HAProxy error logs for rewrite or proxy errors
