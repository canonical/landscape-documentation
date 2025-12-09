(how-to-manage-maintenance)=
# How to manage maintenance tasks

Landscape Server installs a few scheduled tasks, defined in the `/etc/cron.d/landscape-server` file.

* `/opt/canonical/landscape/scripts/maintenance.sh`
    - This task does the daily maintenance of adding monitoring graphs tables and deleting older data. Failure to run this task for multiple days prevents monitoring data from being stored, and will lead to gaps in the graphs.
* `/opt/canonical/landscape/scripts/update_security_db.sh`
    - This task loads new USN/CVE data. This is required for identifying which updates are "security updates".
* `( /opt/canonical/landscape/scripts/update_alerts.sh; /opt/canonical/landscape/scripts/landscape_profiles.sh; /opt/canonical/landscape/scripts/process_alerts.sh )`
    - This set of tasks processes alerts and applies {ref}`profiles <reference-terms-profiles>`. Part of the Landscape functionalities depends on checking conditions at frequent intervals. This includes offline alerts, and package profile compliance.
* `/opt/canonical/landscape/scripts/hash_id_databases.sh`
    - This tasks regenerates packages hash-ids mapping files. Those hash-id files are what helps for newly registered computers to report their installed and available packages quickly. Out-of-date hash-id files causes computers to report their package at a slower rate (500 packages at a time).
* `/opt/canonical/landscape/scripts/meta_releases.sh`
    - This task checks for new releases of Ubuntu.
* `/opt/canonical/landscape/scripts/sync_lds_releases.sh`
    - This task verifies if there are new Landscape Server upgrades available in order to add a notification on the account page.
* `/opt/canonical/landscape/scripts/report_anonymous_metrics.sh`
    - This task reports some anonymous metrics, such as the installed Landscape Server version.


## Optional Cleaning of Activity History

Landscape already includes maintenance tasks to limit monitoring graphs history, as mentioned previously. Extra maintenance jobs can also be scheduled to limit old activities and old events to a retention period. For example, if you create a `/etc/cron.d/ls_maintenance` file and add the following:

```text
0 3 * * * landscape /opt/canonical/landscape/cleanup-activities 90
30 3 * * * landscape /opt/canonical/landscape/cleanup-events 90
```

This will schedule 2 tasks:

- A cleanup of finished activities older than 90 days. Runs every day at 3:00.
- A cleanup of events older than 90 days. Runs every day at 3:30.

Those tools will log their output to syslog. This can be inspected by running

```text
journalctl -t cleanup-activities -t cleanup-events
```

The result of those tasks can also be logged to separate files, much like other Landscape services. To do that, edit the `/etc/rsyslog.d/20-landscape.conf` file and add the following lines to the end:

```text
if $programname == 'cleanup-activities' then /var/log/landscape-server/cleanup-activities.log;Landscape
& ~
if $programname == 'cleanup-events' then /var/log/landscape-server/cleanup-events.log;Landscape
& ~
```

Then restart the logging service by running:

```text
sudo systemctl restart rsyslog.service
```

