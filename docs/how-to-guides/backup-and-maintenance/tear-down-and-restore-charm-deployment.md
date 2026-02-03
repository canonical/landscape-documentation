(how-to-tear-down-and-restore-charm-deployment)=

# Tearing down and restoring a charm deployment

## Backup

Back up the configuration and database data for a charmed Landscape deployment.

1. Back up the Juju configuration for each application:

 ```sh
 juju config landscape-server
 ```

 Repeat for all applications listed in `juju status`.

1. Save the Juju status output:

 ```sh
 juju status --integrations > juju_status.txt
 ```

 This may vary by setup (for example, if using Mojo or a bundle file).

1. Back up the Landscape `service.conf` file on each unit:

 ```sh
 juju exec --unit landscape-server/leader -- sudo cat /etc/landscape/service.conf
 ```

1. Back up the PostgreSQL passwords (the operator password is the most important):

 ```sh
 juju run postgresql/leader get-password username=operator
 juju run postgresql/leader get-password username=replication
 juju run postgresql/leader get-password username=rewind
 ```

1. Pause Landscape Server on all units and keep it paused for the entire backup and restore procedure:

 ```sh
 juju run landscape-server/unit pause
 ```

 If the service resumes during the process, connected clients may lose data. Always use a fresh backup.

1. Dump the database data:

1. Note the IP address of the primary PostgreSQL unit.
1. SSH into the leader unit:

  ```sh
  juju ssh postgresql/leader
  ```

 1. Change to the snap data directory (the only directory the snap can access):

  ```sh
  cd /var/snap/charmed-postgresql/current
  ```

 1. Create a backup directory and move into it:

  ```sh
  sudo mkdir backup
  cd backup
  ```

 1. Set the operator password and PostgreSQL host:

  ```sh
  export PG_PASSWORD="<operator-password>"
  export PG_HOST="<postgres-ip>"
  ```

 1. Dump each database:

  ```sh
  DB_NAME="landscape-test-main"; sudo PGPASSWORD=$PG_PASSWORD charmed-postgresql.pg-dump -d $DB_NAME -U operator -h $PG_HOST -f $DB_NAME.dump -F directory
  ```

  Repeat for all six databases:

- `landscape-standalone-main`
- `landscape-standalone-package`
- `landscape-standalone-account-1`
- `landscape-standalone-resource-1`
- `landscape-standalone-knowledge`
- `landscape-standalone-session`

 1. Confirm that each dump directory contains data:

  ```sh
  du -sh */
  ```

1. Export the backup files. This step varies by setup. For LXC, for example:

 ```sh
 lxc file pull juju-c4b624-2/var/snap/charmed-postgresql/current/backup -r .
 ```

## Restore

Restore the deployment from the backup.

1. Create a new Landscape model (optionally destroy the old one). Keep the Juju configuration consistent with your backup. Start with a single PostgreSQL unit and scale later.

2. Wait for the model to become functional, then pause Landscape Server on all units:

 ```sh
 juju run landscape-server/0 pause
 ```

 Repeat for each unit (change the unit number accordingly).

1. Verify that the `service.conf` in the new model closely matches your backup. Passwords and keys will differ because the model is new.

2. Import the database files to the new PostgreSQL leader unit. This varies by setup. For LXC, for example:

 ```sh
 lxc file push ./backup juju-e66e50-2/home/ubuntu/ -r
 ```

1. Copy the backup files into the snap-accessible path and change into the backup directory:

 ```sh
 sudo cp ./backup /var/snap/charmed-postgresql/current/. -r
 cd /var/snap/charmed-postgresql/current/backup
 ```

1. Restore each database:

 ```sh
 DB_NAME="landscape-test-main"; sudo PGPASSWORD=$PG_PASSWORD charmed-postgresql.pg-restore -U operator -h $PG_HOST -d $DB_NAME $DB_NAME.dump -c
 ```

 Repeat for all six databases.

1. Scale PostgreSQL to the desired number of units.

2. Clear the hash ID databases and regenerate them:

 ```sh
 juju ssh landscape-server/leader
 ```

 ```sh
 sudo rm -rf /var/lib/landscape/hash-id-databases/*
 ```

 Exit the leader unit shell, then run:

 ```sh
 juju run landscape-server/leader hash-id-databases --wait=30m
 ```

1. Resume Landscape on all units:

 ```sh
 juju run landscape-server/leader resume
 ```
