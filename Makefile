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

.PHONY: start-funnel
start-funnel:
	@echo "Starting Tailscale funnel for MCP server..."
	@tailscale funnel --bg 8000

.PHONY: stop-funnel
stop-funnel:
	@echo "Stopping Tailscale funnel..."
	@tailscale funnel reset

.PHONY: remove-funnel
remove-funnel:
	@echo "Removing Tailscale funnel..."
	@tailscale funnel reset

.PHONY: list-funnels
list-funnels:
	@echo "Active Tailscale funnel status:"
	@tailscale funnel status
