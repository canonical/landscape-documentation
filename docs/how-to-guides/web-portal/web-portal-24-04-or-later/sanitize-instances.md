(how-to-guides-web-portal-web-portal-24-04-or-later-sanitize-computers)=
# How to sanitize instances from the Landscape web portal

You can sanitize instances from the **Info** tab. To access this tab, go to **Instances** > Select your instance.

You can sanitize an instance with **Sanitize**.

It will prompt you to enter `"sanitize <instance title>"` before sanitizing. This will create an activity to send the sanitize script and shutdown the instance after a delay.

The sanitize script erases the keyslots of each encrypted volume on the instance.

**Note:** **Please make sure you are sanitizing the correct computer. This action is irreversible once the activity is delivered.**
