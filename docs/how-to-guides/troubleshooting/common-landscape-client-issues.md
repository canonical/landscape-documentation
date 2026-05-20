---
myst:
  html_meta:
    description: "Troubleshoot Landscape Client registration, connectivity, package reporting, and Ubuntu Pro status issues."
---

(howto-troubleshoot-landscape-client)=
# How to troubleshoot Landscape Client issues

Use this guide to troubleshoot common Landscape Client issues with registration, communication with the server, client package reporting, and Ubuntu Pro status reporting.

(heading-client-general-checks)=
## If you don't know where to start

If Landscape Client isn't working and you don't know the cause yet, use these checks to narrow down the issue. After you find a specific error or symptom, go to the matching section in this guide.

### Check whether the service is running

```bash
sudo systemctl status landscape-client
```

If the service is inactive, failed, or skipped because of `Start condition unmet`, see {ref}`client-start-condition-unmet`.

### Check the broker log

```bash
sudo tail -n 50 /var/log/landscape/broker.log
```

The broker log is usually the best first log to check for client registration, certificate, hostname resolution, and client-server communication issues.

Use the log output to choose the next section:

- If the log contains `Error 60` or `server certificate verification failed`, see {ref}`client-certificate-not-trusted`.
- If the log contains `Error 77`, see {ref}`client-certificate-not-readable`.
- If the log contains `Error 6` or `Could not resolve host`, see {ref}`client-dns-resolution`.
- If the client is registered but doesn't appear online or doesn't pick up activities, see {ref}`client-debug-logging`.
- If package status is incorrect or stale, see {ref}`client-package-reporting`.

### Check hostname resolution

```bash
getent hosts <LANDSCAPE-SERVER-NAME>
```

You can also test with:

```bash
ping <LANDSCAPE-SERVER-NAME>
dig <LANDSCAPE-SERVER-NAME>
```

If the hostname doesn't resolve, fix DNS or add the correct hostname mapping to `/etc/hosts`. Then see {ref}`client-dns-resolution`.

### Check the client configuration

```bash
grep -E '^(url|ping_url|ssl_public_key)' /etc/landscape/client.conf
```

Confirm that:

- `url` points to the Landscape message system.
- `ping_url` points to the Landscape ping endpoint.
- `ssl_public_key` points to the expected certificate file (if your deployment requires one).

If the hostname, URL, or certificate path is wrong, update `/etc/landscape/client.conf` or re-run `landscape-config` with the correct values.

(client-registration-fails)=
## Registration fails

Use this section if `landscape-config` fails, the client doesn't appear as a pending instance (computer) in Landscape, or registration doesn't complete successfully.

(client-certificate-not-trusted)=
### Certificate isn't trusted

**Problem:**

The client can't register because it doesn't trust the certificate used by the Landscape server. This is common in self-hosted deployments that use a self-signed certificate or a certificate signed by an internal certificate authority.

This issue usually means the client can reach the server, but can't verify the server certificate.

**Error message:**

The registration command will fail with an SSL or signature validation error. The broker log should show an error similar to:

```text
2026-02-11 21:43:26,420 INFO     [MainThread] Starting urgent message exchange with https://<LANDSCAPE-SERVER-NAME>/message-system.
2026-02-11 21:43:26,486 ERROR    [PoolThread-twisted.internet.reactor-0] Error contacting the server at https://<LANDSCAPE-SERVER-NAME>/message-system.
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/landscape/lib/fetch.py", line 127, in fetch
    curl.perform()
pycurl.error: (60, 'server certificate verification failed. CAfile: none CRLfile: none')

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/landscape/client/broker/transport.py", line 98, in exchange
    curly, data = self._curl(
                  ^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/landscape/client/broker/transport.py", line 60, in _curl
    fetch(
  File "/usr/lib/python3/dist-packages/landscape/lib/fetch.py", line 129, in fetch
    raise PyCurlError(e.args[0], e.args[1])
landscape.lib.fetch.PyCurlError: Error 60: server certificate verification failed. CAfile: none CRLfile: none
```

