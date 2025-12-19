(reference-rest-api-users)=
# Users

## DELETE `/users`

Deletes users by their computer IDs and usernames.

Required query parameters:

- `computer_ids`: The numerical IDs of the computers.
- `username`: The usernames of the users to delete.

Optional query parameters:

- `delete_home`: The user's home directory will also be deleted.

Example request:

```bash
curl -X DELETE   -H "Authorization: Bearer $JWT" "landscape.canonical.com/api/users?computer_ids=1&usernames=john"
```

Example response:

```json
{
  "activity_status": "undelivered",
  "completion_time": null,
  "creation_time": "2024-04-11T15:50:26Z",
  "creator": {
      "email": "john@example.com",
      "id": 1,
      "name": "John Allen Smith"
  },
  "deliver_delay_window": 0,
  "id": 218,
  "parent_id": null,
  "result_code": null,
  "result_text": null,
  "summary": "Delete user john (UID 1000)",
  "type": "ActivityGroup"
}
```

## GET `/users`

Get user information from the specified computer.

Path parameters:

- `computer_id`: The numerical ID of the computer

Query parameters:

- None

Example request:

```bash
curl -X GET   -H "Authorization: Bearer $JWT" "landscape.canonical.com/api/users?computer_id=23"
```

Example response:

```json
{
  "count": 2,
  "results": [
  {
    "enabled": true,
    "home_phone": null,
    "location": null,
    "name": null,
    "primary_gid": 65534,
    "uid": 105,
    "username": "_apt",
    "work_phone": null
  },
  {
    "enabled": true,
    "home_phone": null,
    "location": null,
    "name": "backup",
    "primary_gid": 34,
    "uid": 34,
    "username": "backup",
    "work_phone": null
  }
}
```

## POST `/users`

Create an activity to create a user on the specified computers.

Required parameters:

- `computer_ids`: he numerical IDs of the computers.
- `username`: The username of the new user.
- `name`: The title name of the new user.
- `password`: The password of the new user.

Optional parameters:

- `require_password_reset`: Requires the user to reset their password on first login.
- `primary_groupname`: The group the new user will be assigned to.
- `location`: The location of the new user.
- `home_phone`: The home phone number of the new user.
- `work_phone`: The work phone number of the new user.

## PUT `/users`

Create an activity to edit information of a user on the specified computers.

Required parameters:

- `computer_ids`: The numerical IDs of the computers.
- `username`: The username of an existing user.

Optional parameters:

- `name`: The new title name of the existing user.
- `password`: The new password for the existing user.
- `primary_groupname`: The new group the existing user will be assigned to.
- `location`: location of the existing user.
- `home_phone`: The home phone number of the existing user.
- `work_phone`: The work phone number of the existing user.

## POST `/users/lock`

Create an activity to apply an operation (lock) to users on the specified computers.

Required parameters:

- `computer_ids`: The numerical IDs of the computers.
- `usernames`: The usernames of the users to apply.

Optional parameters:

- None

Example request:

```bash
curl -X POST \
  -H "Authorization: Bearer $JWT" \
  -d '{
  "computer_ids": [1],
  "usernames": ["john"]
  }' \
  https://landscape.canonical.com/api/v2/users/lock
```

Example response:

```json
{
  "id": 226,
  "creation_time": "2024-04-11T15:56:29Z",
  "creator": {
    "name": "John Allen Smith",
    "email": "john@example.com",
    "id": 1
  },
  "type": "ActivityGroup",
  "summary": "Lock out user john (UID 1000)",
  "completion_time": null,
  "parent_id": null,
  "deliver_delay_window": 0,
  "result_text": null,
  "result_code": null,
  "activity_status": "undelivered"
}
```

## POST `/users/unlock`

Create an activity to apply an operation (unlock) to users on the specified computers.

Required parameters:

- `computer_ids`: The numerical IDs of the computers.
- `usernames`: The usernames of the users to apply.

Optional parameters:

- None

Example request:

```bash
curl -X POST   -H "Authorization: Bearer $JWT"   -d '{
  "computer_ids": [1],
  "usernames": ["john"]
  }'   https://landscape.canonical.com/api/v2/users/unlock
```


Example response:
```json
{
  "id": 228,
  "creation_time": "2024-04-11T15:58:15Z",
  "creator": {
    "name": "John Allen Smith",
    "email": "john@example.com",
    "id": 1
  },
  "type": "ActivityGroup",
  "summary": "Unlock user john (UID 1000)",
  "completion_time": null,
  "parent_id": null,
  "deliver_delay_window": 0,
  "result_text": null,
  "result_code": null,
  "activity_status": "undelivered"
}
```
