(how-to-guides-web-portal-classic-web-portal-manage-packages)=
# How to manage packages

## Access package information

To access package information:

1. Navigate to the **Computers** page from the header
2. Click the **Packages** tab
   - This tab displays a screen where you can search for information about all the packages Landscape knows about. You may first specify a package name or other search string.
3. Press **Enter** or click the arrow next to the box 

Landscape then displays a list of packages that meet the search criteria.

The **Summary** section displays summary information about the packages, including clickable links to which computers have security updates and other upgrades to be installed, and the number of computers that are up-to-date and those that have not reported package information.

The **Security issues** section provides a list of security issues on computers that need security updates. You can click on the name or USN number of a security issue to see a full Ubuntu Security Notice.

The **Package information** section displays package information for each selected computer, including the number of packages available and installed, pending upgrades, and held upgrades. You can click on the number of pending or held upgrades to see a screen that lets you modify the relevant package list and set a time for the upgrades to take place.

The **Request upgrades** button at the bottom of the screen lets you quickly request that all possible upgrades be applied to the selected computers. Any resulting activities require explicit administrator approval.

## Add a package profile

To add a [package profile](/explanation/terms/profiles/package-profile):

1. Navigate to your organization's home page
2. Click the **Profiles** tab
3. Click **Package Profiles**
4. Click **Add package profile**
5. Enter the requested information
6. Click **Save**

Package constraints are packages that this profile depends on or conflicts with. They are optional to include. The constraints dropdown menu lets you add constraints in three ways: 
-  Based on a computer's installed packages
- Imported from a previously exported CSV file or the output of the `dpkg --get-selections` command
- Manually added

Use the first option if you want to replicate one computer to another. That option makes all currently installed packages that are on the selected computer dependencies of the package profile you're creating. The second option imports the dependencies of a previously exported package profile. The manual option is suitable when you have few dependencies to add, all of which you know.

When you save a package profile, Landscape creates a Debian package with the specified dependencies and conflicts and gives it a name and a version. Every time you change the package profile, Landscape increments the version by one.

If Landscape finds computers on which the package profile should be installed, it creates an activity to do so. That activity will run unattended, except that you must provide explicit administrator approval to remove any packages that the package profile wants to delete.

Additionally, note that Debian package names can't contain underscores (`_`). If you push packages to Debian machines and your package profile name contains an underscore (`_`), this could lead to a `debsums` error.

## Export a package profile

To export a [package profile](/explanation/terms/profiles/package-profile):

1. Navigate to your organization's home page
2. Click the **Profiles** tab
3. Click **Package Profiles**
4. Select each package you want to export 
5. Click **Download as CSV**

## Modify a package profile

To modify a [package profile](/explanation/terms/profiles/package-profile):

1.  Navigate to your organization's home page
2. Click the **Profiles** tab
3. Click **Package Profiles**
4. Click the name of the package profile you want to modify
5. Modify it as desired
6. Click **Change**

## Delete a package profile

To delete a [package profile](/explanation/terms/profiles/package-profile):

1. Navigate to your organization's home page
2. Click the **Profiles** tab
3. Click **Package Profiles**
4. Select each package you want to delete
5. Click **Remove**

The package profile is deleted immediately. There is no prompt to confirm the action.

