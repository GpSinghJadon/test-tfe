FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y  curl git python3 python3-pip openssl dos2unix
# RUN apt-get install -y software-properties-common
# RUN add-apt-repository ppa:deadsnakes/ppa
# RUN apt-get update \
#     && apt-get install -y python3.8 python3-pip

# RUN apt-get update \
    # && apt-get install -y vim jq sudo python3 python3-pip curl git openssl
    
RUN git config --global user.email "robin.budhathoki@pwc.com"
RUN git config --global user.name "robin-budhathoki"

# RUN curl -SsL https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 \
#   | tee /usr/local/bin/json2hcl > /dev/null && chmod 755 /usr/local/bin/json2hcl && json2hcl -version
#RUN mkdir /root/.ssh/known_hosts
RUN mkdir -p /usr/src/git_scrapper/.ssh
COPY ./requirements.txt ./
COPY ./.ssh/ /usr/src/git_scrapper/
COPY ./* /usr/src/git_scrapper/
RUN pip3 install --no-cache-dir -r requirements.txt

#ADD ./* /usr/src/app/
WORKDIR /usr/src/git_scrapper/


#RUN curl -SsL https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 \
#  | sudo tee /usr/local/bin/json2hcl > /dev/null && sudo chmod 755 /usr/local/bin/json2hcl && json2hcl -version

CMD ["sh", "/usr/src/git_scrapper/start_app.sh"]
