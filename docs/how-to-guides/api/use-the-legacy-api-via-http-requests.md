(how-to-use-legacy-api-http)=
# How to use the legacy API via HTTP requests


## Making a request

API requests are HTTPS requests that use the HTTP verb GET or POST and a query parameter named action. To be able to make a request, you’ll need to know which endpoint to use, what the action is, and what parameters it takes.

All methods take a list of mandatory arguments which you need to pass every time (unless using JWT authentication, where only `action` and `version` are required):

- `action`: The name of the method you want to call
- `access_key_id`: The access key given to you in the Landscape Web UI. You need to go to your settings section in Landscape to be able to generate it along with the secret key.
- `signature_method`: The method used to signed the request, always HmacSHA256 for now.
- `signature_version`: The version of the signature mechanism, always 2 for now.
- `timestamp`: The time in UTC in ISO 8601 format, used to indicate the validity of the signature.
- `version`: The version of the API, 2011-08-01 being the current one. It’s in the form of a date.

## Authentication

You can authenticate your requests using either an API Key/Secret (HMAC signature) or a JSON Web Token (JWT).

### Using a JWT

If you use a JWT, you do not need to sign your requests or provide the `access_key_id`, `signature_method`, `signature_version`, or `timestamp` parameters.

Example:

1.  Obtain a JWT:

    ```bash
    TOKEN=$(curl -s -X POST "https://<LANDSCAPE-HOSTNAME>/api/v2/login" \
      -H "Content-Type: application/json" \
      -d '{"email": "<YOUR-EMAIL>", "password": "<YOUR-PASSWORD>"}' | jq -r '.token')
    ```
2.  Include the token in the `Authorization` header of your request.
    ```bash
    curl -X GET "https://<LANDSCAPE-HOSTNAME>/api/?action=GetComputers&version=<VERSION-NUMBER>" \
      -H "Authorization: Bearer <YOUR_TOKEN>"
    ```
> **Note**: The `version` parameter is mandatory in the URL for the legacy API. Without it, the request will fail.

### Using API Key and Secret (HMAC Signature)

If you are not using a JWT, you must sign every request.

Here’s an example request:

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

Note that all the parameters must be URL encoded (like timestamp here). It may be skipped in the documentation to make it easier to read. The mandatory arguments will be skipped too for simplicity.

## Creating a signature

To create the signature:

- Create the canonicalized query string that you need later in this procedure:
- Sort the UTF-8 query string components by parameter name with natural byte ordering. The parameters can come from the GET URI or from the POST body (when Content-Type is application/x-www-form-urlencoded). URL encode the parameter name and values according to the following rules:
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
- The HTTPRequestURI component is the HTTP absolute path component of the URI up to, but not including, the query string. If the HTTPRequestURI is empty, use a forward slash (`/`).
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

## Passing list of values

Some actions takes list of parameters. These lists are specified using the param.# notation. Values of # are integers starting from 1, and need to be specified even if there is only one value. For example:

```text
action=AddTagsToComputers&tags.1=web&tags.2=server
```

## Passing files

Some actions take files as parameters. The contents of the file should be base64-encoded, and should be prepended with the filename. Since base64 cannot generate it “$$” is used as a separator. For example:

```text
action=CreateScriptAttachment&filename=bucket.txt$$SSBhbSBhIGJ1Y2tldCE=
```

