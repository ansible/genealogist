deploy-base-sla
===============

Copy of `satlab-ansible/deploy/deploy-base` role with SLA check added as a metadata dependency.
This should be used as a default deploy role for RHV VMs instead of the legacy
`playbooks/deploy-template/deploy-template.yml` playbook.

Requirements
------------
- `generate-sla-stats`
- `check-sla-limit`
- `ovirt.vm-infra`

Role Variables
--------------

Check docs for ovirt.vm-infra.


License
-------

BSD

Author Information
------------------

SatLab Admin
