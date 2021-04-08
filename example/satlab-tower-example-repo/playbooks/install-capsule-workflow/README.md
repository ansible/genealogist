Playbooks to Create a Satellite Template in Ansible Tower
=========================================================

This directory contains playbooks designed to be used together in a workflow in Ansible Tower using Ansible.

A template called `tpl-capsule-{{satellite_version}}-snap-{{snap_version}}` will be generated on the hypervisor (currently default to RHV).


Requirements
------------
In order to execute the playbooks successfully, an Ansible Tower workflow must be ran.

The playbooks in this directory are not designed or intended to be ran on command line.


How to use files in this directory in the Ansible Tower Workflow
----------------------------------
There are 5 playbooks in this directory designed to be ran in a single work flow ( `workflow-update-satellite-capsule-template` ) in Ansible Tower.

The playbooks, ran in parallel with `install-capsule-workflow`, all end in the same converged `set-stats-template-workflow` workflow are the following:

1) `../utils/deploye-template-baserhel7.yml` -- Deploys a RHEL template to install Satellite

2) `install-capsule-workflow.yml` -- Installs the Capsule RPM and all pre-requistes without a configuration installation of Capsule.

3) `../utils/save-template.yml`   -- Saves a template of the installed Capsule RPM as a template on the hypervisor (RHVM by default)

4) `../utils/remove-vm.yml`   -- Powers down the installed Satellite VM and saves a template able to be deployed later by anyone.

5) `../install-satellite-workflow/set-stats-template-workflow.yml` -- Sets the aggregated workflow branches into a single `set_stats` data structure called `template` for Jenkins to consume.

Example Execution commands
---------------------------

Log into the production Ansible Tower, infra-ansible-tower-01.infra.sat.rdu2.redhat.com, and run the `workflow-update-satellite-capsule-template` as an appropriately privledged user or excuted the appropriate Production Job Workflow from Satellite Jenkins.

License
-------

None

License
-------

None

Author Information
------------------

SatLab <satellite-lab-list@redhat.com>
