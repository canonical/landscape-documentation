---
myst:
  html_meta:
    description: "Migrate repository mirrors from legacy reprepro-managed repositories (Landscape 25.10 and earlier) to the new debarchive service introduced in Landscape 26.04 LTS."
---

(how-to-migrate-repository-mirrors-to-debarchive)=
# How to migrate repository mirrors to Deb Archive

This guide describes how to migrate your existing reprepro-managed repository mirrors from Landscape 25.10 (and earlier) to the new Deb Archive service introduced in Landscape 26.04 LTS.

```{note}
This guide assumes you have already:
- Upgraded to Landscape 26.04 LTS ({ref}`how-to-upgrade-to-26-04-lts`)
- Installed and configured the `landscape-debarchive` snap ({ref}`how-to-debarchive-repository-management`)
```

## Overview

In Landscape 25.10 and earlier, repository management was handled by an internal reprepro-based system that managed mirrors through distributions, series, and pockets. In Landscape 26.04 LTS, this system is replaced by the `debarchive` service, which provides a REST API for managing mirrors, local repositories, and publications.

The migration strategy depends on the type of pocket you're migrating:

| Legacy pocket type | Migration strategy |
|---|---|
| **Sync (mirror) pocket** | Create a new mirror in Deb Archive pointing at the original upstream source and sync it |
| **Pull pocket** | Create a new mirror with a `filter` matching your existing allowlist/blocklist |
| **Upload pocket** | Create a local repository and import packages from the existing reprepro pool |

```{important}
If you need to preserve the **exact state** of a sync mirror (the precise set of package versions currently stored, rather than the latest upstream state), you should treat it as an upload pocket and import its packages into a new local repository instead.
```

## Prerequisites

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

This file contains stanzas like:

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

The `Update:` field indicates a sync (mirror) pocket. Stanzas with a `Pull:` field are pull pockets. Stanzas without either are upload pockets.

To see what packages are currently in a pocket:

```bash
reprepro -b /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION> list noble-release
```

Replace `<DISTRIBUTION>` with the appropriate distribution directory name.

## Migrate sync (mirror) pockets

For sync pockets that mirror an upstream archive, create a new mirror in Deb Archive pointing at the same upstream source.

### 1. Identify the upstream source

Check the update rules in the reprepro configuration:

```bash
cat /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/conf/updates
```

Look for stanzas matching your pocket. For example:

```text
Name: noble-updates
Method: http://archive.ubuntu.com/ubuntu
Suite: noble-updates
Components: main restricted universe multiverse
Architectures: amd64
```

The `Components` and `Architectures` fields may not be present. If they're missing, use the values from the corresponding distribution stanza.

### 2. Create the mirror

```bash
curl -X POST "$API_BASE/mirrors" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "noble-updates",
    "archiveRoot": "http://archive.ubuntu.com/ubuntu",
    "distribution": "noble-updates",
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
  -H "Content-Type: application/json" \
  -d '{}'
```

This returns a long-running operation. Poll for its completion:

```bash
curl -X GET "$API_BASE/operations/<OPERATION_ID>" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json"
```

The operation is complete when `done` is `true`.

### 4. Repeat for each sync pocket

Repeat steps 2–3 for each sync pocket (`release`, `updates`, `security`, etc.).

## Migrate pull pockets

Pull pockets in the legacy system stage packages from another pocket using allowlist or blocklist filters. In Deb Archive, this is achieved by creating a mirror with a `filter` expression that replicates your allowlist or blocklist.

### 1. Identify the filter rules

Check the reprepro `pulls` configuration:

```bash
cat /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/conf/pulls
```

Example stanza:

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

- **Blocklist** (exclude these packages): Use a negated filter expression. In this case, you typically don't set a filter on the mirror itself — instead, create a standard mirror and exclude packages at publication time, or use the `!` operator:

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
    "displayName": "noble-release-staging",
    "archiveRoot": "http://archive.ubuntu.com/ubuntu",
    "distribution": "noble",
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

### 2. Make packages accessible via URL

The `ImportLocalPackages` API accepts a URL pointing to a `.deb` file. You need to make your existing packages accessible via HTTP or a `file://` URL.

If the Deb Archive service runs on the same machine as your existing repository, you can use `file://` URLs directly:

```bash
# Example: find all .deb files for the staging pocket's component
find /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/pool/main/ -name "*.deb"
```

Alternatively, if the packages are served by the existing Landscape repository web server, they may already be accessible at:

```
https://$LANDSCAPE_FQDN/repository/standalone/<DISTRIBUTION>/pool/
```

### 3. Create a local repository

```bash
curl -X POST "$API_BASE/locals" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "noble-staging",
    "defaultDistribution": "noble",
    "defaultComponent": "main"
  }'
```

The response includes a `localId`.

### 4. Import packages

Import each package into the local repository:

```bash
curl -X POST "$API_BASE/locals/<LOCAL_ID>:importLocalPackages" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "file:///var/lib/landscape/landscape-repository/standalone/pool/main/m/my-package/my-package_1.0-1_amd64.deb"
  }'
```

