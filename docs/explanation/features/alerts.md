---
myst:
  html_meta:
    description: "Understand alerts in Landscape including different scopes, statuses, and trigger conditions"
---

(explanation-alerts)=
# Alerts

Landscape uses alerts to notify administrators when action is required across their estate. There are two types of alerts: account-scoped and instance-scoped. This document explains how alerts work and the conditions that trigger them.

## Working with alerts

An alert can have three statuses:
- **OK**: No action required
- **Alerted**: Administrator investigation recommended
- **Disabled**: Inactive alert

Resolving the condition triggering an alert will return the alert to the **OK** state.

While alerts are typically actionable, in some cases an administrator may want to dismiss an alert and clear its **Alerted** state. This can be done with the {ref}`REST API <reference-rest-api-alert-dismiss>`.

Instance-scoped alerts can be configured to only be enabled for instances with certain tags, or disabled entirely. Disabled alerts remain inactive until they're re-enabled for a set of instances.

## How to be notified

```{warning}
In self-hosted Landscape, Postfix must be configured for emails to be sent for alerts. See {ref}`how-to-configure-postfix`.
```

Landscape notifies administrators of currently active alerts via email. To receive email notifications, administrators must subscribe to the relevant alert. Similarly, administrators can unsubscribe from alerts that they are not interested in being notified about.

You can manage your subscription status for alerts using the {ref}`legacy API <reference-legacy-subscribe-to-alert>`, the {ref}`classic web portal <how-to-classic-web-portal-alerts>`, or the new web portal under **Account settings** >**Alerts**.

## Available alerts

### Account-scoped alerts

Account-scoped alerts are relevant to the Landscape estate as a whole.

- `PendingComputersAlert` Instances are pending acceptance or rejection
- `LicenseExpiryAlert` A license is approaching expiration
- `UbuntuProContractExpirationAlert` An Ubuntu Pro contract is approaching expiration
  - Available from 25.10 onwards

#### Self-hosted alerts

Certain account-scoped alerts are exclusive to self-hosted Landscape.

- `StandaloneOverflowAlert` License entitlements are exceeded
- `StandaloneScriptAlert` A Landscape cron job fails
- `StandaloneSystemEmailAlert` System email is misconfigured


### Instance-scoped alerts

Instance-scoped alerts are relevant to individual managed instances.

- `PackageUpgradesAlert` Package upgrades are available
- `PackageProfilesAlert` A package profile is not applied
- `SecurityUpgradesAlert` Ssecurity upgrades are available
- `PackageReporterAlert` Package reporting (`apt-get update`) fails
- `EsmDisabledAlert` ESM (Expanded Security Maintenance) updates are disabled
- `UnapprovedActivitiesAlert` Activities require explicit administrator acceptance or rejection
- `ComputerOfflineAlert` An instance has not contacted Landscape within the last five minutes
- `ComputerRebootAlert` An instance needs to be rebooted in order for a package update (such as a kernel update) to take effect
- `ComputerDuplicateAlert` A duplicate instance exists
- `ChildInstanceProfileAlert` An instance is not compliant with a child instance profile
  - Available from 24.10 onwards
