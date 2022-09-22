from pathlib import Path
import yaml
import pprint

import genealogist.config
from genealogist.job_templates import AnsibleTowerJobTemplates

class AnsibleTowerInventories:
    def __init__(self, at_configs):
        self.ansible_tower = at_configs

    def read_invs(self):
        inventories = Path(self.ansible_tower.inventories)
        _line_lookup = {}
        curr_space = "header"
        with inventories.open() as invs:
            for l_no, line in enumerate(invs):
                if "name:" in line:
                    curr_space = line.split(":")[1].strip()
                _line_lookup[l_no + 1] = curr_space
        return _line_lookup

    def derive_relations(self, given_inv=None, lines_changed=[]):
        invs = self.read_invs()
        inv_job_map = {}

        for line in lines_changed:
            inventory = self.pull_inventories(invs[line])
            if len(inventory) != 1:
                raise Exception("No or more than 1 Inventories found, expected only 1!")
            inv_job_map[inventory[0]] = self.map_inventories_to_jobs(inventory[0])
        if given_inv:
            inv_job_map[given_inv] = self.map_inventories_to_jobs(given_inv)
        jts = AnsibleTowerJobTemplates(self.ansible_tower)
        for inv in inv_job_map: 
           for job in inv_job_map[inv]: 
               inv_job_map[inv][job] = jts.derive_relations(given_jt=job)[job]
        return inv_job_map

    def pull_inventories(self, given_inv):
        # List out all inventories found matching given_inv
        if given_inv:
            return [inv['name']
                    for inv in
                    self.ansible_tower.configs['tower_inventories']
                    if inv['name'] == given_inv
                    ]
        # else:
        #     return [inv['name'] for inv in self.ansible_tower.configs['tower_inventories']]

    def map_inventories_to_jobs(self, given_inv):
        job_templates = {}
        for jt in self.ansible_tower.configs['tower_templates']:
            if jt['inventory'] == given_inv:
                job_templates[jt['name']] = None
        return job_templates

 
if __name__ == "__main__":
    at_configs = config.load_ansible_tower_configs()
    atp = AnsibleTowerInventories(at_configs)
    pprint.pprint(atp.derive_relations(lines_changed=[15,25,32], given_inv="localhost"))
