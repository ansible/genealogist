## Description

Playbook used to setup a base RHEL image for use to deploy new infra-/env- enviroments manually or with the playbook `deploy-template`.

### Assumptions
* The target OS is RHEL
* The server was manually installed and is reachable with standard credential defaults.
* Keys have already been exchanged with the target hosts using `ssh-copy-id` for `root`.

#### setup-infra/setup-infra.yml

* Enable the SatLab RHEL service account
* Copies over the basic OS utilities and packages required for administration of SatLab nodes.
* Sets up `cloud-init` and copies in `/etc/cloud/cloud.cfg` to enable auto-deployment for `deploy-template.yml`

##### Example


```
$ ansible-playbook -i inventory -i 10.1.1.234, -l 10.1.1.234  -u root playbooks/setup-infra/setup-infra.yml
```
