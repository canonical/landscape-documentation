(reference-release-notes-23-03)=
# 23.03 release notes

These are the release notes for Landscape 23.03.

## Highlights

* Landscape Server can be installed on Ubuntu 20.04 LTS (Focal Fossa) and Ubuntu 22.04 LTS (Jammy Jellyfish)
* Manages all versions from Ubuntu 16.04 (Xenial Xerus) onwards
* Native Ubuntu Pro awareness
* Landscape Client is compatible with Debian Bullseye
* Landscape manages all machines with an Ubuntu Pro subscription without needing a license.txt file to be installed on the server
* Compatible with Canonical's air-gapped contract server
* Landscape Client package for the RISC-V (RV64) CPU architecture
* Landscape Server packages for the s390x, rv64, and arm64 (AArch64) CPU architectures
* Modernized Charms authored in Juju's Operator Framework
* Added the publication date of Ubuntu Security Notices (USNs) to the Packages page
* Landscape API HTTP request parameters are now order-agnostic
* Query optimization on the Activities page when selecting many computers
* Added public keys for mirroring Jammy pockets
* Improved user experience and API for environments where machines are cloned
* Computer count on dashboard sidebar is consistent with other counts
* Faster out-of-the-box reporting of packages, for Ubuntu 22.10 (Kinetic Kudu) and onwards

## Bug fixes
* Bug 1945456: Landscape Login page using an older version of jQuery
* Bug 1966970: GPG license gets truncated if it's too large
* Bug 1966199: XSS - Cross-Site Scripting vulnerability via the page_key parameter
* Bug 1970224: Update logos
* Bug 2009079: Landscape can't use Duo for OIDC
* Bug 2043035: Landscape UI lag
* Bug 2070049: Allow binary script uploads via API and downloads via UI

## Upgrade Notes
Performing an in-place upgrade from Landscape 19.10 entails a fresh installation using either Juju, Quickstart, or a Manual installation; and restoring the database. Going forward, Juju is the recommended installation method. In the future, upgrading Landscape via Juju will be a two-step process: one command to pause Landscape, and one command to perform the upgrade.

[Upgrade a Landscape 19.10 Quickstart Installation to Landscape 23.03](https://discourse.ubuntu.com/t/upgrade-a-landscape-19-10-quickstart-installation-to-landscape-23-03/34336/)

[Upgrade a Landscape 19.10 Manual Installation to Landscape 23.03](https://discourse.ubuntu.com/t/upgrade-a-landscape-19-10-manual-installation-to-landscape-23-03/34335/)

## Patch Notices

- landscape-server 23.03+18.3 published on 25 June 2024

   * Fix: allow binary script uploads via API and downloads via UI (LP: [#2070049](https://bugs.launchpad.net/landscape/+bug/2070049))

- landscape-server 23.03+18.2 published 5 June 2024

  * fix(package-search): include sslmode parameter in config for connections to Postgres. Previously hardcoded to 'disable' (LP: [#2064756](https://launchpad.net/bugs/2064756))

- landscape-server 23.03+18.1 published 19 Apr 2024

  * Fix: reduce number of hanging /ajax polls (LP: [#2043035](https://launchpad.net/bugs/2043035))

- landscape-server 23.03+18 published 17 Jan 2024

  * Backport: re-apply Ubuntu Pro licenses to machines that have lost theirs

- landscape-server 23.03+17 published 21 Sep 2023

  * update message handler and UI for snap holds and summary info
  * add API endpoint remove-wsl-hosts
  * add API endpoint and activity to delete child computer instances
  * add API endpoint to get mirror repo info
  * add option to removal profile to also remove child computers
  * add API endpoint and activity to stop child computer instances
  * add API endpoint and activity to start child computer instances
  * add async server to manage hostagent messages
  * escape registration key shell characters
  * add API endpoint list-wsl-hosts
  * bugfix for API endpoint create-script-attachment
  * rewrite update_computer_packages in PL/pgSQL; regenerate DB schema using
    PostgreSQL 12
  * reimplement package name searches using pg_trgm; port packagesearch to use
    native pg_trgm

- landscape-server 23.03+16 published 13 Jul 2023

  * Fixed missing python patch files for activity_info

- landscape-server 23.03+15 published 12 Jul 2023

  * Snap management for installing, refreshing, and removing snaps
  * Add distribution and series to API get-repository-profiles
  * Fix flat repo handling

- landscape-server 23.03+14 published 29 Jun 2023

  * Fixed issue with SQL patch

- landscape-server 23.03+13 published 27 Jun 2023

  * Restart services periodically to reduce memory usage
  * Upload path mirror repo fix
  * Fix create script api bug
  * Fix script page UI bug

- landscape-server 23.03+12 published 25 May 2023

  * Reworded esm-disabled message
  * Added lunar hash-ids

- landscape-server 23.03+11 published 19 May 2023

  * Add identity argument to bootstrap accounts script
  * Add `UbuntuPro` to license role name mapping for accounts

- landscape-server 23.03+10 published 10 May 2023

  * Fixes when writing meta-release tag files.
  * New messaging to prompt landscape-client upgrades prior to problematic
    release-upgrades.
  * Fixed flat repository mirroring when mirror suite is "/".

- landscape-server 23.03+9 published 25 Apr 2023

  * Fix invitations for OIDC login.
  * Clean up API JSON output.

- landscape-server 23.03+8 published 07 Apr 2023

  * Remove `next_url` parameter for OIDC logins.
  * Fix tags overflowing in UI. 

- 23.03+7 published on April 4, 2023
  * Improved CSV formatting and `--cve` option for security vulnerability API
  * Fix for login redirects, and API decoding errors
  * Provide hash-id-databases script that ignores maintenance status
  * Duo OIDC login error fix

