(reference-rest-api-scripts)=
# Scripts

## GET `/scripts`

Get stored scripts associated with the current account.

Path parameters:

- None

Query parameters:

- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.

Example request:
```bash
curl -X GET   -H "Authorization: Bearer $JWT" "https://landscape.canonical.com/api/v2/scripts"
```

Example output:
```bash
{
  "count": 1,
  "results": [
	{
  	"id": 2,
  	"access_group": "server",
  	"creator": {
    	"name": "John Allen Smith",
    	"email": "john@example.com",
    	"id": 1
  	},
  	"title": "Execute python attachment",
  	"time_limit": 20,
  	"username": "user",
  	"attachments": [
    	"run.py"
  	]
	}
}
```

