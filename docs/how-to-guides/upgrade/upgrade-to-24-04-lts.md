(how-to-upgrade-to-24-04-lts)=
# How to upgrade to Landscape Server 24.04 LTS

```{note}
There is a [known issue](https://bugs.launchpad.net/ubuntu/+source/rabbitmq-server/+bug/2074309) affecting Ubuntu 22.04 LTS (Jammy) to Ubuntu 24.04 LTS (Noble) upgrades for systems that run RabbitMQ, which includes systems that use Landscape. If you run into this issue, we recommend waiting until it's resolved before upgrading your Ubuntu version. This issue doesn't affect Landscape upgrades, and you can still upgrade to Landscape 24.04 LTS for Jammy.
```

To upgrade your self-hosted Landscape server to 24.04 LTS, you should first follow the basic upgrade instructions. See {ref}`how-to-upgrade`. Note that you must be running Ubuntu 24.04 LTS Noble Numbat or 22.04 Jammy Jellyfish to upgrade to Landscape 24.04 LTS.

## Additional upgrade steps

After you’ve completed the basic upgrade instructions, you need to make some additional manual changes to finish your upgrade.

### Update `service.conf`

Add the following lines to your `service.conf` file. This is commonly located in `/etc/landscape/service.conf`.

```bash
[broker]
hostagent_virtual_host = landscape-hostagent
hostagent_task_queue = landscape-server-hostagent-task-queue

[grpc]
grpc.max_connection_age_ms = 2592000000 # 30 days

[hostagent-message-consumer]
threads = 1
stores = main account-1
```

### Update Apache config

In your Apache config file (commonly in `/etc/apache2/sites-available/landscape.conf`), you need to add the following RewriteRule.

```bash
RewriteRule ^/(new_dashboard.*) http://localhost:8080/$1 [P,L]
```
And edit the existing API RewriteRule to match the following:

```bash
RewriteRule ^/api/(.*) http://localhost:9080/api/$1 [P,L]
```

You can see a full Apache config example in our {ref}`how to configure the web server <how-to-heading-manual-install-configure-web-server>` guide.

To configure Windows Subsystem for Linux (WSL), you should also complete the steps in our {ref}`how-to-wsl-configure-landscape-beta` guide.

## Manual installations
If you're upgrading a Landscape Server instance that was manually installed (instead of Quickstart), you also need to complete the following steps. These changes are needed to access the new web portal introduced in Landscape 24.04 LTS.

- In your `service.conf` file, add an entry for `secret-token` in the `[landscape]` section and set it as a random string. You can set any string you want, but it should be reasonably long. You can use `openssl` to create a random string. For example, `openssl rand -base64 128 | tr -d '\n'`.
- Update your Apache vhost if it wasn't already auto-upgraded

