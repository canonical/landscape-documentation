(explanation-package-reporting)=
# Landscape package reporting

Package management is a core feature of Landscape. This document describes package reporting, a component of package management, and outlines the services and steps involved for Landscape to gather and display package information.

## Overview of package reporting

For Landscape to manage packages effectively, Landscape Client must first report the package state of a managed instance to Landscape Server. Client does this through a process called "package reporting".

Package reporting is initiated by Landscape Client, which periodically runs a process called `package-reporter`. This process updates the instance's local package cache, detects any changes, and sends those changes to Landscape Server. 

Landscape Server stores this information in its database. Landscape administrators can then perform package actions that instruct Client to change the instance's package state, such as installing, upgrading, holding, unholding, or removing packages.

## Services involved in package reporting

There are two key services involved in package reporting: `package-reporter` and `message-system`. And like most things in Landscape, package reporting involves activity on both the Client-side and the Server-side.

Client is responsible for maintaining a view of the state of packages on a managed instance and reporting changes in that state to Server. The Client service that performs these tasks is called `package-reporter`, which is run periodically on the instance as the `landscape` user.

Server is responsible for maintaining its own view of the state of packages on the instance as well, which it keeps synchronized with Client's view by processing package reporting messages from Client. Server also provides a mechanism for bootstrapping Client's information about packages which can speed up package reporting.

Once package reporting messages are sent to Server from Client, they're received by Server's `message-system` service, which immediately processes them.

## Data stores involved in package reporting

Landscape Server and Landscape Client both store package reporting state. Here's a list of the different stores of package information and their types. More details on each can be found in the [Package reporting step-by-step](#package-reporting-step-by-step) section.

