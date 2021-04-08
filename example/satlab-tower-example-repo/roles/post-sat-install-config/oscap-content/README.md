oscap-content
=========

Populating oscap-content during post installation of satellite.

Requirements
------------

Satellite installation has to be successfully installed before running any post configuration.

Role Variables
--------------

None

Dependencies
------------

infra-install/install-satellite

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: Populate oscap-content
      command: "foreman-rake foreman_openscap:bulk_upload:default"

License
-------

None

Author Information
------------------

SatLab <satellite-lab-list@redhat.com>
