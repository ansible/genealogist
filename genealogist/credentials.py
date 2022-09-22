from pathlib import Path

import genealogist.config
from genealogist.inventory_sources import AnsibleTowerInventorySources
from genealogist.projects import AnsibleTowerProjects
from genealogist.job_templates import AnsibleTowerJobTemplates
# credentials->job template->workflow templates
# credentials->projects->job template->workflow templates
# credentials->inventory sources->inventory->job template->workflow templates


class AnsibleTowerCredentials:
    def __init__(self, at_configs):
        self.ansible_tower = at_configs

    def read_credentials(self):
        credentials = Path(self.ansible_tower.credentials)
        line_lookup = {}
        region = "header"
        with credentials.open() as creds:
            for n, line in enumerate(creds):
                if "name:" in line and not "username:" in line:
                    region = line.split(':')[1].strip()
                line_lookup[n+1] = region
        return line_lookup

    def derive_relations(self, given_credential=None, lines_changed=[]):
        all_creds = self.read_credentials()
        cred_inv_src_map = {}
        cred_proj_map = {}
        cred_job_map = {}

        for line in lines_changed:
            creds = self.pull_credentials(all_creds[line])
            if len(creds) != 1:
                raise Exception("No or more than 1 creds found, expected only 1!")
            # TODO: Remove duplication and split the function
            cred_inv_src_map[creds[0]] = self.map_to_inventory_sources(creds[0])
            cred_proj_map[creds[0]] = self.map_to_projects(creds[0])
            cred_job_map[creds[0]] = self.map_to_jobs(creds[0])

        if given_credential:
            cred_inv_src_map[given_credential] = self.map_to_inventory_sources(given_credential)
            cred_proj_map[given_credential] = self.map_to_projects(given_credential)
            cred_job_map[given_credential] = self.map_to_jobs(given_credential)
        for cred in cred_inv_src_map:
            for inv_src in cred_inv_src_map[cred]:
                cred_inv_src_map[cred][inv_src] = AnsibleTowerInventorySources(self.ansible_tower).derive_relations(inv_src)[inv_src]
        for cred in cred_proj_map:
            for proj in cred_proj_map[cred]:
                mappings = AnsibleTowerProjects(self.ansible_tower).derive_relations(proj)
                cred_proj_map[cred][proj] = {'project_jobs_map': None, 'project_inv_src_map': None}
                cred_proj_map[cred][proj]['project_jobs_map'] = mappings[0][proj]
                cred_proj_map[cred][proj]['project_inv_src_map'] = mappings[1][proj]
        for cred in cred_job_map:
            for job in cred_job_map[cred]:
                cred_job_map[cred][job] = AnsibleTowerJobTemplates(self.ansible_tower).derive_relations(job)[job]
        return cred_inv_src_map, cred_proj_map, cred_job_map

    def pull_credentials(self, given_credential=None):
        """List out all credentials found matching given_credential."""
        if given_credential:
            return [creds['name']
                    for creds in
                    self.ansible_tower.configs['tower_credentials']
                    if creds['name'] == given_credential
                    ]
        else:
            return [creds['name'] for creds in self.ansible_tower.configs['tower_credentials']]

    def map_to_jobs(self, given_credential=None):
        """Map credentials to job templates."""
        jobs = {}
        for cred in self.pull_credentials(given_credential):
            for jt in self.ansible_tower.configs['tower_templates']:
                if jt.get('credentials') is None:
                    continue
                for jt_cred in jt['credentials']:
                    if jt_cred == cred:
                        jobs[jt['name']] = cred
        return jobs

    def map_to_projects(self, given_credential=None):
        """Map credentials to projects."""
        projects = {}
        for cred in self.pull_credentials(given_credential):
            for proj in self.ansible_tower.configs['tower_projects']:
                if proj.get('scm_credential') is None:
                    continue
                if proj['scm_credential'] == cred:
                    projects[proj['name']] = cred
        return projects

    def map_to_inventory_sources(self, given_credential=None):
        """Map credentials to inventory sources."""
        inv_sources = {}
        for cred in self.pull_credentials(given_credential):
            for isrc in self.ansible_tower.configs['tower_inventory_sources']:
                if isrc.get('credential') is None:
                    continue
                if isrc['credential'] == cred:
                    inv_sources[isrc['name']] = {}
        return inv_sources


if __name__ == "__main__":
    from pprint import pprint
    at_configs = config.load_ansible_tower_configs()
    at_creds = AnsibleTowerCredentials(at_configs)
    #print(at_creds.pull_credentials())
    #pprint(at_creds.map_to_jobs())
    # for name in ["satlab-user-vault",
    #     "gitlab-personal-access-token for satqe_auto_droid",
    #     "admin@internal-RHVM-02"]:
    #     print('='*80)
    #     print("Credential", name)
    #     print('='*80)
    #     print("In use by the following job template(s)...")
    #     pprint(at_creds.map_to_jobs(name).keys())
    #     print('-'*80)
    #     print("In use by the following projects(s)...")
    #     pprint(at_creds.map_to_projects(name).keys())
    #     print("In use by the following inventory source(s)...")
    #     pprint(at_creds.map_to_inventory_sources(name).keys())
    pprint(at_creds.derive_relations(lines_changed=[10]))
