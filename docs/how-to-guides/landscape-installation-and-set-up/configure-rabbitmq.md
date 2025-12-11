(how-to-configure-rabbitmq)=
# How to configure RabbitMQ for Jammy 22.04 (or later)

RabbitMQ is configured with a default timeout of 30 minutes in Jammy 22.04 or later. This timeout can cause issues when installing Landscape Server or syncing repository mirrors. Any tasks that run longer than 30 minutes without reporting any progress or updates are automatically flagged as failed. RabbitMQ then disconnects from the task due to this perceived failure, and the system assigns a “failed” status to the entire operation. The error message for this issue is `No transition: delivered=>delivered`.

If you encounter this issue, try increasing or disabling the timeout and re-run your task. If you’re syncing a repository mirror, you may also need to delete a lock file for your task to re-run successfully.

## Configure the RabbitMQ timeout to be longer than 30 minutes

The default timeout is set in milliseconds at 1,800,000 milli seconds (30 minutes). To increase it to five hours:

1. Create a new file in `/etc/rabbitmq` and name it `rabbitmq`:

    ```bash
    sudo touch /etc/rabbitmq/rabbitmq
    ```

2. Add the variable `consumer_timeout` in that file (`/etc/rabbitmq/rabbitmq`) and set it to `18,000,000` (5 hours) or longer:

    ```bash
    consumer_timeout = 18000000
    ```

3. Restart RabbitMQ:

    ```bash
    systemctl restart rabbitmq-server.service
    ```

4. (Optional) Verify the timeout is set as expected:

    ```bash
    sudo rabbitmq-diagnostics environment | grep consumer_timeout
    ```

Now you can re-run your original task. If you’re syncing a repository mirror, you may need to delete a lock file for the task to re-run successfully. For more information, see {ref}`how to delete the lock file <how-to-header-delete-lock-file>`.

## Disable the RabbitMQ timeout

If you don’t want RabbitMQ to have a timeout at all, you can fully disable it:

1. Create a new file in `/etc/rabbitmq` and name it `advanced.config`:

    ```bash
    sudo touch /etc/rabbitmq/advanced.config
    ```

2. Add the following lines in that file (`/etc/rabbitmq/advanced.config`):

    ```bash
    [
      {rabbit, [
        {consumer_timeout, undefined}
      ]}
    ].
    ```

3. Restart RabbitMQ:

    ```bash
    systemctl restart rabbitmq-server.service
    ```

4. (Optional) Verify the timeout is set as expected:

    ```bash
    sudo rabbitmq-diagnostics environment | grep consumer_timeout
    ```

Now you can re-run your original task. If you’re syncing a repository mirror, you may need to delete a lock file for the task to re-run successfully. For more information, see {ref}`how to delete the lock file <how-to-header-delete-lock-file>`.

(how-to-header-delete-lock-file)=
## (If necessary) Delete the lock file

If you’re syncing a repository mirror, you may get the following error when you re-run your task:

```bash
b"The lock file './db/lockfile' already exists. There might be another instance with the\r\nsame database dir running. To avoid locking overhead, only one process\r\ncan access the database at the same time. Do not delete the lock file unless\r\nyou are sure no other version is still running!\r\nThere have been errors!\r\n"
```

The lock file is set while a sync operation is running to avoid changes to the repository on disk. You can delete it without issue if you’re re-running the same task. The full file path is `/var/lib/landscape/landscape-repository/standalone/{REPOSITORY_NAME}/db/lockfile`, but change `{REPOSITORY_NAME}` to the name you assigned for that repository (distribution). For example, `/var/lib/landscape/landscape-repository/standalone/ubuntu-main/db/lockfile`.

To delete the file:

```bash
sudo rm /var/lib/landscape/landscape-repository/standalone/ubuntu-main/db/lockfile
```
