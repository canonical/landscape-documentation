---
myst:
  html_meta:
    description: "Make REST API requests to Landscape 24.04 LTS using curl and JWT authentication. Learn login credentials and token management."
---

(how-to-rest-api-request)=
# How to make a REST API request

> See also: {ref}`reference-rest-api-login`

This guide demonstrates how to login and make a request using the Landscape REST API. You need Landscape 24.04 LTS (or higher) to use the REST API. This guide provides general steps and examples using `curl`.

> **Note**: When using state-changing methods (i.e. `POST`, `PUT`, and `PATCH`), you must explicitly declare `Content-Type` as `application/json`. You can do this manually or automatically using a library such as [HTTPie](https://httpie.io/).

## Make a REST API request with your preferred API tool

The general steps to make a REST API request are:

1. Provide your login credentials with `POST`
2. Copy your token from the output
3. Assign your token to a new variable, such as `JWT`
4. Make your API request, using your token for authorization

## Password authentication: Make a REST API request with `curl`

This method is for those using password authentication to login.

 To make a REST API request with `curl`:

1. Provide your login credentials with `POST`. Your request will be similar to the following

    ```bash
    curl -X POST "https://your-landscape.domain.com/api/v2/login" \
      -H "Content-Type: application/json" \
      -d '{"email": "jane@example.com", "password": "jane-pwd", "account": "standalone"}'
    ```

    And you’ll receive output similar to:

    ```json
    {
        "accounts": [
            {
                "default": true,
                "name": "standalone",
                "title": "Jane-Organisation"
            }
        ],
        "current_account": "standalone",
        "email": "jane@example.com",
        "name": "Jane Smith",
        "token": "qkJ0eXAiOiJKV1QiLCJhbGciOiJskdi296MTcxMDM2MTQxNiwic3ViIjoieWFuaXNhLnNjaGVyYmVyQGNhbm9uaWNhbC5jb20iLCJhY2MiOiJzdGFuZGFsb2i93nboPRfXp50"
    }
    ```

1. Copy your token from the output and assign it to a new variable, such as `JWT`:

    ```bash
    JWT="qkJ0eXAiOiJKV1QiLCJhbGciOiJskdi296MTcxMDM2MTQxNiwic3ViIjoieWFuaXNhLnNjaGVyYmVyQGNhbm9uaWNhbC5jb20iLCJhY2MiOiJzdGFuZGFsb2i93nboPRfXp50"
    ```

1. Make your API request, using your token as authorization. For example:

    ```bash
    curl -X GET https://your-landscape.domain.com/api/v2/activities -H "Authorization: Bearer $JWT"
    ```
