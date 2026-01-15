(how-to-manage-maintenance-cron-jobs)=
# How to manage maintenance cron jobs

Landscape Server installs and manages a set of maintenance cron jobs that are enabled by default. These jobs are essential for normal operation and are defined in the `/etc/cron.d/landscape-server` file.

## Default maintenance cron jobs

The following are automatically scheduled cron jobs.

- `maintenance.sh`
  - Performs daily maintenance of monitoring graphs tables and deleting older data. It also runs schema maintenance tasks. Failure to run this task for multiple days prevents monitoring data from being stored and will lead to gaps in graphs.
- `update_security_db.sh`
  - Loads the latest Ubuntu Security Notices (USNs) and processes them. Required for identifying which updates are classified as security updates.
- `update_alerts.sh`
  - Updates alert rules that require periodic checks (e.g. detecting offline computers and expired accounts).
- `process_alerts.sh`
  - Process alert rules for all accounts and sends pending alert notifications emails.
- `landscape_profiles.sh`
  - Applies {ref}`profiles <reference-terms-profiles>` to computers.
- `hash_id_databases.sh`
  - Regenerates packages hash-ids mapping files. Enables newly registered computers to report installed and available packages quickly. Out-of-date hash-id mapping files causes computers to report packages at a slower rate (approximately 500 packages at a time).
- `meta_releases.sh`
  - Checks for new releases of Ubuntu.

## Optional Cleaning of Activity History

Landscape includes default maintenance tasks to limit monitoring graphs history. Additional maintenance jobs can be scheduled to limit old activities and events to a defined retention period. 

### Setting up optional cleanup tasks
Create a `/etc/cron.d/ls_maintenance` file and add the following:

```bash
0 3 * * * landscape /opt/canonical/landscape/scripts/cleanup-activities.sh 90
30 3 * * * landscape /opt/canonical/landscape/scripts/cleanup-events.sh 90
```

This will schedule two tasks:

- `cleanup-activities`
  - Removes finished activities older than 90 days. Runs daily at 03:00.
- `cleanup-events.sh`
  - Removes events older than 90 days. Runs every day at 03:30.

### Viewing cleanup task logs
Cleanup tasks will log their output to syslog.

```bash
journalctl -t cleanup-activities -t cleanup-events
```

To log these tasks to separate files, edit `/etc/rsyslog.d/20-landscape.conf` and add the following lines.

```bash
if $programname == 'cleanup-activities' then /var/log/landscape-server/cleanup-activities.log;Landscape
& ~
if $programname == 'cleanup-events' then /var/log/landscape-server/cleanup-events.log;Landscape
& ~
```

Then restart the logging service.

```bash
sudo systemctl restart rsyslog.service
```
