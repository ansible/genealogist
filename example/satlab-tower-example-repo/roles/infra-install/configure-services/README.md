configure-services
=========

Role to configure all adminstrative tools required to manage SatLab infra- servers and server instances.

Requirements
------------

None.

Role Variables
--------------

None.

Dependencies
------------

For RHEL instances, a subscription has already been enabled with `subscription-manager`.

For other distributions, the appropriate repositories have been enabled.

Example Playbook
----------------

Example:

    - hosts: servers
      roles:
         - role: configure-services

License
-------

See underlying module for license inheritance.

Author Information
------------------

SatelliteQE
