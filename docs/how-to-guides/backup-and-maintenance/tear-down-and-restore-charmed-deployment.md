(how-to-tear-down-and-restore-charmed-deployment)=

# Tearing down and restoring a charmed deployment

This guide covers the complete process of backing up, tearing down, and restoring a charmed Landscape deployment. This is useful when you need to rebuild your deployment, migrate to a new environment, or recover from a failure.

The process involves three main phases:

1. **Backup**: Collecting configuration, passwords, and database data from the running deployment
2. **Restore**: Creating a new deployment and restoring all data and configuration
3. **Tear down**: Destroying the old model (after confirming the restore was successful)

## Backup

Back up the configuration and database data for a Landscape Server deployment .

1. Save the configuration for the Juju model:

```sh
juju export-bundle | tee bundle.yaml
```

This will write a Juju bundle representing the current model to `bundle.yaml`.

1. Back up the `service.conf` file on each `landscape-server` unit:

```sh
mkdir -p service-conf
juju ssh landscape-server/0 -- sudo cat /etc/landscape/service.conf > service-conf/0.conf
```

Replacing `0` with the unit ID.

1. Record the PostgreSQL `operator` password:

```sh
juju run postgresql/leader get-password username=operator
```

We need this to dump and restore the databases.

1. Pause all of the Landscape Server units and keep them paused for the entire backup and restore procedure:

```sh
juju run landscape-server/0 pause
```

Repeat for each landscape-server unit (landscape-server/1, landscape-server/2, etc.).

If the service resumes during the process, connected clients may lose data. Always use a fresh backup.

1. Dump the database data:

1. Note the IP address of the PostgreSQL leader unit from `juju status`.
1. SSH into the PostgreSQL leader unit:

```sh
juju ssh postgresql/leader
```

1. Change to the snap data directory (the only directory the snap can access):

```sh
cd /var/snap/charmed-postgresql/current
```

1. Create a backup directory and move into it:

```sh
sudo mkdir -p backup
sudo chmod 755 backup
cd backup
```

1. Set `PG_PASSWORD` to the operator password you recorded and `PG_HOST` to the PostgreSQL leader unit's IP address:

```sh
export PG_PASSWORD="<operator-password>"
export PG_HOST="<postgres-ip>"
```

1. Dump each database:

```sh
for DB_NAME in \
    landscape-standalone-main \
    landscape-standalone-package \
    landscape-standalone-account-1 \
    landscape-standalone-resource-1 \
    landscape-standalone-knowledge \
    landscape-standalone-session; do
    sudo PGPASSWORD=$PG_PASSWORD charmed-postgresql.pg-dump -d $DB_NAME -U operator -h $PG_HOST -f $DB_NAME.dump -F directory
done
```

1. Confirm that each dump directory contains data:

```sh
sudo du -sh */
```

1. Change ownership of the backup directory so it can be copied:

```sh
cd ..
sudo chown -R ubuntu:ubuntu backup
exit
```

1. Export the backup files from the PostgreSQL unit to your local backup location:

```sh
juju scp -- -r postgresql/leader:/var/snap/charmed-postgresql/current/backup .
```

## Restore

Restore the deployment from the backup.

1. Create a new Landscape model and deploy Landscape the same way you did originally. Keep the Juju configuration consistent with your backup. Start with a single PostgreSQL unit and scale later if needed.

1. Wait for the model to settle. All units should reach active status:

```sh
juju wait-for model <new-model-name> --timeout 3600s --query='forEach(units, unit => unit.workload-status == "active")'
```

This waits up to 1 hour for all units to become active. Adjust the timeout as needed for your deployment.

1. Pause Landscape Server on all units:

```sh
juju run landscape-server/0 -m <new-model-name> pause
```

Repeat for each unit if your deployment has multiple `landscape-server` units.

1. Import the database backup files to the PostgreSQL leader unit:

```sh
juju scp -m <new-model-name> -- -r backup postgresql/leader:/tmp/
```

1. Copy the backup files into the snap-accessible path:

```sh
juju ssh -m <new-model-name> postgresql/leader "sudo cp -r /tmp/backup /var/snap/charmed-postgresql/current/"
```

1. Get the new PostgreSQL credentials:

```sh
juju run -m <new-model-name> postgresql/leader get-password username=operator
```

Note the password. Get the PostgreSQL leader unit's IP address from `juju show-unit -m <new-model-name> postgresql/0`.

1. Restore each database by connecting to the PostgreSQL leader unit:

```sh
juju ssh -m <new-model-name> postgresql/0
cd /var/snap/charmed-postgresql/current/backup
export PG_PASSWORD="<operator-password>"
export PG_HOST="<postgres-ip>"
for DB_NAME in \
    landscape-standalone-main \
    landscape-standalone-package \
    landscape-standalone-account-1 \
    landscape-standalone-resource-1 \
    landscape-standalone-knowledge \
    landscape-standalone-session; do
    sudo PGPASSWORD=$PG_PASSWORD charmed-postgresql.pg-restore -U operator -h $PG_HOST -d $DB_NAME $DB_NAME.dump -c
done
exit
```

Replace `0` with the unit number of your PostgreSQL leader unit.

1. Scale PostgreSQL to the desired number of units (if needed):

 ```sh
 juju add-unit postgresql -m <new-model-name> -n <num-units>
 ```

1. Wait for all units to become active again:

 ```sh
 juju wait-for model <new-model-name> --timeout 3600s --query='forEach(units, unit => unit.workload-status == "active")'
 ```

1. Clear the hash ID databases and regenerate them:

 ```sh
 juju ssh -m <new-model-name> landscape-server/leader "sudo rm -rf /var/lib/landscape/hash-id-databases/*"
 juju run -m <new-model-name> landscape-server/leader hash-id-databases --wait=30m
 ```

1. Resume Landscape on all units:

 ```sh
 juju run -m <new-model-name> landscape-server/0 resume
 ```

Repeat for each unit if your model has multiple `landscape-server` units.

1. Verify that the deployment is healthy:

```sh
juju status -m <new-model-name>
```

The `landscape-server` unit(s) should be active.

1. Confirm the restore was successful:

Check that all services are running

```sh
juju exec -m <new-model-name> --unit landscape-server/leader -- sudo systemctl status landscape-appserver landscape-api landscape-msgserver
```

Verify `service.conf` has been updated:

```sh
juju exec -m <new-model-name> --unit landscape-server/leader -- sudo cat /etc/landscape/service.conf
```

Check that data was restored by querying the database

```sh
juju ssh -m <new-model-name> postgresql/0
export PG_PASSWORD="<operator-password>"
export PG_HOST="<postgres-ip>"
echo "SELECT COUNT(*) FROM computer;" | sudo PGPASSWORD=$PG_PASSWORD charmed-postgresql.psql -U operator -h $PG_HOST -d landscape-standalone-main
exit
```

If you had registered computers before the backup, they should appear in the count. Access the Landscape web interface to verify your data is present.

## Tear down

Remove the original deployment after confirming the restore was successful.

1. Destroy the original model:

```sh
juju destroy-model <original-model-name>
```

This removes all deployed applications and units from the original model. Only do this after confirming your restored deployment is working correctly.
