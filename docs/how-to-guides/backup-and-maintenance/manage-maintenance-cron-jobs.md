(how-to-manage-maintenance-cron-jobs)=
# How to manage maintenance cron jobs

Landscape Server installs and manages a set of maintenance cron jobs that are enabled by default. These jobs are essential for normal operation and are defined in the `/etc/cron.d/landscape-server` file.

## Default maintenance cron jobs

The following are automatically scheduled cron jobs. These scripts are all located in the `/opt/canonical/landscape/scripts` directory.

- `maintenance.sh`
  - Performs daily maintenance of monitoring graphs and tables, deletes data older than 28 days (e.g., load average, memory info, network traffic, temperature, free space, CPU usage data), and runs schema maintenance tasks. Failure to run this task for multiple days may result in housekeeping tasks to lag behind, monitoring data not being stored, and gaps appearing in graphs.
- `update_security_db.sh`
  - Loads and processes the latest Common Vulnerabilities and Exposures (CVEs) and Ubuntu Security Notices (USNs). Required for identifying which updates are classified as security updates.
- `update_alerts.sh`
  - Updates alert rules that require periodic checks (e.g., detecting offline client instances and expired accounts).
- `process_alerts.sh`
  - Process alert rules for all accounts and sends pending alert notifications emails.
- `landscape_profiles.sh`
  - Applies {ref}`profiles <reference-terms-profiles>` to client instances.
- `hash_id_databases.sh`
  - Regenerates packages hash-ids mapping files. Enables newly registered computers to report installed and available packages quickly. Out-of-date hash-id mapping files causes computers to report packages at a slower rate (approximately 500 packages at a time).
- `meta_releases.sh`
  - Checks for new releases of Ubuntu.
- `sync_lds_releases.sh` (Landscape 25.08 and earlier)
  - Checks for available Landscape Server upgrades. This job was removed in Landscape 25.10.
- `report_anonymous_metrics.sh` (Landscape 25.04 and earlier)
  - Reports anonymous metrics (e.g., the installed Landscape Server version). This job was removed in Landscape 25.08.

## Optional Cleaning of Activity History

Landscape includes some basic cleanup tasks in the `maintenance.sh` job. You may want to create additional jobs to limit old activities and events to a defined retention period. 

### Set up optional cleanup tasks

Create a `/etc/cron.d/ls_maintenance` file and add the following:

```bash
0 3 * * * landscape /opt/canonical/landscape/scripts/cleanup-activities.sh 90
30 3 * * * landscape /opt/canonical/landscape/scripts/cleanup-events.sh 90
```

This will schedule two tasks:

- `cleanup-activities.sh`
  - Removes finished activities older than 90 days. Runs daily at 03:00 UTC.
- `cleanup-events.sh`
  - Removes events older than 90 days. Runs every day at 03:30 UTC.

### Viewing Cleanup Task Logs

Cleanup tasks will log their output to syslog. To view them:

```bash
journalctl -t cleanup-activities -t cleanup-events
```

Or, to log these tasks to separate files, edit `/etc/rsyslog.d/20-landscape.conf` and add the following lines.

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
