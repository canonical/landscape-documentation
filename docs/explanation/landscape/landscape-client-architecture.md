(explanation-client-architecture)=
# Landscape Client architecture

Landscape Client is the client-side component of the Landscape ecosystem.
It is made up of a collection of processes.
This document explains these processes and their purposes.

A Landscape Client has four main services:

  * [Watchdog](#watchdog) — initializes and supervises other long-running processes
  * [Broker](#broker) — exchanges messages with Landscape Server
  * [Monitor](#monitor) — collects information from the client
  * [Manager](#manager) — performs actions and applies side effects on the client

There are also important processes that run either periodically or on demand:

  * [Package reporter](#package-reporter) - reports the status of packages on the client
  * [Package changer](#package-changer) - applies package changes
  * [Config](#config) - configures the client
  * [Release upgrader](#release-upgrader) — upgrades the operating system to a new Ubuntu release

## Process description

Landscape Client has several processes that are essential to its functionality.
This section describes each process in detail.

### Watchdog

The Watchdog service serves as the entry point for Landscape Client.
It initializes other long-running processes (i.e. Broker, Monitor, and Manager).
It also monitors and restarts these services in case they become unresponsive.

### Broker

The Broker service communicates with Landscape Server in two ways.
It sends HTTP requests to the Landscape Server's message system service, relaying information and
receiving activities to be performed on the client.
It also periodically sends HTTP heartbeats to the Landscape Server ping service.
This serves both as a heartbeat and as notfication for pending messages from the server.

### Monitor

The Monitor service acts as a top-level scheduler for specific monitors.
A monitor can be thought of as a lightweight thread that periodically gathers information from the client (e.g. system temperature).
Once new information is collected, it is queued to be sent by the Broker service.
Monitors do not require elevated privileges (i.e. run as the `landscape` user).

### Manager

The Manager service acts as a top-level scheduler for specific managers.
A manager can mostly be thought of as a lightweight thread that executes activities received from the server (e.g. script execution).
Once an activity completes, its result is queued to be sent by the Broker service.
Managers require elevated privileges (i.e. run as `root`).

### Package reporter

The Package reporter process is a distinguised monitor that is periodically invoked by the Monitor service.
It collects information about the client's package states (installed, removed, ...) and reports these changes to the Landscape Server via the Broker service.
For a more detailed explanation, refer to [Package reporting internals](/explanation/features/explanation-package-reporting).

### Package changer

The Package changer process is a distinguished manager that is invoked when Landscape Server requests package
changes on the client.
It applies the requested package operations (installations, removals, ...) and queues the results to be relayed back to the server via the Broker service.

### Config

The Config process is used to configure the Landscape Client.
It is an interactive process that saves information required to connect to Landscape Server, along with other configuration values.
It is responsible for registering the client with Landscape Server.

### Release upgrader

The Release upgrader process is a distinguished manager that is invoked to perform an Ubuntu upgrade on the client.
Like the Package reporter and Package changer, its results are queued and sent via the Broker service.
