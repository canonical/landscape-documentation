(explanation-client-architecture)=
# Landscape Client architecture

Landscape Client is the client-side component of the Landscape ecosystem. It is made up of a collection of processes. This document explains these processes and their purposes.

A Landscape Client has four main services:

  * [Broker](#broker) - exchanges messages with Landscape Server
  * [Manager](#manager) - performs actions and applies side effects on the client
  * [Monitor](#monitor) - collects information from the client
  * [Watchdog](#watchdog) - initializes and supervises other long-running processes

There are also important processes that run either periodically or on demand:

  * [Config](#config) - configures the client
  * [Package changer](#package-changer) - applies package changes
  * [Package reporter](#package-reporter) - reports the status of packages on the client
  * [Release upgrade manager](#release-upgrade-manager) - upgrades the operating system to a new Ubuntu release

## Process description

Landscape Client has several processes that are essential to its functionality. This section describes each process in detail.

### Watchdog

The Watchdog service serves as the entry point for Landscape Client. It initializes other long-running processes (i.e. Broker, Monitor, and Manager). It also monitors and restarts these services in case they become unresponsive.

### Broker

The Broker service communicates with Landscape Server in two ways. It sends HTTP requests to the Landscape Server's message system service, relaying information and receiving activities to be performed on the client. It also periodically sends HTTP heartbeats to the Landscape Server ping service. This serves both as a heartbeat and as notification for pending messages from the server.

### Monitor

The Monitor service acts as a top-level scheduler for specific monitors. A monitor can be thought of as a lightweight thread that periodically gathers information from the client (e.g. system temperature). Once new information is collected, it is queued to be sent by the Broker service. Monitors do not require elevated privileges (i.e. run as the `landscape` user).

### Manager

The Manager service acts as a top-level scheduler for specific managers. A manager can mostly be thought of as a lightweight thread that executes activities received from the server (e.g. script execution). Once an activity completes, its result is queued to be sent by the Broker service. Managers require elevated privileges (i.e. run as `root`).

### Package reporter

The Package reporter process is a distinguished monitor that is periodically invoked by the Monitor service. It collects information about the client's {ref}`explanation-package-reporting-package-state` and reports these changes to the Landscape Server via the Broker service. For a more detailed explanation, refer to {ref}`Package reporting internals <explanation-package-reporting>`.

### Package changer

The Package changer process is a distinguished manager that is invoked when Landscape Server requests package changes on the client. It applies the requested package operations (such as installations, removals, etc.) and queues the results to be relayed back to the server via the Broker service.

### Config

The Config process is used to configure the Landscape Client. It's responsible for registering the client with Landscape Server. It is an interactive process that saves information required to connect to Landscape Server, along with other configuration values. For more details, refer to {ref}`how-to-configure-landscape-client`.

### Release upgrade manager

The Release upgrade manager process is a distinguished manager that is invoked to perform an Ubuntu upgrade on the client. Like the Package reporter and Package changer, its results are queued and sent via the Broker service.
