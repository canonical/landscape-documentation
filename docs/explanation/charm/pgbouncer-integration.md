---
myst:
  html_meta:
    description: "Understanding PgBouncer integration with Landscape Server charm, including the postgresql_client interface requirement and compatibility considerations."
---

(explanation-pgbouncer-integration)=
# PgBouncer integration with Landscape Server

PgBouncer is a lightweight connection pooler for PostgreSQL that can significantly improve database performance and scalability in Landscape Server deployments. By pooling and reusing database connections, PgBouncer reduces the overhead of establishing new connections and allows your deployment to handle more concurrent operations efficiently.

PgBouncer is available for Landscape Server charmed deployments.

There are some benefits and trade-offs to consider if implementing PgBouncer.

## Benefits

- **Reduced connection overhead**: Reusing connections eliminates the cost of repeatedly establishing new database connections
- **Lower memory footprint**: Fewer active connections to PostgreSQL means lower memory usage on the database server
- **Improved concurrency**: More clients can be served with the same database resources
- **Connection limits**: Helps manage PostgreSQL's `max_connections` limit by multiplexing many client connections through fewer backend connections
- **Query performance**: Better query throughput through efficient connection management

## Trade-offs

- **Additional component**: Introduces another service to deploy, monitor, and maintain
- **Compatibility requirement**: Requires a recent Landscape Server charm revision with `postgresql_client` interface support
- **Debugging complexity**: Connection issues may require examining both PgBouncer and PostgreSQL logs
- **Configuration overhead**: Requires understanding PgBouncer pooling modes and parameters for optimal performance

## When to use PgBouncer

PgBouncer is recommended for:

- **Production deployments** with significant client loads
- **High-availability configurations** where connection management is critical
- **Large-scale environments** managing hundreds or thousands of clients
- **Resource-constrained setups** where database connection limits are a concern

For small test deployments or proof-of-concept environments with minimal client loads, direct PostgreSQL connections will often be sufficient.

## Connection architecture

When deploying with PgBouncer, the connection architecture changes from a direct connection to a pooled connection pattern:

**Without PgBouncer:**
```
Landscape Server → PostgreSQL
```

**With PgBouncer:**
```
Landscape Server → PgBouncer → PostgreSQL
```

PgBouncer sits between Landscape Server and PostgreSQL, managing a pool of connections to the database and efficiently distributing requests across the connection pool.

## The `postgresql_client` interface

Integration with PgBouncer requires the Landscape Server charm to use the `database` relation endpoint, which uses the `postgresql_client` charm interface under the hood. This contrasts with the legacy `db` endpoint and `pgsql` interface used for direct PostgreSQL connections without a pooler.

```{important}
Only recent revisions of the Landscape Server charm support the `postgresql_client` interface required for PgBouncer integration. See {ref}`explanation-charm-compatibility` for details on which charm revisions support this integration.
```

## Juju relation pattern

In a Juju deployment with PgBouncer, the relations are configured as follows:

```yaml
relations:
  - [landscape-server:database, pgbouncer:database]
  - [pgbouncer:backend-database, postgresql:database]
```

The Landscape Server charm relates to PgBouncer using the `database` endpoint, and PgBouncer relates to PostgreSQL using its `backend-database` endpoint. This creates the connection pooling layer between the application and the database.

In a 26.04 HA deployment, {ref}`Debarchive <how-to-debarchive-repository-management>` and {ref}`Landscape Task Handler <how-to-juju-ha-installation>` are required components alongside Landscape Server. Since a PgBouncer application's `database` endpoint can only serve one principal application, they cannot share Landscape Server's PgBouncer; each would need its own dedicated PgBouncer application if pooling were used for them.

**Debarchive** may optionally use a dedicated PgBouncer application, since it only ever needs its own single database:

```yaml
relations:
  - [landscape-debarchive:database, pgbouncer-debarchive:database]
  - [pgbouncer-debarchive:backend-database, postgresql:database]
```

