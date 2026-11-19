---
myst:
  html_meta:
    description: "REST API endpoints for authentication and login to Landscape. Obtain JWT tokens using email and password for API access."
---

(reference-rest-api-login)=
# Login

## POST `/login`

Login to the REST API with an email address and password.

Required parameters:

- `email`
- `password`

Optional parameters:

- `account`

Example request:

```bash
curl -X POST "https://landscape.canonical.com/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "pwd", "account": "onward"}'
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
