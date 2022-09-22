from pathlib import Path
from pprint import pprint

import genealogist.config
from genealogist.inventories import AnsibleTowerInventories
from genealogist.job_templates import AnsibleTowerJobTemplates

# Permissions->job template/Projects/Inventory/InventorySources/workflow templates

class AnsibleTowerPermissions:
    def __init__(self, at_configs):
        self.ansible_tower = at_configs

    def derive_relations(self, lines_changed=[]):
        perms = self.read_permissions()
        jts = AnsibleTowerJobTemplates(self.ansible_tower)
        invs = AnsibleTowerInventories(self.ansible_tower)
        for line_no in lines_changed:
            line = perms[line_no]
            if "inventory:" in line:
                print('\nInventory Mappings: \n')
                pprint(invs.derive_relations(line.split(":")[1].strip()))
            elif "job_template:" in line:
                print('\nJob Templates Mappings: \n')
                pprint(jts.derive_relations(line.split(":")[1].strip()))
            elif "workflow:" in line:
                pprint(f'Following WF permissions were modified: {line.split(":")[1].strip()}')
            elif "credential:" in line:
                pprint(line.split(":")[1].strip())
            elif "organization:" in line:
                pprint(line.split(":")[1].strip())
            elif "project:" in line:
                pprint(line.split(":")[1].strip())



    def read_permissions(self):
        permissions = Path(self.ansible_tower.permissions)
        print(self.ansible_tower.permissions)
        _line_lookup = {}
        curr_space = "header"
        with permissions.open() as perms:
            for l_no, line in enumerate(perms):
                if "inventory:" in line:
                    curr_space = f'inventory:{line.split(":")[1].strip()}'
                elif "job_template:" in line:
                    curr_space = f'job_template:{line.split(":")[1].strip()}'
                elif "workflow:" in line:
                    curr_space = f'workflow:{line.split(":")[1].strip()}'
                elif "credential:" in line:
                    curr_space = f'credential:{line.split(":")[1].strip()}'
                elif "organization:" in line:
                    curr_space = f'organization:{line.split(":")[1].strip()}'
                elif "project:" in line:
                    curr_space = f'project:{line.split(":")[1].strip()}'
                _line_lookup[l_no + 1] = curr_space
        return _line_lookup


if __name__ == "__main__":
    at_configs = config.load_ansible_tower_configs()
    atp = AnsibleTowerPermissions(at_configs)
    # print(atp.read_permissions())
    atp.derive_relations([84,6,75,55])
