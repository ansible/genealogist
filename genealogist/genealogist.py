import click
from pathlib import Path
from pprint import pprint

from genealogist import config
from genealogist import configParser
from genealogist import gitdiff as gd
from genealogist import inventories as inv
from genealogist import job_templates as jt
from genealogist.playbooks import AnsibleTowerPlaybooks
from genealogist.roles import build_dependencies as role_dependencies
from genealogist.roles import derive_relations as roles_derive_relations
from genealogist.credentials import AnsibleTowerCredentials
from genealogist.inventories import AnsibleTowerInventories
from genealogist.inventory_sources import AnsibleTowerInventorySources
from genealogist.job_templates import AnsibleTowerJobTemplates
from genealogist.permissions import AnsibleTowerPermissions
from genealogist.projects import AnsibleTowerProjects


valid_options = """configs, credentials, hosts, inventories, inventory_sources,
                   job_templates, organizations, permissions, playbooks, projects,
                   roles, teams, users, workflows
                """
multiple_options = "roles, playbooks"

def get_valid_names():
    valid_ops = ''
    ops = valid_options.split(", ")
    for s in ops:
        if 'inventories' in s:
            valid_ops += 'inventory, '
        else:
            valid_ops += s[:-1]+ ', '

    #Remove last two characters
    valid_ops = valid_ops[:-2]

    return valid_ops

@click.group()
def listAll():
    pass


@click.group()
def out_diff():
    pass

@out_diff.command()
@click.option('--branch1',
              help='A branch to use in generating the diff. If only one branch'
                   ' is specified (branch1 or branch2), it will be compared '
                   'with the current state of the git repo. If two branches'
                   ' are specified (branch1 and branch2), '
                   'they will be compared against one another'
                   'Default: HEAD')
@click.option('--branch2',
              help='A branch to use in generating the diff. If only one branch'
                   ' is specified (branch1 or branch2), it will be compared'
                   ' with the current state of the git repo. If two branches'
                   ' are specified (branch1 and branch2), they will be'
                   ' compared against one another'
                   'Default: master')
@click.option('--path', multiple=True, type=(str,str), help=f'Path to a tower config that will override the value(s) in config file. Expected format is \'tower_config_name=path\'. Can have multiple values and expected tower_config_name values are {valid_options}')
@click.option('--config-file',required=True)
@click.option('--repo', default=Path(), help='The name of the repo where analysis should be done')
def diff(repo, branch1, branch2, path, config_file):
    """Determine what Tower Configurations have changed in a repo"""
    override_paths = {}
    parse_paths(path, override_paths)

    repo_path=Path(repo)
    cp = configParser.load_ansible_tower_configs(config_file, override_paths)

    #playbooks_path=cp.playbooks_path
    #roles_path= cp.roles_path
    config_path=cp.configs_path
    ansible_tower = config.AnsibleTowerConfigurations(
        cp.credentials_path,
        cp.job_templates_path,
        cp.projects_path,
        cp.inventories_path,
        cp.inventory_sources_path,
        cp.workflows_path,
        cp.permissions_path,
        cp.hosts_path,
        cp.users_path,
        cp.teams_path,
        cp.organizations_path
    )
    at_pb = AnsibleTowerPlaybooks(ansible_tower)
    hashes = []
    if branch1 is not None:
        hashes.append(branch1)
    if branch2 is not None:
        hashes.append(branch2)

    diff = gd.GitDiff.git_diff(hashes, repo_path, cp.roles_paths, cp.playbooks_paths,
                               cp.configs_path)
    pprint(diff)
    for config_type in diff['tower-config']:
        derive_relations(config_type, diff, cp, repo, branch1, branch2)

    if ansible_tower:
        print('*'*80)
        for r in diff['roles']:
            print('*'*80)
            pprint(roles_derive_relations(repo_path, given_role=r, at_configs=ansible_tower))
            print('*'*80)
        for playbook in diff['playbooks']:
            print('*'*80)
            pprint(at_pb.derive_relations(playbook))
            print('*'*80)
    else:
        print("\n***No Ansible Tower Config was found. Only deriving relation between roles->playbooks.***\n")
        for r in diff['roles']:
            print('*'*80)
            pprint(role_dependencies(repo_path, given_role=r))
            print('*'*80)

