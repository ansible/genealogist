check-sla-limit
===============

This role checks number of already deployed VMs for an user, and fails if the number is higher
than the limit.

Requirements
------------

None

Role Variables
--------------

- `sla_vm_limits` - a dictionary containing default VM limit and custom limit for specific users.
The dictionary **must** always contain the key `default`, which defines the general limit.
Any other keys are treated as user names, and their values are used as limit for the specific user.
See `defaults` for an example.

Dependencies
------------

Requires sla/generate-sla-stats to be present and run first, as it is defined as a dependency.


License
-------

BSD

Author Information
------------------

SatLab Admin
