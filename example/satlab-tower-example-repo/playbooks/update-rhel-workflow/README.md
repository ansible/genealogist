Playbooks to Update RHEL Templates in Ansible Tower
=========================================================

This directory contains playbooks designed to be used together in a workflow in Ansible Tower using Ansible.

A templates called `tpl-rhel-{{rhel_version}}-latest` will be generated on the hypervisor (currently default to RHV).

Requirements
------------
In order to execute the playbooks successfully, an Ansible Tower workflow must be ran.

The playbooks in this directory are not designed or intended to be ran on command line.


How to use files in this directory in the Ansible Tower Workflow
----------------------------------
There are 3 playbooks in this directory designed to be ran in a single work flow ( `workflow-update-rhel-template` ) in Ansible Tower.

The playbooks are the following:

1) `../utils/deploye-template-baserhel7.yml` -- Deploys a RHEL template update
2) `../setup-infra/setup-infra.yml`          -- Updates the RHEL template and ensures Satlab Admin utils are installed on the template
3) `../utils/save-template.yml`   -- Saves a template of the updated RHEL as a template on the hypervisor (RHVM by default)
4) `../utils/remove-vm.yml`   -- Powers down the installed Satellite VM and saves a template able to be deployed later by anyone.
5) `set-stats-template-workflow.yml` -- Sets a single `set_stats` data structure called `template` for Jenkins to consume.

Example Execution commands
---------------------------

Log into the production Ansible Tower, infra-ansible-tower-01.infra.sat.rdu2.redhat.com, and run the `workflow-update-rhel-template` as an appropriately privileged user or executed the appropriate Production Job Workflow from Satellite Jenkins.

License
-------

None

Author Information
------------------

SatLab <satellite-lab-list@redhat.com>
