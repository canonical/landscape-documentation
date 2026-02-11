---
myst:
  html_meta:
    description: "Understand how AppArmor security system integrates with Landscape Client snap and provides application-level access controls for Ubuntu."
---

(explanation-apparmor)=
# AppArmor and Landscape

[AppArmor](https://apparmor.net/) is a security system for Linux applications that allows you to set fine-grained access controls on a per-application basis. In Ubuntu, AppArmor is installed by default.

AppArmor itself doesn’t directly impact your Landscape deployment, unless you’re using the Landscape Client snap.

## Landscape Client snap and AppArmor

When Landscape Client is deployed as a snap, it is confined by the snap ecosystem’s standard security policies, which includes AppArmor. You can read more about how AppArmor relates to snap security in Snapcraft’s [security policies](https://snapcraft.io/docs/security-policies) and [snap system architecture](https://snapcraft.io/docs/system-architecture) documentation.

The Landscape Client snap’s AppArmor policy is generated automatically by snapd, and Landscape users won’t generally need to interact with AppArmor directly.
