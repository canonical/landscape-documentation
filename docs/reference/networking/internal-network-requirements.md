(reference-internal-network-requirements)=
# Internal network requirements

Landscape consists of a number of individual services and dependencies. These components communicate with each other across the network in a variety of ways. Landscape Clients may also communicate with Landscape Server across the internet.

This page documents how Landscape Server's components communicate with each other – which communication protocols are used and what network settings are required to allow this. For more information on the individual components and their purposes, see {ref}`this explanation of the Landscape Server architecture <explanation-server-architecture>`.

![Landscape Network Diagram](/assets/images/landscape-server-networking.jpg "Landscape Networking")

## External network traffic

External clients communicate with Landscape Server over the internet. These clients include web browsers interacting the Landscape's web UI, Landscape API clients, Landscape-managed instances, and Landscape repository package uploaders.

The first point of contact for all of this traffic is the reverse proxy, which also acts as a load-balancer and performs TLS termination. In most Landscape Server deployments, this role is filled by [HAProxy](https://www.haproxy.org/), but in some deployments, it may be [Apache Server](https://httpd.apache.org/).

All External network traffic to and from Landscape uses HTTP. Consequently, TCP ports 80 and 443 (for HTTPS) on the reverse proxy must be exposed to the wide area network. In addition, port 6554 must be exposed for gRPC (HTTP/2) communication with [Ubuntu Pro for WSL](https://documentation.ubuntu.com/wsl/stable/).

## Internal network traffic

Internal Landscape components communicate with each other directly. These are the first- and third-party services that provide all of Landscape's features. This traffic is "internal" because it should only traverse the local area network in which Landscape Server is deployed.

Internal network traffic is "behind" a reverse proxy. In most Landscape Server deployments, the role of reverse proxy is filled by [HAProxy](https://www.haproxy.org/), but in some deployments, it may be [Apache Server](https://httpd.apache.org/).

(reference-internal-network-requirements-client-serving)=
### Components that receive client traffic

The reverse proxy accepts external HTTP traffic originating from clients and proxies it to internal components. It also performs TLS termination. By default, each internal component listens for HTTP traffic on a different range of ports. A range is used to allow for scalability – multiple workers for each component can be active at the same time.

These are the current port ranges for each internal component that accepts traffic from the reverse proxy. Each range is inclusive.

  - 8070-8079: {ref}`Appserver <explanation-server-architecture-appserver>`
  - 8080-8089: {ref}`Pingserver <explanation-server-architecture-pingserver>`
  - 8090-9079: {ref}`Message system <explanation-server-architecture-message-system>`
  - 9080-9098: {ref}`API <explanation-server-architecture-api>`
  - 9099: {ref}`Package search <explanation-server-architecture-package-search>`
  - 9100: {ref}`Package upload <explanation-server-architecture-package-upload>`
  - 50052: {ref}`Hostagent messenger <explanation-server-architecture-hostagent-messenger>`
  
### Third-party components

Third-party components are internal components that receive traffic from the components that {ref}`serve client traffic <reference-internal-network-requirements-client-serving>`. For more information on the role each of these components serves, see {ref}`the explanation of Landscape Server's architecture <explanation-server-architecture>`.

These components are generally configured to accept traffic on the default ports for their respective services:

  - 5432: PostgreSQL
  - 5672: RabbitMQ Server
  - 8200: HashiCorp Vault

## Client instance networking information

Registered Landscape instances regularly communicate their network interface information to Landscape Server. This information includes the IP address, MAC address, broadcast address, and netmask for each interface. Client reports this information shortly after registration. Currently, it does not update this information after reporting it the first time.
