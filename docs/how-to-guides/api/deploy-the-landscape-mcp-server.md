---
myst:
  html_meta:
    description: "Deploy the Landscape MCP server with Juju on Kubernetes and publish it at /mcp behind the HAProxy that fronts your Landscape Server deployment."
---

(how-to-deploy-landscape-mcp-server)=
# How to deploy the Landscape MCP server behind HAProxy

> See also: {ref}`how-to-rest-api-request`, {ref}`how-to-juju-ha-installation`

The [Landscape MCP server](https://github.com/jansdhillon/landscape-mcp) lets AI agents that support the [Model Context Protocol](https://modelcontextprotocol.io/) query Landscape through the Landscape API. This guide shows how to deploy it as a Kubernetes charm and publish it at `https://<your-landscape-host>/mcp`, through the same HAProxy that fronts your Landscape Server charm deployment.

This guide applies to Landscape Server deployed with Juju, where HAProxy is deployed by the `haproxy` charm. The Landscape MCP server charm is built from source and isn't published on Charmhub.

## Prerequisites

You need:

- A Landscape Server deployment with Juju and HAProxy, using the `haproxy-route` relations. See {ref}`how-to-juju-ha-installation`.
- A Juju Kubernetes controller (for example, MicroK8s) that can offer or consume cross-model relations with the model that contains HAProxy.
- Network access from HAProxy to the Landscape MCP server unit. HAProxy uses the unit's address on the relation network as the backend address, so that address must be routable from the HAProxy machine.
- A Landscape API access key and secret key for the account the MCP server should query.
- `rockcraft`, `charmcraft`, and `git`.

## Build the rock and the charm

1. Clone the repository:

    ```bash
    git clone https://github.com/jansdhillon/landscape-mcp
    cd landscape-mcp
    ```

2. Build the OCI image and the charm:

    ```bash
    rockcraft pack
    (cd charm && charmcraft pack)
    ```

3. Make the image available to your Kubernetes cluster, for example by pushing it to a registry the cluster can pull from.

## Deploy the charm

1. In your Kubernetes model, deploy the charm with the image resource and the Landscape API URI:

    ```bash
    juju deploy ./charm/landscape-mcp_ubuntu@24.04-amd64.charm landscape-mcp \
      --resource landscape-mcp-image=<your-registry>/landscape-mcp:latest \
      --config landscape-api-uri=https://<your-landscape-host>/api/
    ```

    The unit is blocked with the message `Missing landscape-api-credentials config` until you complete the next step.

2. Store the API credentials in a Juju secret, grant it to the application, and set the charm option to the secret ID:

    ```bash
    juju add-secret landscape-api-creds api-key=<access-key> api-secret=<secret-key>
    juju grant-secret landscape-api-creds landscape-mcp
    juju config landscape-mcp landscape-api-credentials=secret:<secret-id>
    ```

    The secret must contain the fields `api-key` and `api-secret`. When you update the secret with `juju update-secret`, the charm restarts the server with the new values.

3. Check that the unit is active:

    ```bash
    juju status landscape-mcp
    ```

    If the unit stays blocked, the message tells you whether the secret is missing, not granted, or lacks a field.

## Publish the server through HAProxy

1. Relate the charm to the HAProxy offer. If HAProxy is in another model, consume its `haproxy-route` offer first:

    ```bash
    juju consume <controller>:<owner>/<haproxy-model>.haproxy
    juju integrate landscape-mcp:mcp-haproxy-route haproxy
    ```

2. Set the hostname that HAProxy serves for Landscape. HAProxy ignores routes that have no hostname:

    ```bash
    juju config landscape-mcp external-hostname=<your-landscape-host>
    ```

    In the HAProxy model, `juju status` reports `N/N valid relations` once HAProxy accepts the route.

3. Make sure the Landscape appserver route doesn't catch `/mcp`.

    The Landscape appserver route matches every path that starts with `/`, and HAProxy evaluates it before the `/mcp` route. The `landscape-server` charm excludes the other Landscape paths (such as `/api` and `/repository`) from that route with a deny list. Unless your `landscape-server` charm revision already includes `/mcp` in that list, requests to `/mcp` return the Landscape appserver's `404` response instead of reaching the MCP server.

    To confirm, check the HAProxy configuration in the HAProxy model:

    ```bash
    juju ssh haproxy/0 sudo grep acl_deny_path /etc/haproxy/haproxy.cfg
    ```

    The `acl_deny_path` line for the appserver backend must include `/mcp`. If it doesn't, add `"/mcp"` to the `deny_paths` list of the appserver route in the `landscape-server` charm's `src/charm.py` and refresh the charm.

## Verify the deployment

Send an MCP `initialize` request to the published path:

```bash
curl -i -X POST "https://<your-landscape-host>/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1"}}}'
```

You'll receive an `HTTP/1.1 200 OK` response with an `mcp-session-id` header, and a body similar to:

```text
event: message
data: {"jsonrpc":"2.0","id":1,"result":{"capabilities":{...},"protocolVersion":"2025-03-26","serverInfo":{"name":"landscape-api","version":"v1.0.0"}}}
```

## Connect an MCP client

Point your client at the published URL with the streamable HTTP transport. For example, in the VS Code `mcp.json` file:

```json
{
  "servers": {
    "landscape-mcp": {
      "type": "http",
      "url": "https://<your-landscape-host>/mcp"
    }
  }
}
```

## Troubleshoot

`/mcp` returns a `404` from the Landscape appserver
: HAProxy routes the request to the appserver. See step 3 in the "Publish the server through HAProxy" section.

HAProxy reports an invalid relation
: The route has no hostname. Set `external-hostname` on the `landscape-mcp` charm.

`/mcp` returns a `503`
: HAProxy hasn't marked the backend healthy yet, or can't reach the unit. Check `juju status` for the unit's address, then confirm that address is reachable from the HAProxy machine, for example with `curl http://<unit-address>:8080/healthz`.
