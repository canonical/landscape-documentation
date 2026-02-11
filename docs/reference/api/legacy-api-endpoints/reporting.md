---
myst:
  html_meta:
    description: "API reference for reporting functionality. Legacy API endpoints to generate compliance reports and identify computers without upgrade profiles."
---

(reference-legacy-api-reporting)=
# Reporting

The methods available here give the ability to do reporting on selections of computers.

## GetCSVComplianceData

Get a breakdown of compliance data in CSV format (including a header row).

The method takes one optional argument:

- `query`: A query string used to select the computers you wish to report on. (See `query` under `GetComputers` for additional details.)
- `limit`: The maximum number of results returned by the method. It defaults to 1000.
- `offset`: The offset inside the list of results.
- `max-days`: Return issues newer than max_days.
- `by-cve`: If `by-cve` is false (the default), a key will be added for each USN released in the last `max-days`. The key name will be the identifier of the USN with timestamp, and the value will indicate whether the issue is present and if it is, whether it has been resolved, and when. If `by-cve` is true, CVEs will be used as the column key instead. (true or false)

For example, the following request will query for all machines running Ubuntu 12.04 (Precise):

```text
?action=GetCSVComplianceData&query=distribution:12.04
```

An example output looks like this:

```text
name,is_pinging,schedule,USN 1234-12 (2012-08-19 14:51)
Server 1,False,Every hour at 30 minutes past the hour,Not present
Server 2,False,Every hour at 30 minutes past the hour,Not present
Web,False,Every hour at 30 minutes past the hour,2012-08-20 14:51
DB,False,Every hour at 30 minutes past the hour,Not present
```

## GetComputersNotUpgraded

Get the ids of computers that are not currently covered by an upgrade profile.

This method takes one optional argument:

- `query`: A query string used to select the computers you wish to report on. (See `query` under `GetComputers` for additional details.)

For example, the following request will query for all machines running Ubuntu 12.04 (Precise) that are not covered by an upgrade profile:

```text
?action=GetComputersNotUpgraded&query=distribution:12.04
```

An example output looks like this:

```json
[1, 3, 39, 500]
```

## GetNotPingingComputers

Get the IDs of computers that have not pinged the server for a give number of minutes.

This method takes the following arguments:

- `since_minutes`: An integer number of minutes elapsed in which computers should have pinged the server.
- `query`: A query string used to select the computers you wish to report on. (See `query` under `GetComputers` for additional details.) (optional)

For example, the following request will query for all machines running Ubuntu 12.04 (Precise) that have not pinged in more than 10 minutes:

```text
?action=GetNotPingingComputers&query=distribution:12.04
    &since_minutes=10
```

An example output looks like this:

```json
[44, 343, 5463]
```

## GetUSNTimeToFix

Get a summary of the lengths of time machines waited to be patched after USN releases.

This method takes four optional arguments:

- `query`: A query string used to select the computers you wish to report on. (See `query` under `GetComputers` for additional details.)
- `fixed_in_days`: A list of integer periods of days from a USN release into which we will group machines. The default value is [2, 14, 30].
- `pending_in_days`: The number of days in history to search for USN releases that are pending on the machines. Note, this parameter is independent of the in_last parameter. The default value is 60.
- `in_last`: The number of days in history to search for USN releases to be considered in patch time statistics. The default value is 30.

For example, the following request will query for all machines running Ubuntu 12.04 (Precise):

```text
?action=GetUSNTimeToFix&query=distribution:12.04
```

This example request will return machines fixed in 7,14,21 days:

```text
?action=GetUSNTimeToFix&fixed_in_days.1=7&fixed_in_days.2=14
    &fixed_in_days.3=21
```

This example request will return statistics for unpatched times on USNs released in a window of 50 days prior to today’s date:

```text
?action=GetUSNTimeToFix&in_last=50
```

Example output looks like:

```json
{
    "30": [
        1,
        2,
        3,
        4,
        5,
        6,
        9,
        10,
        11
    ],
    "14": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        9,
        10,
        11
    ],
    "2": [
        1,
        2,
        3,
        4,
        5,
        6,
        9,
        10,
        11
    ],
    "pending": []
}
```

## GetUpgradedComputersByFrequency

Get a summary of the upgrade schedules of computers.

This method takes one optional argument:

- `query`: A query string used to select the computers you wish to report on. (See `query` under `GetComputers` for additional details.)

For example, the following request will query for all machines running Ubuntu 12.04 (Precise):

```text
?action=GetUpgradedComputersByFrequency&query=distribution:12.04
```

Example output looks like:

```json
{
    "Every hour at 30 minutes past the hour": [
        1,
        2,
        3,
        6,
        7,
        8
    ]
}
```
