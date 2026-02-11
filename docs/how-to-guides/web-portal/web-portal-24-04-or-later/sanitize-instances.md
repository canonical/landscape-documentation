---
myst:
  html_meta:
    description: "Permanently delete LUKS encryption keys on instances using Landscape's 24.04+ portal, making encrypted data unrecoverable."
---

(how-to-web-portal-sanitize-computers)=
# How to sanitize instances

You can sanitize instances in Landscape. This action permanently deletes the encryption keys for all LUKS encrypted volumes on that instance, making data on those volumes unrecoverable.

To do this from the web portal:

1. Go to **Instances**
1. Select your instance
1. In the **Info** tab, click **Sanitize**
1. Follow the instructions in the prompt, then click **Sanitize**

This creates an activity to send the sanitize script and shutdown the instance after a delay.

The sanitize script erases the key slots for each LUKS encrypted volume on the instance.

**Note:** **Make sure you're sanitizing the correct computer. This action is irreversible once the activity is delivered.**
