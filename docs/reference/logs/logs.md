---
myst:
  html_meta:
    description: "Reference for Landscape log files for client and server services, including locations for broker, manager, API, message-server, and more."
---

(reference-logs)=
# Logs

Landscape generates logs for both client- and server-side services. This document lists where to find these logs and what the logs are used for. The standard locations for core third-party dependency logs are also noted.

## Client logs

Landscape Client logs are located in `/var/log/landscape/`.

- `broker.log`: The client's message broker logs. This handles communication to the server.
- `manager.log`: Logs client-side management activity, such as modifying local (system) user accounts.
- `monitor.log`: Logs client-side monitoring activity, such as system metrics.
- `package-changer.log`: Logs operations where the client applies package changes (installation, upgrade, etc.) from the server.
- `package-reporter.log`: Logs the details of the packages reported by the client to the server.
- `watchdog.log`: Logs from the top-level watchdog process that monitors other client daemons (manager, monitor, etc.) and restarts them if they fail.

## Server logs

Landscape Server logs are located in `/var/log/landscape-server/`.

- `anonymous-metrics.log`: Logs from the `anonymous-metrics` cron job about the Ubuntu version, Landscape server version, and the number of registered clients
- `api.log`: Logs for the API services that handles requests from the web UI (`landscape-ui`) and `landscape-api` clients
- `appserver.log`: Logs for the application server for the *legacy* web UI
- `async-frontend.log`: Logs for the `async-frontend` server for the *legacy* web UI
- `distributed-lock.log`: Logs for the distributed lock, which ensures there is at most one instance of critical scripts running at a time (such as cron jobs that modify shared state)
- `hash-id-databases.log`: Logs from the script which builds the list of available packages for clients
- `job-handler.log`: Logs for the `job-handler` service, which controls the execution of back-end tasks queued by the server, such as repository operations or reporting jobs
- `landscape-profiles.log`: Logs output from the cron job generating profiles
- `landscape-quickstart.log`: (Quickstart only) Logs from the post-installation script
- `landscape-setup.log`: (Quickstart only) Logs from the setup script
- `maintenance-script.log`: Logs output from the maintenance cron job, which removes old monitoring data and performs other maintenance tasks
- `message-server.log`: Logs the output of `message-server`, which handles communication between the clients and the server
- `meta-releases.log`: Logs from the `meta-releases` script, which checks periodically for new Ubuntu releases
- `package-search.log`: Logs from the `package-search` service, which allows searching for packages by name through the web UI
- `package-upload.log`: Logs output of the `package-upload` server, which is used in repository management for upload pockets.
- `pingserver.log`: Logs the output of `pingserver`, which tracks client heartbeats to monitor for unresponsive clients
- `process-alerts.log`: Logs output of the cron job used to trigger alerts and send out alert email messages
- `schema-maintenance.log`: Logs from the maintenance cron job that cleans up old monitoring data, such as historical temperature, network traffic, and CPU load data.
- `syncldsreleases.log`: Logs from the daily cron job that checks for new self-hosted Landscape release versions
- `update-alerts.log`: Logs output of the cron job that determines which clients are offline
- `update-security-db.log`: Logs output of the cron job that checks for new Ubuntu Security Notices
- `usn-script.log`: Logs output from the `usn-script`, which process the new data from the Ubuntu Security Notices

## Other logs

Landscape also relies on the following third-party infrastructure: HAProxy (if used), PostgreSQL, and RabbitMQ. The typical locations for these logs are:

### HAProxy

- `/var/log/haproxy.log`

### PostgreSQL

- `/var/log/postgresql/postgresql-<VERSION>-main.log`

### RabbitMQ

- `/var/log/rabbitmq/rabbitmq-server.log`
- `/var/log/rabbitmq/rabbit@<HOSTNAME>.log`
- `/var/log/rabbitmq/rabbitmq-server.error.log`
