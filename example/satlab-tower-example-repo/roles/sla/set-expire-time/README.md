set-expire-time
===============

Used for setting the expire time of a VM. Must be run on Ansible Tower, as it uses its fact
caching persistence.

For more details see https://docs.engineering.redhat.com/display/SQE/SatLab+SLAs

Requirements
------------

Ansible Tower

Role Variables
--------------

- `target_vm` - name of the VM that should be extended. This is not used directly by the role, but it must be set for the `playbooks/sla/set-expire-time.yml`
to run properly
- `new_expire_time` - the new expire time to be set for a VM. Three different formats are
supported:
    - epoch timestamp in seconds
    - relative time in seconds
    - human friendly format

    Again, for more info see https://docs.engineering.redhat.com/display/SQE/SatLab+SLAs

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.


License
-------

BSD

Author Information
------------------

SatLab Admin
