# Ansible Genealogist
#### NOTE: Read this document before starting.
## Summary
This project is about building a mechanism to detect when a change in an Ansible component will have cascading changes throughout the user’s Ansible workspace. The most notable example would be an Ansible Tower Project/Credentials(or any other assets), as well as Playbooks/Roles change causing potential changes in Tower Workflows and singular Job Templates. 

### Glossary of Ansible Terms
- Playbook - YAML file that Ansible can use to run arbitrary tasks. 
- Project - SCM repo that has a bunch of playbook files. Ansible Tower can fetch a Project and get a list of Playbooks within it.
- Job Template - Also known as a JT. Tower’s basic functionality. It sources a project and picks a playbook, then adds a bunch of wrapper configuration.
- Workflow - A big chain of Job Templates. Also called “Workflow Job Templates”, or WFJTs (yes, it’s a mouthful) or WFs. The Tower UI manages them on the same page as JTs.
- Inventory - It's just a list of hosts to run on that Ansible uses.
- Credentials - A configuration within Ansible that can be used as any kind of arbitrary credential. Supports various things from SSH to AWS, etc.

### Prerequisite

**Project structure should be either:**

- Match standard Ansible Repo Structure
- (Advanced) Genealogist should be able to take configuration to understand custom dir structure
Inputs 
- A Git diff for the latest git commit on any given Pull Request/Branch 
- Name of the branch to compare it with(Default master)
Outputs
- What files would be affected by the proposed changes?
- Job Templates that use the Tower Assets/Roles/Playbook in question
- Workflows that are using Job Templates affected

### Sample Ansible repo

There is a example ansible repo that is added in the repo for you to play with and understand it. The tower-configurations are stores in `playbooks/setup-ansible-tower/tower-configs`.
All playbooks are under `playbooks/` and all roles are under `roles/` directory for the convenience.
Actual user may have different directory names or structure, we should provide user an option to configure those as input values to genealogist to inform genealogist where to look for things.


### Limitations:
For all tower objects, name should be the first attribute in the list.

Example:

This is accepted:
```yaml
 - name: gitlab-personal-access-token for satqe_auto_droid
    kind: scm
    description: General purpose token that can be used by anyone for satlab-tower (or other private) repo clone
    username: gitlab
    password: "{{ gitlab_automation_user_personal_access_token }}"
    organization: Satellite
```
This is not acceptable, as name is not first attribute:
```yaml
  - kind: vault
    name: satlab-tower-vault
    vault_password: "{{ vault_admin_secret }}"
    vault_id: admin
    description: satlab-tower-vault password aka vault_admin_secret
    organization: Satellite
```

__*Author*__

Kedar Vijay Kulkarni (kvk@redhat.com)
