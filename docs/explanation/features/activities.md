(explanation-activities)=
# Activities

Landscape tracks the progress of various tasks using activities. There are two types of activities: client activities and server activities. This document will explain how each type of activity is tracked and their possible states.

## Client activities

Client activities are tasks that execute on Landscape Client. Examples include {ref}`remote script execution <explanation-remote-script-execution>`. They are processed by the `message-system` when an instance exchanges messages with Landscape Server.

### Client activity states

Activities can start in the `Queued`, `Scheduled`, `Waiting`, or `Blocked` states.

- `Queued`: Activity will run the next time the client exchanges messages. Can transition to `In Progress`, `Canceled`, or `Blocked`.
- `Scheduled`: Activity will run at a future time. Can transition to `In Progress` or `Canceled`.
- `Waiting`: Activity will not run until another activity completes or reaches a progress threshold. Can transition to `Queued`, `In Progress`, or `Canceled`.
- `Blocked`: Activity is paused (often awaiting admin approval). Can transition to `Queued`, `Canceled`, or `Waiting`.
- `In Progress`: Activity has been sent to the client. Can transition to `Failed`, `Succeeded`, or `Canceled`.
- `Failed`: Landscape Client reported an error while executing. This is a final state.
- `Canceled`: Activity was stopped before completion. If the activity was canceled during execution on Landscape Client, it remains `Canceled` until Landscape Client reports the activity result.
- `Succeeded`: Landscape Client reported a successful execution. This is a final state.

### Life cycle of a client activity

1. An activity is created for an instance (e.g., by an admin action or scheduled profile).
1. The instance starts a message exchange with Landscape Server.
1. Landscape moves the activity from `Queued` or `Scheduled` to `In Progress`.
1. The activity is sent to the instance as a message containing an `operation-id`.
1. Landscape Client stores the message metadata and calls the corresponding handler to execute the activity.
1. Once done, Landscape Client creates an `operation-result` message containing the same `operation-id` and the result.
1. The instance exchanges messages with Landscape Server again.
1. Landscape Server receives the `operation-result` and updates the activity's status to `Succeeded` or `Failed`.

## Server activities

Server activities run on Landscape Server without interacting with Landscape Client. Examples include {ref}`downloading security profile reports <reference-rest-api-security-profiles>`. These activities are placed into a RabbitMQ queue and are processed by the `job-handler` service.

### Server activity states

Activities can start in the `Queued`, `Scheduled`, `Waiting`, or `Blocked` states.

- `Queued`: Activity will run as soon as the `job-handler` service consumes this activity from the queue. Can transition to `In Progress`, `Canceled`, or `Blocked`.
- `Scheduled`: Activity will run at a future time. Can transition to `Queued`, `In Progress`, or `Canceled`.
- `Waiting`: Activity will not run until another activity completes or reaches a progress threshold. Can transition to `Queued`, `In Progress`, or `Canceled`.
- `Blocked`: Activity is paused (often awaiting admin approval). Can transition to `Queued`, `Canceled`, or `Waiting`.
- `In Progress`: Activity is running on the job handler. Can transition to `Failed`, `Succeeded`, or `Canceled`.
- `Failed`: `job-handler` encountered an error while executing the activity. This is a final state.
- `Canceled`: Activity was stopped before completion. This is a final state.
- `Succeeded`: Activity completed successfully. This is a final state.

### Life cycle of a server activity

1. An activity is created (e.g., by an admin action or scheduled profile) and added to a RabbitMQ queue.
1. The `job-handler` consumes the activity from the queue and moves the activity from `Queued` or `Scheduled` to `In Progress`.
1. The `job-handler` completes the activity and updates the status to `Succeeded` or `Failed`.
