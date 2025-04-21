(explanation-cryptographic-technology)=
# Cryptographic technology in Landscape

Landscape Server uses various cryptographic technologies internally. They’re used for communication between Landscape Server services and dependency services, Landscape Client and users of the web interface and APIs.

This document describes how Landscape uses cryptographic technology and our recommendations for a secure deployment.

## Cryptographic technology used by Landscape

### TLS/HTTPS

TLS is used to secure HTTP communications in the following scenarios:

* **Landscape Client and Server communications:** TLS secures HTTP traffic between Landscape Server services and Landscape Client-managed instances.
* **Web interface and API requests:** TLS is used by internet browsers when users access the Landscape Server web interface and when making requests to the Legacy and REST APIs.
* **External authentication providers:** TLS secures communications between Landscape Server services and external authentication providers, such as Ubuntu One.

Optionally, TLS can also be configured to secure communications between the Landscape server and its PostgreSQL database, but this is not enabled by default. When this option is enabled, PostgreSQL relies on the system's OpenSSL implementation for TLS-secured database communication.

TLS for HTTP communications is enforced by the reverse proxy used to serve Landscape Server externally:

* **For charmed installations and Landscape SaaS**: TLS is provided by HAProxy
* **For other installations**: TLS is typically provided by Apache Server

The system administrator supplies the TLS certificates, and OpenSSL is used as the underlying implementation for both HAProxy and Apache Server.

### JSON Web Tokens

JSON Web Tokens (JWTs) are generated for authenticated users to interact with the Landscape Server APIs. These tokens are cryptographically signed using HMAC with the SHA-256 hash algorithm.

JWTs are implemented via the [PyJWT](https://pypi.org/project/PyJWT/) library, which uses Python’s `hashlib` and `hmac` modules. Both modules rely on OpenSSL implementations of the hashing algorithms.

### Password authentication

Password authentication is the default authentication method for Landscape self-hosted installations. Administrators authenticate by identifying themselves with an email address and providing a password. The password is stored hashed and salted in the Landscape self-hosted database.

Passwords are salted with a string of 8 randomly-selected alphanumeric ASCII characters, then hashed with a single round of SHA-512. Password hashing is provided by Python’s `hashlib` module, which relies on OpenSSL implementations of the hashing algorithms.

Passwords are not stored for installations that use external authentication.

### GPG signing and signatures

Landscape Server uses Ubuntu’s public GPG keys to verify upstream Ubuntu archive repositories. The public GPG keys used are the 2004, 2012 and 2018 Ubuntu public keys. The 2004 key is a 1024-bit DSA key, and the 2012 and 2018 keys are 4096-bit RSA keys. GPG key signing and signature verification is performed using GnuPG.

Any other GPG keys used for signature verification or for signing Landscape-managed repositories must be provided by the user.

## Recommended usage and settings

We have the following recommendations for secure deployments.

### TLS/HTTPS

We recommend using TLS for all endpoints. By default, traffic to Landscape Server is secured using TLS for most endpoints. Landscape Server charm installations use HAProxy with TLS and other installations typically use Apache Server with TLS. There are a few select endpoints that allow non-TLS traffic: `ping`, `repository`, and `hash-id-databases`. However, TLS can be used for these endpoints by modifying the Landscape Client and repository profile configurations.

To enable HTTPS for the `ping` and `hash-id-databases` endpoints, Landscape Clients can be configured using the `ping_url` and `package_hash_id_url` settings to use HTTPS.

To enable HTTPS for the `repository` endpoint, Landscape repository profiles can be configured to use HTTPS APT sources, but this may require creating those APT sources manually rather than having Landscape determine them automatically based on created repository mirrors.

### JSON Web Tokens

The JWT signing algorithm relies on the `secret-token` setting in the Landscape Server configuration. During installation, a randomized 172-character token is generated. If you change this token, we recommend using a secret token that's at least 64 characters long.

### Password authentication

It’s generally recommended to use strong passwords that follow standard password security practices, although it’s up to the user to enforce these. Landscape doesn’t have specific password format requirements.

### GPG signing and signatures

Landscape Server administrators provide the GPG keys used for signing. We recommend using one of the following public key algorithms:

* RSA with at least 2048-bit keys, 4096-bit recommended
* ED25519
* ED448

For repository mirroring, administrators also generate a private key to sign and validate mirrored packages. You should ensure this private key is securely stored, as stolen signing keys can be used as an attack vector. We recommend using a dedicated key specifically for your repository mirrors to reduce the potential impact if the key is compromised.

## Cryptographic technology available to users

Landscape doesn’t provide cryptography services for external uses, so users can't use Landscape to perform their own cryptographic actions, such as signing files or encrypting uploaded data. However, users can change the cryptographic settings in Landscape that would impact the security of their Landscape deployments. See the earlier section on [recommended usage and settings](#recommended-usage-and-settings) for guidance.

