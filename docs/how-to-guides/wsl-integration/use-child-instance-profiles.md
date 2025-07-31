(how-to-use-child-instance-profiles)=

# How to use child instance profiles

```{note}
This feature is currently in beta.
```

> See also: {ref}`reference-rest-api-wsl`.

This guide describes how to use child instance profiles to provision WSL instances and manage them with Landscape.

## Create a child instance profile

You can add Windows host machines to the profile by assigning tags or by associating to all computers.

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles -H "Authorization: Bearer $JWT" -d '{"title": "JammyProfile", "description": "Jammy", "image_name": "Ubuntu-22.04", "all_computers": "true"}'
```

## Apply a child instance profile

This will create activities to provision WSL instances on every associated Windows host machine.

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles/JammyProfile:reapply -H "Authorization: Bearer $JWT"'
```

## Apply all child instance profiles by Windows host machine

This will create activities to provision WSL instances on specified Windows host machines for all associated child instance profiles.

```bash
curl -X POST https://your-landscape.domain.com/api/v2/child-instance-profiles/make-hosts-compliant -H "Authorization: Bearer $JWT" -d '{"host_computer_ids": [6, 15]}'
```
