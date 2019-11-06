all: build up
.PHONY: all

build:
	@echo "---> Building Docker images..."
	@docker-compose build
	@echo "Done."
.PHONY: install

up:
	@echo "---> Starting Docker containers..."
	@docker-compose up
.PHONY: build

clean:
	@echo "---> Cleaning up..."
	@docker-compose clean
	@echo "Done."
.PHONY: clean
