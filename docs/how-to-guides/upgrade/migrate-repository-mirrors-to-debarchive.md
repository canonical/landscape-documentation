---
myst:
  html_meta:
    description: "Migrate repository mirrors from pre-26.04 reprepro-managed repositories (Landscape 25.10 and earlier) to the new debarchive service introduced in Landscape 26.04 LTS."
---

(how-to-migrate-repository-mirrors-to-debarchive)=
# How to migrate repository mirrors to Deb Archive

This guide describes how to migrate your existing reprepro-managed repository mirrors from Landscape 25.10 (and earlier) to the new Deb Archive service introduced in Landscape 26.04 LTS.

## Overview

In Landscape 25.10 and earlier, repository management was handled by an internal reprepro-based system that managed mirrors through distributions, series, and pockets. In Landscape 26.04 LTS, this system is replaced by the `debarchive` service, which provides a REST API for managing mirrors, local repositories, and publications.

The migration strategy depends on the type of pocket you're migrating:

| Pre-26.04 pocket type | Migration strategy |
|---|---|
| **Sync (mirror) pocket** | Create a new mirror in Deb Archive pointing at the original upstream source and sync it |
| **Pull pocket** | Create a new mirror with a `filter` matching your existing allowlist/blocklist |
| **Upload pocket** | Create a local repository and import packages from the existing reprepro pool |

```{important}
If you need to preserve the **exact state** of a sync mirror (the precise set of package versions currently stored, rather than the latest upstream state), you should treat it as an upload pocket and import its packages into a new local repository instead.
```

## Prerequisites

This guide assumes you have already:

- Installed and configured the `landscape-debarchive` snap ({ref}`how-to-debarchive-repository-management`)

## Set environment variables

Set the following environment variables for use throughout this guide:

```bash
export LANDSCAPE_FQDN="landscape.example.com"
export API_BASE="https://$LANDSCAPE_FQDN/debarchive/v1beta1"
export JWT="<your-jwt-token>"
```

To obtain a JWT token, authenticate against the Landscape REST API. See {ref}`reference-rest-api-login` for details.

## Identify your existing repositories

Before migrating, inventory your existing reprepro-managed repositories. On the Landscape Server, the reprepro repository data is stored under `/var/lib/landscape/landscape-repository/standalone/`.

List all configured distributions and their pockets. Each distribution has its own configuration directory:

```bash
cat /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/conf/distributions
```

where `<DISTRIBUTION>` is the name of the distribution you created (e.g., `ubuntu`, `ubuntu-staging`).

This file contains sections like:

```text
Codename: noble-release
Components: main restricted universe multiverse
Architectures: amd64
SignWith: <KEY_FINGERPRINT>
```

```text
Codename: noble-updates
Components: main restricted universe multiverse
Architectures: amd64
SignWith: <KEY_FINGERPRINT>
Update: noble-updates
```

```text
Codename: noble-staging
Components: main
Architectures: amd64
SignWith: <KEY_FINGERPRINT>
```

The `Update:` field indicates a sync (mirror) pocket. Sections with a `Pull:` field are pull pockets. Sections without either are upload pockets.

To see what packages are currently in a pocket:

```bash
reprepro -b /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION> list <CODENAME>
```

Replace `<DISTRIBUTION>` with the appropriate distribution directory name and `<CODENAME>` with the codename of the pocket (e.g., `noble-updates`).

## Migrate sync (mirror) pockets

For sync pockets that mirror an upstream archive, create a new mirror in Deb Archive pointing at the same upstream source.

### 1. Identify the upstream source

Check the update rules in the reprepro configuration:

```bash
cat /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/conf/updates
```

Look for sections matching your pocket. For example:

```text
Name: noble-updates
Method: http://archive.ubuntu.com/ubuntu
Suite: noble-updates
Components: main restricted universe multiverse
Architectures: amd64
```

The `Components` and `Architectures` fields may not be present. If they're missing, use the values from the corresponding distribution section.

### 2. Create the mirror

```bash
curl -X POST "$API_BASE/mirrors" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "<CODENAME>",
    "archiveRoot": "http://archive.ubuntu.com/ubuntu",
    "distribution": "<CODENAME>",
    "architectures": ["amd64"],
    "components": ["main", "restricted", "universe", "multiverse"]
  }'
```

The response includes a `mirrorId` that you'll use in subsequent requests.

### 3. Sync the mirror

Trigger a sync to download packages from the upstream source:

```bash
curl -X POST "$API_BASE/mirrors/<MIRROR_ID>:sync" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

This returns a long-running operation. Poll for its completion:

```bash
curl -X GET "$API_BASE/operations/<OPERATION_ID>" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

The operation is complete when `done` is `true`.

### 4. Verify the mirror

Once the sync is complete, confirm the packages are present in the mirror:

```bash
curl -X GET "$API_BASE/mirrors/<MIRROR_ID>/packages" \
  -H "Authorization: Bearer $JWT"
```

