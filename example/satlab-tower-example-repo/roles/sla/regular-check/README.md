regular-check
=============

The SLA regular check that performs shutdown and removal of expired VMs. For more info see
https://docs.engineering.redhat.com/display/SQE/SatLab+SLAs

Requirements
------------

Must be run on Ansible Tower, as it makes a use of its fact caching persistence.

Role Variables
--------------

- `sla_shutdown_period`: Together with `sla_shutdown_period_unit` defines for how long after
its expire time will the VM be kept around after it was shutdonw by SLA. Default is `3`
- `sla_shutdown_period_unit`: Length of the period for `sla_shutdown_period` in seconds.
The final number is computed as `sla_shutdown_period * sla_shutdown_period_unit`.
The default is 86400 (1 day). When put together, this means default is 3 days
- `expiration_warning_period`: How long before the expire time will be the VM reported
as "expiring soon". Default is 1.
- `expiration_warning_period_unit`: Lenght of the period for `expiration_warning_period`
. Default is 86400 (1 day).
- `default_expire` - default expire period set if a VM without `expire_date` set is
encountered during the check. Default is 259200.

Dependencies
------------

- `generate-sla-stats`

License
-------

BSD

Author Information
------------------

SatLab Admin
