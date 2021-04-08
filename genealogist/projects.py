'''
Projects->JT/Inv_Src mappings->all the way to WFs
'''
from pathlib import Path
import yaml
import pprint

import genealogist.config
from genealogist.job_templates import AnsibleTowerJobTemplates
from genealogist.inventory_sources import AnsibleTowerInventorySources

class AnsibleTowerProjects:
    def __init__(self, at_configs):
        self.ansible_tower = at_configs

    def read_projects(self):
        projects = Path(self.ansible_tower.projects)
        _line_lookup = {}
        curr_space = "header"
        with projects.open() as projs:
            for l_no, line in enumerate(projs):
                if "name:" in line:
                    curr_space = line.split(":")[1].strip()
                _line_lookup[l_no + 1] = curr_space
        return _line_lookup

    def derive_relations(self, given_proj=None, lines_changed=[]):
        projs = self.read_projects()
        proj_job_map = {}  # mapping proj->jts->wfs
        proj_inv_src_map = {}  # mapping proj->inv-src->inv->jts->wfs

        for line in lines_changed:
            project = self.pull_projects(projs[line])
            if len(project) != 1:
                raise Exception("No or more than 1 Projects found, expected only 1!")
            proj_job_map[project[0]] = self.map_projects_to_jobs(project[0])
            proj_inv_src_map[project[0]] = self.map_projects_to_inv_srcs(project[0])
        if given_proj:
            proj_job_map[given_proj] = self.map_projects_to_jobs(given_proj)
            proj_inv_src_map[given_proj] = self.map_projects_to_inv_srcs(given_proj)
        jts = AnsibleTowerJobTemplates(self.ansible_tower)
        inv_srcs = AnsibleTowerInventorySources(self.ansible_tower)
        for proj in proj_job_map: 
            for job in proj_job_map[proj]: 
                proj_job_map[proj][job] = jts.derive_relations(given_jt=job)[job]
            for inv_src in proj_inv_src_map[proj]:
                proj_inv_src_map[proj][inv_src] = inv_srcs.derive_relations(given_inv_src=inv_src)[inv_src]
        return proj_job_map, proj_inv_src_map

    def pull_projects(self, given_proj):
        # List out all project found matching given_proj
        if given_proj:
            return [proj['name']
                    for proj in
                    self.ansible_tower.configs['tower_projects']
                    if proj['name'] == given_proj
                    ]
        # else:
        #     return [inv['name'] for inv in self.ansible_tower.configs['tower_inventories']]

    def map_projects_to_jobs(self, given_proj):
        job_templates = {}
        for jt in self.ansible_tower.configs['tower_templates']:
            if jt['project'] == given_proj:
                job_templates[jt['name']] = None
        return job_templates

    def map_projects_to_inv_srcs(self, given_proj):
        inv_srcs = {}
        for i_src in self.ansible_tower.configs['tower_inventory_sources']:
            try:
                if i_src['source_project'] == given_proj:
                    inv_srcs[i_src['name']] = None
            except KeyError:
                # print(f'{i_src} has no attribute source_project')
                continue
        return inv_srcs
 
if __name__ == "__main__":
    at_configs = config.load_ansible_tower_configs()
    atp = AnsibleTowerProjects(at_configs)
    proj_job_map, proj_inv_src_map = atp.derive_relations(lines_changed=[15], given_proj="satlab-tower-master")
    print("Projects to Job/WF Mapping ==========>")
    pprint.pprint(proj_job_map)
    print("Projects to inv_src to inv to Job/WF Mapping ============>")
    pprint.pprint(proj_inv_src_map)
