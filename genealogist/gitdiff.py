import re
import sys
import git
from pathlib import Path
from os.path import relpath


class GitDiff:
    @staticmethod
    def git_diff(hashes=[], repo_path='satlab-tower-example-repo',
                 roles_path=None, playbooks_path=None, config_path=None):
        """
        Utility to assemble a list of files that differ between two commits.
        It organizes this list into three categories: 'roles', 'playbooks',
        and 'tower-config'.

        Args:
            hashes (list): A list of commit hashes to compare.
            repo_path (list): Base of the git repository.
            roles_path (list): Path(s) of dirs containing Ansible roles.
            playbooks_path (list): Path(s) containing Ansible playbooks.
            config_path (list): Path(s) of dirs containing config files.

        Returns:
            A dict with three keys (one for each of the above categories).
            Each contains a set of strings of files in that part of the diff.
        """
        repo = git.Repo(repo_path)

        if len(hashes) > 2:
            raise TypeError('maximum number of commits passed to diff is 2')
        elif len(hashes) == 2:
            branches = f'{hashes[0]}..{hashes[1]}'
        elif len(hashes) == 1:
            branches = hashes[0]  # defaults to HEAD if none given
        else:
            branches = None  # handled by git module
        # multiple paths can be used
        if roles_path is None:
            roles_path = [
                'satlab-tower-example-repo/roles',
                'satlab-tower-example-repo/external-roles']
        if playbooks_path is None:
            playbooks_path = ['../satlab-tower-example-repo/playbooks']
        if config_path is None:
            config_path = [(
                'satlab-tower-example-repo/playbooks/' +
                'setup-ansible-tower/tower-configs')]

        roles_path = [roles_path] if isinstance(roles_path, str) \
            else roles_path
        playbooks_path = [playbooks_path] if isinstance(playbooks_path, str) \
            else playbooks_path
        config_path = [config_path] if isinstance(config_path, str) \
            else config_path

        # At time of writing, there is a bug in GitPython
        # where it does not handle multiple subpaths
        # and uses an invalid git diff flag "--paths".
        # This can be bypassed with a loop.
        overall_diff = set(repo.git.diff(branches, name_only=True)
                           .splitlines())
        if len(overall_diff) > 20:  # Assuming anything above this would be probably slow to execute
            print(f"\n\nWARN: Diff between two branches {branches} is too big, genealogist may run slower.\n\n")
            print(f"\n\nINFO:Consider rebasing {branches} on one another appropriately.\n\n")
        # Organize the sets into proper categories
        diff = GitDiff.categorize_diff(overall_diff, branches, repo_path,
                                       roles_path, playbooks_path, config_path)
        return diff

    @staticmethod
    def diff_lines(repo, branches, path):
        """Gets the line numbers that were changed in the format of a
        unified output diff hunk"""
        diff = repo.git.diff(branches, unified=0, relative=path).splitlines()

        hunk_headers = [item for item in diff if item.startswith('@@')]
        lines = []
        for item in hunk_headers:
            lines.extend(re.findall(r'@@ (.*) @@', item))

        # scan the diff to find out what lines are being changed
        # if we have two hunks, @@ -1 +3,4 @@ and @@ -5,6 +7,8 @@
        # default value of 'empty' numbers after a comma is 1
        # final value of scan would be [[1, 1], [3, 4], [5, 6], [7, 8]]
        scan = []
        for item in lines:
            before = re.search(r'-(.*) +', item).group(1).split(',')
            before = [int(i) for i in before]
            after = re.search(r'\+(.*)', item).group(1).split(',')
            after = [int(i) for i in after]
            scan.extend([before, after])

        removed = set()
        added_modified = set()

        total_lines_removed = 1
        if len(scan[0]) == 2:
            total_lines_removed = scan[0][1]
        total_lines_added_modified = 1
        if len(scan[1]) == 2:
            total_lines_added_modified = scan[1][1]

        remove_counter, add_counter = 0, 0  # simple line counters for loop
        remove_offset, add_offset = 0, 1  # counter for the current diff hunk

        # since we preprocessed the first diff hunk to initialize our counters
        # set the next loop to start immediately after the first hunk
        start = 0
        for i in range(len(diff)):
            if diff[i].startswith('@@'):
                start = i + 1
                break

        # main line counting loop
        for item in diff[start:]:
            if item.startswith('@@'):
                remove_offset += 2
                add_offset += 2
                total_lines_removed = 1
                if len(scan[remove_offset]) == 2:
                    total_lines_removed = scan[remove_offset][1]
                total_lines_added_modified = 1
                if len(scan[add_offset]) == 2:
                    total_lines_added_modified = scan[add_offset][1]
                remove_counter, add_counter = 0, 0


            # count lines that have been removed
            if item.startswith('-') and (total_lines_removed != 0):
                removed.add(scan[remove_offset][0] + remove_counter)
                remove_counter += 1
                total_lines_removed -= 1

            # count lines that have been added/modified.
            # if they are also present in the "removed" list, then they were
            # actually modified, so we remove them from that list.
            if item.startswith('+') and (total_lines_added_modified != 0):
                added_modified.add(scan[add_offset][0] + add_counter)
                removed -= {scan[add_offset][0] + add_counter}
                add_counter += 1
                total_lines_added_modified -= 1
        return {'removed': sorted(removed), 'added_modified': sorted(added_modified)}

    @staticmethod
    def remove_prefix(paths, prefix):
        prefix = str(prefix)
        for i in range(len(paths)):
            if paths[i].startswith(prefix):
                paths[i] = paths[i][len(prefix) + 1:]
        return paths

    @staticmethod
    def categorize_diff(diff, branches, repo_path, roles_path,
                        playbooks_path, config_path):
        repo = git.Repo(repo_path)

        roles_list, playbooks_diff, config_diff = dict(), dict(), dict()

        # saved for later when doing role logic
        roles_prefixes = []
        for p in roles_path:
            roles_prefixes.append(Path(p).resolve())

        # Strip the parent repo path to categorize different kinds of files
        roles_path = GitDiff.remove_prefix(roles_path, repo_path)
        playbooks_path = GitDiff.remove_prefix(playbooks_path, repo_path)
        config_path = GitDiff.remove_prefix(config_path, repo_path)
        for item in diff:
            for path in roles_path:
                if item.startswith(path):  # we don't need line numbers for roles/playbooks atm
                    roles_list[item] = {}  # GitDiff.diff_lines(repo, branches, item)
            for path in playbooks_path:
                if item.startswith(path):
                    playbooks_diff[item] = {}
                        # GitDiff.diff_lines(repo, branches, item)
            for path in config_path:
                if item.startswith(path):
                    config_diff[item] = \
                        GitDiff.diff_lines(repo, branches, item)

        # Roles need a special definition --
        # overall name of a role is the parent of the tasks/ folder.
        # This loop starts from the altered file and recursively moves upwards
        # to find a tasks/ folder, then assigns the parent folder as the "role"
        # that was changed.
        roles_diff = dict()

        root = Path(repo_path).resolve()
        for file_path in roles_list:
            role = (root / file_path).parent
            while not (role / 'tasks').is_dir():
                role = role.parent
                if role == '.':
                    err_msg = (
                        f'File {file_path} was found to have changed in the '
                        'roles directory, but the overall role appears to be '
                        'missing a tasks/ folder. Ensure the role directory '
                        'is properly organized.'
                    )
                    raise FileNotFoundError(err_msg)

            # strip prefix of the overall roles directory
            for pre in roles_prefixes:
                absolute_role = role.resolve()
                if str(absolute_role).startswith(str(pre)):
                    roles_diff[relpath(role, pre)] = roles_list[str(file_path)]

        result = {
            'roles': roles_diff,
            'playbooks': playbooks_diff,
            'tower-config': config_diff
            }
        return result

    @staticmethod
    def switch_branch(branch, repo_path='.'):
        repo = git.Repo(repo_path)
        repo.git.execute(command=["git", "checkout", branch])

if __name__ == '__main__':
    vars = sys.argv[1:]
    GitDiff.git_diff(*vars)
