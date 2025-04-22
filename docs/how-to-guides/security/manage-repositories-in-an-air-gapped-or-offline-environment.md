(how-to-manage-repos-airgapped)=
# How to manage repositories in an air-gapped or offline environment

> See also: {ref}`explanation-repo-mirroring`

You can manage repositories with Landscape in an air-gapped or offline environment, although the setup is more involved than in a standard online environment. This guide provides a high-level overview of how to set up Landscape in an air-gapped environment. If you aren’t familiar with repository mirroring and management in Landscape, it’s recommended that you read our {ref}`explanation-repo-mirroring` first.

This guide assumes you already have Landscape installed and set up in your air-gapped environment. If you don’t have Landscape installed yet, follow the instructions in {ref}`how-to-install-airgapped` before completing this guide.

## Background information

To use Landscape’s repository management feature within an air-gapped environment, you need to have two Landscape Servers: one online server that’s *outside* the environment, and one offline server that’s *inside* the environment.

There are two possible configurations for your air-gapped environment:

* **Restricted network air-gap** (One-way controlled access): The inside (offline) server doesn’t have direct access to the public internet, but it’s allowed to communicate with the outside (online) server through a controlled endpoint. In this configuration, the inside server can still receive updates and data from the outside server in a secure, controlled way. The client machines do not have access outside the air-gapped environment. This reduces the manual effort required to transfer data into the air-gapped environment with physical media.
* **Fully disconnected air-gap** (Manual data transfer): The inside (offline) server has no network connectivity to the outside (online) server or the public internet. Any updates or data must be manually transferred into the air-gapped environment using physical media.

Using a restricted network air-gap drastically simplifies the Landscape repository management process, although managing repositories in a fully disconnected air-gap is still possible.

### Limitations

For fully disconnected air-gapped environments, using physical media to manually transfer large amounts of data can be a challenge. At this time, Landscape doesn’t have the ability to generate a diff between the existing repository contents and the latest repository contents. This means you can’t bring only the differences into the air-gapped environment—you must bring in the *entire repository contents* every time you update. Since the size of the Ubuntu repositories is 100s of GB of data per version of Ubuntu, this manual transfer of data can be difficult and time-consuming.

## Restricted network air-gap

**Note:** This process will take awhile to set up, especially if you’re not familiar with repository management. For general information on repository management in Landscape, see our {ref}`explanation-repo-mirroring`.

If you’re in a restricted network air-gap, setting up the repository mirrors is relatively similar to the standard (online) way, but with some additional steps. You need to set up your outside server as a third-party repository for the inside server. For detailed instructions, see {ref}`how-to-create-tiered-repo-mirrors`.

After you’ve set up your repository mirror structure, see {ref}`how-to-manage-repos-api` for instructions on how to create the repositories, repository profiles, and associate the profiles to client machines (computers).

## Fully disconnected air-gap

**Note:** This process will take awhile to set up, especially if you’re not familiar with repository management. For general information on repository management in Landscape, see our {ref}`explanation-repo-mirroring`.

If you’re in a fully-disconnected air-gap, the general process is that you copy the necessary data from your outside (online) server and manually transfer it to your inside (offline) server via physical media.

To make this work, you need to set up identical repository structures in your outside and inside servers. This includes using the same GPG key in both servers.

### Create your repository structure and profile(s)

Use the following steps to create your repository structure. It doesn’t matter which server you start with; it only matters that they are built identically.

1. On one of your servers, follow the guidance in {ref}`how-to-manage-repos-api` to create your repository structure and any profiles. You need to use the API (instead of the web portal) because the inside server won’t have network access.
    - We recommend you save the commands that you ran so you can use them again on the other server
2. On your other server, re-create the repository structure and profiles exactly the same as the first server. This includes using the same GPG key.

### Manually transfer data into your air-gapped environment

To manually transfer the data:

1. In your outside server, copy the contents of `/var/lib/landscape/landscape-repository/standalone/` to an acceptable form of physical media for your environment, such as a DVD or USB drive.
2. Manually transfer those files into the same location on your inside server.

Once all of the data is successfully transferred to the inside server, Landscape will serve the repository contents to all of your Landscape Client machines based on the profiles.