from collections import ChainMap
from pathlib import Path
import yaml
import pprint

class AnsibleTowerConfigurations:
    """A class that holds all AnsibleTower configurations."""

    def __init__(
        self,
        credentials_path,
        job_templates_path,
        projects_path,
        inventories_path,
        inventory_sources_path,
        workflows_path,
        permissions_path,
        hosts_path,
        users_path,
        teams_path,
        organizations_path
    ):
        self.credentials = Path(credentials_path)
        self.jobs = Path(job_templates_path)
        self.projects = Path(projects_path)
        self.inventories = Path(inventories_path)
        self.inventory_sources = Path(inventory_sources_path)
        self.workflows = Path(workflows_path)
        self.permissions = Path(permissions_path)
        self.hosts = Path(hosts_path)
        self.users = Path(users_path)
        self.teams = Path(teams_path)
        self.organizations= Path(organizations_path)
        self.configs = {}
        self._load()

    def __str__(self):
        return str(self.configs)

    def _load(self):
        self.configs = ChainMap(
            self._load_yaml(self.credentials),
            self._load_yaml(self.jobs),
            self._load_yaml(self.projects),
            self._load_yaml(self.inventories),
            self._load_yaml(self.inventory_sources),
            self._load_yaml(self.workflows),
            self._load_yaml(self.permissions),
            self._load_yaml(self.hosts),
            self._load_yaml(self.users),
            self._load_yaml(self.teams),
            self._load_yaml(self.organizations),
        )

    def _load_yaml(self, path):
        if not isinstance(path, Path):
            path = Path(path)
        with path.open() as f:
            return yaml.load(f, Loader=yaml.BaseLoader)

def load_ansible_tower_configs():
    # TODO: This function should accept args for all paths or lookup via config.yml file
    credentials_path = (
        f"{Path.cwd()}/satlab-tower-example-repo/"
        "playbooks/setup-ansible-tower/"
        "tower-configs/tower-credentials.yml"
    )
    job_templates_path = (
        f"{Path.cwd()}/satlab-tower-example-repo/"
        "playbooks/setup-ansible-tower"
        "/tower-configs/tower-job-templates.yml"
    )
    projects_path = (
        f"{Path.cwd()}/satlab-tower-example-repo/"
        "playbooks/setup-ansible-tower/"
        "tower-configs/tower-projects.yml"
    )
    inventories_path = (
        f"{Path.cwd()}/satlab-tower-example-repo/"
        "playbooks/setup-ansible-tower/"
        "tower-configs/tower-inventories.yml"
    )
    inventory_sources_path = (
        f"{Path.cwd()}/satlab-tower-example-repo/"
        "playbooks/setup-ansible-tower/"
        "tower-configs/tower-inventory-sources.yml"
    )
    workflows_path = (
        f"{Path.cwd()}/satlab-tower-example-repo"
        "/playbooks/setup-ansible-tower/"
        "tower-configs/tower-workflows.yml"
    )
    permissions_path = (
        f"{Path.cwd()}/satlab-tower-example-repo"
        "/playbooks/setup-ansible-tower/"
        "tower-configs/tower-permissions.yml"
    )
    hosts_path = (
        f"{Path.cwd()}/satlab-tower-example-repo"
        "/playbooks/setup-ansible-tower/"
        "tower-configs/tower-hosts.yml"
    )
    users_path = (
        f"{Path.cwd()}/satlab-tower-example-repo"
        "/playbooks/setup-ansible-tower/"
        "tower-configs/tower-user-accounts.yml"
    )
    teams_path = (
        f"{Path.cwd()}/satlab-tower-example-repo"
        "/playbooks/setup-ansible-tower/"
        "tower-configs/tower-teams.yml"
    )
    orgnizations_path = (
        f"{Path.cwd()}/satlab-tower-example-repo"
        "/playbooks/setup-ansible-tower/"
        "tower-configs/tower-organization.yml"
    )
    return AnsibleTowerConfigurations(
        credentials_path,
        job_templates_path,
        projects_path,
        inventories_path,
        inventory_sources_path,
        workflows_path,
        permissions_path,
        hosts_path,
        users_path,
        teams_path,
        orgnizations_path
    )
if __name__ == "__main__":
    ansible_tower = load_ansible_tower_configs()
    pprint.pprint(ansible_tower)
