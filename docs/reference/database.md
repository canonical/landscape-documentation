(reference-database)=
# Database

## Database users

Landscape defines two categories of database users:

- **Users**: Can read and write data in the database.
- **Superusers**: In addition to read and write access, they can also perform schema changes.

Most Landscape deployments need the following users:

- `landscape`: User with read and write access to all databases.
- `landscape_maintenance`: User with read and write access to all databases.
- `landscape_superuser`: Superuser with read and write access to all databases, and permission to apply schema changes to any database.

For details on configuring these users in a manual installation of Landscape, see {ref}```the `service.conf` reference <reference-service-conf>```. Landscape Quickstart creates these users by default. Charmed deployments will use the default `postgres` superuser if one is not provided to the Landscape charm.

```{note}
If the PostgreSQL `set_user` extension is available, Landscape authenticates to the database using the `landscape_maintenance` role instead of `landscape_superuser` when performing schema updates. After authentication, Landscape switches the session to `landscape_superuser`.
```

## Database tables

Each database managed by Landscape contains a defined set of tables, as listed below:

### `account_1`

- `account_entity_data`
- `account_twin`
- `activity`
- `activity_child_event`
- `activity_group`
- `activity_info`
- `activity_ordering`
- `activity_parent`
- `activity_parent_access`
- `activity_request`
- `add_group_member_request`
- `add_juju_charm_request`
- `add_juju_machine_request`
- `add_juju_relation_request`
- `add_juju_unit_request`
- `apt_source`
- `apt_source_gpg_key`
- `attachment`
- `availability_zone`
- `change_package_profile_request`
- `change_package_request`
- `change_upgrade_profile_request`
- `child_instance_profile`
- `cloud`
- `computer_group`
- `computer_group_item`
- `computer_group_tag`
- `computer_twin`
- `configure_availability_zones_zone`
- `configure_availability_zones_zone_machine`
- `configure_vip_request`
- `create_glance_image_request`
- `create_group_request`
- `create_project_request`
- `custom_graph`
- `delete_user_request`
- `deploy_juju_service_request`
- `disable_nova_services_request`
- `distribution`
- `edit_user_request`
- `enable_nova_services_request`
- `event_log_entry`
- `execute_script_attachment`
- `execute_script_request`
- `gpg_key`
- `incurred_cost`
- `juju_action`
- `juju_action_request`
- `juju_application`
- `juju_bootstrap_request`
- `juju_machine`
- `juju_model`
- `juju_model_destroy_application_request`
- `juju_run_on_all_machines_request`
- `juju_run_request`
- `juju_service_set_request`
- `juju_unit`
- `lock_user_request`
- `maas_server`
- `maas_target_machine`
- `node_maintenance_request`
- `openstack_region_request`
- `openstack_token`
- `outbox`
- `package_profile`
- `package_profile_constraint`
- `patch`
- `payment`
- `pocket`
- `pocket_upload_gpg_key`
- `region`
- `region_hypervisor`
- `region_log`
- `region_machine`
- `region_request_data`
- `registration_otp`
- `release_upgrade_request`
- `removal_profile`
- `remove_group_member_request`
- `repository_profile`
- `repository_profile_apt_source`
- `repository_profile_pocket`
- `resynchronize_request`
- `rule`
- `rule_state`
- `rule_state_notification`
- `rule_subscription`
- `sample_account_rule`
- `sample_computer_rule`
- `saved_search`
- `scheduled_activity_profile`
- `script`
- `script_attachment`
- `script_profile`
- `script_profile_limits`
- `script_profile_run`
- `script_version`
- `series`
- `signal_process_request`
- `stored_stub_request`
- `sync_pocket_request`
- `tenant_network_setup_request`
- `unlock_user_request`
- `upgrade_profile`
- `upload`
- `usg_history`
- `usg_profile`
- `wsl_feature_limit`

### `knowledge`

- `article`
- `article_category`
- `article_view`
- `article_vote`
- `attachment`
- `category`
- `patch`

### `main`

- `access_context`
- `account`
- `account_invitation`
- `account_oidc_configuration`
- `api_credentials`
- `autoinstall_file`
- `cloud_init`
- `computer`
- `computer_autoinstall_provision`
- `computer_contract`
- `computer_license`
- `computer_message_type`
- `computer_relationship`
- `computer_selection_data`
- `computer_status`
- `computer_tag`
- `computer_utilisation`
- `contract`
- `distributed_lock`
- `distribution`
- `employee`
- `employee_computer`
- `employee_group`
- `employee_group_membership`
- `enabled_feature`
- `google_service_account`
- `installed_snap`
- `invitation_role`
- `lds_available_release`
- `lds_license`
- `lds_release`
- `lds_script_execution_log`
- `license`
- `license_lds_license`
- `message_type`
- `meta_release`
- `oidc_authn_configuration`
- `oidc_group_import_session`
- `oidc_issuer`
- `password_recovery`
- `patch`
- `pending_computer`
- `person`
- `person_access`
- `person_account`
- `person_computer`
- `person_oidc_identity`
- `ping_server`
- `ping_time`
- `removed_account_name`
- `role`
- `role_access_context`
- `role_permission`
- `role_person`
- `salesforce_activated_asset`
- `salesforce_user`
- `server_identity`
- `snap`
- `snap_publisher`
- `staged_oidc_group`
- `stored_secret`
- `system_configuration`
- `tag`
- `trial_account`
- `ubuntu_installer_attach_session`
- `utility_cost`
- `utility_credit`
- `vat_rate`
- `wsl_instance`

### `package`

- `cve`
- `name`
- `package`
- `package_binary`
- `package_lock`
- `patch`
- `usn`

### `resource_1`

- `active_process`
- `annotation`
- `ceph_usage`
- `cloud_instance_metadata`
- `computer_apt_preferences_file`
- `computer_group`
- `computer_packages`
- `computer_packages_buffer`
- `computer_twin`
- `computer_user`
- `computer_user_group`
- `cpu_usage`
- `custom_graph_data`
- `custom_graph_data_point`
- `free_space`
- `hardware_info`
- `hardware_info_key`
- `historic_process`
- `keystone_token`
- `load_average`
- `memory_info`
- `message`
- `message_info`
- `mount_info`
- `network_device`
- `network_traffic`
- `package_reporter_result`
- `patch`
- `processor`
- `reboot_required_info`
- `swift_usage`
- `temperature`
- `thermal_zone`
- `usn_issue`

### `session`

- `openid_association`
- `openid_nonce`
- `patch`
- `session_data`
- `session_pkg_data`
