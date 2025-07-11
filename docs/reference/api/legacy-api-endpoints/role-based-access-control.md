(reference-legacy-api-role-based-access-control)=
# Role Based Access Control


Methods for managing role based access control (RBAC) within Landscape.

Central to RBAC is the concept of a role. Roles can have permissions, access groups and administrators associated with them.

## AddAccessGroupsToRole

Add the given access groups to a role.

Arguments:

- `name`: The name of the role to modify.
- `access_groups`: A list of names of access groups to add.

The following errors may be raised:

- `UnknownRole`: No role with the specified name was found.
- `UnknownAccessGroups`: One or more of the given access groups are unknown.
- `ReadOnlyRoleError`: The role’s access groups are read-only.

For example, the following request adds the access group ‘my-group’ to the role named ‘MyRole’. Any person with this role granted will inherit ‘my-group’ permissions:

```text
?action=AddAccessGroupsToRole&name=MyRole
&access_groups.1=my-group
```

The method returns a JSON serialized representation of the edited role:

```text
{
    "key": 1012,
    "name": "MyRole",
    "description": "",
    "permissions": [],
    "persons": [],
    "access_groups": [
        "my-group"
    ]
}
```

## AddPermissionsToRole

Add permissions to a role.

Arguments:

- `name`: The name of the role to modify.
- `permissions`: A list of permissions to add.

The following errors may be raised:

- `UnknownRole`: No role with the specified name was found.
- `InvalidPermissions`: One or more of the given permissions are invalid.
- `ReadOnlyRole`: The specified role can’t be modified.

For example, the following request adds the ‘ExecuteScript’ permission to the role named ‘MyRole’:

```text
?action=AddPermissionsToRole&name=MyRole&permissions.1=ExecuteScript
```

The method returns a JSON serialized representation of the edited role:

```text
{
    "key": 1012,
    "name": "MyRole",
    "description": "",
    "permissions": [
        "ExecuteScript"
    ],
    "persons": [],
    "access_groups": []
}
```

## AddPersonsToRole

Add the given persons to a role. Those persons will be granted the role.

Arguments:

- `name`: The name of the role to modify.
- `persons`: A list of emails of persons to add.

The following errors may be raised:

- `UnknownRole`: No role with the specified name was found.
- `UnknownPersons`: One or more of the given emails are unknown.

For example, the following request grants the role named ‘MyRole’ to the person in the account with email 'john@example.com‘:

```text
?action=AddPersonsToRole&name=MyRole&persons.1=john@example.com
```

The method returns a JSON serialized representation of the edited role:

```text
{
    "key": 1012,
    "name": "MyRole",
    "description": "",
    "permissions": [],
    "persons": [
        "john@example.com"
    ],
    "access_groups": []
}
```

## CopyRole

Copy an existing access role to an access role with a new name.

Arguments:

- `name`: The name of an existing access role to copy.
- `destination_name`: The name of the copied role. It must start with a letter and can contain alphanumeric characters, ‘-‘ and ‘+’.
- `description`: Optional description of the role.

The following errors may be raised:

- `UnknownRole`: No role with the specified name is found.
- `DuplicateRole`: A role with the specified name exists.
- `InvalidRoleName`: The provided name is not valid for a role.

For example, the following request creates a role named ‘BaseRole1’ from BaseRole:

```text
?action=CopyRole&name=BaseRole&destination_name=BaseRole1
```

The method returns a JSON serialized representation of the new role:

```text
{
    "key": 1012,
    "name": "BaseRole1",
    "description": "",
    "permissions": [],
    "persons": [],
    "access_groups": []
}
```

## CreateAccessGroup

Create a new access group.

Arguments:

- `title`: The title of the access group.
- `parent`: Optionally, the name of the access group that this access group should be added as a child of. If this parameter is omitted the child will be added below the root access group of the account.

The following errors may be raised:

- `DuplicateAccessGroup`: An access group with the specified title already exists.
- `InvalidAccessGroup`: The provided name is not valid for an access group.

For example, the following request creates an access group named ‘Production’ as child of the access group ‘Servers’:

```text
?action=CreateAccessGroup&name=Production
&title=Production&parent=Servers
```

The method returns a JSON serialized representation of the new access group:

```text
{
    "title": "MyAccessGroup",
    "parent": "ParentAccessGroup",
    "children": ""
}
```

## CreateRole

Create a new access role.

Arguments:

- `name`: The name of the role. It must start with a letter and can contain alphanumeric characters, ‘-‘ and ‘+’.
- `description`: Optional description of the role.

The following errors may be raised:

- `DuplicateRole`: A role with the specified name exists.
- `InvalidRoleName`: The provided name is not valid for a role.

