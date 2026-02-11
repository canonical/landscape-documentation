---
myst:
  html_meta:
    description: "Install Landscape Server on Google Cloud using cloud-init. Set up gcloud CLI, configure authentication, and deploy standard or FIPS-compliant instances."
---

(how-to-install-on-google-cloud)=
# How to install Landscape Server on Google Cloud

This guide provides an example of how to install and set up your Landscape server on Google Cloud with [cloud-init](https://cloudinit.readthedocs.io/en/latest/). The instructions here can be used for both standard or FIPS-compliant deployments. 

```{note}
For the most up-to-date documentation on Google Cloud, see [Google Cloud's documentation](https://cloud.google.com/docs).
```

## Install and set up Google Cloud CLI

### Install `gcloud`

To install `gcloud`, run:

```bash
sudo snap install google-cloud-cli --classic
```

### Connect `gcloud` with your Google Cloud account

1. To initialize the Google Cloud CLI, run:

    ```bash
    gcloud init
    ```

2. Enter **Y** when prompted with *Would you like to log in (Y/n)?*
3. Visit the authentication link provided
    - The authentication link should start with `https://accounts.google.com/`
4. Sign in with a Google account
5. Click **Allow** to grant access to the Google Cloud SDK
6. Click **Copy** to copy the verification code
7. Paste the verification code into the terminal window where the `gcloud init` process is running

If you complete the `gcloud init` process successfully, you will receive the following output:

```text
You are now logged in as [your@email.com].
Your current project is [None].  You can change this setting by running:
  $ gcloud config set project PROJECT_ID
```

### Provision resources and deploy

1. List the projects that are in your account:

    ```bash
    gcloud projects list
    ```

    You’ll receive output similar to:

    ```bash
    PROJECT_ID        NAME              PROJECT_NUMBER
    project-id        project-name      12345678910
    ```

2. Set your project ID to the `PROJECT_ID` environment variable. Replace `project-id` with your personal project ID from the previous output:

    ```bash
    PROJECT_ID=project-id
    ```

    This step isn’t required, but it’s recommended because the `PROJECT_ID` variable is used often.

3. Connect `gcloud` to this `PROJECT_ID`:

    ```bash
    gcloud config set project $PROJECT_ID
    ```

    This is where the Landscape virtual machine (VM) will be launched.

4. List the available cloud zones and cloud regions where VMs can be run:

    ```bash
    gcloud compute zones list
    ```

    You’ll receive output similar to:

    ```text
    NAME                       REGION                   STATUS  NEXT_MAINTENANCE  TURNDOWN_DATE
    us-east1-b                 us-east1                 UP
    ```

5. Set the `ZONE` and `REGION` environment variables. Replace `us-east1-b` and `us-east1` with your desired zone and region from the previous output:

    ```bash
    ZONE=us-east1-b
    REGION=us-east1
    ```

6. Reserve a static IP address and label it `landscape-external-ip`:

    ```bash
    gcloud compute addresses create landscape-external-ip --region=$REGION
    ```

    This step isn’t required, but it's recommended because Landscape benefits from a static IP address assignment. A DNS record called an “A record” is responsible for pointing the fully qualified domain name (FQDN) to the Landscape Server’s IP address. If you use a static IP address, the A record doesn’t have to be updated every time the dynamic IP changes.

7. List the addresses you’ve created:

    ```bash
    gcloud compute addresses list
    ```

8. Copy the IP address and set it as the A record value for the domain or subdomain that will serve as the FQDN. You set the A record in your DNS service.
9. Verify the A record using `nslookup`. Replace `{landscape-fips.domain.com}` with your FQDN:

    ```bash
    nslookup {landscape-fips.domain.com}
    ```

    You’ll receive output similar to:

    ```text
    Server:     127.0.0.53
    Address:    127.0.0.53#53

    Non-authoritative answer:
    Name:    landscape-fips.domain.com
    Address: 34.139.255.120
    ```

    If the address value in the `nslookup` output matches the value of the `landscape-external-ip` static IP address, the LetsEncrypt SSL provisioning step defined in the cloud-init configuration automation template will succeed.

## Deploy Landscape Server VMs with cloud-init

Before beginning the deployment process with cloud-init, you must choose which of the two cloud-init configuration automation templates you want to use. In the [Landscape Scripts](https://github.com/canonical/landscape-scripts) Github repository, there are two Landscape Quickstart cloud-init configuration templates: [`cloud-init-quickstart.yaml`](https://github.com/canonical/landscape-scripts/blob/main/provisioning/cloud-init-quickstart.yaml) and [`cloud-init-quickstart-fips.yaml`](https://github.com/canonical/landscape-scripts/blob/main/provisioning/cloud-init-quickstart-fips.yaml).

The `cloud-init-quickstart.yaml` template is designed for anyone, and the `cloud-init-quickstart-fips.yaml` is designed for FIPS compliant deployments of Landscape Server. For more information, see {ref}`how-to-install-fips-compliant`.

Once you’ve chosen your configuration template, complete the following steps.

1. Set the `IMAGE_FAMILY` environment variable based on the cloud-init configuration you chose.
    - If you’re using `cloud-init-quickstart.yaml`, run:

        ```bash
        curl -s https://raw.githubusercontent.com/canonical/landscape-scripts/main/provisioning/cloud-init-quickstart.yaml -o cloud-init.yaml
        IMAGE_FAMILY=ubuntu-pro-2204-lts
        ```

    - If you’re using `cloud-init-quickstart-fips.yaml`, run:

        ```bash
        curl -s https://raw.githubusercontent.com/canonical/landscape-scripts/main/provisioning/cloud-init-quickstart-fips.yaml -o cloud-init.yaml
        IMAGE_FAMILY=ubuntu-pro-fips-2004-lts
        ```

2. Open the downloaded cloud-init YAML file in an editor, determine which configuration parameters need to be changed between lines 4 and 32 and change these parameters.

    The `HOSTNAME` on line 16 and `DOMAIN` on line 19 must be changed. Updating `EMAIL` on line 9, and adding your SendGrid API key on line 29 as the `SMTP_PASSWORD` are optional, but strongly recommended.

3. Run the following code to launch a machine with generally suitable resource specifications:

    ```bash
    gcloud compute instances create landscape \
        --zone $ZONE \
        --machine-type=c3-standard-4 \
        --address landscape-external-ip \
        --tags http-server,https-server \
        --boot-disk-size 200 \
        --image-family $IMAGE_FAMILY \
        --image-project ubuntu-os-pro-cloud \
        --metadata-from-file user-data=cloud-init.yaml
    ```

    You can also downgrade `machine-type` from `c3-standard-4` to `e2-medium`, and `boot-disk-size` from `200` to `20` for cost savings. However, the `e2-medium` machine is a shared compute resource and using it may result in temporary and sporadic instability of the Landscape dashboard. This size machine should only be used for proof-of-concepts and limited testing.

4. List all VMs in this project:

    ```bash
    gcloud compute instances list
    ```

5. Observe the process by tailing the `cloud-init-output.log` file:

    ```bash
    gcloud compute ssh landscape --zone $ZONE --command "tail -f /var/log/cloud-init-output.log"
    ```

6. If you are a first time `gcloud` user, you’ll be prompted for a passphrase twice. This can be left blank. Press **Enter** twice to proceed:

    ```bash
    WARNING: The private SSH key file for gcloud does not exist.
    WARNING: The public SSH key file for gcloud does not exist.
    WARNING: You do not have an SSH key for gcloud.
    WARNING: SSH keygen will be executed to generate a key.
    Generating public/private rsa key pair.
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    ```

7. A reboot may be required during the cloud-init process. If a reboot is required, you’ll receive the following output:

    ```bash
    2023-08-20 17:30:04,721 - cc_package_update_upgrade_install.py[WARNING]: Rebooting after upgrade or install per /var/run/reboot-required
    ```

    If the `IMAGE_FAMILY` specified earlier contained all the security patches, this reboot step may not occur.

8. Repeat the following code if a reboot was necessary to continue observing the log file:

    ```bash
    gcloud compute ssh landscape --zone $ZONE --command "tail -f /var/log/cloud-init-output.log"
    ```

9. Wait until the cloud-init process is complete. When it's complete, you’ll receive two lines similar to this:

    ```bash
    cloud-init v. 23.2.2-0ubuntu0~20.04.1 running 'modules:final' at Sun, 20 Aug 2023 17:30:43 +0000. Up 25.14 seconds.
    cloud-init v. 23.2.2-0ubuntu0~20.04.1 finished at Sun, 20 Aug 2023 17:30:56 +0000. Datasource DataSourceGCELocal.  Up 37.35 seconds
    ```

10. Press `CTRL + C` to terminate the tail process in your terminal window.

## Configure Landscape

1. Navigate to the Landscape dashboard by entering the FQDN of the Landscape VM into a browser window
2. Provide a name, email address, and password for the first global administrator on the machine.

    If the email address Landscape sends emails from should not be a subdomain based on the machine’s hostname, remove the hostname, or make the appropriate correction.

    Alerts and administrator invitations sent via email are less likely to fail SPF or DMARC checks if the system email address is configured in a way the email service provider expects. If the email service provider sends emails which fail SPF and DMARC checks, mail delivery can be delayed or miscategorized as spam.

## Clean up provisioning metadata containing secrets

To delete the cloud-init `user-data` key, run:

```bash
gcloud compute instances remove-metadata landscape --zone $ZONE --keys=user-data
```

Cloud-init scripts are provided in a custom metadata key named `user-data`. The `user-data` key is consumed during instance creation and is executed when the instance starts. Sensitive information such as API keys shouldn’t be left visible within the custom metadata of the VM or in the cloud dashboard. Once the cloud-init process is complete, it’s safe to delete the cloud-init `user-data` key.

## (Optional) Perform a complete teardown

You may want to perform a teardown to clean up unused or unnecessary resources. This can help control costs and optimize resources. To perform a complete teardown:

1. Delete the VMs:

    ```bash
    gcloud compute instances delete landscape --zone $ZONE
    ```

2. Release the static IP:

    ```bash
    gcloud compute addresses delete landscape-external-ip --region $REGION
    ```
