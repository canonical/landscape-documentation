(reference-known-issues)=
# Known issues

## gRPC version

Landscape installs its own version of `python3-protobuf` and `python3-grpcio` from its PPA, which are incompatible with the versions currently available in different releases of Ubuntu. Applications that require gRPC connectivity cannot currently coexist with Landscape as the gRPC stubs would not be compatible with the gRPC packages installed by Landscape.

(reference-known-issues-lsctl-restart)=
## `lsctl restart`

{ref}`lsctl restart <reference-lsctl-restart>` does not enable or disable Landscape cron jobs. In order to manually enable Landscape cron jobs, remove the `/opt/canonical/landscape/maintenance.txt` file. In order to manually disable Landscape cron jobs, add the `/opt/canonical/landscape/maintenance.txt` file.

## Pydantic with ESM enabled

Since version 24.10, Landscape Server relies on `python3-pydantic (>= 2.4.2)`. However, the ESM repositories for jammy and noble have a lower version of that package available with a higher apt pin priority. This conflict can cause Landscape Server upgrades and installations to fail on instances with ESM enabled.

To work around this conflict, you can add the following to a `/etc/apt/preferences.d/landscape-server` file:

```text
Explanation: The ESM archives have a version of python3-pydantic that
Explanation: is a lower version than the one required by Landscape Server.
Package: python3-pydantic
Pin: release o=LP-PPA-landscape-latest-stable
Pin-Priority: 550
```

Replace the PPA on the `Pin:` line with the appropriate one for your Landscape Server installation (e.g. use `LP-PPA-landscape-self-hosted-beta` for the beta PPA).
