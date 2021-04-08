from pathlib import Path
import yaml

# playbooks -> setup-ansible-tower ->
# tower-configs -> tower workflows
# in tower config - name, org, job templates

# ansible.cfg for paths?
# tower-permissions? could pull anyway
# for permissions-based tests


class AnsibleTowerConfig:
    def __init__(self, workflow_path):
        self.file = Path(workflow_path)
        self.templates_file = self.file.parent.joinpath("tower-job-templates.yml")
        self.workflows = {}
        self.raw_data = self._load_file()
        self.raw_job_templates = self._load_file(self.templates_file)
        for workflow in self.raw_data.get("tower_workflows", []):
            parsed = self.parse_workflow(workflow)
            if parsed:
                self.workflows[parsed["name"]] = parsed

    def _load_file(self, file=None):
        file = file or self.file
        if not isinstance(file, Path):
            file = Path(file)
        with file.open() as f:
            return yaml.load(f, Loader=yaml.BaseLoader)

    def parse_workflow(self, workflow):
        # name, organization, job templates
        parsed = {
            "name": workflow["name"],
            "organization": workflow["organization"],
            "job templates": self.pull_templates(workflow.get("schema", [])),
        }
        return parsed

    def pull_templates(self, template_list):
        templates = []
        for item in template_list:
            if isinstance(item, dict):
                for key, val in item.items():
                    if key == "job_template":
                        templates.append(val)
                    else:
                        templates.extend(self.pull_templates(val) or [])
            elif isinstance(item, list):
                templates.extend(self.pull_templates(val))
        templates = list(set(templates))
        templates = {
            template: self.pull_template_info(template)
            for template in templates
            if template
        }
        return templates

    def pull_template_info(self, template):
        # inventory, credentials, playbook
        if self.raw_job_templates:
            for job_template in self.raw_job_templates["tower_job_templates"]:
                if job_template["name"] == template:
                    return {
                        "name": job_template.get("name"),
                        "inventory": job_template.get("inventory"),
                        "credentials": job_template.get("credentials"),
                        "playbook": AnsibleFile(job_template["playbook"]),
                    }


class AnsibleFile:

    dep_keys = ["roles", "role"]

    def __init__(self, file_path):
        self.file = Path(file_path)
        self.dependencies = []
        self.dependents = []
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
                    self._add_dependency(value)
        elif isinstance(data, list):
            for item in data:
                self._parse(item)

    def _add_dependency(self, dep):
        if isinstance(dep, dict):
            for key, value in dep.items():
                if key in self.dep_keys:
                    self._add_dependency(value)
        elif isinstance(dep, list):
            for d in dep:
                self._add_dependency(d)
        else:
            self.dependencies.append(dep)

    def add_dependent(self, dep):
        if dep not in self.dependents:
            self.dependents.append(dep)

    def get_dependents(self):
        deps = []
        for dep in self.dependents:
            deps.extend(dep.get_dependents())
        return list(set(deps))

    def link_dependencies(self, files_dict):
        for dep in self.dependencies:
            if dep in files_dict:
                files_dict[dep].add_dependent(self)


def parse_directory(curr_directory, base_directory=None):
    base_directory = base_directory or curr_directory
    directory_struct = {}
    for child in curr_directory.iterdir():
        if child.is_dir() and not child.is_symlink():
            directory_struct.update(parse_directory(child, base_directory))
        elif child.suffix in [".yml", ".yaml"]:
            directory_struct[child.relative_to(base_directory)] = AnsibleFile(child)
    return directory_struct


def link_all_deps(files_dict):
    for file in files_dict.values():
        file.link_dependencies(files_dict)


def affected_by(file_name, files_dict):
    if file_name in files_dict:
        return files_dict[file_name].get_dependents()


# if __name__ == "__main__":
#     directory = Path(input("Enter the base directory path: "))
#     while not directory.is_dir():
#         directory = Path(input("Enter a valid base directory path: "))
#     files_dict = parse_directory(directory)
#     print(files_dict)
#     link_all_deps(files_dict)
#     (f_key, f_val), *rem, (l_key, l_val) = files_dict.items()
#     print(f_key)
#     print(f_val.get_dependents())
#     print(l_key)
#     print(l_val.get_dependents())