For example, the following request creates a role named ‘MyRole’:

```text
?action=CreateRole&name=MyRole
```

The method returns a JSON serialized representation of the new role:

```text
{
    "key": 1012,
    "name": "MyRole",
    "description": "",
    "permissions": [],
    "persons": [],
    "access_groups": []
}
```

## GetAccessGroups

Get all access groups in the account.

Arguments:

- `names`: Optionally, a list of access group names to get. Only matching access groups will be returned.

For example, the following request fetches all access groups in the caller’s account:

```text
?action=GetAccessGroups
```

The method returns a JSON serialized representation of the account access groups:

```text
[
    {
        "name": "MyAccessGroup",
        "title": "",
        "parent": "ParentAccessGroup",
        "children": ""
    }
]
```

## GetPermissions

Get all available permissions.

Example of valid call:

```text
?action=GetPermissions
```

The method returns a JSON serialized list of permissions:

```text
[
    {
        "name": "ViewComputer",
        "title": "View Computers"
    },
    {
        "name": "ManageComputer",
        "title": "Manage Computers"
    },
    "..."
]
```

## GetRoles

Get all roles in the account.

Arguments:

- `names`: Optionally, a list of role names to get. Only matching roles will be returned.

For example, the following request fetches all roles in the caller’s account:

```text
?action=GetRoles
```

The method returns a JSON serialized representation of the account roles:

```text
[
    {
        "key": 1012,
        "name": "MyRole",
        "description": "",
        "permissions": [],
        "global_permissions": [],
        "persons": [],
        "access_groups": []
    }
]
```

## RemoveAccessGroup

Remove an access group.

Arguments:

- `name`: The name of the access group to remove.

For example, the following request removes an access group named ‘MyAccessGroup’, a child of the access group ‘ParentAccessGroup’:

```text
?action=RemoveAccessGroup&name=MyAccessGroup
```

The method returns a JSON serialized representation of the state of the parent access group after the child is removed:

```text
{
    "name": "ParentAccessGroup",
    "title": "parent",
    "parent": "GrandParentAccessGroup",
    "children": ""
}
```

## RemoveAccessGroupsFromRole

Remove the given access groups from a role.

Arguments:

- `name`: The name of the role to modify.
- `access_groups`: A list of names of access groups to remove.

For example, the following request removes the access group ‘my-group’ from the role named ‘MyRole’. Any person with this role granted will lose ‘my-group’ permissions:

```text
?action=RemoveAccessGroupsFromRole&name=MyRole
&access_groups.1=my-group
```

The method returns a JSON serialized representation of the edited role:

```text
{
    "key": 1012,
    "name": "MyRole",
    "description": "",
    "permissions": [],
    "persons": [],
    "access_groups": []
}
```

## RemovePermissionsFromRole

Remove permissions from a role.

Arguments:

- `name`: The name of the role to modify.
- `permissions`: A list of permissions to remove.

The following errors may be raised:

- `UnknownRole`: No role with the specified name was found.
- `InvalidPermissions`: One or more of the given permissions are invalid.
- `ReadOnlyRole`: The specified role can’t be modified.

For example, the following request will remove the ‘ExecuteScript’ permission to the role named ‘MyRole’:

```text
?action=RemovePermissionsFromRole&name=MyRole
&permissions.1=ExecuteScript
```

The method returns a JSON serialized representation of the edited role:

```text
{
    "key": 1012,
    "name": "MyRole",
    "description": "",
    "permissions": [],
    "persons": [],
    "access_groups": []
}
```

## RemovePersonsFromRole

Remove the given people from a role.

Arguments:

- `name`: The name of the role to modify.
- `persons`: A list of the email addresses of people to remove.

The following errors may be raised:

- `UnknownRole`: No role with the specified name was found.
- `UnknownPersons`: One or more of the given email addresses are unknown.

For example, the following request removes the role named ‘MyRole’ from the person in the account with email 'john@example.com‘:

```text
?action=RemovePersonsFromRole&name=MyRole&persons.1=john@example.com
```

The method returns a JSON serialized representation of the edited role:

```text
{
    "key": 1012,
    "name": "MyRole",
    "description": "",
    "permissions": [],
    "persons": [],
    "access_groups": []
}
```

## RemoveRole

Removes an access role.

Arguments:

- `name`: The name of the role.

The following errors may be raised:

- `UnknownRole`: No role with the specified name was found.
- `InvalidRoleName`: When trying to remove the default GlobalAdmin role.

For example, the following request removes a role named ‘MyRole’:

```text
?action=RemoveRole&name=MyRole
```

An empty response is returned is the role is successfully removed:

```text
{}
```

