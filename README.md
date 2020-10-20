## Example execution:
```code
python github-scrapper.py --source_repo_url <git-hub-url> --destination_repo_url <git-hub-url> \
--source_branch_name <git-exisiting-branch-name> --destination_branch_name <git-branch-name> \
--src_resource_path <path-of-the-terraform-files-directory>
```
## Example command:
```code
python3 git_repo_extracter.py --source_repo_url https://github.com/someDeveloper89-dev/test-tfe.git \
--destination_repo_url https://github.com/GpSinghJadon/test_repo.git --destination_branch_name testing9
```

## Setup on LINUX (Debian)
* Install PYTHON 3, Python PIP3

``` 
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.8
$ sudo apt-get install python3-pip 
```
* Install Python package via pip:
Execute the below command in the parent directory of the repo

```
$ pip3 install -r requirements.txt 
```
* Setup json2hcl package of the below mentioned repo:
https://github.com/kvz/json2hcl
```
curl -SsL https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 \
  | sudo tee /usr/local/bin/json2hcl > /dev/null && sudo chmod 755 /usr/local/bin/json2hcl && json2hcl -version
  ```

## Docker setup:
# Create an Image of the current project.
```
docker build -t git_scrapper:latest .
```
# Create a running container with the given environment vairables
```
docker run --rm -it -e source_repo_url='https://github.com/someDeveloper89-dev/test-tfe.git' \
-e destination_repo_url='git@github.com:GpSinghJadon/test-tfe.git' -e destination_branch_name='branch-20' 
-e private_ssh_key_path='test'  -v "$(pwd)/:/usr/src/git_scrapper"  git_scrapper:latest
```
```
docker run --rm -it -e source_repo_url='https://github.com/someDeveloper89-dev/test-tfe.git' \
-e destination_repo_url='https://github.com/GpSinghJadon/test-tfe.git' -e destination_branch_name='branch-20' \
-v "$(pwd)/:/usr/src/git_scrapper"  git_scrapper:latest
```

# Notes:
* The destination branch can be a new non-existing branch.