### 5. Repeat for each sync pocket

Repeat the previous steps for each sync pocket (`release`, `updates`, `security`, etc.).

## Migrate pull pockets

Pull pockets in the pre-26.04 system stage packages from another pocket using allowlist or blocklist filters. In Deb Archive, this is achieved by creating a mirror with a `filter` expression that replicates your allowlist or blocklist.

### 1. Identify the filter rules

Check the reprepro `pulls` configuration:

```bash
cat /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/conf/pulls
```

Example section:

```text
Name: noble-release-staging
From: noble-release
Components: main
Architectures: amd64
FilterList: install noble-release-staging.list
```

The referenced filter list file (e.g., `noble-release-staging.list`) contains package name patterns, one per line. Examine the filter list:

```bash
cat /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/conf/noble-release-staging.list
```

Example allowlist content:

```text
nginx install
curl install
libssl3 install
```

### 2. Translate the filter to a Deb Archive filter expression

Deb Archive mirrors support package filtering using an aptly-compatible filter syntax. Translate your allowlist into a filter expression:

- **Allowlist** (only include these packages): Use a filter expression that matches the package names:

  ```
  Name (= nginx) | Name (= curl) | Name (= libssl3)
  ```

- **Blocklist** (exclude these packages): Use a negated filter expression. In this case, you typically don't set a filter on the mirror itself. Instead, create a standard mirror and exclude packages at publication time, or use the `!` operator:

  ```
  !Name (= unwanted-package) , !Name (= another-unwanted)
  ```

### 3. Create the filtered mirror

Create a mirror pointing at the same upstream as the original source pocket, with the filter applied:

```bash
curl -X POST "$API_BASE/mirrors" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "<CODENAME>",
    "archiveRoot": "http://archive.ubuntu.com/ubuntu",
    "distribution": "<CODENAME>",
    "architectures": ["amd64"],
    "components": ["main"],
    "filter": "Name (= nginx) | Name (= curl) | Name (= libssl3)",
    "filterWithDeps": true
  }'
```

Set `filterWithDeps` to `true` if you want the filter to also include dependencies of matched packages (recommended for allowlists).

### 4. Sync the filtered mirror

```bash
curl -X POST "$API_BASE/mirrors/<MIRROR_ID>:sync" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

### 5. Verify the filtered mirror

Once the sync is complete, confirm the filtered packages are present in the mirror:

```bash
curl -X GET "$API_BASE/mirrors/<MIRROR_ID>/packages" \
  -H "Authorization: Bearer $JWT"
```

## Migrate upload pockets

Upload pockets contain packages that were manually uploaded by users. Since there's no upstream source to sync from, you need to import the existing packages into a new local repository.

### 1. Identify the packages

List the packages in the upload pocket:

```bash
reprepro -b /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION> list noble-staging
```

The pool directory containing the actual `.deb` files is at:

```
/var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/pool/
```

```{important}
The reprepro pool directory is shared across all distributions in the same reprepro tree. Scanning or archiving the entire pool will include packages from sync mirror and pull pockets, not just your upload pocket. Use one of the approaches in the next section to import only the packages that belong to this specific pocket.
```

### 2. Make packages accessible via URL

The `importPackages` API accepts a URL pointing to a `.deb` file. You need to make your existing packages accessible via HTTP or a `file://` URL.

If the Deb Archive service runs on the same machine as your existing repository, you can use `file://` URLs directly:

```bash
# Example: find all .deb files for the staging pocket's component
find /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/pool/main/ -name "*.deb"
```

Alternatively, if the packages are served by the existing Landscape repository web server, they may already be accessible at:

```
http://$LANDSCAPE_FQDN/repository/standalone/<DISTRIBUTION>/pool/
```

### 3. Create a local repository

```bash
curl -X POST "$API_BASE/locals" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "<CODENAME>",
    "defaultDistribution": "<CODENAME>",
    "defaultComponent": "main"
  }'
```

The response includes a `localId`.

### 4. Import packages

Import a single package into the local repository:

```bash
curl -X POST "$API_BASE/locals/<LOCAL_ID>:importPackages" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"url": "file:///path/to/my-package_1.0-1_amd64.deb"}'
```

This is a long-running operation. Poll the returned operation for completion before importing the next package.

```{note}
When using `file://` URLs, the path must be accessible to the `landscape-debarchive` snap. Because snap confinement restricts filesystem access, `file://` URLs pointing to arbitrary paths outside the snap's data directory will not work. Packages must instead be served over HTTP — either by the Landscape Server itself, or by a temporary HTTP server.
```

If the Landscape Server is already serving the repository, packages are accessible at:

```
http://$LANDSCAPE_FQDN/repository/standalone/<DISTRIBUTION>/pool/m/my-package/my-package_1.0-1_amd64.deb
```

Alternatively, start a temporary HTTP server:

```bash
python3 -m http.server 8080 --directory /path/to/packages
```

Then reference packages as `http://localhost:8080/my-package_1.0-1_amd64.deb`.

