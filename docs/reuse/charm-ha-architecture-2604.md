```{mermaid}
flowchart TD
    Client([Client])
    TLS[TLS Provider]
    subgraph model[Juju model]
        HAProxy["HAProxy<br/>2.8/stable"]
        LS0[landscape-server/0]
        LS1[landscape-server/1]
        LS2[landscape-server/2]
        PG[(PostgreSQL)]
        RMQ[RabbitMQ Server]
        DA[landscape-debarchive]
        TH[landscape-task-handler]
    end
    TLS -- certificates --> HAProxy
    TLS -- certificates --> TH
    Client -- HTTPS --> HAProxy
    HAProxy -- haproxy-route --> LS0
    HAProxy -- haproxy-route --> LS1
    HAProxy -- haproxy-route --> LS2
    LS0 & LS1 & LS2 --- PG
    LS0 & LS1 & LS2 --- RMQ
    LS0 -- debarchive --> DA
    DA --- PG
    HAProxy -- debarchive-haproxy-route --> DA
    LS0 -- task-handler --> TH
    TH --- PG
    HAProxy -- grpc-haproxy-route --> TH
```
