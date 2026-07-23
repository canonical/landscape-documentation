```{important}
If you change `landscape.task-handler.server.host` or `landscape.task-handler.server.grpc-port` from the defaults shown above, you must also update the outbox's `landscape.task-handler.grpc-address` snap key to match. Otherwise the outbox's services will still report as **active**, but hard deletion requests will fail at runtime. See {ref}`reference-outbox-configuration` for details.
```
