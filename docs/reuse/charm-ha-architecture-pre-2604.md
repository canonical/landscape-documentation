```{mermaid}
flowchart TD
    Client([Client])
    subgraph model[Juju model]
        HAProxy["HAProxy<br/>latest/stable"]
        LS0[landscape-server/0]
        LS1[landscape-server/1]
        LS2[landscape-server/2]
        PG[(PostgreSQL 14)]
        RMQ[RabbitMQ Server]
    end
    Client -- HTTPS --> HAProxy
    HAProxy -- reverseproxy --> LS0
    HAProxy -- reverseproxy --> LS1
    HAProxy -- reverseproxy --> LS2
    LS0 & LS1 & LS2 --- PG
    LS0 & LS1 & LS2 --- RMQ
```
