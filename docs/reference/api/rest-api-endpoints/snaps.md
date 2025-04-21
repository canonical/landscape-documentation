(reference-rest-api-snaps)=
# Snaps

## POST `/snaps`

Perform actions on snaps by computer IDs.

Required parameters:

- `action`: The action to perform for the provided snaps.
- `computer_ids`: The numerical IDs of the computers.
- `snaps`: An array of snaps to perform the action(s) on.

Optional parameters:

- `deliver_after`
- `deliver_after_window`

Example request:
```bash
curl -X POST   -H "Authorization: Bearer $JWT"   -d '{
	"action": "install",
	"computer_ids": [23],
	"snaps": [
    	{"name": "hello"},
    	{"name": "spotify"}
	]
  }'   https://landscape.canonical.com/api/v2/snaps
```

Example output:
```bash
{
  "id": 214,
  "creation_time": "2024-04-10T23:29:25Z",
  "creator": {
	"name": "John Allen Smith",
	"email": "john@example.com",
	"id": 1
  },
  "type": "ActivityGroup",
  "summary": "Install snaps on computer",
  "completion_time": null,
  "parent_id": null,
  "deliver_delay_window": 0,
  "result_text": null,
  "result_code": null,
  "activity_status": "undelivered"
}
```

