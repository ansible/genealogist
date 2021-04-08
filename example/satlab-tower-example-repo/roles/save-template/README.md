save-template
=============

This role creates a RHV template from a given VM.

Requirements
------------

Ansible 2.8+

Role Variables
--------------

- *source_vm*: name of the VM to be used as template source
- *target_template*: name of the template to be created/updated
- *seal_template*: should we seal the template (yes by default)
- *engine_fqdn*: which RHV will be used (infra-rhvm-02.infra.sat.rdu2.redhat.com by default)
- *engine_user*: RHV user (should be read from inventory vars)
- *engine_password*: RHV pass ((should be read from inventory vars))
- *snap_version*: name of the sub-version of the template ("SNAP1" by default)
- *wait_timeout*: how long to wait in seconds for template save to be finished (360 by default)

Dependencies
------------

None

Example Playbook
----------------

```
---
- name: Save a template on RHVM
  hosts: localhost
  gather_facts: true

  vars:
    engine_fqdn: infra-rhvm-02.infra.sat.rdu2.redhat.com
    source_vm: rdrazny-rhel-7.7-latest-1582717390-deployrole
    target_template: rdrazny-template-save-role-test

  roles:
    - save-template
```
License
-------

BSD

Author Information
------------------

Radovan Drazny (rdrazny@redhat.com)
Satellite QE
