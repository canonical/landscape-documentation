---
myst:
  html_meta:
    description: "Troubleshoot Landscape Client registration, connectivity, package reporting, and Ubuntu Pro status issues."
---

(howto-troubleshoot-landscape-client)=
# How to troubleshoot Landscape Client issues

Issues with Landscape Client can have many different causes. This guide describes common problems and troubleshooting steps you can take.

If you've worked through these steps and still need help, we recommend contacting [Canonical Support](https://support-portal.canonical.com/). Note that you'll need a Support contract to use our Support Portal.

(heading-client-general-checks)=
## Start here: Initial client checks

If Landscape Client isn't working and you don't know the cause yet, use these general checks to narrow down the issue. After you find a specific error or symptom, go to the matching section in this guide.

### Check whether the service is running

```bash
sudo systemctl status landscape-client
```

If the service shows `Start condition unmet`, see {ref}`heading-client-start-condition-unmet`.

### Check the broker log

```bash
sudo tail -n 50 /var/log/landscape/broker.log
```

The broker log is usually the first log you should check for client registration, certificate, hostname resolution, and client-server communication issues.

Use the log output to choose the next section:

- If the log contains `Error 60` or `server certificate verification failed`, see {ref}`heading-client-certificate-not-trusted`.
- If the log contains `Error 77`, see {ref}`heading-client-certificate-not-readable`.
- If the log contains `Error 6` or `Could not resolve host`, see {ref}`heading-client-dns-resolution`.
- If the log contains an error referencing `prostatus.json`, see {ref}`heading-client-pro-status`.
- If the client is registered but doesn't appear online or doesn't pick up activities, see {ref}`heading-client-debug-logging`.
- If package status is incorrect or stale, see {ref}`heading-client-package-reporting`.

### Check hostname resolution

Check that the Landscape server hostname resolves correctly:

```bash
getent hosts <LANDSCAPE-SERVER-NAME>
```

If hostname resolution works, this command returns an IP address followed by the hostname. If it returns no output, the hostname didn't resolve.

You can also test with:

```bash
ping <LANDSCAPE-SERVER-NAME>
dig <LANDSCAPE-SERVER-NAME>
```

With `ping`, failed resolution usually shows an error such as `Name or service not known` or `Temporary failure in name resolution`. With `dig`, failed resolution usually appears as `status: NXDOMAIN`.

If the hostname doesn't resolve, see {ref}`heading-client-dns-resolution`.

### Check the client configuration

Check the key settings in the Landscape Client configuration file:

```bash
grep -E '^(url|ping_url|ssl_public_key)' /etc/landscape/client.conf
```

Confirm that:

- `url` points to the Landscape message system.
- `ping_url` points to the Landscape ping endpoint.
- `ssl_public_key` points to the expected certificate file (if your deployment requires one).

If the hostname, URL, or certificate path is wrong, update `/etc/landscape/client.conf` or re-run `landscape-config` with the correct values.

(heading-client-registration-fails)=
## Registration fails

This section covers issues where `landscape-config` fails or the client doesn't appear in Landscape after registration.

(heading-client-certificate-not-trusted)=
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

First, copy the correct certificate to the client:

- If your Landscape server uses a self-signed certificate, copy that certificate to the client.
- If your Landscape server uses a certificate signed by an internal certificate authority, copy the issuing CA certificate to the client (not the server leaf certificate).

Then configure certificate trust using one of these methods:

**Method 1: Tell Landscape Client directly about the certificate**

Pass the certificate path when running `landscape-config`:

```bash
sudo landscape-config \
  --computer-title "${HOSTNAME}" \
  --account-name <ACCOUNT-NAME> \
  --url https://<LANDSCAPE-SERVER-NAME>/message-system \
  --ping-url http://<LANDSCAPE-SERVER-NAME>/ping \
  --ssl-public-key=/etc/landscape/landscape-server.pem
```

