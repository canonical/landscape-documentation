(how-to-create-a-core-image)=
# How to create an Ubuntu Core image with Landscape Client included

You can manage your Ubuntu Core device deployments with the Landscape Client snap and the Landscape web portal. This guide demonstrates how you can deploy your devices at scale by building a custom Ubuntu Core image that includes the Landscape Client snap and configuring the image to automatically register each device after its first boot.

The example provided here is based on [Ubuntu Core’s tutorial for building your first Ubuntu Core image](https://ubuntu.com/core/docs/build-an-image). It uses a Raspberry Pi running Ubuntu Core 22, but the instructions still generally apply to other devices and configurations.

## Prerequisites

To build your custom Ubuntu Core image, you must have the following:

- An Ubuntu One account
- A Raspberry Pi running Ubuntu Core 22
- A host system running Ubuntu 22.04 LTS or later
- 10GB of free storage space on the host system
- A 4GB+ microSD card to store the image

## Define your custom image

To define your image to include Landscape Client, you’ll need to get the appropriate reference model to create your base image and manually add the Landscape Client snap.

### Get the reference model assertion

Run the following to download the reference model for Raspberry Pi running Ubuntu Core 22:

```bash
wget -O my-model.json https://raw.githubusercontent.com/snapcore/models/master/ubuntu-core-22-pi-arm64.json
```

For other reference models for supported Ubuntu Core devices, see the [`snapcore/models` GitHub repository](https://github.com/snapcore/models).

### Edit the reference model assertion

You need to edit the model file to set `authority-id` and `brand-id` to your own developer ID. These properties define the authority responsible for the image. You can retrieve your developer ID with the `snapcraft whoami` command. For more information, see [Ubuntu Core’s guide on creating a model assertion](https://ubuntu.com/core/docs/create-model-assertion).

You can use a text editor to edit these properties. Your model file will be similar to the following:

```json
{
    "type": "model",
    "series": "16",
    "model": "ubuntu-core-22-pi-arm64",
    "architecture": "arm64",
    "authority-id": "(DEVELOPER_ID}",
    "brand-id": "(DEVELOPER_ID}",
    "timestamp": "2022-04-04T10:40:41+00:00",
    "base": "core22",
    "grade": "signed",
    "snaps": [
        {
            "name": "pi",
            "type": "gadget",
            "default-channel": "22/stable",
            "id": "YbGa9O3dAXl88YLI6Y1bGG74pwBxZyKg"
        },
        {
            "name": "pi-kernel",
            "type": "kernel",
            "default-channel": "22/stable",
            "id": "jeIuP6tfFrvAdic8DMWqHmoaoukAPNbJ"
        },
        {
            "name": "core22",
            "type": "base",
            "default-channel": "latest/stable",
            "id": "amcUKQILKXHHTlmSa7NMdnXSx02dNeeT"
        },
        {
            "name": "snapd",
            "type": "snapd",
            "default-channel": "latest/stable",
            "id": "PMrrV4ml8uWuEUDBT8dSGnKUYbevVhc4"
        }
    ]
}

```

### Add the Landscape Client snap

Now, add an additional record in the `snaps` array for the Landscape Client snap. The record you add will be similar to the following:

```json
        {
            "name": "landscape-client",
				      "type": "app",
			      "default-channel": "latest/beta",
			      "id": "ffnH0sJpX3NFAclH777M8BdXIWpo93af"
        }
```

The `id` parameter is unique to each snap with the value shown here belonging to the Landscape Client snap. If you need to find the ID of any other snap, you can use the `snap info <snap-name>` command in your terminal and find the snap ID.

## Configure your custom image

Once you’ve created your model assertion, you’re technically able to sign and build the image. However, the image you would build at this stage would need additional manual configuration on each client device, which isn’t ideal for many deployments.

Instead, you can pre-configure the client with your information when building your image and also configure it to automatically register each device without manual intervention.

### Create and configure a gadget snap with your account details and auto-registration

You need to create a gadget snap to configure the client when building your image. A “gadget snap” is a special type of snap that contains device specific support code and data. For more information on gadget snaps, see [Snapcraft’s documentation on gadget snaps](https://ubuntu.com/core/docs/gadget-snaps).

To create and configure your gadget snap:

1. Fork the official [Ubuntu Core 22 gadget snap repository](https://github.com/snapcore/pi-gadget/) to your local environment.
    - Other reference gadget snaps are available for different architectures from the [Snapcore GitHub account](https://github.com/snapcore/). Search for repositories with “gadget” in the name.
2. Append the following configuration at the bottom of the `gadget.yaml` file that defines the gadget snap:
    
    ```text
    defaults:
      # landscape client
      ffnH0sJpX3NFAclH777M8BdXIWpo93af:
        landscape-url: {LANDSCAPE_ACCOUNT_URL}
        account-name: (ACCOUNT_NAME)
        registration-key: "(REGISTRATION_KEY)"
        auto-register:
          enabled: true
          computer-title-pattern: test-${model:7}-${serial:0:8}
          wait-for-serial-as: true
    ```
    
    Replacing the following values with the relevant configuration values:
    
    - `{LANDSCAPE_ACCOUNT_URL}`: The full URL of your Landscape account.
    - `(ACCOUNT_NAME)`: Self-hosted Landscape users should set this to `standalone`.
    - `(REGISTRATION_KEY)`: Your registration key.
    
    Now, you’ve finished configuring the details of your Landscape server instance. In the `auto-register` section, you’ll likely want to change `computer-title-pattern` to your preferred method of identifying devices. For more information on these parameters, see {ref}`header-explanation-auto-reg-process-gadget-snap` located in this guide.
    
These details will be the same for all devices that run this image.

## Build the gadget and update your model assertion

### Build the gadget snap

To build the gadget snap, you just need to run the following in your terminal:

```bash
snapcraft
```

Now, you have your snap. This is the snap you want to include in your model assertion.

### Update the model assertion

If you have your own brand store, publish your custom gadget snap there and update the name and ID of the gadget snap in your model assertion. 

If you don’t have a brand store, you’ll need to use your local **`.json`** file instead. This is because it’s not permitted to upload custom gadget snaps to the global snap store. To reference your custom gadget snap in your model assertion:

1. Open your `.json` file and set the grade of the snap to “dangerous” as it hasn’t been signed by a store. 
2. Remove the **`snap-id`** and **`default-channel`** values.
3. Update the name to that of your snap filename.

This section of your local `.json` file should look similar to the following example.

```bash
  "grade": "dangerous",
    "snaps": [
        {
            "name": "pi-22-2-arm64",
            "type": "gadget",
        },
```

## Sign the model assertion

If you don’t have a signing key yet, run the following command to create one, replacing `{KEY_NAME}` with your chosen name for your signing key:

```bash
snapcraft create-key {KEY_NAME}
```

Next, sign the model assertion:

```bash
$ snap sign -k {KEY_NAME} model.json > landscape.model
```

## Build the custom Ubuntu Core image

Now, you need to build a custom Ubuntu Core image from the signed model using the `ubuntu-image` tool:

1. If you don’t have the `ubuntu-image` tool, install it with `snap install ubuntu-image --classic`.
2. Build the custom Ubuntu Core image from the signed model using the `ubuntu-image` tool. Use the `--snap` flag to specify the location of your local snap file. Your command should be similar to the following:
    
    ```bash
    ubuntu-image snap --snap pi-22-2-arm64.snap landscape.model
    ```
    
If done successfully, this will produce the image `pi.img` which is ready to be written to an SD card and inserted into your Raspberry Pi.

## Write the image to an SD card

You’ll need to write the image to an SD card. There are various tools you can use, such as *Startup Disk Creator*, which is included in many Ubuntu variants or can be downloaded from the Snap Store.

To write the image to an SD card with *Startup Disk Creator*:

1. Select your image file and target SD card
2. Click **Make Startup Disk**
3. Click **Yes** to confirm

This process typically takes 10 minutes or less.

## Boot the device

To boot the device:

1. Insert the SD card with the image into your Raspberry Pi.
2. Turn on the device
3. After a short delay your device should appear fully registered with your Landscape server

If done successfully, your device(s) should be registered, and they can now be remotely managed with your Landscape server. This process is essential for deploying large fleets or installing devices in inaccessible areas.

(header-explanation-auto-reg-process-gadget-snap)=
## Explanation: Auto-registration process in the gadget snap

The `gadget.yaml` file contains a configuration that is similar to the following:

```text
defaults:
  # landscape client
  ffnH0sJpX3NFAclH777M8BdXIWpo93af:
    landscape-url: {LANDSCAPE_ACCOUNT_URL}
    account-name: (ACCOUNT_NAME)
    registration-key: "(REGISTRATION_KEY)"
    auto-register:
      enabled: true
      computer-title-pattern: test-${model:7}-${serial:0:8}
      wait-for-serial-as: true
```

### Parameters

In this example, there are three parameters within the `auto-register` section. They are:

- **`enabled`**
    
    When `true`, this turns on the auto-registration feature. This means that the device will attempt to register itself with the Landscape server when it’s booted for the first time.
    
- **`computer-title-pattern`**
    
    This allows you to define how the computer title will be generated for this specific device. The pattern uses the bash shell parameter expansion format to manipulate the available parameters. For more information, see [GNU’s documentation on shell parameter expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html).
    
    In this example, the computer title is set to the string `test-` followed by the device model starting from the eighth character (see your model assertion) and then the first eight characters of the device serial number taken from its serial assertion.
    
    In this case, the `computer-title-pattern` would be similar to: **test-core-22-pi-arm64-f6ec1539**
    
    The available parameters to use with `computer-title-pattern` are:
    
    | Parameter | Description |
    | --- | --- |
    | `serial` | Serial from device’s serial assertion |
    | `model` | model id from device’s serial assertion |
    | `brand` | brand-id from device’s serial assertion |
    | `hostname` | device’s network hostname |
    | `ip` | device’s IP address of primary NIC |
    | `mac` | device’s MAC address of primary NIC |
    | `prodiden` | Product identifier |
    | `serialno` | Serial Number |
    | `datetime` | date/time of auto-enrollment |

- **`wait-for-serial-as`**
    
    When `true`, this tells the auto-registration function to wait until the device has been able to obtain its serial assertion from a serial vault before trying to create the title and perform the registration.

    If you don't have your own serial vault deployed, you can request a serial assertion from the global snap store by adding `"serial-authority": [ "generic" ]` to your model assertion. Without a serial authority specified, the device will wait indefinitely and not register with the Landscape Server.
    

### Step-by-step process

When a client with the previous auto-registration parameters starts for the first time, it follows this process:

1. The client checks the `enabled` parameter. If this is set to `true`, the client proceeds with the auto-registration process.
2. The client checks the `wait-for-serial-as` parameter. If this is set to `true`, the client waits until it has obtained its serial assertion from a serial vault.
3. Once the serial assertion is obtained, the client generates a computer title based on the `computer-title-pattern` parameter.
4. The client registers itself with the Landscape server, using the generated computer title and Landscape account details provided earlier in the configuration (URL, account name)
5. The device is ready to be managed remotely through the Landscape server

