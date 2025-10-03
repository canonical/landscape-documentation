(how-to-remove-duplicate-instances)=
# How to remove duplicate instances

Duplicate registrations of instances can sometimes happen in Landscape when clients have issues communicating with the Landscape server, or if the `lanscape-config` command is used multiple times. In some cases, these issues result in those client instances sending a new registration request, which can result in a clone or duplicate instance if those requests are accepted.

This guide describes how to remove duplicate instances.

## Option #1: Manual removal in the web portal

If you have any duplicate client instances, you can manually remove them one-by-one in the web portal. 

### Web portal (24.04 LTS and later)

Duplicate instances will appear on the home page dashboard. To remove the duplicate, click the instances in the *Duplicate* tile, select your instance, and remove it from Landscape (**More actions** > **Remove from Landscape**).

### Classic web portal

If you have any duplicate instances, you'll see them as an alert, "\<n\> computers have duplicates". To remove the duplicate, click this alert, select your computer, and remove it from Landscape.

## Option #2: Automated removal with removal profiles

You can use a removal profile to automatically remove instances that haven't contacted the Landscape server after a set amount of time (days). Instances with a duplicate registration have their pings associated with their most recent registration, so the old registration will appear offline and can be automatically removed by the removal profile.

You can create and manage your removal profiles in **Profiles** > **Removal profiles**. Once you've created the profile, the duplicate registrations in the given access group will be removed after the provided number of days, 

## Option #3: Automated removal with the API

```{note}
These endpoints are only available in the **legacy** API at this time.
```

You can use the Landscape legacy API {ref}`reference-legacy-api-computers` endpoints to automate removing duplicate registration requests. Using the API, you can create a script to get a list of computers (instances), identify duplicates (same hostname but different registration dates or last ping time), and remove these duplicate computers.
