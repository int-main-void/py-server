FROM ubuntu

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python python-pip

WORKDIR /opt/app

ADD root /opt/app

# Install app dependencies
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/bin/python src/main/python/server.py"]
