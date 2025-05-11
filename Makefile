IMAGE_NAME = pico-dev

build:
	docker build -t $(IMAGE_NAME) .

install:
	pipx install . --force


.PHONY: build
