(explanation-server-architecture)=
# Landscape Server architecture

Landscape Server is the server-side component of the Landscape ecosystem. It is made up of a collection of services. This document explains these services, their purposes, and their relationships to each other and external components.

![Landscape Service Diagram](/assets/images/landscape-services.jpg "Landscape Services")

A Landscape Server deployment has six required services:

* [API](#api) - serves REST API and Legacy API requests
* [Appserver](#appserver) - serves Legacy UI and static files for the new UI
* [Async frontend](#async-frontend) - serves Legacy UI notifications
* [Job handler](#job-handler) - runs background jobs such as repository mirror syncs
* [Message system](#message-system) - exchanges messages with Landscape Clients
* [Pingserver](#pingserver) - records Landscape Client heartbeat pings

There are also optional services. Without these, Landscape Server is usable, but certain features will not be available:

* [Hostagent consumer](#hostagent-consumer) - for WSL instance management
* [Hostagent messenger](#hostagent-messenger) - for WSL instance management
* [Package search](#package-search) - for improved package management performance
* [Package upload](#package-upload) - for upload pocket repository management
* [Secrets](#secrets) - for HashiCorp Vault-backed secrets storage

A deployment requires a number of third-party components as well:

* cron - for scheduled tasks such as Landscape Profiles, cleanup of old or stale records, and updating Landscape Alerts
* reverse proxy and load-balancer - usually [HAProxy](https://www.haproxy.org/) or [Apache Server](https://httpd.apache.org/), listens for external connections and forwards them to the responsible core service
* [PostgreSQL](https://www.postgresql.org/) - database, the main store of Landscape data regarding accounts, users, packages, and managed instances
* [RabbitMQ Server](https://www.rabbitmq.com/) - message-broker, used between services for background tasks and asynchronous communication
* reprepro - repository-mirroring utility, used to create, manage, and sync Landscape-managed Debian repository mirrors
* [systemd](https://systemd.io/) - service manager, used to start, stop, restart, enable, and disable the Landscape services

There is also one optional third-party component:

* [HashiCorp Vault](https://www.hashicorp.com/en/products/vault) - secrets storage, used to store sensitive data for delivery to managed instances. Alternatively, secrets can be encrypted for storage in the PostgreSQL database.

## Service descriptions

Landscape Server's individual services are long-running processes that provide different aspects of Landscape's functionality. This section describes each service in detail.

(explanation-server-architecture-api)=
### API

The API service responds to HTTP requests with JSON-encoded responses. Requests made to Landscape Server's `/api` endpoint are routed by the reverse proxy to this service. It is intended for use by Landscape Administrators. It interacts with all third-party components and most other Landscape Server services.

The API service currently supports two versions: the REST API and the Legacy API. It also supports two forms of authentication: JSON Web Tokens (JWTs) and HMAC-signed requests.

#### REST API

HTTP requests made to `/api/v2` are routed to the REST API. This API only supports JWT authentication. The REST API can be interacted with directly, but also acts as the back-end for the new Landscape UI.

* [Make a REST API request](/how-to-guides/api/make-a-rest-api-request)
* [REST API endpoint reference](/reference/api/rest-api-endpoints/index)

#### Legacy API

HTTP requests made to `/api` are routed to the Legacy API.

* [How to use the legacy API](/how-to-guides/api/use-the-legacy-api)
* [Legacy API endpoint reference](/reference/api/legacy-api-endpoints/index)

(explanation-server-architecture-appserver)=
### Appserver

The Appserver service responds to HTTP requests that are not routed to another service. It either responds directly to requests, or routes them again to other services. When responding directly to requests, responses are generally in the form of HTML, but it also serves JavaScript and CSS for the new and legacy Landscape UIs. It interacts with all third-party components and most other Landscape Server services.

### Async frontend

The Async frontend service supports live status updates in the legacy Landscape UI for long-running Landscape Activities such as repository mirror syncs or intermittently-updated Alert notifications. It primarily interacts with RabbitMQ Server and the Appserver service.

### Job handler

The Job handler service processes periodic, long-running, or background tasks – usually produced by the API, Appserver, or Message system services. It primarily interacts with PostgreSQL, RabbitMQ Server, and other Landscape Server services.

(explanation-server-architecture-message-system)=
### Message system

The Message system service responds to HTTP requests from Landscape Client, accepting incoming messages and responding with outgoing messages. It updates Landscape Server's view of the Client's state, and delivers Activities to be performed by the Client. Other than Clients, it primarily interacts with the PostgreSQL databases.

(explanation-server-architecture-pingserver)=
### Pingserver

The Pingserver service responds to HTTP requests from Landscape Clients, alerting them when they have pending outgoing messages from Landscape Server. It also updates Clients "last ping" times, which are used to alert for offline Clients. It primarily interacts with the PostgreSQL databases.

### Hostagent consumer

The Hostagent consumer service processes tasks from WSL-related queues. This supports actions related to managed Windows machines and their WSL instances. It primarily interacts with the PostgreSQL databases and RabbitMQ Server.

(explanation-server-architecture-hostagent-messenger)=
### Hostagent messenger

The Hostagent messenger service communicates with Ubuntu Pro for WSL on managed Windows machines. It does this using a persistent GRPC connection. It sends WSL-related activities to managed Windows machines and processes incoming messages from them onto the WSL-related task queues to be processed by [Hostagent consumer](#hostagent-consumer). It primarily interacts with RabbitMQ Server.

(explanation-server-architecture-package-search)=
### Package search

The Package search service responds to internal HTTP requests with the Debian package state information of instances. It acts as an in-memory cache of this information, improving the performance of package queries. Without it, package queries go directly to the database. It primarily interacts with the PostgreSQL database.

(explanation-server-architecture-package-upload)=
### Package upload

The Package upload service responds to dput or FTP requests to upload Debian packages to Landscape-managed package repositories. It maintains a queue of package uploads and processes them into the appropriate repositories. It primarily interacts with the PostgreSQL database and the filesystem.

### Secrets

The Secrets service responds to internal HTTP requests with scoped access tokens for the secrets back-end. It is only needed if HashiCorp Vault is being used to store secrets. If secrets are instead being stored in the PostgreSQL database, then the Secrets service does not need to be running.
