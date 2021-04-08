install-satellite
=========

This deploys a simple satellite onto a RHEL template and sets all required pre-requisites for Satellite to function.


Requirements
------------

* EPEL repo needs to be skipped or the Satellite install WILL NOT function.
* The `target_host` must be defined for initialization.


Role Variables
--------------
The variables used need to be defined by default in a config in the playbook directory, such as `playbooks/create-satellite-template/deploy-template-config.yml`
* `template_hostname` : The hostname for the target satellite from the template default. Default: `template-satellite.infra.sat.rdu2.redhat.com`
* `sat_username` : API username to update the hostname with the `satellite-change-hostname` CLI. Default: satellite-qe default
* `sat_password` : API password to update the hostname with the `satellite-change-hostname` CLI. Default: satellite-qe default
* `rhel_version` : Specifies the version string used in the satellite oh-snap URI to check. Default: `el7`


Dependencies
------------

* `setup-infra.yml` : Installs all the basic utils, repos and subscriptions required to install satellite.

Example Playbook
----------------


    import_playbook: setup-infra.yml

    name: Install Satellite
    hosts: localhost
    vars:
      # Defines the vars required for deploying a template
      - vm_definition: 'deploy-template-config.yml'

      vars_files:
      - "{{ vm_definition }}"

    roles:
      - install-satellite

License
-------

None.

Author Information
------------------

"SatLab" <satellite-lab-list@redhat.com>
