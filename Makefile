# Usage:
#   make project=empty
#   make clean project=empty

FQBN     = arduino:avr:uno
PORT     = /dev/ttyUSB0
PROJECT ?= $(project)

all: build upload

build:
	arduino-cli compile --fqbn $(FQBN) $(PROJECT)

upload:
	arduino-cli upload -p $(PORT) --fqbn $(FQBN) $(PROJECT)

clean:
	rm -rf $(PROJECT)/build