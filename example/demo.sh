#!/bin/bash
set -euxo pipefail
if [ ! -d "venv" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  virtualenv venv
fi
source venv/bin/activate
pip install .
echo " " >> satlab-tower-example-repo/playbooks/setup-ansible-tower/install-tower.yml
echo " " >> satlab-tower-example-repo/roles/set-stats/handlers/main.yml
echo " " >> satlab-tower-example-repo/roles/sla/generate-report/defaults/main.yml

genealogist diff --config-file object_config.yaml
echo -e "\n\n\n\n"

genealogist diff --branch1 master --config-file object_config.yaml
echo -e "\n\n\n\n"

genealogist diff --path playbooks satlab-tower-example-repo/playbooks --config-file override_playbooks_config.yaml

genealogist dependencies --asset inventory satlab-tower-inventory --config-file object_config.yaml
echo -e "\n\n\n\n"

genealogist dependencies --asset job-template satlab-tower-deploy-baserhel-from-rhvm-02 --config-file object_config.yaml
echo -e "\n\n\n\n"

genealogist dependencies --asset project satlab-tower-master --config-file object_config.yaml
echo -e "\n\n\n\n"

genealogist dependencies --asset role remove-vm --config-file object_config.yaml
echo -e "\n\n\n\n"

genealogist dependencies --path inventories satlab-tower-example-repo/playbooks/setup-ansible-tower/tower-configs/tower-inventories.yml --config-file override_inventories_config.yaml
echo -e "\n\n\n\n"

genealogist diff --branch2 d29c68458c75bc0a65e3cd640bb02af023968f5a --config-file object_config.yaml
echo -e "\n\n\n\n"

genealogist diff --branch1 5499bf08e771da856024d08864d594d35a222d19 --branch2 d29c68458c75bc0a65e3cd640bb02af023968f5a --config-file object_config.yaml
echo -e "\n\n\n\n"
