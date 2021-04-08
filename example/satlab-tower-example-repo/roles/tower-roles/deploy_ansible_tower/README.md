Role Name
=========

This is a role written for Ansible Tower/AWX Deployment.

Requirements
------------

It is a good idea to use CentOS/Fedora system as you don't need to have subscriptions etc(which you do need to have on RHEL)

Role Variables
--------------

Following are variables set in the Defaults/main.yml which you may override.
tower_min_memory_mb: This variable will be used in pre_checks to make sure we have at least this much memory on the VM.
tower_min_vcpus: This variable will be used in pre_checks to make sure we have at least this much number of CPUs on the VM.
tower_min_disk_gb: This variable will be used in pre_checks to make sure we have at least this much storage on the VM in `/` mountpoint.
tower_setup_bundle_tar_url: Release URL for ansible tower like follows: https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-w.x.y-1.el7.tar.gz
tower_admin_password: Defaults to changeme
tower_pg_password: Defaults to changeme
tower_rabbitmq_password: Defaults to changeme
tower_license: if this variable is defined, role would try to add license to tower. Recommended to put the tower_license in encrypted file.


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:


`- name: Deploy tower on my_tower_vms
  hosts: my_tower_vms
  roles:
    - deploy_ansible_tower`

License
-------

BSD

Author Information
------------------

contact me on GitHub (@kedark3) for help.
