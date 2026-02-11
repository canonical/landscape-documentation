---
myst:
  html_meta:
    description: "REST API endpoints to retrieve and manage Landscape alerts. Monitor computer offline, duplicate, and security alerts for your account."
---

(reference-rest-api-alerts)=
# Alerts

The endpoints available here are for managing alerts for an account.

## GET `/alerts`

Get alerts associated with the account.

Path parameters:

- None

Query parameters:

- None

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/alerts -H "Authorization: Bearer $JWT" 
```

Example response:

```json
[
  {
  "alert_type": "ComputerDuplicateAlert",
  "description": "Alert when a duplicate computer exists",
  "subscribed": true,
  "status": "Alerted",
  "scope": "computer",
  "all_computers": true,
  "tags": [],
  "label": "Computer Duplicate Alert"
  },
  {
  "alert_type": "ComputerOfflineAlert",
  "description": "Alert when computer has not contacted Landscape for some time",
  "subscribed": true,
  "status": "Alerted",
  "scope": "computer",
  "all_computers": true,
  "tags": [],
  "label": "Computer Offline Alert"
  },
]
```

## GET `/alerts/summary`

Get a summary of alerts on the account. This includes the alert types, summaries and most recent activation time.

Path parameters:

- None

Query parameters:

- `include_inactive`: Include inactive alerts

Example request:

```bash
curl -X GET https://landscape.canonical.com/api/v2/alerts/summary -H "Authorization: Bearer $JWT"
```

Example response:

```json
{
  "alerts_summary": [
    {
      "alert_type": "PackageUpgradesAlert",
      "summary": "4 computers have package upgrades available",
      "activation_time": "2024-03-08 20:30:01.801179"
    },
    {
      "alert_type": "SecurityUpgradesAlert",
      "summary": "5 computers have security upgrades available",
      "activation_time": "2024-02-08 00:48:03.313249"
    },
  ]
}
```
