---
myst:
  html_meta:
    description: "Description I haven't written yet"
---

(explanation-alerts)=
# Alerts

Placeholder

## Types of alerts

### Account-based alerts

Account-based alerts are relevant to the Landscape estate as a whole.

- `PendingComputersAlert` alerts when instances are pending acceptance or rejection
- `LicenseExpiryAlert` alerts when a license is approaching expiration
- `UbuntuProContractExpirationAlert` alerts when an Ubuntu Pro contract is approaching expiration
  - Available from 25.10 onwards

#### Self-hosted alerts

```{warning}
In self-hosted Landscape, Postfix must be configured for emails to be sent on alerts. See {ref}`how-to-configure-postfix`.
```

Certain account-based alerts are exclusive to self-hosted landscape.

- `StandaloneOverflowAlert` alerts when license entitlements are exceeded
- `StandaloneScriptAlert` alerts when a Landscape cron job fails
- `StandaloneSystemEmailAlert` alerts when system email is misconfigured


### Instance-based alerts

Instance-based alerts are scoped to individually managed instances.

- `PackageUpgradesAlert` alerts when package upgrades are available
- `PackageProfilesAlert` alerts when a package profile is not applied
- `SecurityUpgradesAlert` alerts when security upgrades are available
- `PackageReporterAlert` alerts when package reporting (`apt-get update`) fails
- `EsmDisabledAlert` alerts when ESM (Expanded Security Maintenance) updates are disabled
- `UnapprovedActivitiesAlert` alerts when activities require explicit administrator acceptance or rejection
- `ComputerOfflineAlert` alerts when an instance has not contacted Landscape within the last five minutes
- `ComputerRebootAlert` alerts when an instance needs to be rebooted in order for a package update (such as a kernel update) to take effect
- `ComputerDuplicateAlert` alerts when a duplicate instance exists
- `ChildInstanceProfileAlert` alerts when an instance is not compliant with a child instance profile
  - Available from 24.10 onwards
