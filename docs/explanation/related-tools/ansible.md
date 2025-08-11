# Related tools: Landscape and Ansible

A common question for new users, especially those with a background in RHEL, is how Landscape and Ansible relate to each other. This page describes the relationship between Landscape and Ansible.

Note that there is **no official integration** between Landscape and Ansible. But this doesn't mean they can't be used together in a complementary way.

## Overview

Landscape and Ansible are both tools used in systems management, but they serve different purposes.

**Landscape** is the centralized management and security platform specifically for Ubuntu. It has a web portal where you can centrally perform management tasks, such as security patching, compliance auditing, running custom scripts, editing user permissions, or managing packages on your client machines.

**Ansible** is an agentless automation tool used to define and apply a desired state on your servers. It's code-based, and uses YAML playbooks and SSH to configure software and orchestrate workflows across different operating systems. While it works on Ubuntu, it doesn't have native awareness of the Ubuntu-specific security ecosystem.

## Comparing Landscape and Ansible

| Feature/Aspect | Landscape | Ansible |
| :--- | :--- | :--- |
| **Main goal** | **Observe and manage state:** Continuously monitors the health, security, and compliance of your Ubuntu estate. | **Define and enforce state:** Configures servers to match a specific, desired state. |
| **Agent** | **Agent-based:** Landscape Client is installed on each managed instance and provides real-time data and control. | **Agentless:** Uses SSH for on-demand connections to execute tasks. |
| **Focus** | **Ubuntu:** Integrated with the Ubuntu ecosystem, including all official repositories, security notices (USNs), Livepatch, and Ubuntu Pro. | **Cross-platform:** A general-purpose tool designed to work across a wide variety of operating systems. |
| **User Interface** | **Web-based GUI and API:** Designed for interactive management via a web portal and integration via a REST API. | **CLI:** Executes playbooks (YAML files) from the command line. |

## How to use them together

While there is no official integration, a common workflow is to use Ansible for initial system setup and Landscape for ongoing management.

1. **Provisioning with Ansible**: Use an Ansible playbook to provision a server. The playbook defines the base configuration, installs necessary applications, and includes a final task to install and register the Landscape client.

2. **Ongoing management with Landscape**: After a machine is provisioned and registered, the ongoing administrative tasks are handled through the Landscape portal, such as: applying security patches, running compliance audits, and monitoring system performance.

This approach assigns the repeatable, initial setup to Ansible, while using Landscape for interactive monitoring and maintenance.

## Why add Landscape to an Ansible workflow?

Landscape provides several capabilities that complement an Ansible workflow:

- **Centralized status monitoring and reporting**: Landscape provides a persistent, dashboard-based view of your Ubuntu estate's status. Landscape collects data over time, which can be used to generate historical reports for security audits and compliance purposes.

- **Security notice integration**: Landscape integrates directly with Ubuntu's security data. Instead of only showing that a package update is available, Landscape provides context by linking the update to specific Ubuntu Security Notices (USNs) and the corresponding CVE severity levels.

- **Role-based access control (RBAC)**: Landscape's web portal includes Role-Based Access Control (RBAC). This feature allows for delegating specific tasks by granting users granular permissions. For example, a security team can be given read-only access to compliance data, while another user is granted permission to apply patches only to a specific group of machines. This allows for task delegation without providing direct SSH access to the individual machines.