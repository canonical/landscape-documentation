(how-to-web-portal-sanitize-computers)=
# How to sanitize instances

You can sanitize instances in Landscape. This permanently deletes the encryption key for that instance, making its data unrecoverable.

To do this from the web portal:

1. Go to **Instances** 
1. Select your instance
1. In the **Info** tab, click **Sanitize**
1. Follow the instructions in the prompt, then click **Sanitize**

This creates an activity to send the sanitize script and shutdown the instance after a delay.

The sanitize script erases the key slots of each encrypted volume on the instance.

**Note:** **Please make sure you're sanitizing the correct computer. This action is irreversible once the activity is delivered.**
