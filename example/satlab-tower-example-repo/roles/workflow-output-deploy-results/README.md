workflow-output-deploy-results
=========

This role outputs formatted information about machines deployed by the deploy-base-role.
Supports printing to the console in a similar manner as the legacy SatLab
workflow-output-deploy-results, but will also supports exporting by Ansible *set_stats*.
This supports multi-machine deployment as well, including multiple separate tags.

Requirements
------------

This role should be used only in the conjunction with deploy-base-role, as it is dependant on data it produces.

Role Variables
--------------

- *group_pattern* - Pattern that is used for detection of RHV created tag groups. This is "ovirt_tag_*" by default
- *print_to_console* - if true, the information about created machines is printed to the console. Default is True.

Dependencies
------------

None

Example Playbook
----------------

```text
- name: Deploying a Template on RHVM
  hosts: localhost
  gather_facts: true

  roles:
    - role: workflow-output-deploy-results
      vars:
        vm_definition: deploy-configs/satellite67.yml

- name: Output deployed hosts
  hosts: localhost
  gather_facts: false

  roles:
    - workflow-output-deploy-results

```

Example output
--------------

```text
TASK [workflow-output-deploy-results : Print the final output] *******************************************************
Saturday 29 February 2020  14:59:07 +0100 (0:00:00.685)       0:02:21.972 *****
ok: [localhost] => {
    "msg": [
        "List of VMs deployed:",
        "Tag baserhel_group_one:",
        "    VM name: rdrazny-rhel-7.7-latest-1582984607-deployrole_1 FQDN: dhcp-2-91.vms.sat.rdu2.redhat.com",
        "    VM name: rdrazny-rhel-7.7-latest-1582984607-deployrole_4 FQDN: dhcp-2-85.vms.sat.rdu2.redhat.com",
        "    VM name: rdrazny-rhel-7.7-latest-1582984607-deployrole_5 FQDN: dhcp-3-77.vms.sat.rdu2.redhat.com",
        "Tag baserhel_group_two:",
        "    VM name: rdrazny-rhel-7.7-latest-1582984607-deployrole_2 FQDN: dhcp-3-50.vms.sat.rdu2.redhat.com",
        "    VM name: rdrazny-rhel-7.7-latest-1582984607-deployrole_3 FQDN: dhcp-3-61.vms.sat.rdu2.redhat.com"
    ]

```
License
-------

BSD

Author Information
------------------

Radovan Drazny (rdrazny@redhat.com)
Satellite QE
