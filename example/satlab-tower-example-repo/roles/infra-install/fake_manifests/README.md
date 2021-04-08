Role Name
=========

Inserts the fake_manifests into Satellite.

Source
------------

Role was modified and placed into `./roles` as a result.

Original Source for the role. https://gitlab.sat.engineering.redhat.com/rplevka/sat-deploy/tree/robottelo_e2e/roles/fake_manifest


Requirements
------------

None

Role Variables
--------------

fake_manifest_url  - location to pickup the fake manifest. Default is provided.

fake_manifest_cert - location of the fake cert. Default is provided.

fake_manifest_key  - location of the fake manifest key. Default is provided.


Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - infra-install/fake_manifests

License
-------

BSD

Author Information
------------------

rplevka@redhat.com
