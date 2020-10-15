FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y  curl git
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update \
    && apt-get install -y python3.8 python3-pip

RUN curl -SsL https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 \
  | tee /usr/local/bin/json2hcl > /dev/null && chmod 755 /usr/local/bin/json2hcl && json2hcl -version

COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

#ADD ./* /usr/src/app/
WORKDIR /usr/src/git_scrapper

#RUN curl -SsL https://github.com/kvz/json2hcl/releases/download/v0.0.6/json2hcl_v0.0.6_linux_amd64 \
#  | sudo tee /usr/local/bin/json2hcl > /dev/null && sudo chmod 755 /usr/local/bin/json2hcl && json2hcl -version

CMD python3 app.py
