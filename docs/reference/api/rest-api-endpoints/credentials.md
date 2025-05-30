(reference-rest-api-credentials)=
# Credentials

## GET `/credentials`

Returns the legacy API credentials for the person logged in for each account.

Required parameters:

- None

Optional parameters:

- None

Example request:
```bash
curl -X GET "https://landscape.canonical.com/api/v2/credentials" -H "Authorization: Bearer $JWT"
```

Example output:
```bash
{
  "credentials": [
    {
      "access_key": "TP64DDDDDDDDWK57C",
      "account_name": "onward",
      "account_title": "Onward, Inc.",
      "endpoint": "https://localhost:9091/api/",
      "exports": "export LANDSCAPE_API_URI='https://landscape.canonical.com/api/'\nexport LANDSCAPE_API_KEY='TP64MXXXXXXXXDWK57C'\nexport LANDSCAPE_API_SECRET='BwpqyAU9999999999999999VZR9QQ0Wdn1jn5P'",
      "secret_key": "BwpqyAU7999999999999y9VZR9QQ0Wdn1jn5P"
    },
    {
      "access_key": "KT1TBBBBBBBBBBB9I2RAB42",
      "account_name": "upside",
      "account_title": "Upside Software, Ltd.",
      "endpoint": "https://localhost:9091/api/",
      "exports": "export LANDSCAPE_API_URI='https://landscape.canonical.com/api/'\nexport LANDSCAPE_API_KEY='KT1TZ5N1NNNNNNN42'\nexport LANDSCAPE_API_SECRET='KG8oo77777777zdhTJqnTX9sK+FMKBNMsXhOOPI'",
      "secret_key": "KG8oo165S77777777777qnTX9sK+FMKBNMsXhOOPI"
    }
  ]
}

```

## POST `/credentials`

Regenerate API credentials.

Required parameters:

- None

Optional parameters:

- None

Example request:
```bash
curl -X POST "https://landscape.canonical.com/api/v2/credentials" -H "Authorization: Bearer $JWT" -d '{"account": "onward"}'
```

Example output:
```bash
{
  "access_key": "DZ6FA1GT9HHHHHHHJA4Q4",
  "account_name": "onward",
  "account_title": "Onward, Inc.",
  "endpoint": "https://localhost:9091/api/",
  "exports": "export LANDSCAPE_API_URI='https://landscape.canonical.com/api/'\nexport LANDSCAPE_API_KEY='DZ6FA1GTTTTTTTTTNYJA4Q4'\nexport LANDSCAPE_API_SECRET='tBXlssS1AuQ/2ZSj3P22222222222222WdHIaX2Vrd'",
  "secret_key": "tBXlssS1AuQ/2ZSj3PdGgI222222222222uwWdHIaX2Vrd"
}

```

