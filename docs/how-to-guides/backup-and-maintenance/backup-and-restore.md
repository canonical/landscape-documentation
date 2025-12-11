(how-to-backup-and-restore)=
# How to backup and restore Landscape

Self-hosted Landscape consists of several stateful components that must be roughly synchronized to guarantee correct functioning of the system as a whole. These include:

- **Landscape Server**: At least 6 PostgreSQL databases, a cache of hash databases, and a variety of configuration files.
- **Landscape Client(s)**: Several SQLite databases for tracking package states.

Landscape Server only supports backup to the latest possible state. So, the only supported backup option is one that permits point-in-time recovery (PITR).

We strongly recommend that administrators of a self-hosted Landscape instance familiarize themselves with PITR facilities and PostgreSQL's archived logging, also called write-ahead logging (WAL). Some syntactic configuration changes have occurred across PostgreSQL versions, so you should select the documentation for your particular PostgreSQL server version:

- [PostgreSQL 14](https://www.postgresql.org/docs/14/continuous-archiving.html) (Ubuntu 22.04 LTS)
- [PostgreSQL 12](https://www.postgresql.org/docs/12/continuous-archiving.html) (Ubuntu 20.04 LTS)
- [PostgreSQL 10](https://www.postgresql.org/docs/10/static/continuous-archiving.html) (Ubuntu 18.04 LTS)

Given the wide variety of clients (from physical hardware, to VMs, to containers, some of which may be permanent and others merely temporary), backup of Landscape Clients (if required at all) isn't covered in this guide.

```{note}
The database guidelines here don't apply to juju deployments with [Charmed PostgreSQL](https://canonical.com/data/docs/postgresql/iaas). Charmed PostgreSQL was introduced in the [Landscape 24.04 LTS charm](https://charmhub.io/landscape-server). See [Charmed PostgreSQL's backup and restore documentation](https://canonical.com/data/docs/postgresql/iaas/h-create-backup) for information on backing up and restoring your charmed database.
```

## Define a backup and retention policy

Before configuring your PostgreSQL instance for continuous archiving and PITR, it's important to decide on a backup policy. You may want to consider the following questions:

1. When should base backups be taken?
    - Recommended: Daily or weekly depending on volume of WAL logs and desired recovery speed.
2. How many base backups should be retained at any given time?
    - This dictates the earliest point in time to which you can initially restore.
3. Where should WAL logs be archived to?
    - Recommended: A separate machine or some form of networked and secure storage.
4. Where should base backups be stored?
    - Recommended: The same machine as the WAL archive so that all materials necessary for restoration are available in one place.

Although it's possible to backup and archive on the same machine as the PostgreSQL server, we recommend that you use a separate machine for base backup and archived log storage. This is to allow restoration in case the server becomes inaccessible for any reason. We also recommend that any other files needed to restore the Landscape application server (such as the configuration files listed in a following section) are also copied to this location to allow recovery of the entire service from one location.

## Configure PostgreSQL

To configure PostgreSQL:

1. In the `postgresql.conf` configuration file, set `wal_level`, `archive_mode`, and `archive_command` according to the PostgreSQL documentation for your server's version. 
2. Test that your `archive_command` operates correctly in all circumstances, including returning the correct exit codes.
3. Once you're confident the configuration is correct, restart the PostgreSQL service to activate archived logging.
4. Monitor the archive destination to ensure logs begin to appear there.
5. (Optional) If your server has very low traffic, you may want to use the `archive_timeout` setting to force archiving of partial logs after a timeout.
6. When WAL logs are being archived successfully, construct a script that executes `pg_basebackup` and stores the result in your base backup storage destination. 
7. Test that this operates correctly as the cluster owner (typically `postgres`).
8. Add a cronjob to periodically execute this script (as the cluster owner).

Note that you don't need to take Landscape offline to perform these backups; `pg_basebackup` can only execute when the cluster is up. There's no need to worry about inconsistency between Landscape's various databases either: a base backup represents the state of the cluster across all databases within it at the instant the backup starts.

## Backup server configuration files

The following files should also be copied from your Landscape Server(s) to your backup destination to ensure that restoration of the Landscape application server is also possible:

- `/etc/landscape/*`: Landscape configuration files and the on-premises Landscape license
- `/etc/default/landscape-server`: Specifies which Landscape application services start on a given machine
- `/etc/apache2/sites-available/<server-name>`: The Landscape Apache vhost configuration file, usually named after the FQDN of the server
- `/etc/ssl/certs/<landscape-cert>`: The Landscape server X.509 certificate
- `/etc/ssl/private/<landscape-cert>`: The Landscape server X.509 key file
- `/etc/postgresql/<pg-version>/main/*`: Various PostgreSQL configuration files

You may also want to backup the following log files. They're not required for normal operation of Landscape Server, but may provide additional information in the case of service outages:

- `/var/log/landscape-server/*`: The Landscape Server log files

If any of these files change periodically (e.g., the SSL certificates), you may also want to set up a cronjob to handle backing-up these files regularly.

## Test recovery procedures

We recommend that administrators of self-hosted Landscape test their recovery procedures after configuring their Landscape Server(s) for archived logging and PITR. This is to ensure that backups are valid and restorable, and that administrators are familiar with these procedures.

To test the recovery procedures:

1. Provision a spare server (or servers) and install Landscape Server as you have on your production machine(s)
2. Stop the Landscape application server, and the PostgreSQL cluster on the spare
3. Copy configuration files (see prior section) to the spare; you may wish to keep a script handy to perform this task in your backup location
4. If your spare isn't installed from scratch (e.g. if it is installed from an image), remove everything under `/var/lib/landscape/hash-id-databases`
5. Restore a recent PostgreSQL base-backup onto the spare; this usually involves (re)moving the existing PostgreSQL cluster's data directory (e.g. /var/lib/postgresql/9.5/main) and replacing it with the contents of the base-backup (or un-tarring the base-backup into it, if tar format was chosen); ensure file ownership and modes are preserved!
6. Construct an appropriate `recovery.conf` file in the new PostgreSQL cluster's data directory; a template for this can be found in `/usr/share/postgresql/<pg-version>/main/recovery.conf.sample`
7. Start the PostgreSQL cluster on the spare and watch the PostgreSQL logs to ensure recovery proceeds by retrieving and replaying WAL logs
8. Once recovery is complete, run `/opt/canonical/landscape/scripts/hash-id-databases.sh` to regenerate the hash databases cache
9. Finally, start the Landscape application server on the spare and test it to verify correct operation
