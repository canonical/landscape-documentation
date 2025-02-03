(how-to-guides-wsl-integration-use-a-specific-image-source)=
# How to use a specific Ubuntu image source for WSL and push the image to your Windows machines

If you don’t want to download your Ubuntu image from the Microsoft Store, you can instead use a different image source. This guide describes how to get your Ubuntu image from a different source and push that image to your WSL machines using the Landscape REST API. 

The example provided here uses `curl` and `jq`, and assumes your Windows host machine(s) are already registered in Landscape. If you haven't registered your host machine yet, see [how to register WSL hosts to Landscape](/how-to-guides/wsl-integration/register-wsl-hosts).

## Set up your environment

First, set up your environment:

1. Install prerequisites:
    
    ```bash
    snap install curl jq
    ```
    
2. Set the environment variables specific to your Landscape installation and user:
    
    ```bash
    export LANDSCAPE_USER_EMAIL=john@example.com
    export LANDSCAPE_USER_PASSWORD=pwd
    export LANDSCAPE_URL=https://landscape-server.domain.com
    ```
    
## Install WSL on multiple Windows host machines

If you’re installing WSL on multiple Windows machines, you can use one of the following scripts. Your Windows host machines should already be registered with Landscape before running this script. If you haven’t registered your machines yet, see [how to register WSL hosts to Landscape](/how-to-guides/wsl-integration/register-wsl-hosts).

### Installing an official Ubuntu image
Before running this script, you first need to edit:

- `PARENT_COMPUTER_IDS`: Contains the array of IDs of the Windows host machines.
- `COMPUTER_NAME`: The name of the Ubuntu image in the store.

Once you’ve edited those variables, execute the full script. The script will display the responses from Landscape.

```bash
#!/usr/bin/env bash

# array of instance ids to install the WSL image on
PARENT_COMPUTER_IDS=(6 7 8 9)

# Exact name of the Ubuntu image in the store
COMPUTER_NAME=Ubuntu-22.04

# build the login payload: {"email": "admin@example.com", "password": "adminpassword"}
LOGIN_JSON=$( jq -n \
    --arg em "$LANDSCAPE_USER_EMAIL" \
    --arg pwd "$LANDSCAPE_USER_PASSWORD" \
    '{email: $em, password: $pwd}' )

# make the login request
LOGIN_RESPONSE=$( curl -s -X POST "$LANDSCAPE_URL/api/v2/login" \
    --data "$LOGIN_JSON" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" )

# extract the JWT from the response and trim the double quotes
JWT=$( echo $LOGIN_RESPONSE | jq .token | tr -d '"')

for COMPUTER_ID in "${PARENT_COMPUTER_IDS[@]}"; do
    # build the request payload: {"computer_name": "Ubuntu-22.04"}
    WSL_JSON=$( jq -n \
        --arg cn "$COMPUTER_NAME" \
        '{computer_name: $cn}' )

    # make the request
    API_RESPONSE=$( curl -s -X POST \
        "$LANDSCAPE_URL/api/v2/computers/$COMPUTER_ID/children" \
        --data "$WSL_JSON" \
        --header "Authorization:Bearer $JWT" \
        --header "Content-Type: application/json" \
        --header "Accept: application/json" )

    # show the response
    echo $API_RESPONSE
    echo
done
```

### Installing with a custom image
Before running this script, you first need to edit:

- `PARENT_COMPUTER_IDS`: Contains the array of IDs of the Windows host machines.
- `ROOTFS_URL`: Contains the URL to download the image from.
- `COMPUTER_NAME`: Contains the name to use for the created WSL instance on each Windows host.

Once you’ve edited those variables, execute the full script. The script will display the responses from Landscape.

