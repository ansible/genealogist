Playbooks to Create a Satellite Template in Ansible Tower
=========================================================

This directory contains playbooks designed to be used together in a workflow in Ansible Tower using Ansible.

Any playbooks here are used to enable quick and easy testing of workflows or job templates for Jenkins CI.

Requirements
------------
In order to execute the playbooks successfully, an Ansible Tower workflow must be ran.

The playbooks in this directory are not designed or intended to be ran on command line.


How to use files in this directory in the Ansible Tower Workflow
----------------------------------
* `jenkins-set-stats-association` -- Requested in SATQE-9094, this is a simple playbook that will take the input variables, assign them to a dictionary called `JENKINS_EXPORT` and pass that out to set stats. This enables quick pipeline testing without having to wait for the deployment and creation of actual templates.

Example Execution commands
---------------------------

Log into the production Ansible Tower, infra-ansible-tower-01.infra.sat.rdu2.redhat.com, and run the `workflow-jenkins-test-workflow` as an appropriately privileged user or executed the appropriate Production Job Workflow from Satellite Jenkins.

License
-------

None

Author Information
------------------

SatLab <satellite-lab-list@redhat.com>
