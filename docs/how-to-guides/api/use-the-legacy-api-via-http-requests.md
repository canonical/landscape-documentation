(how-to-use-legacy-api-http)=
# How to use the legacy API via HTTPS requests

This guide describes how to call the Landscape legacy API using standard HTTPS requests and the parameters required for each request.

## Make a legacy API request

API requests to the legacy endpoint are HTTPS requests that use the HTTP verb GET or POST and a query parameter named `action`. To be able to make a request, you’ll need to know which endpoint to use, what the action is, and what parameters it takes.

All methods take a list of mandatory arguments which you need to pass every time (unless using JWT authentication, where only `action` and `version` are required):

- `action`: The name of the method you want to call
- `access_key_id`: The access key given to you in the Landscape Web UI. You need to go to your settings section in Landscape to be able to generate it along with the secret key.
- `signature_method`: The method used to sign the request, always `HmacSHA256` for HMAC requests.
- `signature_version`: The version of the signature mechanism, always `2` for HMAC requests.
- `timestamp`: The time in UTC in ISO 8601 format, used to indicate the validity of the signature (HMAC only).
- `version`: The version of the API. `2011-08-01` is the default legacy API version used in the client, but any legacy-style date string matching `YYYY-MM-DD` is treated as a legacy API version by the server and will work if that version is registered.

## Authentication

The legacy API accepts two authentication methods:

- **JWT**: JSON Web Token. The legacy API endpoint accepts either a token or a Landscape session JWT cookie.
- **API Key and Secret**: The API Key and Secret method that requires signing requests.

### JWT

If you use a JWT, you do not need to sign your requests or provide the `access_key_id`, `signature_method`, `signature_version`, or `timestamp` parameters.

Here's an example request:

1. Obtain a JWT:

    ```bash
    TOKEN=$(curl -s -X POST "https://<LANDSCAPE-HOSTNAME>/api/login" \
      -H "Content-Type: application/json" \
      -d '{"email": "<YOUR-EMAIL>", "password": "<YOUR-PASSWORD>"}' | jq -r '.token')
    ```

2. Include the token in the `Authorization` header of your request.

    ```bash
    curl -X GET "https://<LANDSCAPE-HOSTNAME>/api/?action=GetComputers&version=<VERSION-NUMBER>" \
      -H "Authorization: Bearer $TOKEN"
    ```

> **Note**: The `version` parameter is mandatory in the URL for the legacy API. Without it, the request will fail.

### API key and secret

If you're not using a JWT, you must sign every request using your API key and secret. This is the method used by the `landscape-api` CLI and the Python `landscape_api` module.

Here's an example request:

```text
https://landscape.canonical.com/api/
    ?action=GetComputers&
    access_key_id=0GS7553JW74RRM612K02EXAMPLE&
    signature_method=HmacSHA256&
    signature_version=2&
    timestamp=2011-08-18T08%3A07%3A00Z&
    version=2011-08-01&
    signature=W1TCDh39uBCk9MlaZo941Z8%2BTWqRtdgnbCueBrx%2BtvA%3D
```

> **Note**: All parameters must be URL encoded (for example, `timestamp`). The sections below may show unencoded parameters and omit mandatory arguments for simplicity and readability.

#### Creating an HMAC signature

You need to create an HMAC signature for requests authenticated with the API Key and Secret method. This step isn't necessary if you authenticated with a JWT.

To create the signature:

- Create the canonicalized query string that you need later in this procedure:
- Sort the UTF-8 query string components by parameter name with natural byte ordering. The parameters can come from the GET URI or from the POST body (when `Content-Type` is `application/x-www-form-urlencoded`). URL encode the parameter name and values according to the following rules:
- Do not URL encode any of the unreserved characters that RFC 3986 defines. These unreserved characters are `A-Z`, `a-z`, `0-9`, hyphen (`-`), underscore (`_`), period (`.`), and tilde (`~`).
- Percent encode all other characters with `%XY`, where `X` and `Y` are hex characters `0-9` and uppercase `A-F`.
- Percent encode extended UTF-8 characters in the form `%XY%ZA....`
- Percent encode the space character as `%20` (and not `+`, as common encoding schemes do).
- Separate the encoded parameter names from their encoded values with the equals sign (`=`) (ASCII character `61`), even if the parameter value is empty.
- Separate the name-value pairs with an ampersand (`&`) (ASCII code `38`).
- Create the string to sign according to the following pseudo-grammar (the “`\n`” represents an ASCII newline):

    ```text
    StringToSign = HTTPVerb + "\n" +
                    ValueOfHostHeaderInLowercase + "\n" +
                    HTTPRequestURI + "\n" +
                    CanonicalizedQueryString <from the preceding step>
    ```

- The `HTTPRequestURI` component is the HTTP absolute path component of the URI up to, but not including, the query string. If the `HTTPRequestURI` is empty, use a forward slash (`/`).
- Calculate an RFC 2104-compliant HMAC with the string you just created, your secret key as the key, and SHA256 as the hash algorithm. For more information, go to [http://www.ietf.org/rfc/rfc2104.txt](http://www.ietf.org/rfc/rfc2104.txt).
- Convert the resulting value to base64.
- Use the resulting value as the value of the signature request parameter. Here is an example string to sign:

    ```text
    GET\n
    landscape.canonical.com\n
    /api/\n
    access_key_id=0GS7553JW74RRM612K02EXAMPLE
    &action=GetComputers
    &signature_method=HmacSHA256
    &signature_version=2
    &timestamp=2023-08-18T08%3A07%3A00Z
    &version=2023-08-01
    ```

## Formatting request parameters

These parameter formatting rules apply to the legacy API and are the same whether you authenticate using JWT or HMAC.

### Lists

Some actions take lists of parameters. These lists are specified using the `param.#` notation. Values of `#` are integers starting from 1, and need to be specified even if there is only one value. For example:

```text
action=AddTagsToComputers&tags.1=web&tags.2=server
```

### Files

Some actions take files as parameters. The contents of the file should be base64-encoded, and should be prepended with the filename. Separate the filename and the base64 content with the separator `$$`. For example:

```text
action=CreateScriptAttachment&filename=bucket.txt$$SSBhbSBhIGJ1Y2tldCE=
```
