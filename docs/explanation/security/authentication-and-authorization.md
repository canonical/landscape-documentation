---
myst:
  html_meta:
    description: "Understand authentication and authorization in Landscape including local users, external identity providers, sessions, and JWT authentication."
---

(authentication-and-authorization)=
# Authentication and authorization in Landscape

This document provides an overview of how user authentication and authorization work in Landscape.

## Authentication methods

Broadly, Landscape users can in be one of two categories:

1. Local users
2. Externally-authenticated users

Both types of users must receive an invitation to join an account. Users cannot be provisioned automatically.

### Local users

Local users have their email and password stored in the Landscape database. See {ref}`explanation-cryptographic-technology` for details on password storage. Landscape does not offer multi-factor authentication (MFA) for local users.

Local users may only be created when an external identity provider is not configured.

### Integration with external identity providers

Landscape can integrate with

- {ref}`Pluggable authentication modules (PAM) <how-to-external-auth-pam>`
- {ref}`Active directory <how-to-external-auth-active-directory>`
- {ref}`OIDC <how-to-external-auth-oidc>`

For any external authentication method, Landscape uses the identity provider for authentication only. Landscape does not integrate with any roles or groups in the external identity provider.

## Authentication model

Prior to Landscape 24.04 LTS, Landscape used sessions for UI authentication and an access key/secret pair for API authentication. Beginning in 24.04 LTS, Landscape introduced JWTs for API and UI authentication.

|            | 24.04 LTS                     | 24.10                         | 25.04                         | 25.10                         |
|------------|-------------------------------|-------------------------------|-------------------------------|-------------------------------|
| Classic UI | Session only                  | Session <br> or JWT           | Session <br> or JWT           | Session <br> or JWT           |
| New UI     | JWT only                      | JWT only                      | JWT only                      | JWT only                      |
| Legacy API | Access key/secret <br> or JWT | Access key/secret <br> or JWT | Access key/secret <br> or JWT | Access key/secret <br> or JWT |
| REST API   | JWT only                      | JWT only                      | JWT only                      | JWT only                      |

### Sessions

Landscape sets a session with the browser when a user logs into the classic UI. It is cleared when the user logs out of either the classic or new UI. A session is only a valid access credential on the classic UI. It is not accepted in the new UI or in any APIs.

### JWTs

Landscape issues a JWT and stores it as a cookie when a user logs into the new UI. The cookie is cleared when the user logs out of either the classic or new UI. JWTs are valid access credentials for the classic and new UIs, and both APIs.

See {ref}`explanation-cryptographic-technology` for details on JWT encryption. JWTs are used for identity only; they do not contain any authorization information.

JWTs expire after 24 hours. JWTs can be invalidated for a user, an account, or the entire system. See {ref}`reference-rest-api-tokens`.

### Access key/secret pairs

Access key/secret pairs are issued when a user creates API credentials in the classic UI. Access key/secret pairs may only be used to access the legacy API. However, they can be exchanged for a JWT that is valid in the REST API. See {ref}`reference-rest-api-login`.

Access key/secret pairs may be regenerated at any time, which will invalidate the old credentials. See {ref}`reference-rest-api-credentials`.

## Authorization model

Landscape uses role-based access control (RBAC). Users are assigned roles, and these roles are mapped to a set of permissions. Permissions determine the actions that a user is authorized to perform in Landscape.

Landscape administrators can create custom roles and map them to which permissions they choose. See {ref}`how-to-web-portal-manage-admins-and-roles`.

## Email uniqueness

Landscape requires unique emails for all users. A user created through local email/password is considered a distinct user from one created through an external authentication method, even if the email is the same. Therefore, it is not possible to create an externally-authenticated user with the same email as a local user. Similarly, it is not possible to create two users with the same email from two different external authentication methods.
