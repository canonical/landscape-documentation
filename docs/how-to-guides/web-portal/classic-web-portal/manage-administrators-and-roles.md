---
myst:
  html_meta:
    description: "Invite and disable administrators, create roles, and manage access permissions in Landscape's classic web portal."
---

(how-to-classic-web-portal-manage-admins-and-roles)=
# How to manage administrators and roles

> See also: {ref}`reference-terms-administrators`

```{note}
You must be an administrator to perform these tasks.
```

This document describes how to manage additional administrators and roles.

## Invite administrators

You can make someone an administrator by sending them an invitation via email. To invite an administrator:

1. Navigate to your organization's home page
2. Click the **Administrators** tab
3. Enter the requested information
4. Click **Invite**

The invitation will send from the email address you specified during Landscape setup. The options available in the **Roles** section are the same roles defined in the **Roles** tab.

Users who receive an invitation will see an HTML link in the email. Clicking this link takes them to a page where they're asked to log in to Landscape or create an Ubuntu Single Sign-on account. Once they do, they gain the administrator privileges associated with the role to which they've been assigned.

The first person to click on the link and submit information becomes an administrator, even if it's not the person with the name and email address to which you sent the invitation. Take care to keep track of the status of administrator invitations.

## Disable administrators

To disable one or more administrators:

1. Navigate to your organization's home page
2. Click the **Administrators** tab
3. Select the checkboxes next to the administrator(s) you want to disable
4. Click **Disable**

The administrator is permanently disabled and will no longer be in Landscape. Although this operation cannot be reversed, you can send another administrator invitation to the same email address.

## Create roles

To add a role:

1. Navigate to your organization's home page
2. Click the **Roles** tab
3. Click **Add role**
4. Enter the requested information
5. Click **Save**

When you add a role, you also specify a set of one or more access groups to which the role applies, and what permissions you want the role to have.

By specifying different permission levels and different access groups, you can create roles and associate them with administrators to get a granular level of control over sets of computers.
