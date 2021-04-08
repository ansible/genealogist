# This is a borderline hack to avoid AT marking powered off RHV VMs as disabled. Facts cached on AT
# for disabled VMs are not available to other jobs. This causes a problem for VM SLA, which needs access to
# cached facts to determine expire time. Following settings keeps even powered off VMs enabled in AT by using
# the cluster name as a flag. We need to change/update this if we ever change cluster name to something
# different than "Default"
# As long as we need to access cached facts for RHV VMs from playbooks/roles that are not targeting these VM directly,
# (SLA typically), and there is no other mechanism to keep powered off RHV VMs enabled, we need this.
RHV_ENABLED_VAR="cluster"
RHV_ENABLED_VALUE="Default"
