Add Storage Network
===================

This is a role written to be able to add static Network Config to any VM.

Requirements
------------

The requirements for this role to work is list of `vars/RedHat.yml`, which is specific to Red Hat distro. Be sure to have your VM subscribed to RHN.

Role Variables
--------------

Following are variables set in the Defaults/main.yml which you may override.
- nmcli_ethernet: it is a dictionary of connections that you'd like to add.
Supported attributes are:
- conn_name: This variable can take any name you'd like to give to the connection.
- ifname: An interface with this name should exist on the system.
- ip4: IPAddress/Prefix format e.g. 192.168.x.x/24
- gw4: Default gateway for the connection.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:


`- name: Deploy tower on my_tower_vms
  hosts: my_tower_vms
  roles:
    - role: add-storage-network
      nmcli_ethernet:
  		- conn_name: eth1
    	  ifname: eth1
          ip4: 192.168.133.30/24
          gw4: 192.168.133.254`

License
-------

BSD

Author Information
------------------

contact me on GitHub (@kedark3) for help.
