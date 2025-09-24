(reference-rest-api-license-management)=
# License Management

## POST `/attach-token`

Attach a provided Ubuntu Pro token to the provided computer ids. This will create an activity on each client and place them into the proper license state if the activity succeeds.

Required parameters:

- `computer_ids`: A list of the specified ID(s) as integers for a computer.
- `token`: The Ubuntu Pro token to attach to computers.

Optional parameters:

- None

Example request:

```bash
curl -X POST https://your-landscape-domain.com/api/v2/attach-token -H "Authorization: Bearer $JWT" -d '{"computer_ids": [1, 2], "token": "<ubuntu-pro-token>"}'
```

Example response:
```json
{
    "activity": {
        "activity_status": "queued",
        "approval_time": null,
        "completion_time": null,
        "creation_time": "2025-09-19T14:24:07Z",
        "creator": {
            "email": "john@example.com",
            "id": 1,
            "name": "John Smith"
        },
        "deliver_delay_window": 0,
        "id": 113,
        "parent_id": null,
        "result_code": null,
        "result_text": null,
        "summary": "Attach a pro token to computers",
        "type": "ActivityGroup"
    },
    "invalid_computer_ids": []
}
```

```{note}
"invalid_computer_ids" in the response are for computers that do not accept the proper message type to attach pro (e.g., older client versions) or a computer id that don't exist. This activity is only available for client versions 25.08.3 and newer.
```

## POST `/detach-token`

Detach an Ubuntu Pro subscription from the provided computer ids. This will create an activity on each client and place them into the proper license state if the activity succeeds.

```{note}
This endpoint is feature flagged behind `ubuntu_pro_licensing`.
```

Required parameters:

- `computer_ids`: A list of the specified ID(s) as integers for a computer.

Optional parameters:

- None

Example request:

```bash
curl -X POST https://your-landscape-domain.com/api/v2/attach-token -H "Authorization: Bearer $JWT" -d '{"computer_ids": [1, 2]}'
```

Example response:

```json
{
    "activity": {
        "activity_status": "queued",
        "approval_time": null,
        "completion_time": null,
        "creation_time": "2025-09-19T14:28:32Z",
        "creator": {
            "email": "john@example.com",
            "id": 1,
            "name": "John Smith"
        },
        "deliver_delay_window": 0,
        "id": 116,
        "parent_id": null,
        "result_code": null,
        "result_text": null,
        "summary": "Detach pro token from computers",
        "type": "ActivityGroup"
    },
    "invalid_computer_ids": []
}
```

```{note}
"invalid_computer_ids" in the response are for computers that do not accept the proper message type to attach pro (e.g., older client versions) or a computer id that don't exist. This activity is only available for client versions 25.08.3 and newer.
```

## GET `/legacy-licenses`

Gets all information on legacy licenses associated with an account.

Required parameters:

- None

Optional parameters:

- `available_only`: only include licenses that have open seats.
- `active_only`: only include licenses that are not expired.

Example request:

```bash
curl -X GET https://your-landscape-domain.com/api/v2/legacy-licenses -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
    "results": [
        {
            "available_seats": 12,
            "expiration_date": null,
            "id": 1
        },
        {
            "available_seats": 4,
            "expiration_date": "2026-09-17",
            "id": 8
        },
        {
            "available_seats": 9,
            "expiration_date": "2026-09-17",
            "id": 9
        }
    ]
}
```

## GET `/legacy-licenses/<int:id>`

Gets the specified legacy license information from provided path id.

Required parameters:

- None

Optional parameters:

- None

Path parameters:

- `id`: license id to get information on

Example request:

```bash
curl -X GET https://your-landscape-domain.com/api/v2/legacy-licenses/8 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
    "available_seats": 4,
    "expiration_date": "2026-09-17",
    "id": 8
}
```

## GET `/contracts`

Gets all information on Ubuntu Pro Contracts associated with an account.

Required parameters:

- None

Optional parameters:

- `active_only`: only include licenses that are not expired.

Example request:

```bash
curl -X GET https://your-landscape-domain.com/api/v2/contracts -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
    "results": [
        {
            "contract_id": "contract-id-1",
            "expiration_date": "2025-12-31T00:00:00",
            "id": 1
        },
        {
            "contract_id": "contract-id-2",
            "expiration_date": "2026-12-31T00:00:00",
            "id": 2
        },
        {
            "contract_id": "contract-id-3",
            "expiration_date": "3000-01-01T00:00:00",
            "id": 3
        }
    ]
}
```

## GET `/contracts/<str:id>`

Gets the specified contract information from provided path id.

Required parameters:

- None

Optional parameters:

- None

Path parameters:

- `id`: contract id to get information on

Example request:

```bash
curl -X GET https://your-landscape-domain.com/api/v2/contracts/contract-id-1 -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
    "contract_id": "contract-id-1",
    "expiration_date": "2025-12-31T00:00:00",
    "id": 1
}
```