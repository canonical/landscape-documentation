(how-to-classic-web-portal-other-tasks)=
# Other tasks in the Landscape web portal

## Identify your Landscape version

```{note}
Landscape beta versions run ahead of the Landscape SaaS version, and the Landscape SaaS version runs ahead of of self-hosted Landscape versions.
```

You may need to know what version of Landscape you're running. To identify your Landscape Server and Landscape Client versions:

- **Landscape Server**: Add `/about` to the URL of your Landscape account. For example, `https://landscape-server.domain.com/about`. If you're using Landscape SaaS, the URL is `https://landscape.canonical.com/about`. If you're using self-hosted Landscape,  you can also run `apt policy landscape-server` in the command line on the server machine.
- **Landscape Client**: Run `apt policy landscape-client` in the command line on the client machine.

## Group machines together to perform a task across the group

You can use tags to manage a group of computers. To add a tag to a group of computers:

1. Click **Computers** in the header
2. Select the computers you want to tag
3. Click **Info**
4. In the **Tags** section, enter the tag you want to use
5. Click **Add**

## Upgrade all packages on a certain group of machines

Using tags, you can perform an upgrade across a group of machines. For example, if you want to upgrade all your desktop computers, you might want to use "desktop" as a tag.

Starting the upgrade:

1. Click **Computers** in the header
2. Click the desired tag from the left column. This will select only the computers associated with the selected tag.
3. Click **Packages**
4. Scroll to the bottom of the page and click **Request upgrades**. This will create a queued activity for upgrading the computers. You can view this activity in the **Activities** tab.

![Activities - Upgrade pending approval](https://assets.ubuntu.com/v1/320a4d2b-usecases1.png)

Note: While the upgrade tasks are now in the queue, they will not be executed until you approve them. To approve the tasks, click **All**, then click **Approve**.

##  Keep a set of machines automatically up to date

The best way is to use {ref}`reference-terms-upgrade-profile`, which rely on {ref}`reference-terms-access-groups`. If an access group is already set up for the group of machines you want to keep updated automatically, click on its name. If not, you must create an access group for them:

1. Click on your organization's name in the header
2. Click **Access groups**
3. Specify a title for your new access group
4. Click **Save**.

You must then add computers to the access group:

1. Click **Computers** in the header
2. Select all of the machines you want to keep updated by:
   * using a tag if one exists
   * using search to find the machines
   * selecting them individually
3. Click **Info**
4. In the **Access group** section, select the access group you want to move the machines to
5. Click **Update access group**.

![Update access group](https://assets.ubuntu.com/v1/c2ac90d0-accessgroups4.png)

Once you've added machines to an access group, you'll need to create an upgrade profile:

1. Click on your organization's name in the header
2. Click **Profiles**
2. Click **Upgrade Profiles**
3. Click **Add upgrade profile**
3. Complete the **Create an upgrade profile** form, defining:
   * name
   * the upgrade settings you want to use
   * an access group
   * the schedule you want to use
4. Click **Save**

## Keep Landscape from upgrading a certain package on one of my servers

1. Click **Computers** in the header
2. Click **Packages**
2. Use the search box at the top of the screen to find the package you want.
3. Click the triangle on the left of the listing line of the package you want to hold, which expands the information for that package.
4. Now click on the icon to the left of the package name. A new icon with a lock will replace the old icon, indicating that this package is to be held during upgrades.
5. Click **Apply changes**

![Locked packages](https://assets.ubuntu.com/v1/d34df398-usecases2.png)

## Create a custom graph

Suppose you want to monitor the size of the PostgreSQL database on your database servers, you may use tags to group these machines together. Now you can create a graph to provide information from all of these servers:

1. Click on your organization's name in the header
2. Click **Graphs**
2. Click **Add graph**
3. Complete the **Create graph** form. In our example, we could do something like:
   * Title: `PostgreSQL database size`
   * Provide a "Y-axis title" and define the machines you want the graph created for.
   * Run as user: `postgres`
   * Code:
        ```
        #!/bin/bash
        psql -tAc "select pg_database_size('postgres')"
        ```
4. Click **Save**

![Create custom graph](https://assets.ubuntu.com/v1/53b56b4f-usecases3.png)

To view the graph, click **Computers** in the header, then click **Monitoring**. You can select the monitoring period from the dropdown menu at the top of the window.

## Ensure all computers with a given tag have a common list of packages installed

Manage them via a {ref}`reference-terms-package-profile`.

