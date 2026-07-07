---
myst:
  html_meta:
    description: "Known issues and workarounds for Landscape Server and Client. Current limitations, compatibility notes, and configuration fixes."
---

(reference-known-issues)=
# Known issues

## RabbitMQ 4.0 and later not supported

Landscape requires RabbitMQ 3.x. RabbitMQ 4.0 dropped support for the AMQP 0-8 protocol that Landscape depends on, so version 4.0 and later are not compatible.

Ubuntu 26.04 LTS (Resolute) ships RabbitMQ 4.x in its archives, so the default `apt install rabbitmq-server` gives you an incompatible version. The Quickstart installation method is not supported on Ubuntu 26.04 for this reason. Ubuntu 22.04 LTS (Jammy) and Ubuntu 24.04 LTS (Noble) both ship RabbitMQ 3.x and are not affected.

If you need to run Landscape on Ubuntu 26.04, you can install RabbitMQ 3.13.x from Team RabbitMQ's apt repositories. Their repositories don't include a resolute-specific entry, but the noble packages work on resolute. You also need to pin Erlang to 26.x, because apt will otherwise select Erlang 27.x which RabbitMQ 3.x doesn't support.

```bash
# Add Team RabbitMQ's signing key
sudo apt-get install -y curl gnupg apt-transport-https
curl -1sLf 'https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA' \
  | sudo gpg --dearmor \
  | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null

# Add the noble-based Erlang and RabbitMQ repos
sudo tee /etc/apt/sources.list.d/rabbitmq.list << 'EOF'
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-erlang/ubuntu/noble noble main
deb [arch=amd64 signed-by=/usr/share/keyrings/com.rabbitmq.team.gpg] https://deb1.rabbitmq.com/rabbitmq-server/ubuntu/noble noble main
EOF

sudo apt-get update

# Install Erlang 26.x explicitly (required by RabbitMQ 3.13.x)
sudo apt-get install -y \
  erlang-base=1:26.2.5.13-1 \
  erlang-asn1=1:26.2.5.13-1 \
  erlang-crypto=1:26.2.5.13-1 \
  erlang-eldap=1:26.2.5.13-1 \
  erlang-ftp=1:26.2.5.13-1 \
  erlang-inets=1:26.2.5.13-1 \
  erlang-mnesia=1:26.2.5.13-1 \
  erlang-os-mon=1:26.2.5.13-1 \
  erlang-parsetools=1:26.2.5.13-1 \
  erlang-public-key=1:26.2.5.13-1 \
  erlang-runtime-tools=1:26.2.5.13-1 \
  erlang-snmp=1:26.2.5.13-1 \
  erlang-ssl=1:26.2.5.13-1 \
  erlang-syntax-tools=1:26.2.5.13-1 \
  erlang-tftp=1:26.2.5.13-1 \
  erlang-tools=1:26.2.5.13-1 \
  erlang-xmerl=1:26.2.5.13-1

# Install RabbitMQ 3.13.x
sudo apt-get install -y rabbitmq-server=3.13.7-1

# Hold Erlang and RabbitMQ to prevent apt upgrade from pulling in incompatible versions
sudo apt-mark hold rabbitmq-server erlang-base erlang-asn1 erlang-crypto erlang-eldap \
  erlang-ftp erlang-inets erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
  erlang-runtime-tools erlang-snmp erlang-ssl erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
```

## gRPC version

Landscape installs its own version of `python3-protobuf` and `python3-grpcio` from its PPA, which are incompatible with the versions currently available in different releases of Ubuntu. Applications that require gRPC connectivity cannot currently coexist with Landscape as the gRPC stubs would not be compatible with the gRPC packages installed by Landscape.

(reference-known-issues-lsctl-restart)=
## `lsctl restart`

{ref}`lsctl restart <reference-lsctl-restart>` does not enable or disable Landscape cron jobs. In order to manually enable Landscape cron jobs, remove the `/opt/canonical/landscape/maintenance.txt` file. In order to manually disable Landscape cron jobs, add the `/opt/canonical/landscape/maintenance.txt` file.

## Pydantic with ESM enabled

Since version 24.10, Landscape Server relies on `python3-pydantic (>= 2.4.2)`. However, the ESM repositories for jammy and noble have a lower version of that package available with a higher `apt` pin priority. This conflict can cause Landscape Server upgrades and installations to fail on instances with ESM enabled.

To work around this conflict, you can add the following to a `/etc/apt/preferences.d/landscape-server` file:

```text
Explanation: The ESM archives have a version of python3-pydantic that
Explanation: is a lower version than the one required by Landscape Server.
Package: python3-pydantic
Pin: release o=LP-PPA-landscape-latest-stable
Pin-Priority: 550
```

Replace the PPA on the `Pin:` line with the appropriate one for your Landscape Server installation (e.g. use `LP-PPA-landscape-self-hosted-beta` for the beta PPA).
