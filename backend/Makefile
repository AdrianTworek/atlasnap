.PHONY: build up up-d down clean logs format lint lint-fix migrate upgrade downgrade

build: ## Build the project
	docker compose build

up: ## Start docker compose services
	docker compose up

up-d: ## Start docker compose services in detached mode
	docker compose up -d

down: ## Stop docker compose services
	docker compose down

clean: ## Stop docker compose services and remove volumes
	docker compose down -v

logs: ## View docker compose services logs
	docker compose logs -f api

format: ## Format code
	docker compose run --rm api sh -c "uv run ruff format ."

lint: ## Run linter
	docker compose run --rm api sh -c "uv run ruff check ."

lint-fix: ## Run linter and fix issues
	docker compose run --rm api sh -c "uv run ruff check . --fix"

migrate: ## Create a new migration (usage: make migrate message="description")
	docker compose run --rm api sh -c "uv run alembic revision --autogenerate -m '$(message)'"

upgrade: ## Apply migrations
	docker compose run --rm api sh -c "uv run alembic upgrade head"

downgrade: ## Rollback one migration
	docker compose run --rm api sh -c "uv run alembic downgrade -1"