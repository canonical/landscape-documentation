(reference-known-issues)=
# Known Issues

## gRPC Version

Landscape installs its own version of `python3-protobuf` and `python3-grpcio` from its PPA, which are incompatible with the versions currently available
in different releases of Ubuntu.
Applications that require gRPC connectivity cannot currently coexist with Landscape as the gRPC stubs would not be compatible with the
gRPC packages installed by Landscape.
