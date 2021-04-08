Playbooks to Create a Satellite Template in Ansible Tower
=========================================================

This directory contains playbooks designed to be ran on the command line with `ansible-playbook` to create a lite version of Satellite on RHVM.

This was the original and PoC playbook to create the initial templates for RHVM.

This playbook is actively being deprecated for the Ansible Tower Workflow using playbooks from `install-satellite-workflow` to run a Workflow on Ansible Tower.

Requirements
------------
In order to execute the playbooks successfully, a pytyhon virtual environment must be installed.

Please see the documentation for this human workflow here (Specifcally linked to Version 41):

* https://docs.engineering.redhat.com/pages/viewpage.action?pageId=115490743

How to use files in this directory in the Ansible Tower Workflow
----------------------------------

There is one configuration file and one playbook in this durectory.

* `deplopy-template-config.yml` -- Use the define the parameters required to deploy a RHEL template on the RHVM used to install Satellite
* `install-satellite.yml` -- installs Satellite onto the deployed template.

The saving of the VM created as a template and removal of that VM must be done by hand.

All Satellite templates are saved a sub-versions of the initial Satellite template for the X.Y. Version in RHVM

Deprecation
-----------
This playbook is actively being deprecated for the Ansible Tower Workflow using playbooks from `install-satellite-workflow` to run a Workflow on Ansible Tower.


Example Execution commands
---------------------------

* To deploy a RHEL template and Install satellite:

```
ansible-playbook playbooks/create-satellite-template/install-satellite.yml -e "sat_version=6.7.0"
```

License
-------

None

Author Information
------------------

"SatLab" <satellite-lab-list@redhat.com>
