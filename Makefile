IMAGE_NAME=phillips-hue-mcp-server

.PHONY: build
build:
	docker compose build

.PHONY: run
run:
	docker compose up

.PHONY: down
down:
	docker compose down
