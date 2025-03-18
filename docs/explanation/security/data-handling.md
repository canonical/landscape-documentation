# Data handling

> See also: [Cryptographic technology in Landscape](/explanation/security/cryptographic-technology.md)

This document provides an overview of how Landscape handles data in transit and at rest for SaaS (Canonical-owned) and self-hosted deployments.

## Data in transit

- **SaaS deployment**: Encrypted with HTTPS (TLS), using RSA with SHA-256.
- **Self-hosted deployment**: Encrypted with HTTPS (TLS) by default, using RSA with SHA-256. See our full [cryptography document](/explanation/security/cryptographic-technology.md) for more information.

## Data at rest

- **SaaS deployment**: Encrypted using AES-128.
- **Self-hosted deployment**: This is user-controlled. Landscape doesn't configure any encryption of a self-hosted database by default, although encryption can be added by the user.