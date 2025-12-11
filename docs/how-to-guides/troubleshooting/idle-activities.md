(how-to-idle-activities)=
# How to troubleshoot idle activities

In some cases, activities in Landscape may stay idle longer than expected. There are many different causes for this issue. This guide describes some common factors that can lead to this behavior and some troubleshooting steps you can take.

Guidance on when to contact [Canonical Support](https://support-portal.canonical.com/) is also provided. Note that you'll need a Support contract to use our Support Portal.

## Background information

> See also: {ref}`explanation-activities`

There are two main activity states that can become stuck: **Queued** and **In progress**.

Queued activities can get stuck if the client is waiting to pick them up from the server, or if the server hasn't received a message from the client indicating the activity was picked up. This is often caused by either the client being too busy to perform the activity, a large message backlog, or the server being too busy to accept new messages from the client. Although there can be other underlying issues, such as no network connectivity.

In progress activities can get stuck when the client acknowledged the task but failed to send a response back. This can be caused by many different reasons, such as loss of connectivity, networking issues, misconfigurations, or the Landscape Client service restarting.

## Queued activities

If activities are queued for a **single client**, it's most likely an issue with that client machine or it's ability to connect to the server. For example, the `ping` location or other client-side networking could be misconfigured, or that client could be offline.

If activities are queued for **all clients**, it's most likely an issue with RabbitMQ on the server-side. You can check if RabbitMQ is running, its internal state, and if there are any authentication errors. Some guidance is provided here, but see the [RabbitMQ documentation](https://www.rabbitmq.com/docs) for more information.

To check if RabbitMQ is running, run:

```bash
systemctl status rabbitmq-server
```

To check {spellexception}`RabbitMQ’s` internal state:

```bash
rabbitmqctl report
```

And to check if there are any errors, view the logs in `var/log/rabbitmq`.

If you've investigated with these steps and still have issues with your activities, we recommend you contact [Support](https://support-portal.canonical.com/) because the underlying issues can have many different root causes. Note that you'll need a Support contract to use our Support Portal.

## In progress activities

If activities are stuck in progress, this means the client received the activity, but the client has not yet sent a response back to the server. This could be for many different reasons, such as a timeout, network issues, the Landscape Client service restarted, a large message backlog on the client, slow message processing on the server, or the activity taking longer than expected to complete.

For those with Support contracts, we recommend you contact [Support](https://support-portal.canonical.com/) if you observe idle "in progress" activities because the underlying issues can have many different root causes.
