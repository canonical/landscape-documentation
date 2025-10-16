(reference-internal-network-requirements)=
# Internal network requirements

Landscape consists of a number of individual services and dependencies. These components communicate with each other across the network in a variety of ways. Landscape Clients may also communicate with Landscape Server across the internet.

This page documents how Landscape Server's components communicate with each other – which communication protocols are used and what network settings are required to allow this. For more information on the individual components and their purposes, see [this explanation of the Landscape Server architecture](/explanation/landscape/landscape-server-architecture).

## External network traffic

External clients communicate with Landscape Server over the internet. These clients include web browsers interacting the Landscape's web UI, Landscape API clients, Landscape-managed instances, and Landscape repository package uploaders.

The first point of contact for all of this traffic is the reverse proxy, which also acts as a load-balancer and performs TLS termination. In most Landscape Server deployments, this role is filled by [HAProxy](https://www.haproxy.org/), but in some deployments, it may be [Apache Server](https://httpd.apache.org/).

All External network traffic to and from Landscape uses HTTP. Consequently, TCP ports 80 and 443 (for HTTPS) on the reverse proxy must be exposed to the wide area network. In addition, port 6554 must be exposed for gRPC (HTTP/2) communication with [Ubuntu Pro for WSL](https://documentation.ubuntu.com/wsl/stable/).

## Internal network traffic

Internal Landscape components communicate with each other directly. These are the first- and third-party services that provide all of Landscape's features. This traffic is "internal" because it should only traverse the local area network in which Landscape Server is deployed.

Internal network traffic is "behind" a reverse proxy. In most Landscape Server deployments, the role of reverse proxy is filled by [HAProxy](https://www.haproxy.org/), but in some deployments, it may be [Apache Server](https://httpd.apache.org/).

### Components that receive client traffic

The reverse proxy accepts external HTTP traffic originating from clients and proxies it to internal components. It also performs TLS termination. By default, each internal component listens for HTTP traffic on a different range of ports. A range is used to allow for scalability – multiple workers for each component can be active at the same time.

These are the current port ranges for each internal component that accepts traffic from the reverse proxy. Each range is inclusive.

  - 8070-8079: [Appserver](/explanation/landscape/landscape-server-architecture/#appserver)
  - 8080-8089: [Pingserver](/explanation/landscape/landscape-server-architecture/#pingserver)
  - 8090-9079: [Message system](/explanation/landscape/landscape-server-architecture/#message-system)
  - 9080-9098: [API](/explanation/landscape/landscape-server-architecture/#api)
  - 9099: [Package search](/explanation/landscape/landscape-server-architecture/#package-search)
  - 9100: [Package upload](/explanation/landscape/landscape-server-architecture/#package-upload)
  - 50052: [Hostagent messenger](/explanation/landscape/landscape-server-architecture/#hostagent-messenger)
