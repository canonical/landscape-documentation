(how-to-guides-iot-for-devices-index)=
# IoT for devices

Managing IoT devices can be a challenge, especially when you consider the requirements for deploying these devices to physically inaccessible locations, or the need to dictate exactly when and how your devices are updated.

Landscape can solve these issues. Landscape enables you to remotely manage, configure, and control each of your devices, choose when and which updates are installed, and allow remote debugging and health checking of your devices all from a centralized web portal.

Using the strictly-confined snap version of Landscape Client, you can add all of your Core devices to your Landscape account and manage them from the web portal. Landscape works with a variety of devices, including devices with limited or intermittent connectivity. Additionally, leveraging the capabilities of the Snap Store ensures transactional, automatic updates with built-in rollback-on-failure support. As a result, you can manage your devices remotely without the need for physical intervention.

## How-to guides

We have the following how-to guides to help you use the Landscape Client snap to manage your IoT devices:

### Install and configure

```{toctree}
:titlesonly:
Install the snap <install-the-snap>
Configure the snap <configure-the-snap>
Create an Ubuntu Core image that includes the snap <create-a-core-image>
```

### Use

```{toctree}
:titlesonly:
Use remote script execution <remote-script-execution>
Use annotations <use-annotations>
Secure removal <secure-removal>
```

## Best practices for IoT

IoT devices come with their own unique characteristics and challenges. Therefore, we recommend the following best practices to make their management as easy, safe and secure as possible.

- **IoT devices should be deployed without any users configured**
    - Users are not necessary and provide an attack vector
    - Adding users can be achieved remotely via Landscape and can be time-scoped
- **Automatic refresh timer should be disabled**
    - This will prevent all snaps from automatically updating when a new version becomes available
    - Chose when and which snaps to update from Landscape to suit your maintenance windows
    - Use groups and tags to control your updates
        - Deploy to test groups first to ensure functionality after upgrade
        - Choose regional rollout strategies to match local maintenance windows
- **Use remote scripting to debug**
    - Use Landscape’s remote scripting interface to collect and parse various logs from your devices to help debug issues

## Limitations of the Landscape Client snap

There are some limitations to be aware of when using the Landscape Client snap and some functionality which isn’t available yet in the web portal. In many cases, you can use remote scripts to overcome these limitations. It’s recommended that you explore the example scripts available in the [Landscape Scripts repository on GitHub](https://github.com/canonical/landscape-scripts).

### Ubuntu Core

You may encounter these limitations when using the Landscape Client snap on Ubuntu Core:

**Remote script execution**

You can use remote script execution in the Landscape Client snap, but the functionality is limited by the confinement of the snap. The automatically connected interfaces allow for extensive system configuration and management via script execution, but it may be necessary to do this in a snap interface-friendly manner. For more information, see [how to use remote script execution](/how-to-guides/iot-for-devices/remote-script-execution) and the [Landscape Scripts repository on GitHub](https://github.com/canonical/landscape-scripts).

**User management**

Adding users through Ubuntu One SSO and system user assertions is supported by the client snap but not yet implemented on Landscape Server and its web portal. It’s possible to perform these actions using a custom script.

Deleting users works since the user is removed from the device but the status is not reported on the portal. The deleted user will be removed from the user list.

Some actions like locking and editing users are unsupported by the [Snapd REST API](https://snapcraft.io/docs/snapd-api).

**Snap services management**

Snap services management is supported on the client snap but not yet implemented on Landscape Server and its web portal. It’s possible to perform these actions using a custom script.

Possible service actions include: start, enable, stop, disable, restart and reload. These can be performed on individual snap services or on a batch of snap services.

**Snap configuration**

Setting snap configuration is supported on the client snap but not yet implemented on Landscape Server and its web portal. It’s possible to perform this action using a custom script.

### Ubuntu Classic

You may encounter these limitations when using the Landscape Client snap on Ubuntu Classic:

**User management**

You can list users, but tasks that require writing directly to files in `/etc` and `/home` aren’t possible with the Landscape Client snap’s confinement on Ubuntu Classic.

**Package management**

Snap confinement doesn’t currently allow the snap to access APT for Debian package management.

**Does not support Ubuntu Pro**

The client snap does not support Ubuntu Pro yet. Reporting of Ubuntu Pro status through the `UbuntuProInfo` plugin is currently disabled on the snap. This is due to it requiring access to the APT package management system, which is not available from the snap.

**Snap services management**

The same issues that affect snap services management on Ubuntu Core also apply to Ubuntu Classic. See the previous section on Ubuntu Core and snap services management.

**Snap configuration**

The same issues that affect snap configuration on Ubuntu Core also apply to Ubuntu Classic. See the previous section on Ubuntu Core and snap configuration.

## Known issues with the snap

### Duplicate machines after reverting snap revisions

Before revision 329, reverting to a previous snap revision could cause clients to re-register with Landscape, resulting in duplicate machines. This was due to the way the client snap stored data. This issue is now fixed in later revisions (after 329).

To remove the duplicate machine(s), go to the Landscape portal and remove any machines that are offline and not pinging. In the newer portal, click on the instance, then **Remove from Landscape**. Or in the classic portal, click the computer, then **Remove computer**. You’ll be prompted to confirm in both web portals.