@listAll.command()
@click.option('--repo', default=Path(), help='The name of the repo where analysis should be done')
@click.option('--config-file', required=True, help='Config file with list of locations for'
                                    ' configurations')
@click.option('--path', multiple=True, type=(str,str), help=f'Path to a tower config that will override the value(s) in config file. Expected format is \'tower_config_name=path\'. Can have multiple values and expected tower_config_name values are {valid_options}')
@click.option('--asset', multiple=True, type=(str,str), help=f'Name of a tower config. Expected format is \'tower_config_type name\'. Can have multiple values and expected tower_config_name values are {get_valid_names()}')
def dependencies(repo, config_file, path, asset):
    """Display the dependencies of various Tower Configurations"""
    override_paths = {}
    parse_paths(path, override_paths)

    repo_path=Path(repo)
    cp = configParser.load_ansible_tower_configs(config_file, override_paths)

    playbooks_path=cp.playbooks_paths
    roles_path=cp.roles_paths
    config_path=cp.configs_path
    inventory_path=cp.inventories_path
    job_templates_path=cp.job_templates_path
    workflow_path=cp.workflows_path

    role_name = ''
    inventory_name = ''
    job_template_name = ''
    inventory_source_name = ''
    project = ''
    credential = ''
    playbook_name = ''
    ########
    # For now, going to let duplicates override
    # But eventually, these will take multiple names
    # so this will also take multiple names
    for nameTup in asset:
        if nameTup[0] == 'role':
            role_name = nameTup[1]
        elif nameTup[0] == 'inventory':
            inventory_name = nameTup[1]
        elif nameTup[0] == 'job_template':
            job_template_name = nameTup[1]
        elif nameTup[0] == 'inventory_source':
            inventory_source_name = nameTup[1]
        elif nameTup[0] == 'project':
            project = nameTup[1]
        elif nameTup[0] == 'credential':
            credential = nameTup[1]
        elif nameTup[0] == 'playbook':
            playbook_name = nameTup[1]

    ansible_tower = load_new_tower_config(cp)

    if role_name and not ansible_tower:
        pprint(role_dependencies(repo_path, given_role=role_name))

    if playbook_name and ansible_tower:
        at_pb = AnsibleTowerPlaybooks(ansible_tower)
        pprint(at_pb.derive_relations(playbook_name))

    if ansible_tower and role_name:
        pprint(roles_derive_relations(repo_path, given_role=role_name, at_configs=ansible_tower))
    if ansible_tower:
        if inventory_name:
            pprint(inv.AnsibleTowerInventories(ansible_tower).derive_relations(given_inv=inventory_name))
        if job_template_name:
            pprint(jt.AnsibleTowerJobTemplates(ansible_tower).derive_relations(given_jt=job_template_name))
        if inventory_source_name:
            pprint(AnsibleTowerInventorySources(ansible_tower).derive_relations(inventory_source_name))
        if project:
            pprint(AnsibleTowerProjects(ansible_tower).derive_relations(project))
        if credential:
            pprint(AnsibleTowerCredentials(ansible_tower).derive_relations(credential))

def parse_paths(path, override_paths):
    regex_options = valid_options.split(', ')
    for p in path:
        if p[0] in regex_options:
            if p[0] in multiple_options:
                # Can be csv
                if p[0] in override_paths:
                    # Append
                    override_paths[p[0]] = override_paths[p[0]] + ',' + p[1]
                else:
                    override_paths[p[0]] = p[1]
            else:
                # will replace entries here
                override_paths[p[0]] = p[1]
        else:
            print(f"{p[0]} is not a valid option: {regex_options}")
            exit()

cli = click.CommandCollection(sources=[listAll, out_diff])



