(how-to-tear-down-and-restore-charm-deployment)=

# Tearing down and restoring a charm deployment

## Backup

Backup current juju configuration data. “juju config landscape-server” Repeat for all applications in “juju status.” Download the juju status output “juju status –integrations > juju_status.txt”. Note this part may be different on setup, for example if using mojo or a bundle file (but the config may be different from the bundle file so this will pull the current configuration).
Backup the landscape service.conf file “juju exec --unit landscape-server/leader \
-- sudo cat /etc/landscape/service.conf” Repeat on all the units as it can be slightly different.
Backup the juju postgres passwords. The operator password is the most relevant but note the others just in case.
Run “juju run postgresql/leader get-password username=operator”
Run “juju run postgresql/leader get-password username=replication”
Run “juju run postgresql/leader get-password username=rewind”
Pause landscape server on all the units “juju run landscape-server/unit pause”. Note the units must remain paused throughout the whole backup and restore procedure. If it doesn’t you may lose all connected clients. This means that a fresh backup must be always used, not an older one.
Dump the database data
Note the ip address of the main postgres unit. It will be used to run the dump command
Run “juju ssh postgresql/leader”
Run “cd /var/snap/charmed-postgresql/current”. It is the directory that contains the postgres configuration files. This directory is the only one on the filesystem that the snap has access to
Run “sudo mkdir backup”
Run “cd backup”
Run “export PG_PASSWORD="8a8R3maTnmhB11a7" This is the password for the user named operator you saved previously.
Run export PG_HOST="10.207.113.42"
Run “DB_NAME="landscape-test-main"; sudo PGPASSWORD=$PG_PASSWORD charmed-postgresql.pg-dump -d $DB_NAME -U operator -h $PG_HOST -f $DB_NAME.dump -F directory”
Repeat for all 6 databases. They are the following: landscape-standalone-main, landscape-standalone-package, landscape-standalone-account-1, landscape-standalone-resource-1, landscape-standalone-knowledge, landscape-standalone-session
Confirm that there is data in each of the backup directories with “du -sh */”
Export the database saved files. Note this will be different based on the setup. In LXC this is “lxc file pull juju-c4b624-2/var/snap/charmed-postgresql/current/backup -r .”

## Restore

Create the new landscape juju model (optionally destroy the old one). Making sure to keep the juju config the same (see backup copy mentioned above). You will need just one postgres unit right now, we will scale after the restore is complete.
Wait for the model to become fully functional. Then pause it with “juju run landscape-server/0 pause”. Make sure to do this for all units, not just 0, changing the ID at the end.
Make sure that the service.conf in the new model looks similar to the one you previously backed up. Note that the database passwords and other keys will be different since you started over.
Import the database saved files to the new postgres leader unit. Note this will be different based on the setup. In LXC it’s “lxc file push ./backup juju-e66e50-2/home/ubuntu/ -r”
Copy the backup files to the proper path that can be accessed by the snap “sudo cp ./backup /var/snap/charmed-postgresql/current/. -r”
Change directories to the backup path “cd /var/snap/charmed-postgresql/current/backup”
Follow similar steps to step 4, except instead of dumping the data, restore it with this “DB_NAME="landscape-test-main"; sudo PGPASSWORD=$PG_PASSWORD charmed-postgresql.pg-restore -U operator -h $PG_HOST -d $DB_NAME $DB_NAME.dump -c”
Repeat these steps for all 6 databases
Scale up postgres now to the desired number of units
Clear out the previous package hashids data and run the hashids script
Run “juju ssh landscape-server/leader”
Remove all the files under  /var/lib/landscape/hash-id-databases
Exit out of the leader unit shell and run “juju run landscape-server/leader hash-id-databases –wait=30m”
Start landscape “juju run landscape-server/leader resume” Repeat for all units.
