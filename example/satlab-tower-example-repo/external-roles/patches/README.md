# Notes

This file is supposed to be a living document noting any patches that we applied to a role in the `external-roles`
and we intend to offset that when upstream role is updated.

For example, KK opened PR#123 and PR#125 against ovirt-ansible-vm-infra(https://github.com/oVirt/ovirt-ansible-vm-infra). PR#125 has not been released yet, but once released, we will update our role from ansible-galaxy to pull in those changes.

Another important reason to have this document is to show that, over the time, how we had to contribute to upstream roles.


# Upstream Contributions

* Fix CPU Pinning/Host Passthrough: https://github.com/oVirt/ovirt-ansible-vm-infra/pull/123/
* Fix set_facts: https://github.com/oVirt/ovirt-ansible-vm-infra/pull/125/
