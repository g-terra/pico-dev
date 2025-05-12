IMAGE_NAME = pico-dev

build:
	docker build ./docker -t $(IMAGE_NAME) -f docker/Dockerfile

install:
	pipx install . --force

.PHONY: build
