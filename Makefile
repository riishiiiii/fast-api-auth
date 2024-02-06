# Determine the operating system
OS := $(shell uname)

# Use different commands based on the operating system
ifeq ($(OS), Linux)
    # Commands for Linux (Ubuntu)
    DC := docker-compose
    PS := sudo docker ps
    BUILD := sudo $(DC) build
    UP := sudo $(DC) up
    DOWN := sudo $(DC) down
else ifeq ($(OS), Windows_NT)
    # Commands for Windows
    DC := docker-compose
    PS := docker ps
    BUILD := $(DC) build
    UP := $(DC) up
    DOWN := $(DC) down
else
    $(error Unsupported operating system)
endif

# Define targets
ps:
	$(PS)

build:
	$(BUILD)

up:
	$(UP)

down d:
	$(DOWN)

run r: build up
