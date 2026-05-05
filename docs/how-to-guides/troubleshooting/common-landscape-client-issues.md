---
myst:
  html_meta:
    description: "Troubleshoot common Landscape Client issues including registration, connectivity, and configuration problems."
---

(howto-common-landscape-client-issues)=
# How to troubleshoot common Landscape Client issues

This guide covers common issues with Landscape Client and the steps you can take to diagnose and resolve them.

## Registration fails

Common causes for Landscape clients to fail when registering.

### SSL certificate verification issues

If registration fails with certificate validation errors, the client likely doesn't trust the Landscape server's SSL certificate. This is common in self-hosted environments using self-signed or internal CA certificates.

- **Symptoms:**
    - The registration command returns a "signature validation failed" error.
    - `broker.log` contains `certificate verification failed`.
- **Resolution (Option A - Client Level):** Provide the public key directly during the registration process to tell the client specifically to trust that server:
    ```bash
    sudo landscape-config --ssl-public-key /path/to/server.pem
    ```
- **Resolution (Option B - System Level):** Import the certificate into the system's trusted authority store so all system processes trust it:
    1. Copy the certificate to `/usr/local/share/ca-certificates/` (ensure it has a `.crt` extension).
    1. Run `sudo update-ca-certificates`.
- **Critical note:** If the server uses an internally signed certificate, you must provide the **CA (Root) certificate**, not just the server's leaf certificate.

### Start condition unmet (error code 5)

If the Landscape Client service doesn't start and reports `Start condition unmet`, the client is usually missing local registration state. The Landscape client checks for evidence of registration before allowing the service to start. This prevents "headless" clients from spamming the server with requests if they aren't authorized.

- **Symptom:** `systemctl status landscape-client` reports `Start condition unmet` with `status=5`.
- **Cause:** The service cannot find the state files (`broker.pickle` or `broker.pickle.old`) in `/var/lib/landscape/client/`.
- **Resolution:** Re-run the configuration command to regenerate the state files and re-register:
    ```bash
    sudo landscape-config --silent
    ```

## Managing duplicate machine entries

When a machine is re-registered (e.g., after a re-install or accidental deletion of a local state file), it may appear as a new "pending" computer in the dashboard.

- **Mapping to previous entries:** In the **Classic UI**, do not simply "Accept" a pending registration. Use the **"Map to a previous machine entry"** option. This merges the new registration with the existing history and data of the previous entry for that machine.
- **Current limitation:** This mapping feature is available in the Classic UI and via the API, but is currently absent from the newer UI iterations.

## Ubuntu Pro or licensing status is incorrect

If a machine shows the wrong licensing state, the Landscape client may be unable to gather data from Ubuntu Pro Client. The Landscape client interacts with Ubuntu Pro Client to determine whether a machine should occupy a "Legacy" or "Pro" seat.

- **Requirement:** Ubuntu Pro Client must be installed and functional for the client to gather licensing data, even if the machine is not actively attached to a Pro subscription.
- **Common failure:** If the logs show a `prostatus.json` parsing error, check for:
    - Broken or non-standard Python environments.
    - Security hardening (e.g., restricted file permissions) that prevents the `landscape` user from executing the `pro` command.

## Package status is incorrect or not updating

### Fast vs. slow reporting methods

If package information is slow to update or appears inconsistent, it helps to understand how Landscape reports package lists. Landscape uses a hash-based system to report package lists efficiently.
- **The fast method:** The client downloads a pre-generated hash database from the server. It compares local packages against these hashes. If they match, it sends a tiny "ID" instead of the full package name/version.
- **The slow method:** If the hashes don't match (common with PPAs or third-party repos), the client sends data in "chunks" of 500 packages.
- **Outdated clients:** If a client hasn't checked in for several months, its local package versions will likely not exist in the server's current hash database, forcing it into "slow mode" until it catches up.

### Forcing a full re-synchronization

If the Landscape dashboard incorrectly reports a machine as "Up to date" while `apt` shows pending updates, the local SQLite database may be out of sync.

1. **Stop the client:** `sudo systemctl stop landscape-client`
1. **Remove the local database:**
    ```bash
    sudo rm /var/lib/landscape/client/package-database
    ```
1. **Restart the client:** `sudo systemctl start landscape-client`
    - The client will detect the missing database, regenerate it from the current system state, and send a full resynchronization message to the server.

## Advanced diagnostic steps

### Enabling debug logging

To see the actual content of messages (scripts, hardware manifests, package lists) being exchanged between the client and server:

1. Open `/etc/landscape/client.conf` in a text editor.
1. Set `log_level = debug`.
1. Restart the service: `sudo systemctl restart landscape-client`.

### Essential log locations

- **`/var/log/landscape/broker.log`**: Covers general communication, registration, and SSL handshaking.
- **`/var/log/landscape/package-reporter.log`**: Details package hashing, chunked reporting, and synchronization events.
- **`/var/log/landscape/manager.log`**: Logs the high-level management of the various client components.