#### Solution

If you use Landscape SaaS, or if your Landscape server uses a certificate trusted by the client system, you normally don't need to configure `ssl_public_key`.

If your Landscape server uses a self-signed certificate, copy that certificate to the client. If your Landscape server uses a certificate signed by an internal certificate authority, copy the issuing CA certificate to the client. Don't use only the server leaf certificate unless the certificate is self-signed.

You can configure certificate trust in either of these ways:

- Provide the certificate to Landscape Client during registration
- Import the certificate into the system CA store

To provide the certificate during registration, copy the certificate to the client and include it in the registration command:

```bash
sudo landscape-config \
  --computer-title "${HOSTNAME}" \
  --account-name <account-name> \
  --url https://<LANDSCAPE-SERVER-NAME>/message-system \
  --ping-url http://<LANDSCAPE-SERVER-NAME>/ping \
  --ssl-public-key=/etc/landscape/landscape-server.pem \
  --silent
```

You can also set the certificate path in `/etc/landscape/client.conf`:

```ini
ssl_public_key = /etc/landscape/landscape-server.pem
```

To trust the certificate system-wide, copy the certificate to `/usr/local/share/ca-certificates/` with a `.crt` extension:

```bash
sudo cp /path/to/certificate.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

System-wide trust is useful if other processes on the client also need to trust the Landscape server certificate.

(client-certificate-not-readable)=
### Certificate file can't be read

**Problem:**

The client is configured with an SSL certificate path, but Landscape Client can't locate or read the certificate file.

This is different from an untrusted certificate. In this case, the client has a certificate path configured, but the file is missing, the path is wrong, or the certificate file isn't readable by the required users.

**Error message:**

The broker log should show an error similar to:

```text
2016-08-16 09:40:24,013 INFO [MainThread] Starting urgent message exchange with https://YOUR.OPL.ADDRESS/message-system.
2016-08-16 09:40:24,020 ERROR [PoolThread-twisted.internet.reactor-1] Error contacting the server at https://YOUR.OPL.ADDRESS/message-system.
Traceback (most recent call last):
File "/usr/lib/python2.7/dist-packages/landscape/broker/transport.py", line 71, in exchange
message_api)
File "/usr/lib/python2.7/dist-packages/landscape/broker/transport.py", line 45, in _curl
headers=headers, cainfo=self._pubkey, curl=curl))
File "/usr/lib/python2.7/dist-packages/landscape/lib/fetch.py", line 109, in fetch
raise PyCurlError(e.args[0], e.args[1])
PyCurlError: Error 77:
2016-08-16 09:40:24,021 INFO [MainThread] Message exchange failed.
2016-08-16 09:40:24,021 INFO [MainThread] Message exchange completed in 0.01s.
```

#### Solution

Check that the `ssl_public_key` setting in `/etc/landscape/client.conf` points to the certificate file that Landscape Client should use. For example:

```ini
ssl_public_key = /etc/ssl/certs/landscape_server_ca.crt
```

Confirm that the configured certificate file exists and is readable. If you changed the path to your certificate, use that path instead of `/etc/ssl/certs/landscape_server_ca.crt`.

```bash
sudo ls -l /etc/ssl/certs/landscape_server_ca.crt
```

The certificate file must be readable by `root` and the `landscape` user.

If another client is registered successfully with the same configuration, compare the certificate file on both machines:

```bash
md5sum /PATH/TO/SSL/CERT
```

If the file path is wrong, update `/etc/landscape/client.conf` or re-run `landscape-config` with the correct `--ssl-public-key` value.

(client-dns-resolution)=
### Server name can't be resolved

**Problem:**

The client can't register or check in because it can't resolve the Landscape server hostname.

This can happen when the server hostname is missing from DNS, the client is using the wrong hostname, or a local test environment requires an `/etc/hosts` entry.

**Error message:**

The broker log should show an error similar to:

```text
2026-02-11 22:07:20,451 INFO     [MainThread] Starting urgent message exchange with https://<LANDSCAPE-SERVER-NAME>/message-system.
2026-02-11 22:07:20,453 ERROR    [PoolThread-twisted.internet.reactor-1] Error contacting the server at https://<LANDSCAPE-SERVER-NAME>/message-system.
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/landscape/lib/fetch.py", line 127, in fetch
    curl.perform()
