---
myst:
  html_meta:
    description: "Technical details on Landscape internal network requirements, port ranges, protocols, and communication between server components and clients."
---

(reference-internal-network-requirements)=
# Internal network requirements

Landscape consists of several services and dependencies. This document lists the network settings and protocols required for communication between the Landscape Server components, as well as between Landscape Clients and the Server. For details on each Landscape Server component, see the {ref}`explanation-server-architecture`.

![Landscape Network Diagram](/assets/images/landscape-server-networking.jpg "Landscape Networking")

## External network traffic

External clients communicate with Landscape Server over the internet. These clients include web browsers interacting the Landscape's web UI, Landscape API clients, Landscape-managed instances, and Landscape repository package uploaders.

The first point of contact for all of this traffic is the reverse proxy, which also acts as a load-balancer and performs TLS termination. In most Landscape Server deployments, this role is filled by [HAProxy](https://www.haproxy.org/), but in some deployments, it may be [Apache Server](https://httpd.apache.org/).

All external network traffic to and from Landscape uses HTTP or HTTPS. Consequently, TCP ports 80 and 443 on the reverse proxy must be exposed to the wide area network. In addition, port 6554 must be exposed for gRPC over HTTP/2 communication with [Ubuntu Pro for WSL](https://documentation.ubuntu.com/wsl/stable/).

## Internal network traffic

Internal Landscape components communicate with each other directly. These are the first- and third-party services that provide all of Landscape's features. This traffic is "internal" because it should only traverse the local area network in which Landscape Server is deployed.

Internal network traffic is "behind" a reverse proxy. In most Landscape Server deployments, the role of reverse proxy is filled by [HAProxy](https://www.haproxy.org/), but in some deployments, it may be [Apache Server](https://httpd.apache.org/).

(reference-internal-network-requirements-client-serving)=
### Components that receive client traffic

The reverse proxy accepts external HTTP traffic originating from clients and proxies it to internal components. It also performs TLS termination. Each internal component has a default port. For services configured with a base port, additional instances use successive ports starting at that base port.

These are the default ports for each internal component that accepts traffic from the reverse proxy:

- 8070: {ref}`explanation-server-architecture-pingserver`
- 8080: {ref}`explanation-server-architecture-appserver`
- 8090: {ref}`explanation-server-architecture-message-system`
- 9080: {ref}`explanation-server-architecture-api`
- 9090: {ref}`explanation-server-architecture-async-frontend`
- 9099: {ref}`explanation-server-architecture-package-search`
- 9100: {ref}`explanation-server-architecture-package-upload`
- 50051: {ref}`explanation-server-architecture-hostagent-messenger`
  
### Third-party components

Third-party components are internal components that receive traffic from the components that {ref}`serve client traffic <reference-internal-network-requirements-client-serving>`. For more information on the role each of these components serves, see the {ref}`explanation-server-architecture`

These components are generally configured to accept traffic on the default ports for their respective services:

- 5432: PostgreSQL
- 5672: RabbitMQ Server
- 8200: HashiCorp Vault

## Client instance networking information

Registered Landscape instances regularly communicate their network interface information to Landscape Server. This information includes the IP address, MAC address, broadcast address, and netmask for each interface. Landscape Client reports this information shortly after registration. Currently, it does not update this information after reporting it the first time.
