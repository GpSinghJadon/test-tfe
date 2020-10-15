docker build . -t git_scrapper:latest
docker run --rm -it -e source_repo_url='https://github.com/someDeveloper89-dev/test-tfe.git' \
                    -e destination_repo_url='https://github.com/GpSinghJadon/test-tfe.git' \
                    -e destination_branch_name='branch-16'
                    -v "$(pwd)/:/usr/src/git_scrapper"
            git_scrapper:latest
# docker run --rm -it -e TFE_TEAM_TOKEN=$(cat /.tfe_team_token)
# -e TFE_TOKEN=$(cat /.tfe_token) -w /app -v "$(pwd)/:/app" ngc_cli:latest bash