This sets `ssl_public_key` in `/etc/landscape/client.conf`. You can also set it directly in the config file:

```ini
ssl_public_key = /etc/landscape/landscape-server.pem
```

**Method 2: Import the certificate into the system CA store**

Copy the certificate to `/usr/local/share/ca-certificates/` with a `.crt` extension and update the system CA store:

```bash
sudo cp /PATH/TO/CERTIFICATE.CRT /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

This approach trusts the certificate system-wide, so all processes on the client trust the Landscape server certificate. It's useful if managing the certificate path in `client.conf` on each client machine individually isn't practical.

(heading-client-certificate-not-readable)=
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
File "/usr/lib/python3/dist-packages/landscape/client/broker/transport.py", line 71, in exchange
message_api)
File "/usr/lib/python3/dist-packages/landscape/client/broker/transport.py", line 45, in _curl
headers=headers, cainfo=self._pubkey, curl=curl))
File "/usr/lib/python3/dist-packages/landscape/lib/fetch.py", line 109, in fetch
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

(heading-client-dns-resolution)=
### Server name can't be resolved

**Problem:**

The client can't register or communicate with the server because it can't resolve the Landscape server hostname.

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

(heading-client-pro-status)=
### Client can't run `pro status`

> See also: [Ubuntu Pro Client documentation](https://documentation.ubuntu.com/pro-client/)

**Problem:**

Landscape Client runs `pro status` during registration to determine whether the machine should receive a Pro (or Legacy) license seat. If the client can't collect this information and send it to the server, the client will fail to register.

**Symptoms:**

- The broker log contains a pre-registration failure error, such as `Pre-registration failure: Could not parse prostatus.json`.
- `pro status` fails when run manually on the client.

**Common causes:**

- Ubuntu Pro Client isn't installed on the client machine
- The client machine has a broken or non-standard Python environment.
- Security hardening or file permissions prevent the `landscape` user from running `pro status`.

#### Solution

Confirm the issue by running `pro status` on the client:

```bash
pro status
```

If this command fails:

- If Ubuntu Pro Client isn't installed, install it:

    ```bash
    sudo apt install ubuntu-pro-client
    ```

- If the error indicates a broken Python runtime or restricted permissions, fix those local issues.
- If additional security hardening is enabled, verify that the `landscape` user can execute `/usr/bin/pro` and read Ubuntu Pro client configuration files.

Then run `pro status` again and confirm it succeeds.

After resolving the issue, re-run registration:

```bash
sudo landscape-config
```

(heading-client-registration-pending)=
## Pending registration belongs to an existing machine

A pending registration can belong to an existing machine instead of a new one. This often happens when the machine is re-registered after a communication failure or after the machine is reinstalled (for example, the OS image is rebuilt).

### Solution

Note that this must be done in the *classic* web portal.

Map the pending registration to the existing machine entry instead of accepting it as a new machine. In the classic web portal, use the **Computer** field on the pending registration form to select the existing registered computer. Then **Accept** the registration.

(heading-client-duplicate-instances)=
## Client appears as a duplicate instance/machine

A client machine can appear more than once in Landscape if a new registration request is accepted as a new client instead of being mapped to the existing entry.

### Solution

For steps to resolve duplicate machines, see {ref}`how-to-remove-duplicate-instances`.

(heading-client-start-condition-unmet)=
## Client service doesn't start

**Problem:**

The `landscape-client` service doesn't start because the client doesn't consider itself registered.

Landscape Client checks whether a registration request has been sent before the service starts. If the local registration state is missing or corrupted, the service start condition fails.

**Error message:**

Running `systemctl status landscape-client` should show output similar to:

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

The expected filepaths are:

- Broker state file: `/var/lib/landscape/client/broker.bpickle`
- Backup file: `/var/lib/landscape/client/broker.bpickle.old`

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

If your deployment requires manual approval of new clients, approve the pending registration in the Landscape web portal.

(heading-client-debug-logging)=
## Client is registered but doesn't pick up activities

**Problem:**

The client is already registered and accepted, but it doesn't appear to pick up activities from Landscape or return activity results.

If this issue affects multiple clients, see {ref}`how-to-idle-activities` as it's likely an issue with the server.

**Symptoms:**

- The client doesn't show a current ping time.
- Activities remain queued or pending.
- Script activities don't appear to run.
- Activity results are not returned to Landscape.

### Solution

Start with the general checks in this guide: {ref}`heading-client-general-checks`. If those checks don't reveal the cause, enable debug logging to get more detail from the broker log.

Open `/etc/landscape/client.conf` and set:

```ini
log_level = debug
```

Then restart Landscape Client and review the broker log:

```bash
sudo systemctl restart landscape-client
sudo tail -n 200 /var/log/landscape/broker.log
```

At debug level, `broker.log` shows the full message exchange between the client and server. Look for:

- Ping exchange entries to confirm the client is reaching the server.
- Incoming message entries describing received activities.
- Outgoing message entries after an activity runs, confirming results are sent back.
- For script activities, the script content received and any output or error returned to the server.

If you can see the client pinging but no activities arriving, the issue is likely on the server side. Check that the client is in the expected access group and has the correct tags for the activity.

If activities arrive but don't complete or return results, look for errors in the log immediately after the activity is received.

After troubleshooting, restore the log level in `/etc/landscape/client.conf`:

```ini
log_level = info
```

And restart the client:

```bash
sudo systemctl restart landscape-client
```

(heading-client-package-reporting)=
## Package status is incorrect or not reporting

**Problem:**

Landscape shows stale or incorrect package information for a client.

This can affect {ref}`upgrade profiles <reference-terms-upgrade-profile>` because Landscape might not detect that updates are available.

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

Look for entries that show whether the client downloaded the `hash-id` database and whether it queued package reporting messages.

Example package reporter log entries:

```text
2025-06-11 18:05:52,551 INFO     [MainThread] Downloaded hash=>id database from https://landscape.canonical.com/hash-id-databases/af6f2dcf-1967-11de-8dd0-001a4b4d8d10_noble_amd64
2025-06-11 18:05:52,562 WARNING  [MainThread] Removing cached hash=>id database /var/lib/landscape/client/package/hash-id/af6f2dcf-1967-11de-8dd0-001a4b4d8d10_noble_amd64
2025-06-11 18:05:58,022 INFO     [MainThread] Queuing request for package hash => id translation on 111 hash(es).
2025-06-11 18:06:42,866 INFO     [MainThread] Queuing message with changes in known packages: 598 installed, 90750 available, 0 available upgrades, 0 locked, 0 autoremovable, 14855 security, 0 not installed, 0 not available, 0 not available upgrades, 0 not locked, 0 not autoremovable, 0 not security.
```

If the server reports that the client isn't reporting package information, check the client's APT sources. A broken APT source can prevent package reporting from completing. Common causes include:

- An old PPA that no longer exists
- A third-party repository that is unavailable
- A repository that doesn't publish packages for the client's Ubuntu release
- An invalid file in `/etc/apt/sources.list.d/`

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

If this doesn't resolve the issue, re-register the machine. If the re-registration appears as pending and belongs to an existing computer, {ref}`map it to the existing machine instead of accepting it as a new one <heading-client-registration-pending>`.

### Solution #3: Check permissions for the Landscape APT update helper

Landscape uses its own helper script to check for updates. This script must keep its `setuid` permission, which some security tools remove.

Check the file permissions:

```bash
ls -lah /usr/lib/landscape/apt-update
```

Expected output should include the `s` permission marker:

```text
-rwsr-xr-- 1 root landscape  /usr/lib/landscape/apt-update
```

For more information about package hashes, package IDs, and package reporting internals, see {ref}`explanation-package-reporting`.
