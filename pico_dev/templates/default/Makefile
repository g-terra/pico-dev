IMAGE_NAME = pico-dev
DEVICE = /dev/ttyACM0
MOUNT_DIR = $(CURDIR)/src

run:
	docker run --rm -it \
		--device=$(DEVICE) \
		-v $(MOUNT_DIR):/src \
		-e DEVICE=$(DEVICE) \
		$(IMAGE_NAME) run

sync:
	docker run --rm -it \
		--device=$(DEVICE) \
		-v $(MOUNT_DIR):/src \
		-e DEVICE=$(DEVICE) \
		$(IMAGE_NAME) sync

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
