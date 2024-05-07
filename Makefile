build:
	poetry build

install:
	poetry install

start:
	poetry run uvicorn app.main:app --reload

.PHONY: docker-build
docker-build:
	docker build -t $(DOCKER_IMAGE) .

.PHONY: docker-run
docker-run:
	docker run -d -p 8080:8080 --name $(DOCKER_IMAGE) $(DOCKER_IMAGE)

.PHONY: docker-start
docker-start:
	docker start $(DOCKER_IMAGE)

.PHONY: docker-init
docker-init: docker-build docker-run

.PHONY: docker-push
docker-push:

.PHONY: docker-tag
docker-tag:
	docker tag $(DOCKER_IMAGE) $(DOCKER_REPO)/$(DOCKER_IMAGE)

.PHONY: docker-login
docker-login:
	docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)

.PHONY: docker-kill
docker-kill:
	docker kill $(DOCKER_IMAGE)

.PHONY: docker-stop
docker-stop:
	docker stop $(DOCKER_IMAGE)

.PHONY: docker-clean
docker-clean:
	docker rm $(docker ps -a -q)

.PHONY: docker-clean-images
docker-clean-images:
	docker rmi $(DOCKER_IMAGE)

.PHONY: docker-clean-containers
docker-clean-containers:
	docker rm $(docker ps -a -q)