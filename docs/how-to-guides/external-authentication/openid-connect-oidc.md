(how-to-external-auth-oidc)=
# How to enable OIDC authentication

Landscape offers support for OpenID-Connect (OIDC) authentication for self-hosted accounts. Common OIDC providers include Okta, Keycloak, Amazon Cognito, Google Identity Platform and Microsoft Entra ID (formerly Azure Active Directory).

```{note}
Landscape uses OIDC only for authentication decisions.
Landscape doesn't currently integrate with external roles, groups, or existing user metadata.
You still need to invite users and assign their roles and permissions within Landscape.
```

## Enable OIDC support in Landscape

To enable OIDC support, add `oidc-issuer`, `oidc-client-id` and `oidc-client-secret` to `/etc/landscape/service.conf` in the `[landscape]` section. For example:

```bash
[landscape]
[…]
oidc-issuer = <https://accounts.google.com/>
oidc-client-id = 000000000000-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.apps.googleusercontent.com
oidc-client-secret = a4sDFAsdfA4F52as-asDfAsd
```

The `oidc-issuer` is the URL of the issuer. That URL should also be a discovery configuration file available by appending `.well-known/openid-configuration`, such as [https://accounts.google.com/.well-known/openid-configuration](https://accounts.google.com/.well-known/openid-configuration). 

The `oidc-client-id` and `oidc-client-secret` should be provided by your OIDC provider when you create the client credentials. The provider may require setting an authorization redirect URI. This should look like `https://your_landscape/login/handle-openid`. If your provider also requires a logout redirect URL, this should be the address of your Landscape server such as `https://your_landscape/`.

### (Optional) Specify your provider to enable additional features

Certain features are available only for certain OIDC providers.
Landscape recognizes the following slugs for providers:

- `google`: Google OAuth 2.0
- `okta`: Okta

```bash
[landscape]
[…]
oidc-issuer = <https://accounts.google.com/>
oidc-client-id = 000000000000-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.apps.googleusercontent.com
oidc-client-secret = a4sDFAsdfA4F52as-asDfAsd
oidc-provider = google
```

You will still be able to authenticate as usual without specifying an `oidc-provider`.
It is not required for basic OIDC authentication.
If you change the value of your `oidc-provider`, it will be updated on your next authentication.

## Restart all Landscape services

To restart all Landscape services, run:

```bash
sudo lsctl restart
```

## (Optional) Configure a logout URL

A logout URL can be configured with `oidc-logout-url` if the provider doesn’t expose one. For example:

```bash
[landscape]
…
oidc-logout-url = <https://accounts.google.com/logout>
```

```{note}
There is no provision yet to upgrade current users to OIDC authentication. Most providers return pairwise subject identifiers (sub) which are not easily available. For this reason, we do not provide a user migration method and recommend recreating users.
```
