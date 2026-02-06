(reference-rest-api-login)=
# Login

## POST `/login`

Login to the REST API with a email address and password.

Required parameters:

- `email`
- `password`

Optional parameters:

- `account`

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/login" -d '{"email": "john@example.com", "password": "pwd", "account": "onward"}'
```

Example response:

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJleHAiOjE3MTExNDYwNjIsEmlhdCI6MTcxYTA1OTYMiwic3ViIjoiam9obkBleGFtcGxlLmNvbSIsImFjYyI6Im9ud8FyZCIsImlkIjoxfQHtqIW_j4ICm43zN3LAsFMDpR9WpxuMBCqWiZe0_R6Vk",
  "email": "jane@example.com",
  "name": "Jane Smith",
  "accounts": [
    {
      "title": "Onward, Inc.",
      "name": "onward",
      "default": true
    },
    {
      "title": "Upside Software, Ltd.",
      "name": "upside"
    }
  ],
  "current_account": "onward"
}
```

## POST `/login/access-key`

Landscape version: 24.10 and later

Authenticates an SSO user, returning user details and an authentication token.

Required parameters:

- `access_key` (string): The access key provided by the user.
- `secret_key` (string): The secret key associated with the access key.

Optional parameters:

- `expiry_minutes` (integer): The duration (in minutes) for which the authentication token will be valid. If not provided, the token will have a default expiry time of 1440 minutes (24 hours).

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/login/access-key" \
-H "Content-Type: application/json" \
-d '{"access_key": "3AS5YX98J8QI9AZ8OS0V", "secret_key": "avlhg23w9HyOWOA1FMzHmrBaB8a97zafzJOApfF2"}'
```

Example response:

```json
{
    "accounts": [
        {
            "default": true,
            "name": "onward",
            "title": "Onward, Inc."
        },
        {
            "default": false,
            "name": "upside",
            "title": "Upside Software, Ltd."
        }
    ],
    "current_account": "onward",
    "email": "john@example.com",
    "name": "John Smith",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjUwMzkyNzYsImlhdCI6MTcyNDk1Mjg3Niwic3ViIjoiam9obkBleGFtcGxlLmNvbSIsImFjYyI6Im9ud2FyZCIsImlkIjoxfQ.8rWW_GN1jRzKownpg4k1Zp4iZMmn_lfLjy0cX-DLh_g"
}
```
