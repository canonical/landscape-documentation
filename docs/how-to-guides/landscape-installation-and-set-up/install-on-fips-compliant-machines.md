(how-to-install-fips-compliant)=
# How to install a FIPS-compliant Landscape Server

This document provides the Landscape-specific steps needed for a FIPS-compliant Landscape deployment. The FIPS-compliant process is quite similar to the standard installation process. 

Note that for FIPS-compliant deployments, Landscape Quickstart isn't suitable for large estates (over a few hundred machines). This is due to some performance configuration introduced by the `openssl` 3.0 package which incorporates delays. To manage a large, FIPS-compliant estate, use the Juju deployment method, which allows for horizontal scaling to overcome this limitation.

## The FIPS-compliant Landscape Quickstart checklist

Use the {ref}`Quickstart <how-to-quickstart-installation>` or {ref}`Manual <how-to-manual-installation>` installation guides, with the following changes:

- **Use Ubuntu 22.04 LTS**
- **Run `pro enable fips-updates`, then reboot**
- **Install Landscape 24.04 LTS**
- **Install packages with `apt` instead of `snap`**
- **Use external authentication instead of username/password**

If you're {ref}`configuring Postfix for emails <how-to-configure-postfix>`, add the following change:

- **After you've used Postconf to configure the `/etc/postfix/main.cf` file, add an additional step to manually set the SMTP TLS fingerprint digest**:

    ```bash
    sudo postconf -e smtp_tls_fingerprint_digest=sha256
    ```

    By default, Postfix uses MD5 hashes with the TLS for backward compatibility. In FIPS mode, the MD5 hashing function is not available. SHA-256 is a secure cryptographic hash function that can be used with FIPS.

## The FIPS-compliant Juju Landscape deployment checklist

- Specify that FIPS should be enabled within a cloud-init.yaml file
    
    ```yaml
    #cloud-config
    ubuntu_pro:
      token: <ubuntu_pro_token>
      enable:
        - fips-updates
    ```

- Ensure that every new machine Juju provisions in this model will have FIPS enabled at first boot, by using this cloud-init.yaml file as the model config in Juju:

    ```bash
    juju model-config --file cloudinit-userdata.yaml
    ```
   
- Follow the [Juju installation steps](../juju-installation/).

## Related topics

Outside of Landscape, there are additional steps you may need when setting up your full FIPS-compliant deployment. See the following related topics:

- [Ubuntu Security | FIPS for Ubuntu](https://ubuntu.com/security/fips)
- [Ubuntu Security | FIPS for Ubuntu 22.04](https://ubuntu.com/security/certifications/docs/2204/fips)
- [Ubuntu Pro | How to manage FIPS](https://documentation.ubuntu.com/pro/pro-client/enable_fips/)

