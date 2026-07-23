The output should show the `task-handler.server` and `task-handler.worker` services as **active**:

```text
Service                        Startup  Current  Notes
landscape-task-handler.server  enabled  active   -
landscape-task-handler.worker  enabled  active   -
```

Other services (`cert-renewer`, `cleanup`) run on their own timers and normally show as `inactive`/`timer-activated` between runs; this is expected.
