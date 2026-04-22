---
myst:
  html_meta:
    description: "Reference for Landscape access groups used to assign administrative rights to instances and organize management responsibilities."
---

(reference-terms-access-groups)=
# Access groups

In Landscape, **access groups** are logical groupings used by administrators to assign specific administrative rights to instances on a per-group basis. Each instance can only be in one access group. In addition to instances, access groups can contain package profiles, scripts and more.

A new Landscape account comes with a single access group, called "global". Any administrators associated with roles that include this access group have control over every instance managed by Landscape. Most organizations will want to subdivide administration responsibilities by creating logical groupings of instances. Typical access groups might be constructed around organizational units or departments, locations or hardware architecture.

When new access groups are created, a parent access group is specified. If an administrator has rights to manage a certain access group, that administrator will also have rights for its children access groups. Every other access group has the global access group as its parent, either directly or indirectly. A nested access group structure might look something like the diagram below.

```bash
global
├── desktop
└── server
    ├── database
    └── web
```

It's good practice to create and document a naming convention for access groups before you deploy Landscape, so that all administrators understand what constitutes an acceptable logical grouping for your organization.

## Managing access groups

### In the new web portal
You can view, add, and delete access groups under **Org. settings** > **Access groups**. See how to [create access groups](/how-to-guides/web-portal/web-portal-24-04-or-later/manage-access-groups.md#create-access-groups), [add instances to access groups](/how-to-guides/web-portal/web-portal-24-04-or-later/manage-access-groups.md#add-instances-to-access-groups), and [associate roles with access groups](/how-to-guides/web-portal/web-portal-24-04-or-later/manage-access-groups.md#associate-roles-with-access-groups).

### In the classic web portal
You can manage access groups from the **Access groups** tab in your organization's home page. See how to [create access groups](/how-to-guides/web-portal/classic-web-portal/manage-access-groups.md#create-access-groups), [add instances to access groups](/how-to-guides/web-portal/classic-web-portal/manage-access-groups.md#add-computers-to-access-groups), and [associate roles with access groups](/how-to-guides/web-portal/classic-web-portal/manage-access-groups.md#associate-roles-with-access-groups).

### Via the API
See the Legacy API reference for [changing an instance's access group](/reference/api/legacy-api-endpoints/computers.md#changecomputersaccessgroup)
