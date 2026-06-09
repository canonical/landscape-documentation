```{mermaid}
flowchart TD
    Client([Client])
    TLS[TLS Provider]
    subgraph model[Juju model]
        HAProxy["HAProxy<br/>2.8/edge"]
        LS0[landscape-server/0]
        LS1[landscape-server/1]
        LS2[landscape-server/2]
        PG[(PostgreSQL)]
        RMQ[RabbitMQ Server]
    end
    TLS -- certificates --> HAProxy
    Client -- HTTPS --> HAProxy
    HAProxy -- haproxy-route --> LS0
    HAProxy -- haproxy-route --> LS1
    HAProxy -- haproxy-route --> LS2
    LS0 & LS1 & LS2 --- PG
    LS0 & LS1 & LS2 --- RMQ
```
