Playbooks to Create a Katello Template
=======================================
This directory contains playbooks that can be used to deploy and configure a Katello template. It deploys a new RHEL VM from a template on Red Hat
Virtualization.

ToDo
----
The playbook within was done as a quick one-off to see if this was a useful effort to continue.

At this time, this monolithic playbook would need to be broken apart and used in a job template and workflow.

Until that time, this playbook is designed only to work from the CLI.

Requirements
------------

A `satlab` functioning venv that can deploy RHVM machines.

For more information, please see:

* https://docs.engineering.redhat.com/display/SQE/HowTo+Deploy+a+Template+in+Satlab#HowToDeployaTemplateinSatlab-Usingapythonvenv(preferred)


How to use files in this directory
----------------------------------

The playbook `install-katello` is meant to be a multi-play playbook to deploy an updated `tpl-katello-latest` playbook where katello could then be installed.

Therefore, as long as the base rhel template is available and the version of vargrant defined in the `configure-katello` role is available, this playbook runs with minimal inputs.


Example Execution commands
---------------------------

* To run end-to-end:
```
ansible-playbook playbooks/create-katello-template/install-katello.yml
```

License
-------

None

Author Information
------------------

SatLab <satellite-lab-list@redhat.com>
