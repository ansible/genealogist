'''
Role->Playbooks dependencies.
'''
from pathlib import Path
import yaml
import pprint

import genealogist.config
from genealogist.playbooks import AnsibleTowerPlaybooks

class AnsibleFile:

    dep_keys = ["roles", "role", "tasks", "block", "include_role", "import_role"]

    def __init__(self, file_path):
        self.file = Path(file_path)
        self.dependencies = []
        self._load_file()
        self._parse()

    def _load_file(self):
        if self.file.exists():
            with self.file.open() as f:
                self.raw_data = yaml.load(f, Loader=yaml.BaseLoader)
        else:
            self.raw_data = {}
            print(f"Couldn't find file: {self.file}")

    def _parse(self, data=None):
        data = data or self.raw_data
        if isinstance(data, dict):
            for key, value in data.items():
                if key in self.dep_keys:
                    if key == 'include_role' or key == 'import_role':
                        self._add_dependency({key:value})
                    else:
                        self._add_dependency(value)
        elif isinstance(data, list):
            for item in data:
                self._parse(item)

    def _add_dependency(self, dep):
        if isinstance(dep, dict):
            for key, value in dep.items():
                if key in self.dep_keys:
                    if key == 'include_role' or key == 'import_role':
                        if isinstance(value, dict) and value['name']:
                            self._add_dependency(value['name'])
                    self._add_dependency(value)
        elif isinstance(dep, list):
            for d in dep:
                self._add_dependency(d)
        else:
            self.dependencies.append(dep)


def parse_directory(curr_directory, base_directory=None):
    base_directory = base_directory or curr_directory
    directory_struct = {}
    for child in curr_directory.iterdir():
        if child.is_dir() and not child.is_symlink():
            directory_struct.update(parse_directory(child, base_directory))
        elif child.suffix in [".yml", ".yaml"]:
            directory_struct[child.relative_to(base_directory)] = AnsibleFile(child)
    return directory_struct


def build_dependencies(curr_directory, given_role=None, base_directory=None):
    # Function to build dict containing roles->playbooks mapping
    mappings = {}
    for path in parse_directory(curr_directory or base_directory):
        roles = AnsibleFile(f'{curr_directory or base_directory}/{path}').dependencies
        if roles:
            for role in roles:
                if given_role and given_role != role:
                    continue
                try:
                    mappings[role].update({str(path):None})
                except KeyError:
                    mappings[role] = {str(path):None}
        else:
            pass
    return mappings

def derive_relations(base_dir, given_role=None, at_configs=None):
    # Function to build relation role -> playbook -> JTs - > WFs
    dependency_mappings = build_dependencies(Path(base_dir), given_role=given_role)
    if not at_configs:
        return dependency_mappings
    playbooks = AnsibleTowerPlaybooks(at_configs)
    for role in dependency_mappings:
        for pb in dependency_mappings[role]:
            dependency_mappings[role][pb] = playbooks.derive_relations(given_pb=pb)[pb]
    return dependency_mappings


if __name__ == "__main__":
    base_dir = Path(input("Enter the base directory path: "))
    given_role = input("Enter name of desired role: ")
    ansible_tower_config = config.load_ansible_tower_configs()
    pprint.pprint(derive_relations(base_dir, given_role, ansible_tower_config))
    # dependency_mappings = build_dependencies(Path(base_dir), given_role=given_role)
    # print(f"Role remove-vm if found in "
    #       f"{dependency_mappings['remove-vm']}")
    # for role in dependency_mappings.keys():
    #     print(f"{role} is found {len(dependency_mappings[role])} times in {dependency_mappings[role]}\n")