def load_new_tower_config(config_parser):
    return config.AnsibleTowerConfigurations(config_parser.credentials_path,
                                             config_parser.job_templates_path,
                                             config_parser.projects_path,
                                             config_parser.inventories_path,
                                             config_parser.inventory_sources_path,
                                             config_parser.workflows_path,
                                             config_parser.permissions_path,
                                             config_parser.hosts_path,
                                             config_parser.users_path,
                                             config_parser.teams_path,
                                             config_parser.organizations_path
                                            )

def derive_relations(config_type, diff, config_parser, repo, branch1, branch2):
    config_path = f'{repo}/{config_type}'
    if config_path == config_parser.credentials_path:
        print('*'*80)
        print("Credentials Genealogy for lines that are added or modified:")
        print('='*80)
        pprint(AnsibleTowerCredentials(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['added_modified'])
        )
        print('*'*80)
        print("Credentials Genealogy for lines that are removed:")
        print('='*80)
        gd.GitDiff.switch_branch(branch1, repo_path=repo)
        pprint(AnsibleTowerCredentials(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['removed'])
        )
        gd.GitDiff.switch_branch(branch2, repo_path=repo)
    elif config_path == config_parser.job_templates_path:
        print('*'*80)
        print("Job Templates Genealogy for lines that are added or modified:")
        print('='*80)
        pprint(AnsibleTowerJobTemplates(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['added_modified'])
        )
        print('*'*80)
        print("Job Templates Genealogy for lines that are removed:")
        print('='*80)
        gd.GitDiff.switch_branch(branch1, repo_path=repo)
        pprint(AnsibleTowerJobTemplates(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['removed'])
        )
        gd.GitDiff.switch_branch(branch2, repo_path=repo)
    elif config_path == config_parser.inventories_path:
        print('*'*80)
        print("Inventories Genealogy for lines that are added or modified:")
        print('='*80)
        pprint(AnsibleTowerInventories(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['added_modified'])
        )
        print('*'*80)
        print("Inventories Genealogy for lines that are removed:")
        print('='*80)
        gd.GitDiff.switch_branch(branch1, repo_path=repo)
        pprint(AnsibleTowerInventories(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['removed'])
        )
        gd.GitDiff.switch_branch(branch2, repo_path=repo)
    elif config_path == config_parser.inventory_sources_path:
        print('*'*80)
        print("Inventory Sources Genealogy for lines that are added or modified:")
        print('='*80)
        pprint(AnsibleTowerInventorySources(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['added_modified'])
        )
        print('*'*80)
        print("Inventory Sources Genealogy for lines that are removed:")
        print('='*80)
        gd.GitDiff.switch_branch(branch1, repo_path=repo)
        pprint(AnsibleTowerInventorySources(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['removed'])
        )
        gd.GitDiff.switch_branch(branch2, repo_path=repo)
    elif config_path == config_parser.projects_path:
        print('*'*80)
        print("Projects Genealogy for lines that are added or modified:")
        print('='*80)
        pprint(AnsibleTowerProjects(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['added_modified'])
        )
        print('*'*80)
        print("Projects Genealogy for lines that are removed:")
        print('='*80)
        gd.GitDiff.switch_branch(branch1, repo_path=repo)
        pprint(AnsibleTowerProjects(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['removed'])
        )
        gd.GitDiff.switch_branch(branch2, repo_path=repo)
    elif config_path == config_parser.permissions_path:
        print('*'*80)
        print("Permissions Genealogy for lines that are added or modified:")
        print('='*80)
        pprint(AnsibleTowerPermissions(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['added_modified'])
        )
        print('*'*80)
        print("Permissions Genealogy for lines that are removed:")
        print('='*80)
        gd.GitDiff.switch_branch(branch1, repo_path=repo)
        pprint(AnsibleTowerPermissions(load_new_tower_config(config_parser)).derive_relations(
            lines_changed=diff['tower-config'][config_type]['removed'])
        )
        gd.GitDiff.switch_branch(branch2, repo_path=repo)