This is a long-running operation. Poll the returned operation for completion before importing the next package.

#### Option A: Script individual imports

To import multiple packages, script the process:

```bash
#!/bin/bash
LOCAL_ID="<LOCAL_ID>"

find /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/pool/ -name "*.deb" | while read -r deb_path; do
  echo "Importing: $deb_path"
  
  RESPONSE=$(curl -s -X POST "$API_BASE/locals/$LOCAL_ID:importLocalPackages" \
    -H "Authorization: Bearer $JWT" \
    -H "Content-Type: application/json" \
    -d "{
      \"url\": \"file://$deb_path\"
    }")

  # Extract operation name and poll for completion
  OP_NAME=$(echo "$RESPONSE" | jq -r '.name')
  
  while true; do
    STATUS=$(curl -s -X GET "$API_BASE/operations/$OP_NAME" \
      -H "Authorization: Bearer $JWT" \
      -H "Content-Type: application/json" \
    )
    
    DONE=$(echo "$STATUS" | jq -r '.done')
    if [ "$DONE" = "true" ]; then
      break
    fi
    sleep 2
  done
done
```

#### Option B: Import from a tarball or zip archive

As an alternative to scripting individual imports, you can collect the `.deb` files into a tarball or zip archive and pass it directly to Deb Archive. The service will extract the archive and import all packages:

```bash
# Create a tarball of all packages
tar -czf packages.tar.gz -C /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/pool/ .

# Import the archive directly
curl -X POST "$API_BASE/locals/$LOCAL_ID:importLocalPackages" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"url": "file:///path/to/packages.tar.gz"}'
```

Alternatively, use a zip archive:

```bash
# Create a zip archive of all packages
cd /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/pool/
zip -r packages.zip .

# Import the zip archive directly
curl -X POST "$API_BASE/locals/$LOCAL_ID:importLocalPackages" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"url": "file:///path/to/packages.zip"}'
```

Deb Archive will automatically extract the archive and import all `.deb` files found within it.

```{note}
If you only need to import packages that were in a specific pocket, cross-reference the output of `reprepro -b /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION> list <codename>` with the files in the pool to identify which `.deb` files to import.
```

## Preserve the exact state of a sync mirror

If you need to preserve the precise package versions currently in a sync mirror — rather than re-syncing from upstream (which may have newer versions) — treat it as an upload pocket and import the packages into a local repository.

### 1. Export the package list

```bash
reprepro -b /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION> list noble-release > noble-release-packages.txt
```

### 2. Create a local repository and import

Follow the same steps as [Migrate upload pockets](#migrate-upload-pockets), using the package files from the pool directory that correspond to the packages listed in your export.

To find the `.deb` files for packages listed by reprepro:

```bash
while read -r line; do
  # reprepro list output format: "codename|component|arch: package version"
  PACKAGE=$(echo "$line" | awk '{print $2}')
  VERSION=$(echo "$line" | awk '{print $3}')
  find /var/lib/landscape/landscape-repository/standalone/<DISTRIBUTION>/pool/ \
    -name "${PACKAGE}_${VERSION}_*.deb" -o -name "${PACKAGE}_${VERSION//:/%3a}_*.deb"
done < noble-release-packages.txt
```

## Publish the migrated repositories

After migrating your mirrors and local repositories, you need to publish them so they're accessible to client machines. This involves creating a publication target and a publication.

### 1. Create a publication target

For a filesystem target (serves repositories from the Landscape Server itself):

```bash
curl -X POST "$API_BASE/publicationTargets" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "filesystem-target",
    "filesystem": {
      "path": "ubuntu"
    }
  }'
```

### 2. Create a publication

Link a mirror or local repository to a publication target:

```bash
curl -X POST "$API_BASE/publications" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "mirrors/<MIRROR_ID>",
    "publicationTarget": "publicationTargets/<PUBLICATION_TARGET_ID>",
    "distribution": "noble-updates",
    "architectures": ["amd64"],
    "gpgKey": {
      "armor": "<ASCII_ARMORED_PRIVATE_GPG_KEY>"
    }
  }'
```

For local repositories, use `"source": "locals/<LOCAL_ID>"` instead.

### 3. Publish

```bash
curl -X POST "$API_BASE/publications/<PUBLICATION_ID>:publish" \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Poll the returned operation until it completes.

## Update client machines

After publishing, update the repository profiles on your managed machines to point to the new Deb Archive publication URLs instead of the legacy repository paths.

The legacy repository was served at:

```
deb https://$LANDSCAPE_FQDN/repository/standalone/ubuntu <codename>-<pocket> <components>
```

The new Deb Archive filesystem publications can be served from the configured published root path using the web server of your choice. Consult your publication target configuration for the exact URL.

## See also

- {ref}`how-to-debarchive-repository-management`
- {ref}`reference-release-notes-26-04-lts`
- {ref}`explanation-repo-mirroring`