```{important}
The reprepro pool directory is shared across all distributions in the same reprepro tree. Scanning or archiving the entire pool will include packages from sync mirror and pull pockets, not just your upload pocket. Use one of the approaches below to import only the packages that belong to this specific pocket.
```

#### Script imports from reprepro list

Use `reprepro list` to enumerate only the packages belonging to this pocket, then locate each `.deb` file and import it via HTTP. Set `REPO_HTTP` to the base URL from which the repository is served:

```bash
#!/bin/bash
LOCAL_ID="<LOCAL_ID>"
DIST_BASE="/var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>"
CODENAME="<CODENAME>"  # e.g., noble-staging
REPO_HTTP="http://$LANDSCAPE_FQDN/repository/standalone/<DISTRIBUTION>"

set -euo pipefail

reprepro -b "$DIST_BASE" list "$CODENAME" | while read -r line; do
  # reprepro list output format: "codename|component|arch: package version"
  PACKAGE=$(echo "$line" | awk '{print $2}')
  VERSION=$(echo "$line" | awk '{print $3}')

  DEB_PATH=$(find "$DIST_BASE/pool/" \
    \( -name "${PACKAGE}_${VERSION}_*.deb" \
    -o -name "${PACKAGE}_${VERSION//:/%3a}_*.deb" \) | head -1)

  if [ -z "$DEB_PATH" ]; then
    echo "Warning: could not find .deb for $PACKAGE $VERSION"
    continue
  fi

  # Convert local path to HTTP URL
  RELATIVE_PATH="${DEB_PATH#$DIST_BASE/}"
  URL="$REPO_HTTP/$RELATIVE_PATH"

  echo "Importing: $URL"
  RESPONSE=$(curl -s -X POST "$API_BASE/locals/$LOCAL_ID:importPackages" \
    -H "Authorization: Bearer $JWT" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"$URL\"}")

  OP_NAME=$(echo "$RESPONSE" | jq -r '.name')

  while true; do
    STATUS=$(curl -s -X GET "$API_BASE/$OP_NAME" \
      -H "Authorization: Bearer $JWT" \
      -H "Content-Type: application/json")
    if [ "$(echo "$STATUS" | jq -r '.done')" = "true" ]; then
      break
    fi
    sleep 2
  done
done
```

### 5. Verify imported packages

Once all imports have completed, confirm the packages are present in the local repository:

```bash
curl -X GET "$API_BASE/locals/<LOCAL_ID>/packages" \
  -H "Authorization: Bearer $JWT"
```

## Preserve the exact state of a sync mirror

If you need to preserve the precise package versions currently in a sync mirror, rather than re-syncing from upstream (which may have newer versions), treat it as an upload pocket and import the packages into a local repository. Use the steps above for migrating upload pockets, but use the sync mirror pocket instead.

## Upgrade to Landscape 26.04 LTS

Once you have confirmed that all packages are present in the new Deb Archive service, clean up the pre-26.04 reprepro Distribution records and then upgrade.

### 1. Delete existing reprepro Distribution records

In the Landscape web portal, navigate to **Repositories**. Each distribution (for example, `ubuntu` or `ubuntu-staging`) has a **Delete** button. Delete each distribution.

```{important}
Only delete a distribution after confirming that its packages have been successfully migrated to the new Deb Archive service. This action cannot be undone, though you could restore from a database backup if needed.
```

### 2. Upgrade Landscape Server

Follow {ref}`how-to-upgrade-to-26-04-lts` to upgrade to Landscape 26.04 LTS.

## Publish the migrated repositories

After upgrading to Landscape 26.04 LTS, publish your migrated mirrors and local repositories so they're accessible to client machines. This involves creating a publication target and a publication in the Landscape web portal.

### 1. Create a publication target

In the Landscape web portal, navigate to **Repositories > Publication Targets** and create a new publication target. For a filesystem target that serves repositories from the Landscape Server itself, set the path to the directory where published repositories should be written.

### 2. Create a publication

Navigate to **Repositories > Publications** and create a new publication. Select the migrated mirror or local repository as the source, choose the publication target you created, and configure the distribution, architectures, and GPG signing key.

### 3. Publish

Trigger the publication. Landscape will generate the repository metadata and make the packages available at the publication target path.

## Update client machines

After publishing, update the repository profiles on your managed machines to point to the new Deb Archive publication URLs instead of the pre-26.04 repository paths.

The pre-26.04 repository was served at:

```
deb https://$LANDSCAPE_FQDN/repository/standalone/ubuntu <codename>-<pocket> <components>
```

The new Deb Archive filesystem publications can be served from the configured published root path using the web server of your choice. Consult your publication target configuration for the exact URL.

## See also

- {ref}`how-to-debarchive-repository-management`
- {ref}`reference-release-notes-26-04-lts`
- {ref}`explanation-repo-mirroring`
