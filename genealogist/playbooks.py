import os
from pathlib import Path
import yaml
import pprint

import genealogist.config
from genealogist.job_templates import AnsibleTowerJobTemplates

class AnsibleTowerPlaybooks:
    def __init__(self, at_configs):
        self.ansible_tower = at_configs

    def derive_relations(self, given_pb):
        results = {}
        if given_pb:
            results[given_pb] = self.map_pbs_to_jts(given_pb)
            jts = AnsibleTowerJobTemplates(self.ansible_tower)
            for pb in results:
                for jt in results[pb]:
                    results[pb][jt] = jts.derive_relations(jt)[jt]
        return results

    def map_pbs_to_jts(self, given_pb):
        # List out all job templates found
        job_templates = {}
        for jt in self.ansible_tower.configs['tower_templates']:
            if jt['playbook'] in given_pb:
                    job_templates[jt['name']] = None
        return job_templates


if __name__ == "__main__":
    at_configs = config.load_ansible_tower_configs()
    atp = AnsibleTowerPlaybooks(at_configs)
    #pprint.pprint(atp.derive_relations(given_pb="<absolute path to playbook>"))
