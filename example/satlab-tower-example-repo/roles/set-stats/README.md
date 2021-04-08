set-stats
=========

Most Ansible Tower Job Templates need to pass data out for for the next template in an Ansible Tower Workflow.

Requirements
------------

A data structure called `data` must be passed to `set-stats`.

Role Variables
--------------

* `data` - Any data structure that is passed as a var which will be passed into `set_stats` for the Job Template

Dependencies
------------

None.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: Save the template of the Satellite VM
      hosts: localhost
      gather_facts: false
      roles:
        - role: save-template
        - role: set-stats
          vars:
            data:
              satellite_target_template: "{{ target_template }}"


License
-------

None

Author Information
------------------

Satlab Admins
