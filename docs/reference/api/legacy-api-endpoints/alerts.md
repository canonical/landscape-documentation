(reference-legacy-api-alerts)=
# Alerts

Methods for retrieving or editing alerts for an account.

## AlertTagAssociationMethod

A common superclass for alert tag association/disassociation methods.

## AssociateAlert

Associate an alert to computers with specific tags or to all computers.

- `name`: Name of alert type.
- `tags.#`: List of tag names to associate to the alert.
- `all_computers`: true if the alert should be associated to all computers. This parameter is optional and defaults to false. Individual tags associated to the alert will remain, but they will only be effective if the `all_computers` flag is later disabled.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request that associates the alert `ComputerOfflineAlert` with the tags `desktop` and `laptop`:

```text
?action=AssociateAlert&name=ComputerOfflineAlert
    &tags.1=desktop
    &tags.2=laptop
    &all_computers=false
```

The following errors may be raised:

- `UnknownAlertTypeError`: No alert with the specified name exists.
- `InvalidAlertTypeError`: Raised when trying to associate tags with an alert with account scope instead of computer scope.
- `InvalidParameterCombination`: Some tags were specified and a `true` value for `all_computers` was passed.

The state of the alert will be returned.

## DisassociateAlert

Disassociate an alert from computers with specified tags or from all computers.

If all_computers=true, the alert will be unflagged as applying to all computers, but will still be enabled for computers which have specific tags associated with it.

- `name`: Name of the alert type.
- `tags.#`: List of tag names to disassociate from the alert.
- `all_computers`: If true, the alert will only remain enabled for computers with tags associated to the alert. This parameter is optional and defaults to false.

`tags.#` and `all_computers=true` are mutually exclusive.

Example of a valid request:

```text
?action=DisassociateAlert&name=ComputerOfflineAlert
    &tags.1=desktop&tags.2=laptop
```

The following errors may be raised:

- `UnknownAlertTypeError`: No alert with the specified name exists.
- `UnknownTag`: No tag with the specified name exists.
- `InvalidParameterCombination`: Some tags were specified and a ‘true’ value for ‘all_computers’ was passed.
- `InvalidAlertTypeError`: Raised when trying to disassociate tags with an alert with account scope instead of computer scope.

The state of the alert will be returned.

## GetAlertSubscribers

Get a list of the subscribers to a given alert type.

- `alert_type`: The name of the alert whose subscribers should be listed. Valid names can be seen by calling the `GetAlerts` method.

Example of a valid request:

```text
?action=GetAlertSubscribers&alert_type=ComputerOfflineAlert
```

The method returns a JSON serialized list of the alert subscribers:

```json
[{u'email': u'person1@example.com',
  u'name': u'Person',
  u'id': 1},
 {u'email': u'person2@example.com',
  u'name': u'Person',
  u'id': 2}]
```

The JSON equivalent of this output is:

```json
[
    {
        "email": "person1@example.com",
        "name": "Person",
        "id": 1
    },
    {
        "email": "person2@example.com",
        "name": "Person",
        "id": 2
    }
]
```

The following errors may be raised:

- `UnknownAlertTypeError`: If an unknown `alert_type` is passed.

## GetAlerts

Get a list of the alerts on the account and computers.

Example of a valid request:

```text
?action=GetAlerts
```

The method returns a JSON serialized list of the alerts:

```text
[{u'alert_type': u'PackageReporterAlert',
  u'all_computers': True,
  u'description': u'Alert when package reporting fails',
  u'scope': u'computer',
  u'status': u'OK',
  u'subscribed': u'Yes',
  u'tags': [u'file-server',
            u'web-server',
            u'desktop',
            u'laptop']},]
```

The JSON equivalent of this output is:

```json
[
    {
        "alert_type": "PackageReporterAlert",
        "all_computers": true,
        "description": "Alert when package reporting fails",
        "scope": "computer",
        "status": "OK",
        "subscribed": "Yes",
        "tags": [
            "file-server",
            "web-server",
            "desktop",
            "laptop"
        ]
    }
]
```

## SubscribeToAlert

Subscribe your user account to a given alert types notifications.

- `alert_type`: The name of the alert type you wish to subscribe to. Valid names can be seen by calling the `GetAlerts` method.

Example of a valid request:

```text
?action=SubscribeToAlert&alert_type=ComputerOfflineAlert
```

The following errors may be raised:

- `UnknownAlertTypeError`: If an unknown `alert_type` is passed.

## UnsubscribeFromAlert

Unsubscribe your user account from a given alert types notifications.

- `alert_type`: The name of the alert type from which you wish to remove your subscription. Valid names can be seen by calling the `GetAlerts` method.

Example of a valid request:

```text
?action=UnsubscribeFromAlert&alert_type=ComputerOfflineAlert
```

The following errors may be raised:

- `UnknownAlertTypeError`: If an unknown `alert_type` is passed.
