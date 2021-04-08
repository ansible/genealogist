from collections import ChainMap
from pathlib import Path
import os
import pprint
import yaml

multiple_options = "roles, playbooks"

class AnsibleTowerConfigurations:
    """A class that holds all AnsibleTower configurations."""

    # NOTE: Can create a mode that allows us to append to
    # paths in config file
    def __init__(self, configFile, override={}, repo=Path()):
        repo = Path(repo)
        self.config_params = self._load_yaml(configFile)
        self.load_files = []
        for key, params in self.config_params.items():
            for param, value in params.items():
                if key in override:
                    setattr(self,key + '_' + param, override[key])
                else:
                    setattr(self,key + '_' + param, value)
                if param == 'path':
                       self._find_paths(repo, value)
                else:
                    for fPath in value:
                       self._find_paths(repo, fPath)

        self.configs = {}
        self._load()

    def __str__(self):
        return str(self.configs)

    def _load(self):
        self.configs = ChainMap({})
        for f in self.load_files:
            self.configs = self.configs.new_child(self._load_yaml(f))

    def _load_yaml(self, path):
        path = Path(path)
        with path.open() as f:
            return yaml.load(f, Loader=yaml.BaseLoader)

    def _find_paths(self,repo, path):
        full_path = repo.joinpath(path)
        if os.path.isfile(full_path):
            self.load_files.append(full_path)


def load_ansible_tower_configs(configFile, override={}, repo=os.getcwd()):
    return AnsibleTowerConfigurations(configFile, override, repo)

if __name__ == "__main__":
    a = load_ansible_tower_configs('object_config.yaml')