**Server**:

  - `packages` database: a PostgreSQL database that contains general, non-Client-specific information regarding packages that Landscape knows about. It is the authoritative source for [Landscape package IDs](#landscape-package-id).
  - `computer_packages` database: a PostgreSQL database table that contains arrays of [Landscape package IDs](#landscape-package-id) for each Client, one column for each [package state](#package-state).
  - `hash-id` database files: a collection of SQLite database files that contain a mapping of [Landscape package hashes](#landscape-package-hash) to [Landscape package IDs](#landscape-package-id). There is one `hash-id` database file per Ubuntu series, per CPU architecture.
  
**Client**:

  - Client `packages` database: a SQLite database file that mirrors the `computer_packages` database on Server. It has one table for each [package state](#package-state) with one column of [Landscape package IDs](#landscape-package-id). It also contains some state regarding the current package reporting progress.
  - `hash-id` database file: one of Server's `hash-id` database files, downloaded from Server and matching the Client's Ubuntu series and CPU architecture. 

## Package state

Before we go into package reporting details step-by-step, it's important to understand what package reporting is actually reporting.

The package state for an instance is the complete set of packages that are available for installation or currently installed on an instance. The package state is represented by six categories, which are *not* mutually exclusive.

The complete breakdown of package categories and their relationships is:

  - **Installed**: The package is installed on the instance
  - **Available**: The package is present in the instance's package sources
  - **Upgrades**: The package is present in the instance's package sources and it is a newer version of an installed package
  - **Held** (also called "locked"): The package is installed and it has been marked as held – its installation state will not be automatically changed
  - **Autoremovable**: The package is installed but it was installed as a dependency of another package and is no longer needed for that purpose
  - **Security**: The package is present in the instance's "security archive" package sources or it was originally installed from one
  
Some of these categories are overlapping, and there's no deduplication if a package appears in multiple overlapping sets. The union of installed and available packages represents the entire package state of the instance.

An individual package is represented by its:

  - [Landscape package ID](#landscape-package-id)
  - [Landscape package type and relation types](#landscape-package-type-and-relation-types)
  - [Landscape package hash](#landscape-package-hash)
  - name
  - version number
  - section ([Debian's documentation on section](https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-section))
  - description summary
  - installed size, and
  - USN ID, if applicable ([Ubuntu Pro Client's documentation on USNs](https://documentation.ubuntu.com/pro-client/en/v32/explanations/cves_and_usns_explained/#what-is-a-usn))

### Landscape package ID

When Server learns about new packages from Client, it adds them to its `packages` database. When a package is added, it is assigned an incremental integer database ID. This ID is used to represent the package both internally on Server and when communicating package reporting and package management activities to and from Client.

**Note**: Landscape package IDs are not portable across installations of Server. This means that if an instance is unregistered and then registered to a new Server installation, it will need to re-report its package state.

### Landscape package type and relation types

This is an integer that represents what type a package is or what type its relations are. The different definitions can be found in [`landscape.lib.apt.package.skeleton`](https://github.com/canonical/landscape-client/blob/b458b49e488a099ba97ff298fa2a1e511199d914/landscape/lib/apt/package/skeleton.py#L6-L18). Most of these definitions are actually used to represent package relations, not packages themselves.

  - `0x10001` / `65537`: a regular Debian package. This is the usual case.
  - `0x20002` / `131074`: (relation) the package provides a virtual package. See [Debian's documentation for more details on virtual packages](https://www.debian.org/doc/debian-policy/ch-relationships.html#virtual-packages-provides).
  - `0x30002` / `196610`: (relation) this is a special relation of a package to its own name and version.
  - `0x40004` / `262148`: (relation) the package requires the related package as a dependency.
  - `0x50004` / `327684`: (relation) the package requires the related package as a dependency, but this dependency could be fulfilled by another package (like `dependency-a | dependency-b`).
  - `0x60008` / `393224`: (relation) the package is an upgrade for the related package.
  - `0x70010` / `458768`: (relation) the package conflicts with the related package – both cannot be installed simultaneously.

### Landscape package hash

When Client updates its package state, it calculates a SHA1 hash for each package from a string that includes the package name, type, version number, and a representation of its relationships with other packages.

Client uses this hash to look up the Landscape package ID in its local "hash to ID" SQLite database. It then uses those IDs to report package state changes to Server.

Server also stores these hashes in its `packages` database. If a Client cannot find the hash in its local database, it can ask Server to provide it. This is further explained in the [Package reporting step-by-step](#package-reporting-step-by-step) section.

Here's an example of a string that's hashed to produce the Landscape package hash:

```text
[65537 0ad-data 0.0.26-1][196610 0ad-data = 0.0.26-1][262148 dpkg >= 1.15.6~][393224 0ad-data < 0.0.26-1]
```

From this and the [Landscape package type and relation types](#landscape-package-type-and-relation-types), you can see that this package:

  - has name `0ad-data` and version `0.0.26-1` (first two segments)
  - requires `dpkg` greater than or equal to version `1.15.6~` as a dependency (third segment), and
  - upgrades `0ad-data` packages with version less than `0.0.26-1` (fourth segment)

## Package reporting step-by-step

Landscape package reporting involves multiple steps, some of which may be repeated in specific circumstances. This section describes the process from the point immediately after the Client registers, through to when the full package state is reported to the Server.

  1. Client: `hash-id` database file download
  
     Client downloads a `hash-id` database file from Server that matches its Ubuntu series and CPU architecure. For example, on an amd64 24.04 Noble Numbat instance, the file would be `<server UUID>_noble_amd64`.
     
  2. Client: update package cache
  
     Client updates its local package cache (equivalent to running `sudo apt update`) if file timestamps and cache state indicate it has not been updated within a configurable window (default: 8 hours).
     
  3. Client: hash packages
  
     Client calculates the [Landscape package hash](#landscape-package-hash) for every package in the package cache.
     
  4. Client: look up [Landscape package IDs](#landscape-package-id)
  
     Client searches for the Landscape package hash in its Client `packages` database, which at this point only consists of the `hash-id` database file. It records which packages it finds Landscape package IDs for (known packages), and which packages are "unknown package hashes".
     
  5. Client: queue `unknown-package-hashes` request message
  
     Client queues a message to Server with type `unknown-package-hashes`, containing the list of unknown hashes. The number of hashes in this request is [configurable](https://github.com/canonical/landscape-client/blob/afebfb75954cc03aea1124651373498a5fe4eca1/example.conf#L222-L226), but the default is 500.
     
  6. Client: detect package state changes
  
     Client compares its package state to its previously known package state. If there are no differences, `package-reporting` ends here, with the exception of processing received `package-ids` messages.
     
  7. Client: queue known `packages` message
  
     If changes to any package states are detected, Client queues a message to Server with type `packages`, containing lists of Landscape package IDs for packages in each [package state](#package-state).
     
  8. Server: respond to `unknown-package-hashes` message with `package-ids` message
  
     Server sends a message to Client with type `package-ids`, containing a list of Landscape package IDs from Server's `packages` database in the same order as the original `unknown-package-hashes` message. If Server does not know the Landscape package ID for a given hash, the ID value is `None`.
     
  9. Server: record known packages state
  
     Server records the package states from the `packages` message in the `computer_packages` database table.
     
  10. Client: respond to `package-ids` with package `add-packages` message
  
      Client records the known Landscape package IDs from Server's `package-ids` message in its Client `packages` database. For every Landscape Package ID that is `None`, Client collects all the package metadata (name, version, description, _etc._). Client then queues a single `add-packages` message to Server containing this information for all of the `None` packages.
     
  11. Server: respond to `add-packages` message with `package-ids` message
  
      Similar to step *8*, Server sends a message to Client with type `package-ids`, containing a list of Landscape package IDs in the same order as the original `add-packages` message. The IDs are generated by adding the package from the `add-packages` message to Server's `packages` database.
      
  12. Client: repeat step *10*, except this time there will be no Landscape Package IDs that are `None`, so no `add-packages` message is queued.
  
  13. Sleep for a configurable amount of time (default 15 minutes), then start again from step *2*.
     
Keep in mind that steps *8*, *9*, *10*, and *11* can occur during any Client-Server message exchange, so their ordering is not necessarily strict. `unknown-package-hashes` and `add-packages` messages each contain a unique `request-id` that is used to correlate the sent messages with Server's `package-ids` responses.

Eventually a steady state is reached, where:

  - No packages are unknown - all packages have Landscape Package IDs in Client's `packages` database
  - No difference in package state is detected by Client
  
At this point, `package-reporting` ends, restarting only when new differences are detected in the package state. This means only steps *2* through *6* (skipping *5*) are performed.

![Landscape package reporting sequence diagram](/assets/package-reporting.jpg "Landscape package reporting sequence diagram")

### Exceptional situations

Sometimes package reporting doesn't go smoothly. Landscape has some mechanisms it uses to attempt to recover from these situations.

#### Example: Package state buffering

Client reports changes to its package state as "deltas" that express the addition and removal of [Landscape Package IDs](#landscape-package-id) from each [package state](#package-state) category.

Sometimes these deltas express a change that appears incomplete. For example, if a package is added to the "upgrades" category, but the package that would be upgraded doesn't appear in "installed".

When this happens, Server "buffers" these deltas in a database table separate from the "real" `computer_packages` store. Each time the Client reports another delta, it checks if the new delta would make the package state "consistent". If so, the buffered package state is copied to the `computer_packages` store.

Currently, if a Client has buffered package state data, Server prevents package management activities from being created for that Client.

#### Example: Resynchronization

Sometimes the deltas are impossible to apply. For example, a delta might say that a package has been removed from the "available" category, even though that package was not present in that category.

When this happens, Server sends a "resynchronize" activity to Client, scoped to "packages". Client acts on this by completely starting its package reporting from scratch (starting at step *1* in ["Package reporting step-by-step"](#package-reporting-step-by-step))

### Hash-id databases

In step *1* of package reporting, Client downloads the `hash-id` database file from Landscape Server. This step significantly decreases total package-reporting time by giving Client some starting data to use for step *4*, looking up the Landscape Package IDs from the Landscape package hashes. However, package reporting can progress and succeed without this step.

The `hash-id` databases are generated by Server from a set of configurable package sources. Server reads the package indices from these sources, calculates the Landscape package hashes, and populates the files. In most deployments, this is done by a weekly `cron` job that is automatically enabled in Landscape.

A usual deployment only includes the official Ubuntu sources and ESM sources in the `hash-id` databases configuration. Therefore, Clients using other sources do not benefit as much from this package reporting bootstrapping mechanism.
