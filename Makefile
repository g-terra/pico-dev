IMAGE_NAME = pico-dev

build:
	docker build -t $(IMAGE_NAME) .

.PHONY: build
