subscription-manager
=========

Ansible role using the `redhat_subscription` public module to activate the SatLab RHEL account.

Requirements
------------

None.

Role Variables
--------------

The `var/credentials` is an Ansible vault that will be using `vault_admin_secret` password to unlock the vault.

This credential is maintained within Ansible Tower and should be included as a credential, `satlab-tower-vault`, with the `vault_id` of `admin` to the calling
Ansible Tower `job_template`.

Dependencies
------------

The RHEL user and group are still active in the `inventory/group_var/all/credentials.yml`.`

Example Playbook
----------------

This playbook is only designed to run on RHEL releases.

Example:

    - hosts: servers
      roles:
         - role: subscription-manager
         when: ansible_distribution == 'RedHat'

License
-------

See underlying module for license inheritance.

Author Information
------------------

SatelliteQE
