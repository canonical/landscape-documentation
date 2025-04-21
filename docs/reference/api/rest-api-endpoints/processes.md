(reference-rest-api-processes)=
# Processes

## POST `/processes/<signal>`

Kill or terminate a process.

Required parameters:

- `signal`: Either "kill" or "terminate"
- `computer_id`: The numerical ID of the computer.
- `pids`: A comma-separated list with the PIDs of the processes to send the signal.

Optional parameters:

- None

Example request:
```bash
curl -X POST \
  -H "Authorization: Bearer $JWT" \
  -d '{
	"computer_id": 1,
	"pids": [1]
  }' \
  https://landscape.canonical.com/api/v2/processes/kill

```

Example output:
```bash
{
  "id": 204,
  "creation_time": "2024-04-10T23:13:38Z",
  "creator": {
	"name": "John Allen Smith",
	"email": "john@example.com",
	"id": 1
  },
  "type": "ActivityGroup",
  "summary": "Signal process init (PID 1) with KILL",
  "completion_time": null,
  "parent_id": null,
  "deliver_delay_window": 0,
  "result_text": null,
  "result_code": null,
  "activity_status": "undelivered"
}
```

