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

## See also

- {ref}`explanation-charm-compatibility` - Charm revision compatibility information
- {ref}`how-to-juju-ha-installation` - High-availability Landscape deployment guide
- [PgBouncer charm documentation](https://charmhub.io/pgbouncer)
- [Charmed PostgreSQL documentation](https://charmhub.io/postgresql)
