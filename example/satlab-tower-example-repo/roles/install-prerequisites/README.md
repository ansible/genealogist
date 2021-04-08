install-prerequisites
=========

Pre-install prerequisite items as part of satellite install

Requirements
------------

None

Role Variables
--------------

None

Dependencies
------------

None

Example Playbook
----------------

    - name: Ping a localhost and hostname
      command: "ping -c1 {{ item }}"
      loop:
        - "{{ ansible_fqdn }}"
        - localhost

License
-------

None

Author Information
------------------

SatLab <satellite-lab-list@redhat.com>
