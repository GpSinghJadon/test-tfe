eval `ssh-agent -s`
dos2unix *

whoami

mkdir -p /root/.ssh/
touch /root/.ssh/known_hosts
ssh-keyscan github.com >> /root/.ssh/known_hosts
cp /usr/src/git_scrapper/.ssh/id_rsa* /root/.ssh/
cp /usr/src/git_scrapper/.ssh/config /root/.ssh/

chmod 0700 /root/.ssh
chmod 0400 /root/.ssh/id_rsa*

ssh-add /root/.ssh/id_rsa
cat /root/.ssh/known_hosts
ls /root/.ssh
export GIT_SSL_NO_VERIFY=1
curl -k -SsL https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 | tee /usr/local/bin/json2hcl > /dev/null && chmod 755 /usr/local/bin/json2hcl && json2hcl -version
python3 app.py
