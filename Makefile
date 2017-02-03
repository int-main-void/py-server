#
# Makefile for building a virtualenv-based Python server and wrapping into a Docker image
#
# env/bin/pip install <library>
# env/bin/pip freeze > requirements.txt
#
.DEFAULT_GOAL := all

SRC= src requirements.txt

IMAGE_DIR=image/
IMAGE_NAME=mwn-python-server:dev-latest
DOCKER_REGISTRY=a-custom-registry.com # edit this to make the target work

clean:
	rm -rf env
	rm -rf $(IMAGE_DIR)

env: requirements.txt
	virtualenv env
	env/bin/pip install -Ur requirements.txt

build-service: env

image: 
	mkdir -p $(IMAGE_DIR)/root
	cp conf/Dockerfile $(IMAGE_DIR)
	cp -a $(SRC) $(IMAGE_DIR)/root
	docker build $(IMAGE_DIR) -t $(IMAGE_NAME)

all: image

publish-image: image
	docker push $(DOCKER_REGISTRY) $(IMAGE_NAME)


run-local: build-service
	env/bin/python src/main/python/server.py

run-image: image
	docker-compose -f conf/docker-compose.yml up

