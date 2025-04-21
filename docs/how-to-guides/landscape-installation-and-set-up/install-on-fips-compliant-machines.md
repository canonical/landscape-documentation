(how-to-install-fips-compliant)=
# How to install on FIPS-compliant machines

This document provides the Landscape-specific steps needed for a FIPS-compliant Landscape deployment. The FIPS-compliant process is quite similar to the standard installation process.

## Install and configure Landscape for FIPS-compliant deployments

Use the [Quickstart](/how-to-guides/landscape-installation-and-set-up/quickstart-installation) or [Manual](/how-to-guides/landscape-installation-and-set-up/manual-installation) installation guides, with the following changes:

- **Use Ubuntu 22.04 LTS**
- **Run `pro enable fips-updates`, then reboot**
- **Install Landscape 24.04 LTS**
- **Install packages with `apt` instead of `snap`**
- **Use external authentication instead of username/password**

If you're [configuring Postfix for emails](/how-to-guides/landscape-installation-and-set-up/configure-postfix), add the following change:

- **After you've used Postconf to configure the `/etc/postfix/main.cf` file, add an additional step to manually set the SMTP TLS fingerprint digest**:

    ```bash
    sudo postconf -e smtp_tls_fingerprint_digest=sha256
    ```

    By default, Postfix uses MD5 hashes with the TLS for backward compatibility. In FIPS mode, the MD5 hashing function is not available. SHA-256 is a secure cryptographic hash function that can be used with FIPS.

## Related topics

Outside of Landscape, there are additional steps you may need when setting up your full FIPS-compliant deployment. See the following related topics:

- [Ubuntu Security | FIPS for Ubuntu](https://ubuntu.com/security/fips)
- [Ubuntu Security | FIPS for Ubuntu 22.04](https://ubuntu.com/security/certifications/docs/2204/fips)
- [Ubuntu Pro | How to manage FIPS](https://documentation.ubuntu.com/pro/pro-client/enable_fips/)

