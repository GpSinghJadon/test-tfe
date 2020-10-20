eval `ssh-agent -s`

whoami

mkdir -p /root/.ssh/
touch /root/.ssh/known_hosts
ssh-keyscan github.com >> /root/.ssh/known_hosts
#chmod 0700 .ssh
#chmod 0400 .ssh/test*
cp .ssh/test* /root/.ssh/
cp .ssh/config /root/.ssh/

ssh-add /root/.ssh/test
cat /root/.ssh/known_hosts
python3 app.py