```bash
#!/usr/bin/env bash

# array of instance ids to install the WSL image on
PARENT_COMPUTER_IDS=(6 7 8 9)

# URL to download the image from
ROOTFS_URL=https://example.com/ubuntu.img

# Name of the image
COMPUTER_NAME=Custom-Image

# build the login payload: {"email": "admin@example.com", "password": "adminpassword"}
LOGIN_JSON=$( jq -n \
    --arg em "$LANDSCAPE_USER_EMAIL" \
    --arg pwd "$LANDSCAPE_USER_PASSWORD" \
    '{email: $em, password: $pwd}' )

# make the login request
LOGIN_RESPONSE=$( curl -s -X POST "$LANDSCAPE_URL/api/v2/login" \
    --data "$LOGIN_JSON" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" )

# extract the JWT from the response and trim the double quotes
JWT=$( echo $LOGIN_RESPONSE | jq .token | tr -d '"')

for COMPUTER_ID in "${PARENT_COMPUTER_IDS[@]}"; do
    # build the request payload: {"rootfs_url": "example.com", "computer_name": "Custom-Image"}
    WSL_JSON=$( jq -n \
        --arg rf "$ROOTFS_URL" \
        --arg cn "$COMPUTER_NAME" \
        '{rootfs_url: $rf, computer_name: $cn}' )

    # make the request
    API_RESPONSE=$( curl -s -X POST \
        "$LANDSCAPE_URL/api/v2/computers/$COMPUTER_ID/children" \
        --data "$WSL_JSON" \
        --header "Authorization:Bearer $JWT" \
        --header "Content-Type: application/json" \
        --header "Accept: application/json" )

    # show the response
    echo $API_RESPONSE
    echo
done
```

### Installing with a custom image and cloud init

Before running this script, you first need to edit:

- `PARENT_COMPUTER_IDS`: Contains the array of IDs of the Windows host machines.
- `ROOTFS_URL`: Contains the URL to download the image from.
- `COMPUTER_NAME`: Contains the name to use for the created WSL instance on each Windows host.
- `CLOUD_INIT_FILE`: Path to the `cloud_init.yaml` file to apply to each WSL instance.

Once you’ve edited those variables, execute the full script. The script will display the responses from Landscape.

```bash
#!/usr/bin/env bash

# array of instance ids to install the WSL image on
PARENT_COMPUTER_IDS=(6 7 8 9)

# URL to download the image from
ROOTFS_URL=https://example.com/ubuntu.tar.gz

# Name of the image
COMPUTER_NAME=Custom-Image

# cloud_init.yaml file
CLOUD_INIT_FILE=/path/to/cloud_init.yaml

# we base64 encode the cloud init file contents
BASE64_ENCODED_CLOUD_INIT=$(cat $CLOUD_INIT_FILE | base64 --wrap=0)

# build the login payload: {"email": "admin@example.com", "password": "adminpassword"}
LOGIN_JSON=$( jq -n \
    --arg em "$LANDSCAPE_USER_EMAIL" \
    --arg pwd "$LANDSCAPE_USER_PASSWORD" \
    '{email: $em, password: $pwd}' )

# make the login request
LOGIN_RESPONSE=$( curl -s -X POST "$LANDSCAPE_URL/api/v2/login" \
    --data "$LOGIN_JSON" \
    --header "Content-Type: application/json" \
    --header "Accept: application/json" )

# extract the JWT from the response and trim the double quotes
JWT=$( echo $LOGIN_RESPONSE | jq .token | tr -d '"')

for COMPUTER_ID in "${PARENT_COMPUTER_IDS[@]}"; do
    # build the request payload: {"rootfs_url": "example.com", "computer_name": "Custom-Image", "cloud_init": <base64 encoded material>}
    WSL_JSON=$( jq -n \
        --arg rf "$ROOTFS_URL" \
        --arg cn "$COMPUTER_NAME" \
        --arg b64 "$BASE64_ENCODED_CLOUD_INIT" \
        '{rootfs_url: $rf, computer_name: $cn, cloud_init: $b64}' )

    # make the request
    API_RESPONSE=$( curl -s -X POST \
        "$LANDSCAPE_URL/api/v2/computers/$COMPUTER_ID/children" \
        --data "$WSL_JSON" \
        --header "Authorization:Bearer $JWT" \
        --header "Content-Type: application/json" \
        --header "Accept: application/json" )

    # show the response
    echo $API_RESPONSE
    echo
done

```

## Install WSL on a single Windows host machine

If you're installing WSL on a single Windows machine, you can use any of the scripts above for installing multiple WSL instances by setting `PARENT_COMPUTER_IDS` to be a singleton in that script:

```bash
PARENT_COMPUTER_IDS=(7)
```

