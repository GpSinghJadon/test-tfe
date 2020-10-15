import subprocess, os
import argparse
from terraform import create_main_tf
import ipdb, json

# Note: the destination branch can be a new non-existing branch.


# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--source_repo_url", help="", required=True)                # Required
parser.add_argument("--destination_repo_url", help="", required=True)           # Required
parser.add_argument("--source_branch_name", help="", required=False, default= 'master')            # Optional: default = master
parser.add_argument("--destination_branch_name", help="", required=False)       # Optional: default = source branch name
parser.add_argument("--private_ssh_key_path", help="", required=False)          # Optional: default = source branch name
parser.add_argument("--src_resource_path", help="", required=False)             # Optional: default = root directory of the repo

args = parser.parse_args()

TF_FILES_PRODUCED = {"provider": 'providers.tf', "main": 'main.tf', "variable": 'variables.tf'}

def scrapper(source_repo_url, destination_repo_url, source_branch_name= False, \
             destination_branch_name= False, private_ssh_key_path= False, src_resource_path= False):
    if not destination_branch_name:
        destination_branch_name = source_branch_name
    # PRIVATE_KEY_FILEPATH = "/Users/gajensin/.ssh/test"
    try:
        repo_name = source_repo_url.split("/")[-1]
        command = ['git', 'clone']

        if source_branch_name:
            command.extend(['--single-branch', '--branch', source_branch_name])

        command.append(source_repo_url)

        if 'https' not in source_repo_url:
            if private_ssh_key_path:
                command.extend(['--config', 'core.sshCommand=ssh -i ' + private_ssh_key_path])
            else:
                Exception('For ssh URL repositories, the private ssh key is required to fetch the repository')

        # clone the source repository
        command.append(repo_name)

        subprocess.call(command)
        os.chdir(repo_name)         # change working directory
        # rename remote in the source repo
        subprocess.call(['git', 'remote', 'remove', 'origin'])              # delete the existing remote
        subprocess.call(['git', 'remote', 'add', 'origin', destination_repo_url])   # add new remote

        # Manipulate terraform files
        main_tf_path = src_resource_path if src_resource_path else ''
        create_main_tf(main_tf_path)

        # stage the newly added files and changes
        add_command = ['git', 'add']
        [add_command.append(TF_FILES_PRODUCED[k]) for k in TF_FILES_PRODUCED.keys()]
        subprocess.call(add_command)

        # commit the new changes
        commit_command = ['git', 'commit', '-am', 'initial commit']
        subprocess.call(commit_command)

        # Push to the new repository
        push_command = ['git', 'push', '--set-upstream', 'origin']
        if destination_branch_name:
            push_command.append('{}:{}'.format(source_branch_name, destination_branch_name))
        subprocess.call(push_command)
    except Exception as e:
        print('An EXCEPTION HAS BEEN RAISED: {}'.format(e))

    return repo_name


# The function is called only if the script is ran as a main script
if __name__ == '__main__':
    scrapper(args.source_repo_url, args.destination_repo_url, args.source_branch_name, \
             args.destination_branch_name, args.private_ssh_key_path, args.src_resource_path)
