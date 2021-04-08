Configure VM as GitLab Docker Runner
====================================

This role is going to help install Docker GitLab Runner requirements on any given VM.

Requirements
------------

This role is tested to work on Red Hat based Linux distribution.

Role Variables
--------------

- ca_cert_url: URL of the Certificate file for RH Root CA
- persistent_vol: Docker containers need to have persistent volume, to keep its configs, this var tells path of that on our VM where docker will be running.
- gitlab_url: your gitlab URL
- gitlab_cert_name: Name of cert file in files dir, usually {{ gitlab-fqdn }}.crt
- gitlab_runner_registration_token: this is a token you need to obtain for your repo from Gitlab->Repo->Settings->CI/CD and find Runner Registration token.
- docker_ce_repo: We use docker ce(community edition) in this role as the docker coming with RHEL repos does not play well with GitLab.
- epel_repo_url: url from which EPEL repo will be installed and enabled.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```
- name: Install and configure Linter
  hosts: target_hosts
  roles:
    - role: linter-setup
```

License
-------

BSD

Author Information
------------------

Kedar Kulkarni (kedar.kulkarni0@gmail.com)
