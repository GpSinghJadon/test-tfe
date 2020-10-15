import os
from git_repo_extracter import scrapper


source_repo_url= os.environ.get('source_repo_url', False)
destination_repo_url= os.environ.get('destination_repo_url', False)
source_branch_name = os.environ.get('source_branch_name', False)
destination_branch_name = os.environ.get('destination_branch_name', False)
private_ssh_key_path = os.environ.get('private_ssh_key_path', False)
src_resource_path = os.environ.get('src_resource_path', False)

scrapper(source_repo_url, destination_repo_url, \
         source_branch_name, destination_branch_name,\
         private_ssh_key_path, src_resource_path)
