from pathlib import Path
import pprint

import genealogist.config

class AnsibleTowerJobTemplates:
    def __init__(self, at_configs):
        self.ansible_tower = at_configs

    def read_jts(self):
        job_templates = Path(self.ansible_tower.jobs)
        _line_lookup = {}
        curr_space = "header"
        with job_templates.open() as jts:
            for l_no, line in enumerate(jts):
                if "name:" in line:
                    curr_space = line.split(":")[1].strip()
                _line_lookup[l_no + 1] = curr_space
        return _line_lookup
    
    def derive_relations(self, given_jt=None, lines_changed=[]):
        jts = self.read_jts()
        results = {}
        for line in lines_changed:
            template = self.pull_job_templates(jts[line])
            if len(template) > 1:
                raise Exception("Multiple templates found, expected only 1!")
            if len(template) == 0:
                continue
            results[template[0]] = self.map_jobs_to_workflows(template[0])
        if given_jt:
            results[given_jt] = self.map_jobs_to_workflows(given_jt)
        return results


    def pull_job_templates(self, given_jt):
        # List out all job templates found
        if given_jt:
            return [jt['name']
                    for jt in
                    self.ansible_tower.configs['tower_templates']
                    if jt['name'] == given_jt
                    ]
        else:
            return [jt['name'] for jt in self.ansible_tower.configs['tower_templates']]

    def map_jobs_to_workflows(self, given_jt):
        workflows = []
        for wf in self.ansible_tower.configs['tower_workflows']:
            if f"'job_template': '{given_jt}'" in str(wf['schema']):
                workflows.append(wf['name'])
        return workflows


if __name__ == "__main__":
    at_configs = config.load_ansible_tower_configs()
    atp = AnsibleTowerJobTemplates(at_configs)
    pprint.pprint(atp.derive_relations(given_jt="satlab-tower-remove-vm-from-rhvm-02",
                               lines_changed=[125,150,200]))