```{important}
PgBouncer's `backend-database` relation to PostgreSQL can intermittently fail to initialise on first setup, due to a known upstream race condition ([postgresql-operator#1927](https://github.com/canonical/postgresql-operator/issues/1927)): PostgreSQL can grant the new PgBouncer relation user a `pg_hba.conf` rule scoped to only its own database instead of `all`, which blocks PgBouncer's own auth-function bootstrap. If the PgBouncer unit's status shows `blocked`/`waiting for backend-database relation to connect` shortly after relating it, this is likely the cause. It is a one-time issue at initial setup, not an ongoing operational risk: once resolved, the relation works normally going forward, including through leader/primary changes and restarts. To resolve it, trigger PostgreSQL to recompute `pg_hba.conf` and PgBouncer to retry its deferred setup, by toggling a value on each application's config back and forth (any value works; this is done purely to trigger the `config-changed` hook on every unit):

```bash
juju config postgresql connection_authentication_timeout=61
juju config postgresql connection_authentication_timeout=60
juju config pgbouncer-debarchive max_db_connections=101
juju config pgbouncer-debarchive max_db_connections=100
```

Wait for the PgBouncer unit to reach `active` before proceeding. If it doesn't recover, repeat the toggle: the underlying condition is a replication-timing race, so it may need more than one attempt.
```

**Landscape Task Handler must always connect directly to PostgreSQL**, never through a dedicated PgBouncer of its own:

```yaml
relations:
  - [landscape-task-handler:task-db, postgresql:database]
```

```{important}
Unlike Debarchive, `landscape-task-handler`'s `task-db` relation cannot be pooled through its own dedicated PgBouncer. `task-db` isn't only used for the task-handler's own queue database: whenever Landscape Server's own published stores address is a loopback address (i.e. Landscape Server itself is fronted by its own PgBouncer), the Task Handler charm substitutes `task-db`'s resolved host/port for the shared `main`/`account`/`resource` stores too, since those otherwise-unreachable loopback details are meaningless outside Landscape Server's own machine. That substitution assumes `task-db` points at a real, directly-reachable PostgreSQL. If `task-db` is instead routed through a dedicated `pgbouncer-task-handler` application, `task-db`'s resolved address becomes a loopback address too (task-handler's own local PgBouncer), one whose `[databases]` section only ever contains the single `task-handler` database, not the shared stores. The charm then substitutes that pgbouncer's address in for the shared stores, which fails outright: PgBouncer has no route configured for `main`/`account`/`resource` at all, and returns a generic `SASL authentication failed` for any database it doesn't recognize. This is not a `pg_hba.conf` or credentials problem: `postgresql-operator#1927`'s workaround above does not apply and will not fix it.

Fixing this properly would require Landscape Server to publish a real, directly-reachable address for the shared stores independently of whatever pooler it uses for itself, which the Task Handler charm cannot control from its own side. Until that exists, keep `task-db` on a direct connection to PostgreSQL.
```

## Interaction with Landscape Server schema migration

Historically, Landscape Server has rejected attempts to run schema migrations when there are active connections other than Postgres itself to the database. However, given the fact that PgBouncer connects to Postgres in between Landscape Server (the client) and Postgres (the server), it needs to stay connected to provide Landscape with a database connection so it can run the schema migration. To accommodate this, the Landscape Server charm's `migrate-schema` action has an `allow-connections` flag, which defaults to `false`. Due to the design of charm interfaces, we cannot reliably know if the database connection for Landscape is being provided directly or via PgBouncer without making assumptions (ex. checking if the port is the default for PgBouncer or not).

## See also

- {ref}`explanation-charm-compatibility` - Charm revision compatibility information
- {ref}`how-to-juju-ha-installation` - High-availability Landscape deployment guide
- [PgBouncer charm documentation](https://charmhub.io/pgbouncer)
- [Charmed PostgreSQL documentation](https://charmhub.io/postgresql)
