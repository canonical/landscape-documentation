(how-to-guides-web-portal-classic-web-portal-manage-access-groups)=
# How to manage access groups

> See also: [Access groups](/explanation/terms/access-groups)

This document describes how to manage access groups.

## Create access groups

To create a new access group:

1. Navigate to your organization's home page
2. Click the **Access groups** tab
3. Enter the requested information
4. Click **Save**.

When you create a new access group, you must provide a title for the access group and a parent. The title can be whatever you want to name this new access group. The parent must be the global access group or an access group that is a child of global. If you want a flat management hierarchy, you can make every access group a child of global. Alternatively, you can use parent/child relationships to create a hierarchy of access groups. For instance, you could specify different sites at a high level, and under them individual buildings, and finally individual departments. Such a hierarchy allows you to specify groups of computers to be managed together by one administrator. Administrators whose roles are associated with higher-level access groups can manage all subgroups of which their access group is a parent.

When a new access group is first created, its administrators are those who have roles linked to its parent access group, but you can edit the roles associated with an access group. For more information, see [how to associate roles with access groups](#associate-roles-with-access-groups) in this guide.

## Edit access groups

To change the name or title of an existing access group:

1. Navigate to your organization's home page
2. Click the **Access groups** tab
3. Click the name of the access group you want to edit
4. Click **Edit access group**
5. Make your changes
6. Click **Save**

## Delete access groups

To delete an existing access group:

1. Navigate to your organization's home page
2. Click the **Access groups** tab
3. Click the name of the access group you want to delete
4. Click **Edit access group**
5. Click **Delete** 
   - You will be asked to confirm this operation.
6. Click **Confirm** to confirm the group's deletion

When you delete an access group, its resources move to its parent access group.

## View existing computers in an access group

To view existing computers in an access group:

1. Navigate to your organization's home page
2. Click the **Access groups** tab
3. Click the name of the access group you want to view
4. Click the link in the text *There is [number] computers in this access group* on the right side of the screen

Or, you can view existing computers directly from the **Computers** page in the header by using the search bar:

1. Navigate to the **Computers** page in the header
2. Enter `access-group` followed by a `:` (colon) and the name of your access group
   - E.g., `access-group:global`

## Add computers to access groups

To add computers to in an access group:

1. Navigate to your organization's home page
2. Click the **Access groups** tab
3. Click the name of the access group you want to add computers to
4. Click **selecting computers** from the text on the right side of the screen
5. Select the checkbox next to each computer you want to add
6. Click the **Info** tab
7. Scroll to the **Access group** section at the bottom of the page
8. Select the access group you want from the dropdown menu
9. Click **Update access group**

You can also add computers to access groups directly from the **Computers** page in the header by using the search bar:

1. Navigate to the **Computers** page in the header
2. Enter `access-group` followed by a `:` (colon) and the name of your access group
   - E.g., `access-group:global`
3. Select the checkbox next to each computer you want to add
4. Click the **Info** tab
5. Scroll to the **Access group** section at the bottom of the page
6. Select the access group you want from the dropdown menu
7. Click **Update access group**

## Associate roles with access groups

To associate a role with one or more access groups:

1. Navigate to your organization's home page
2. Click the **Roles** tab
3. Click the name of the role that you want to edit
4. Select the checkbox next to the access group you want to associate the role with on the right side of the screen
5. Click **Save**

Note that you cannot modify the GlobalAdmin role, so there is no link associated with that label.

