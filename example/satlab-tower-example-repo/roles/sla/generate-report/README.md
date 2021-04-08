generate-sla-report
===================

The role used to generate SLA report either for a specific user, or for all users.

Requirements
------------

- `generate-sla-stats`

Role Variables
--------------

- `sla_user` - name of the user for which a report should be generated. By default the
current username or AT user is used
- `report_for_all` - generate a report for all found users

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

SatLab Admin
