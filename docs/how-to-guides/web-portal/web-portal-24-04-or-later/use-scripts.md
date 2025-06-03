(how-to-web-portal-use-scripts)=
# How to use scripts

Scripts can be used to execute code on instances.

> **Note**: This feature, in the state described below, is only available in **Landscape 25.04** and later.

## Creating a script

From the web portal:

1. Go to **Scripts**.
3. Click on **Add script**.

In the script creation form, fill out the following fields:

- **Title**: Title of the script.
- **Code**: Script code intended to run on instances.
- **Access group**: The access group the script will belong to.
- **Attachments**: A list of attachments that may be used inside the script, and submitted to instances.

## Managing a script profile

You can manage a script using the **Actions** menu:

- **Edit**: Modify the title, code, or attachments.
  Note that modifying the code creates a new version of the script.
- **Archive**: Archive the script, making it inactive.
  This operation also archives any associated script profile(s).
  Note that archiving is irreversible.
- **Delete**: Delete the script by redacting every version of the script, and deleting associated attachments.
  This operation also archives any associated script profile(s).
  Note that deletion is irreversible.
