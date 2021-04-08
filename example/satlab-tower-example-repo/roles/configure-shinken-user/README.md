Configure Shinken User
======================

This role is used to create a new user for monitoring(Shinken in this case) and inject correct SSH public key into that users authorized keys.
This will enable Shinken to ssh to newly created system without password with its Private key counterpart.

Requirements
------------
Let's say you have a System A that will be monitoring(or accessing in anyway) System B via (passwordless)SSH. So you should create a SSH key pair on System A, and copy its public part to System B under
correct user's home directory. This role requires you to have that keypair created.


Role Variables
--------------

You can define following two variables:

```
shinken_username: defaults to "shinken" but could be any user of your choice in case you are authenticating with a different user.
monitoring_ssh_key_public: "Required".defaults to None. Role will fail if you haven't defined this variable. This is usually content of the file ~/.ssh/id_rsa.pub
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: configure-shinken-user }

License
-------

BSD

Author Information
------------------

Kedar Kulkarni <kedar.kulkarni0@gmail.com>
