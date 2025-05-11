IMAGE_NAME = pico-dev
DEVICE = /dev/ttyACM0
MOUNT_DIR = $(CURDIR)/src

SHELL   := /bin/bash
.PHONY: init
.SILENT:

init:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -U micropython-rp2-pico_w-stubs --target typings --no-user && \
	npm install && \
	echo "✔  venv + stubs + npm modules installed"

run:
	docker run --rm -it \
		--device=$(DEVICE) \
		-v $(MOUNT_DIR):/src \
		-e DEVICE=$(DEVICE) \
		$(IMAGE_NAME) run

sync-src:
	docker run --rm -it \
		--device=$(DEVICE) \
		-v $(MOUNT_DIR):/src \
		-e DEVICE=$(DEVICE) \
		$(IMAGE_NAME) sync

sync-lib:
	docker run --rm -it \
		--device=$(DEVICE) \
		-v $(CURDIR)/lib:/src/lib \
		-e DEVICE=$(DEVICE) \
		$(IMAGE_NAME) sync

sync: sync-src sync-lib
	echo "project sync completed"

list:
	docker run --rm -it \
		--device=$(DEVICE) \
		-v $(MOUNT_DIR):/src \
		-e DEVICE=$(DEVICE) \
		$(IMAGE_NAME) list

clean:
	docker run --rm -it \
		--device=$(DEVICE) \
		-v $(MOUNT_DIR):/src \
		-e DEVICE=$(DEVICE) \
		$(IMAGE_NAME) clean

shell:
	docker run --rm -it \
		--device=$(DEVICE) \
		-v $(MOUNT_DIR):/src \
		-e DEVICE=$(DEVICE) \
		$(IMAGE_NAME) shell

web:
	@echo "Starting Tailwind in watch mode…"
	@npx @tailwindcss/cli -i ./src/web/static/styles/tailwind.css -o ./src/web/static/styles/main.css --watch & \
	echo "Starting live-server…" && \
	live-server ./src/web/static \
	  --open=index.html \
	  --watch=src/web/static/styles,src/web/static/scripts
