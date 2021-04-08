Playbooks Utilies Used by Ansible Playbooks and Workflows within Ansible Tower
==============================================================================

This directory contains playbooks that should be common actions used between many workflows.

Utility Playbooks
-----------------

The following are the utility playbooks within this directory:

* `deploy-configs`    -- Configurations used by commond `deploy-template-<application>.yml` to deploy templtes commonly on the hypervisor. Placed here as most deploys should be using a common or centralized version. This makes it easy to make changes for resource allocation to deployment or creation of VMs.
* `deploy-template-baserhel7.yml` -- Deployment configuration used to deploy a common base rhel vm.
* `remove-vm.yml`     -- Remove a target VM
* `save-template.yml` -- Save a target VM template
* `set-stats.yml`     -- Define the set-stats with data structure `data`

How to use files in this directory
----------------------------------
Within an Ansible Tower Workflow, the above Utility playbooks should be already setup as `job_templates`.

These templates can be utilized within any Ansible Tower Workflow to complete the simplex actions by each of the above playbooks.

Example Execution Workflows
---------------------------

* For all Utilities, please see either Ansible Tower Workflow `workflow-update-rhel-template` or `workflow-update-satellite-capsule-template` for examples of usage.

License
-------

None

Author Information
------------------

SatLab <satellite-lab-list@redhat.com>
