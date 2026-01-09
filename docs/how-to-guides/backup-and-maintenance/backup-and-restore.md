(how-to-backup-and-restore)=

# How to backup and restore Landscape

This guide describes the suggested method for backing up and restoring a self-hosted Landscape Server.

It covers:

- Backup and restore of the Landscape Server database using PostgreSQL point-in-time recovery (PITR)
- Backup of Landscape Server configuration files required to restore the application server
- Testing recovery procedures on a spare server

It doesn't cover:

- Juju deployments using [Charmed PostgreSQL](https://canonical-charmed-postgresql.readthedocs-hosted.com/14/), which was introduced in the [24.04 LTS release of the Landscape Server charm](https://charmhub.io/landscape-server). See [Charmed PostgreSQL's backup and restore documentation](https://canonical-charmed-postgresql.readthedocs-hosted.com/14/how-to/back-up-and-restore/create-a-backup/index.html) for information on backing up and restoring your charmed database.
- Backup of Landscape Clients
- PostgreSQL tuning or general database administration beyond what's required for PITR

Backup of Landscape Clients isn't covered due to the wide variety of client environments (physical hardware, VMs, containers, some permanent and others ephemeral). In many deployments, client-side data doesn't need to be backed up because clients can re-register with Landscape Server and the main records are stored server-side.

It is strongly recommended that administrators of a self-hosted Landscape instance familiarize themselves with PITR facilities and PostgreSQL's archived logging, also called write-ahead logging (WAL). Some syntactic configuration changes have occurred across PostgreSQL versions, so you should select the documentation for your particular PostgreSQL server version:

- [PostgreSQL 16](https://www.postgresql.org/docs/16/continuous-archiving.html) (Ubuntu 24.04 LTS)
- [PostgreSQL 14](https://www.postgresql.org/docs/14/continuous-archiving.html) (Ubuntu 22.04 LTS)

## High availability (HA)

If you operate an HA deployment, perform the PostgreSQL backup and recovery steps per database instance in the cluster, and back up Landscape configuration files on each Landscape Server node.

## Define a backup and retention policy

To configure PostgreSQL for continuous archiving and PITR:

1. When should base backups be taken?
    - Recommended: Daily or weekly depending on volume of WAL logs and desired recovery speed.
2. How many base backups should be retained at any given time?
    - This dictates the earliest point in time to which you can initially restore.
3. Where should WAL logs be archived to?
    - Recommended: A separate machine or some form of networked and secure storage.
4. Where should base backups be stored?
    - Recommended: The same machine as the WAL archive so that all materials necessary for restoration are available in one place.

Although it's possible to backup and archive on the same machine as the PostgreSQL server, it is recommended that you use a separate machine for base backup and archived log storage. This is to allow restoration in case the server becomes inaccessible for any reason. We also recommend that any other files needed to restore the Landscape application server (such as the configuration files listed in a following section) are also copied to this location to allow recovery of the entire service from one location.

## Configure PostgreSQL for continuous archiving and PITR

To configure PostgreSQL:

1. In the `postgresql.conf` configuration file, set `wal_level`, `archive_mode`, and `archive_command` according to the PostgreSQL documentation for your server's version.
2. Test that your `archive_command` operates correctly in all circumstances and check the results of the `archive_command` in the PostgreSQL logs:

    - Force a WAL switch, then verify a new WAL file appears in your archive location:

        sudo -u postgres psql -c "SELECT pg_switch_wal();"

    - Check the PostgreSQL logs for archiving messages and ensure the archive command completed successfully (exit code is 0).

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
5. Restore a recent PostgreSQL base-backup onto the spare; this usually involves (re)moving the existing PostgreSQL cluster's data directory (e.g. `/var/lib/postgresql/<pg-version>/main`) and replacing it with the contents of the base-backup (or un-tarring the base-backup into it, if tar format was chosen); ensure file ownership and modes are preserved!
6. Configure recovery settings in the PostgreSQL cluster's data directory by setting recovery configuration options in `postgresql.conf` (e.g., `restore_command`). See the "Archive Recovery" documentation section in that file for examples and documentation of recovery settings. Then, create an empty `recovery.signal` file in the cluster data directory to trigger recovery mode.
7. Start the PostgreSQL cluster on the spare and watch the PostgreSQL logs to ensure recovery proceeds by retrieving and replaying WAL logs. Upon completion, PostgreSQL 14+ will automatically remove the `recovery.signal` file.
8. Once recovery is complete, run `/opt/canonical/landscape/hash-id-databases` to regenerate the hash databases cache
9. Finally, start the Landscape application server on the spare and test it to verify correct operation, including:
    - The UI loads and you can log in
    - Existing data (accounts, computers, activities) is present
    - Connected clients remain registered and are reporting data
    - Landscape services are active and healthy (e.g., `sudo lsctl status` shows the services as active)
