(how-to-configure-postfix)=
# How to configure Postfix for emails

```{note}
These steps use SendGrid as an example email service provider that can be configured to work with Postfix. They may still generally apply to other email service providers, such as Mailjet, Amazon SES or Google.
```

```{note}
To learn more about Postfix, see [Ubuntu Server's documentation on Postfix](https://documentation.ubuntu.com/server/how-to/mail-services/install-postfix/).
```

You can configure Postfix to handle your Landscape Server email notifications and alerts.

## Set environment variables

To set the necessary environment variables, run the following code. Replace `{API_KEY}` with an API key from `https://app.sendgrid.com/settings/api_keys`:

```bash
SMTP_HOST='smtp.sendgrid.net'
SMTP_PORT='587'
SMTP_USERNAME='apikey'
SMTP_PASSWORD='{API_KEY}'
```

## Install Postfix

To install Postfix, run:

```bash
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y postfix
```

## Use Postconf to configure the `/etc/postfix/main.cf` file

1. Configure the `/etc/postfix/main.cf` file with Postconf:

    ```bash
    sudo postconf -e myhostname="$FQDN"
    sudo postconf -e mydomain="$DOMAIN"
    sudo postconf -e myorigin="$DOMAIN"
    sudo postconf -e masquerade_domains="$DOMAIN"
    sudo postconf -e mydestination=localhost
    sudo postconf -e default_transport=smtp
    sudo postconf -e relay_transport=smtp
    sudo postconf -e relayhost="[${SMTP_HOST}]:${SMTP_PORT}"
    sudo postconf -e smtp_sasl_auth_enable=yes
    sudo postconf -e smtp_sasl_password_maps=hash:/etc/postfix/sasl_passwd
    sudo postconf -e smtp_sasl_security_options=noanonymous
    sudo postconf -e header_size_limit=4096000
    ```

    This code block includes the following values that must be changed:

    `{SMTP_HOST}`: The hostname or IP address of the SMTP server to which Postfix will relay outgoing emails

    `{SMTP_PORT}`: The port number on which the SMTP server is listening for incoming connections
2. SendGrid requires TLS encryption when connecting on Port 587, so you must make the following additional configurations:

    ```bash
    sudo postconf -e smtp_use_tls=yes
    sudo postconf -e smtp_tls_security_level=encrypt
    sudo postconf -e smtp_sasl_tls_security_options=noanonymous
    ```

## Finish configuration

1. Write `/etc/postfix/sasl_passwd` with the authentication credentials:

    ```bash
    sudo sh -c "echo \"[$SMTP_HOST]:$SMTP_PORT $SMTP_USERNAME:$SMTP_PASSWORD\" > /etc/postfix/sasl_passwd"
    ```

2. Generate a hashed version of that file:

    ```bash
    sudo postmap /etc/postfix/sasl_passwd
    ```

3. Secure `/etc/postfix/sasl_passwd.db`:

    ```bash
    sudo chmod 600 /etc/postfix/sasl_passwd.db
    ```

4. Remove `/etc/postfix/sasl_passwd` for security:

    ```bash
    sudo rm /etc/postfix/sasl_passwd
    ```

5. Restart Postfix for these settings to take effect:

    ```bash
    sudo /etc/init.d/postfix restart
    ```

## (Optional) Add an email alias

To ensure that important system emails get attention, we recommend adding an alias for Landscape on your local environment.

1. Open the `aliases` file:

    ```bash
    sudo vim /etc/aliases
    ```

1. Add the Landscape alias, replacing `<RECIPIENT_EMAIL>` with the email where Landscape notifications should be sent:

    ```text
     landscape: <RECIPIENT_EMAIL>
    ```

1. Rebuild your aliases:

    ```bash
    sudo /usr/bin/newaliases
    ```
