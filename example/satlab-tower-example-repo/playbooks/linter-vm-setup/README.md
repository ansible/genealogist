Playbooks to Deploy-configure Docker GitLab Runner
===================================================

This directory contains playbooks that can be used to deploy and configure a new VM with Docker and required GitLab runner configs.

Requirements
------------
In order to execute the playbooks successfully, you would want to review following two files:

* deploy-template-config.yml - This file contains all necessary variables to deploy a new VM on RHV using the template specified and resource configurations as well as Role specific variables for Linter role.


How to use files in this directory
----------------------------------
There is only 1 playbook in repo:
* main.yml - this playbook runs end-to-end and deploys-configures brand new VM as Docker GitLab Runner.

Example Execution commands
---------------------------

* To run end-to-end:
```
ansible-playbook playbooks/linter-vm-setup/main.yml
```

License
-------

BSD

Author Information
------------------

Kedar Kulkarni <kedar.kulkarni0@gmail.com>
