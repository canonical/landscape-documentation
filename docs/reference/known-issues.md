(reference-known-issues)=
# Known issues

## gRPC version

Landscape installs its own version of `python3-protobuf` and `python3-grpcio` from its PPA, which are incompatible with the versions currently available in different releases of Ubuntu. Applications that require gRPC connectivity cannot currently coexist with Landscape as the gRPC stubs would not be compatible with the gRPC packages installed by Landscape.

(reference-known-issues-lsctl-restart)=
## `lsctl restart`

{ref}`lsctl restart <reference-lsctl-restart>` does not enable or disable Landscape cron jobs. In order to manually enable Landscape cron jobs, remove the `/opt/canonical/landscape/maintenance.txt` file. In order to manually disable Landscape cron jobs, add the `/opt/canonical/landscape/maintenance.txt` file.
