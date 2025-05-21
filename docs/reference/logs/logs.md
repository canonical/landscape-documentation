(reference-logs)=
# Logs

You can find the Landscape's logs in the following locations:

- **Landscape Client logs**: `/var/log/landscape/`
- **Landscape Server logs**: `/var/log/landscape-server/`

These are some of the different logs generated:

* `anonymous-metrics.log`: Logs from the anonymous-metrics cron about the Ubuntu version, Landscape server version and the number of registered computers.
* `api.log`: Log for API server; the API services handles requests from landscape-api clients
* `appserver.log`: Output of the application server
* `async-frontend.log`: Log for async-frontend server; the async front end delivers AJAX-style content to the web user interface
* `broker.log`: The client's message broker logs.
* `distributed-lock.log`: Log for the distributed lock, which ensures there is at most one instance of scripts running at a time
* `hash-id-databases.log`: Logs from the script which builds the list of available packages
* `job-handler.log`: Log for job-handler server; the job handler service controls individual back-end tasks on the server
* `landscape-profiles.log`: Output from the cron job generating profiles
* `landscape-quickstart.log`: Post-installation script logs
* `landscape-setup.log`: Logs from the setup script
* `maintenance-script.log`: Output of that cron job; removes old monitoring data and performs other maintenance tasks
* `message_server.log`: Output of message server; the message server handles communication between the clients and the server
* `meta-releases.log`: Log from the meta-releases script, which checks periodically if there are new ubuntu releases
* `package-search.log`: Log from the package-search service; this service allows searching for packages by name through the web interface
* `package-upload.log`: Output of package-upload server, which is used in repository management for upload pockets, which are repositories that hold packages that are uploaded to them by authorized users
* `pingserver.log`: Output of pingserver; the pingserver tracks client heartbeats to watch for unresponsive clients
* `process-alerts.log`: Output of the cron job used to trigger alerts and send out alert email messages
* `syncldsreleases.log`: Daily cron job that checks for new self-hosted Landscape release versions
* `update-security-db.log`: Output of the cron job that checks for new Ubuntu Security Notices
* `update-alerts.log`: Output of that cron job. Used to determine which computers are offline
* `usn-script.log`: Output from the usn-script, which process the new data from the Ubuntu Security Notices

