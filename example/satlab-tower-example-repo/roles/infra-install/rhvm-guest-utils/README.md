Role Name
=========

A role to configure RHVM guests with the appropriate utilities so all RHVM features on the guest function.

Requirements
------------

Guest is deployed.

Role Variables
--------------

None.

Dependencies
------------

None.

Example Playbook
----------------

Example:

    - hosts: servers
      roles:
         - role: rhvm-guest-utils

License
-------

See underlying module for license inheritance.

Author Information
------------------

SatelliteQE
