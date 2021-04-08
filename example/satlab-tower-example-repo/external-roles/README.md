# Purpose of External-Roles

## We had following problems:

* Sometimes Roles may update upstream causing failures for us if we pull those dynamically using requirements.yml
* There could be network issues in fetching roles dynamically for every run


## Solution:

Cache those roles in this directory and maintain working version of it in our repo.

### Advantages:

* No network failures fear
* No uncertain/unwanted changes introduced due to upstream development



# Usage

This section will be a live section that should be kept up-to-date about which roles are brought in and why + any other relevant info.
```
* Role: ovirt.vm-infra
  Installed from: Ansible Galaxy
  Usage: All RHV VM deployment playbooks use this role to conduct deployment. Hence this role is backbone for lot of our work.

* Role:  ovirt.repositories
  Installed from: Ansible Galaxy
  Usage: Originally used by nested RHV auto-deployment playbooks

* Role: ovirt.infra
  Installed from: Ansible Galaxy
  Usage: Originally used by nested RHV auto-deployment playbooks

* Role: ovirt.engine-setup
  Installed from: Ansible Galaxy
  Usage: Originally used by nested RHV auto-deployment playbooks

* Role: ome.nfs_mount
  Installed from: Ansible Galaxy
  Usage: Originally used to mount NFS on Tower VM during the fresh tower vm installation.

* Role: ericsysmin.chrony
  Installed from: Ansible Galaxy
  Usage: Part of setup-infra playbooks to setup chrony

* Role: ovirt.image-template
  Installed from: Ansible Galaxy
  Usage: Added for future use cases, around Interop testing
```
