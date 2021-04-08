Role Name
=========

This role removes a given VM.

Requirements
------------

Ansible 2.8+

Additional Information
--------------
This role is designed to work on one vm at a time, not lists.

There is error checking within the role to ensure:
* There is actually a vm returned to be removed, else error.
* There is a `source_vm` name that is given actually exists, else error.
* If the delete protection is on and `force_delete` is not set, error.

The `Get VM Info` that returns a list is only used for error checking and not generating an iterative list of VMs to remove from the return.

If this role is desired to be updated to enhance this functionality, please do so. At the time of creation, that was not required functionality for this role.

Role Variables
--------------

* source_vm: name of the VM to be used as template source
* engine_fqdn: which RHV will be used (infra-rhvm-02.infra.sat.rdu2.redhat.com by default)
* engine_user: RHV user (should be read from inventory vars)
* engine_password: RHV pass ((should be read from inventory vars))
* force_delete:
   * `False` (default), will not override delete protection before deleting the VM. This may result in a failure of the playbook, which is correct behavior to protect the VM
   * `True` will verify delete protection is off before deleting the VM

Dependencies
------------

None

Example Playbook
----------------

        hosts: localhost
        vars:
          # `engine_user` and `engine_password` is defined in inventory
          # `force_delete` to ensure the VM is removed.
          vars:
          - engine_fqdn: infra-rhvm-02.infra.sat.rdu2.redhat.com
          - source_vm: "{{ hostvars['localhost']['ovirt_vms'][0]['name'] }}"
          - force_delete: True

        roles:
          - remove-vm


License
-------

None

Author Information
------------------

Satlab Admin
