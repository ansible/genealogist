from pathlib import Path
import yaml

import genealogist.config
from genealogist.inventories import AnsibleTowerInventories


class AnsibleTowerInventorySources:
    def __init__(self, at_configs):
        self.ansible_tower = at_configs

    def read_inv_srcs(self):
        inventory_srcs= Path(self.ansible_tower.inventory_sources)
        _line_lookup = {}
        curr_space = "header"
        with inventory_srcs.open() as inv_srcs:
            for l_no, line in enumerate(inv_srcs):
                if "name:" in line:
                    curr_space = line.split(":")[1].strip()
                _line_lookup[l_no + 1] = curr_space
        return _line_lookup

    def derive_relations(self, given_inv_src=None, lines_changed=[]):
        inventory_srcs = self.read_inv_srcs()
        inv_src_inv_map = {}

        for line in lines_changed:
            inv_src = self.pull_inventory_sources(inventory_srcs[line])
            if len(inv_src) != 1:
                raise Exception("No or more than 1 Inv Sources found, expected only 1!")
            inv_src_inv_map[inv_src[0]] = self.map_to_inventories(inv_src[0])
        if given_inv_src:
            inv_src_inv_map[given_inv_src] = self.map_to_inventories(given_inv_src)
        invs = AnsibleTowerInventories(self.ansible_tower)
        for inv_src in inv_src_inv_map: 
            for inv in inv_src_inv_map[inv_src]: 
               inv_src_inv_map[inv_src][inv] = invs.derive_relations(given_inv=inv)[inv] 
        return inv_src_inv_map

    def pull_inventory_sources(self,given_inv_src):
        # List out all inventory_sources found matching given_inv_src
        if given_inv_src:
            return [inv_src['name']
                    for inv_src in
                    self.ansible_tower.configs['tower_inventory_sources']
                    if inv_src['name'] == given_inv_src
                    ]
        # else:
        #     return [inv_src['inventory']
        #             for inv_src in self.inv_srcs['tower_inventory_sources']]

    def map_to_inventories(self, given_inv_src):
        # Map out all inventories to inventory sources it is using found
        # in given inventory sources
        inventories = {}
        for inv_src in self.ansible_tower.configs['tower_inventory_sources']:
            if inv_src['name'] == given_inv_src:
                inventories[inv_src['inventory']] = None
        return inventories


if __name__ == "__main__":
    at_configs = config.load_ansible_tower_configs()
    atp = AnsibleTowerInventorySources(at_configs)
    print(atp.derive_relations(lines_changed=[20], given_inv_src='project-inventory-source-satlab-tower'))
