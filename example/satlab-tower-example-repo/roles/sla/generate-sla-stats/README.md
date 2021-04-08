generate-sla-stats
==================

A backend role used to gather stats about VM, and group them by a username. These stats are
used and further processed by other SLA roles.

Requirements
------------

ovirtsdk4

Role Variables
--------------

- `search_pattern` - by what pattern VMs are searched for. Default is `name=*-*`, as
the standard SatLab VM name looks like `username-satellite-6.7-latest-1585426414`
- `bad_vms_search_pattern` - pattern to find names not conforming to SatLab standard.
The default is `name!=*-*`
- `ignore_vm` - list of VMs that will be ignored by SLA. VMs listed here will be not taken
into account for SLA limits calculations, are invisible to SLA regular check, and
never will be removed or shutdown by it.

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
