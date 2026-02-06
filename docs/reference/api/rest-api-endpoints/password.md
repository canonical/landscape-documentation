(reference-rest-api-password)=
# Password

## PUT `/password`

Apply a new password.

Path parameters:

- None

Required parameters:

- `password`: The current password.
- `new_password`: The new password with a minimum length of 3 and maximum length of 30.

Optional parameters:

- None

Example request:

```bash
curl -X PUT "https://landscape.canonical.com/api/v2/password" -d '{"password": "pwd", "new_password": "more_secure_pwd"}' -H Authorization:"Bearer $JWT"
```
