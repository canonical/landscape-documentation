---
myst:
  html_meta:
    description: "Reference for securing Landscape with network firewall rules including publicly accessible URIs and recommended access restrictions."
---

(reference-network-firewall)=
# Network firewall

## Publicly accessible URIs

For security reasons, it's important to restrict access from the public internet. If you have a self-hosted Landscape deployment with clients outside your local network, it's strongly advised you restrict network access to your Landscape server.

You should only permit access to the following URIs:

- `/ping`
- `/message-system`
- `/repository`
- `/attachments`
- `/hash-id-databases`

The URIs listed follow your Landscape FQDN. For example, `https://landscape-server.example.com/ping`.

The paths `/repository`, `/attachments` and `/hash-id-databases` contain several subpaths. Depending on your specific purpose, you can choose to restrict access to one or more of these subpaths. For example, in single-tenant architectures, access to the path `/repository` can be limited exclusively to `/repository/standalone/*`.
