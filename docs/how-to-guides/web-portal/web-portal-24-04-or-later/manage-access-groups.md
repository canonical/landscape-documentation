(how-to-web-portal-manage-access-groups)=
# How to manage access groups

> See also: [Access groups](/reference/terms/access-groups)

These guides describe how to manage access groups.

## Create access groups

To create a new access group:

1. Click **Org. settings** > **Access groups** from the sidebar
2. Click **Add access group**
3. Enter a title and parent access group
4. Click **Add**

When you create a new access group, you must provide a title for the access group and a parent. The title can be whatever you want to name this new access group. The parent must be the global access group or an access group that is a child of global. If you want a flat management hierarchy, you can make every access group a child of global. Alternatively, you can use parent/child relationships to create a hierarchy of access groups. For example, you could specify different sites at a high level, and under them individual buildings, and finally individual departments. Such a hierarchy allows you to specify groups of computers to be managed together by one administrator. Administrators whose roles are associated with higher-level access groups can manage all subgroups of which their access group is a parent.

When a new access group is first created, its administrators are those who have roles linked to its parent access group, but you can edit the roles associated with an access group. For more information, see the section on how to associate roles with access groups later in this guide.

## Delete access groups

To delete an existing access group:

1. Click **Org. settings** > **Access groups** from the sidebar
2. Click the name of the access group you want to edit
3. Click the trash can icon in the row of the access group you want to delete. You will be asked to confirm this operation.
4. Click **Delete** to confirm deleting the group

When you delete an access group, its resources move to its parent access group.

## Add instances to access groups

You can add instances individually to access groups. To do this:

1. Click **Instances** from the side bar
2. Click the instance you want to add to an access group
3. Click **Edit**
4. Select the access group you want from the dropdown menu
5. Click **Save changes**

## Associate roles with access groups

To associate a role with one or more access groups:

1. Click **Org. settings** > **Roles** from the sidebar
2. Click the pencil icon in the row of the role you want to edit
3. Select the checkbox next to the access group(s) you want to associate the role with
4. Click **Save changes**

Note that you cannot modify the GlobalAdmin role. If you attempt to edit this role, you’ll get the following error: “The role 'GlobalAdmin' is read-only”.

