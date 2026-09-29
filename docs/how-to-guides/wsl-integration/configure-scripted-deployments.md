---
myst:
  html_meta:
    description: "Note for scripting Ubuntu Pro for WSL against Landscape: set GRPC_ENFORCE_ALPN_ENABLED=false before starting ubuntu-pro-agent.exe directly."
---

(how-to-wsl-configure-scripted-deployments)=
# Note for scripted Ubuntu Pro for WSL deployments

If you're scripting Ubuntu Pro for WSL against Landscape (for example, setting the registry keys and starting `ubuntu-pro-agent.exe` directly instead of going through the app), remember to set this environment variable first:

```powershell
$env:GRPC_ENFORCE_ALPN_ENABLED = "false"
```

When the agent is started by the Ubuntu Pro for WSL app, the app's launcher sets this variable for you. When you start `ubuntu-pro-agent.exe` yourself, it isn't set, and the agent can't connect to Landscape's hostagent endpoint (port 6554). You'll see repeated TLS handshake warnings in `%USERPROFILE%\.ubuntupro\log`:

```text
level=warning msg=Landscape: could not connect to Landscape server: rpc error: code = Unavailable
desc = connection error: desc = "transport: authentication handshake failed: credentials: cannot
check peer: missing selected ALPN property. ..."
```

The value must be exactly `false` (case-insensitive), and it must be set in the same session before the agent starts. Don't use `[Environment]::SetEnvironmentVariable(..., "User")` here: it writes to the registry but doesn't update the current PowerShell process, so an agent launched from the same session won't see it. This is a temporary requirement until the Landscape server negotiates ALPN on that endpoint.

If you configure Landscape through the app, none of this applies to you. See {ref}`how-to-register-wsl-hosts`.