pycurl.error: (6, 'Could not resolve host: landscape-2404-noble')

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/landscape/client/broker/transport.py", line 98, in exchange
    curly, data = self._curl(
                  ^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/landscape/client/broker/transport.py", line 60, in _curl
    fetch(
  File "/usr/lib/python3/dist-packages/landscape/lib/fetch.py", line 129, in fetch
    raise PyCurlError(e.args[0], e.args[1])
landscape.lib.fetch.PyCurlError: Error 6: Could not resolve host: <LANDSCAPE-SERVER-NAME>
```

#### Solution

Check that the client can resolve the Landscape server hostname or FQDN:

```bash
getent hosts <LANDSCAPE-SERVER-NAME>
```

You can also check DNS with:

```bash
dig <LANDSCAPE-SERVER-NAME>
```

If you are testing in a local environment, or if the server name isn't in DNS, add the correct hostname mapping to `/etc/hosts`.

Check the configured Landscape URLs:

```bash
grep -E '^(url|ping_url)' /etc/landscape/client.conf
```

Confirm that the configured hostname matches the hostname that the client can resolve.

After fixing DNS or `/etc/hosts`, run registration again:

```bash
sudo landscape-config
```

For non-interactive registration, use `--silent` only when the required values are already in `/etc/landscape/client.conf` or provided as command-line options.

(client-registration-pending)=
### Registration remains pending

**Problem:**

The registration command succeeds, but the machine doesn't appear as a fully managed computer in Landscape.

**Symptoms:**

- `landscape-config` reports that the registration request was sent successfully.
- The machine appears as a pending computer in the Landscape web portal.
- The machine doesn't appear as a fully managed computer yet.

#### Solution

If your deployment requires manual approval, approve the pending computer in the Landscape web portal.

If the pending registration belongs to an existing machine, map it to the existing machine entry instead of accepting it as a new computer. In the classic web portal, use the **Computer** field on the pending registration form to select the existing computer before accepting the registration.

For more information about duplicate-management workflows, see {ref}`how-to-remove-duplicate-instances`.

(client-start-condition-unmet)=
## Client service doesn't start

**Problem:**

The `landscape-client` service doesn't start because the client doesn't consider itself registered.

Landscape Client checks whether a registration request has been sent before the service starts. If the local registration state is missing or corrupted, the service start condition fails.

**Error message:**

`systemctl status landscape-client` may show output similar to this:

```text
○ landscape-client.service - Landscape client daemons
     Loaded: loaded (/usr/lib/systemd/system/landscape-client.service; enabled; preset: enabled)
     Active: inactive (dead) (Result: exec-condition) since Thu 2026-02-12 18:17:32 UTC; 7s ago
   Duration: 19h 2min 58.628s
  Condition: start condition unmet at Thu 2026-02-12 18:17:31 UTC; 8s ago
       Docs: man:landscape-client(1)
             man:landscape-config(1)
    Process: 20873 ExecCondition=/usr/bin/landscape-config --is-registered (code=exited, status=5)
        CPU: 420ms

Feb 12 18:17:31 noble-squid-proxy systemd[1]: Starting landscape-client.service - Landscape client daemons...
Feb 12 18:17:32 noble-squid-proxy landscape-config[20873]: Registered:    False
Feb 12 18:17:32 noble-squid-proxy landscape-config[20873]: Config Path:   /etc/landscape/client.conf
Feb 12 18:17:32 noble-squid-proxy landscape-config[20873]: Data Path      /var/lib/landscape/client
Feb 12 18:17:32 noble-squid-proxy systemd[1]: landscape-client.service: Skipped due to 'exec-condition'.
Feb 12 18:17:32 noble-squid-proxy systemd[1]: Condition check resulted in landscape-client.service - Landscape client daemons being skipped.
```

### Solution

Check for the broker state file and its backup:

```bash
sudo ls -l /var/lib/landscape/client/broker.bpickle*
```

The broker state file is:

```text
/var/lib/landscape/client/broker.bpickle
```

The backup file is:

```text
/var/lib/landscape/client/broker.bpickle.old
```

If the broker state file is missing or corrupted, send a new registration request:

```bash
sudo landscape-config
```

If `/etc/landscape/client.conf` already contains the required account and server configuration, you can reuse the existing configuration:

```bash
sudo landscape-config --silent
```

Only use `--silent` when the required configuration values are already present in `/etc/landscape/client.conf` or provided as command-line options.

After registration is sent, check the service again:

```bash
sudo systemctl status landscape-client
```

If your deployment requires manual approval, approve the pending registration in the Landscape web portal.

(client-duplicate-instances)=
## Client appears as a duplicate machine

A client machine can appear more than once in Landscape if it sends a new registration request and that request is accepted as a new computer.

This can happen after communication problems, repeated use of `landscape-config`, reinstalling a machine, restoring a machine, or deleting local client state. Also, if the server has a registration key configured and auto-registration is enabled, registration requests are accepted automatically.

### Solution

If the machine is still pending (not yet duplicated), map it to the existing machine entry. Note this is only available in the *classic* web portal.

1. Open the pending registration.
1. In the **Computer** dropdown, select the existing machine you want to map it with
1. Accept the pending registration.

If duplicate machines already exist, follow {ref}`how-to-remove-duplicate-instances`.

(client-pro-status)=
## Ubuntu Pro or licensing status is wrong

**Problem:**

Landscape shows the wrong Ubuntu Pro or licensing status for a client.

Landscape Client uses Ubuntu Pro Client to gather status information. Ubuntu Pro Client must be installed and functional even if the machine isn't attached to an Ubuntu Pro subscription.

**Symptoms:**

- Landscape shows the wrong seat type or licensing status.
- The client fails to send Ubuntu Pro status information.
- The broker log contains an error related to `prostatus.json`.
- `pro status` fails on the client.
- The machine has a broken or non-standard Python environment.
- Security hardening prevents the `landscape` user from running the required command.

### Solution

Check whether Ubuntu Pro Client works locally:

```bash
pro status
```

Review recent Landscape Client logs:

```bash
sudo tail -n 100 /var/log/landscape/broker.log
sudo tail -n 100 /var/log/landscape/manager.log
```

Check for local conditions that might prevent Landscape Client from collecting Ubuntu Pro status:

- Ubuntu Pro Client is missing or broken.
- The machine has a broken or non-standard Python environment.
- File permissions prevent the `landscape` user from running the required command.
- Security hardening has changed permissions expected by Landscape Client.

After fixing the local issue, restart Landscape Client:

```bash
sudo systemctl restart landscape-client
```

(client-package-reporting)=
## Package status is incorrect or not reporting

**Problem:**

Landscape shows stale or incorrect package information for a client.

This can affect upgrade profiles because Landscape might not detect that updates are available.

**Symptoms:**

- Landscape reports the machine as up to date, but `apt` shows pending updates.
- Upgrade profiles don't run because Landscape doesn't detect available updates.
- Landscape shows an alert that the client is having trouble reporting package information.
- `/var/log/landscape/package-reporter.log` contains package reporting errors.
- Package reporting is very slow or appears stuck.

### Solution #1: Fix broken APT sources

First, update the local package list and confirm whether the client has pending updates:

```bash
sudo apt update
```

Then review the package reporter log:

```bash
sudo tail -n 100 /var/log/landscape/package-reporter.log
```

Look for entries that show whether the client downloaded the hash-to-ID database and whether it queued package reporting messages.

Example package reporter log entries:

```text
2025-06-11 18:05:52,551 INFO     [MainThread] Downloaded hash=>id database from https://landscape.canonical.com/hash-id-databases/af6f2dcf-1967-11de-8dd0-001a4b4d8d10_noble_amd64
2025-06-11 18:05:52,562 WARNING  [MainThread] Removing cached hash=>id database /var/lib/landscape/client/package/hash-id/af6f2dcf-1967-11de-8dd0-001a4b4d8d10_noble_amd64
2025-06-11 18:05:58,022 INFO     [MainThread] Queuing request for package hash => id translation on 111 hash(es).
2025-06-11 18:06:42,866 INFO     [MainThread] Queuing message with changes in known packages: 598 installed, 90750 available, 0 available upgrades, 0 locked, 0 autoremovable, 14855 security, 0 not installed, 0 not available, 0 not available upgrades, 0 not locked, 0 not autoremovable, 0 not security.
```

If the server reports that the client is having trouble reporting package information, check the client's APT sources. A broken APT source can prevent package reporting from completing. Common causes include:

- an old PPA that no longer exists
- a third-party repository that is unavailable
- a repository that doesn't publish packages for the client's Ubuntu release
- an invalid file in `/etc/apt/sources.list.d/`

After fixing broken APT sources, run:

```bash
sudo apt update
```

Then restart Landscape Client:

```bash
sudo systemctl restart landscape-client
```

### Solution #2: Force a package reporting resynchronization

If package reporting appears to run, but Landscape still shows stale package information, force the client to rebuild its local package state.

Remove the local package state database:

```bash
sudo rm /var/lib/landscape/client/package/database
```

Then restart Landscape Client:

```bash
sudo systemctl restart landscape-client
```

Landscape Client should rebuild the local package database and send updated package information to the server.

If this doesn't resolve the issue, re-register the machine. If the re-registration appears as pending and belongs to an existing computer, map it to the existing computer instead of accepting it as a new one.

### Solution #3: Check permissions for the Landscape APT update helper

Landscape uses its own helper script to check for updates. This script must have the expected permissions, including the `setuid` bit. Some security tools may remove this permission.

Check the file permissions:

```bash
ls -lah /usr/lib/landscape/apt-update
```

Expected output should include the `s` bit:

```text
-rwsr-xr-- 1 root landscape  /usr/lib/landscape/apt-update
```

If the logs show that Landscape can't run this script, check whether a security tool or hardening policy changed the permissions.

For more information about package hashes, package IDs, and package reporting internals, see {ref}`explanation-package-reporting`.

(client-debug-logging)=
## Client is registered but doesn't pick up activities

**Problem:**

The client is registered, but it doesn't appear to pick up activities from Landscape or return activity results.

**Symptoms:**

- The client doesn't show a current ping time.
- Activities remain queued or pending.
- Script activities don't appear to run.
- Activity results are not returned to Landscape.
- The default broker log doesn't contain enough detail to diagnose the issue.

### Solution

Check whether the service is running:

```bash
sudo systemctl status landscape-client
```

Review the broker log:

```bash
sudo tail -n 100 /var/log/landscape/broker.log
```

Check the configured URLs:

```bash
grep -E '^(url|ping_url)' /etc/landscape/client.conf
```

The `ping_url` is used for client heartbeat checks. The `url` is used for message exchange between the client and server, including activities and activity results.

If the broker log doesn't show enough detail, enable debug logging.

Open `/etc/landscape/client.conf` and set:

```ini
log_level = debug
```

Restart Landscape Client:

```bash
sudo systemctl restart landscape-client
```

Review the broker log again:

```bash
sudo tail -n 100 /var/log/landscape/broker.log
```

At debug level, `broker.log` can show the full message exchange between the client and server. For script activities, debug logging can show the script received by the client and the output returned to the server.

Debug logs can contain detailed system information, activity payloads, and script output. Disable debug logging after troubleshooting:

```ini
log_level = info
```

Then restart the client:

```bash
sudo systemctl restart landscape-client
```