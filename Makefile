MANAGE := FLASK_APP=runserver.py

ifneq (,$(wildcard ./.flaskenv))
    include ./.flaskenv
    export
endif

.PHONY: help
help: ## Show this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: pipenv-shell
pipenv-shell: ## Make a new virtual environment
	pipenv shell

.PHONY: pipenv-install
pipenv-install: ## Install or update dependencies
	pipenv install

.PHONY: pip-install
pip-install: ## Install packages with pip
	pip install -r env/dev.txt

createdb: ## Create database
	$(MANAGE) flask init_db

init: ## Init database
	$(MANAGE) flask db init

migrate: ## Generate an initial migration
	$(MANAGE) flask db migrate -m 'Intial Migration'

upgrade: ## Apply the upgrade to the database
	$(MANAGE) flask db upgrade

test: ## Run the unit tests
	python3 -m unittest discover -s tests

shell: ## Flask Shell Load
	$(MANAGE) flask shell

.PHONY: kill-process
kill-process: ## Kill process the server
	sudo lsof -t -i tcp:5000 | xargs kill -9

.PHONY: run
run: ## Run
	docker compose up --build -d

.PHONY: restart
restart:	## restart one/all containers
	docker compose restart $(s)

.PHONY: create-db
create-db: ## Run
	docker-compose exec venone FLASK_APP=runserver.py flask db init && FLASK_APP=runserver.py flask init_db

.PHONY: logs
logs: ## View logs from one/all containers
	docker compose logs -f $(s)

.PHONY: down
down: ## Stop the services, remove containers and networks
	docker compose down -v

.PHONY: destroy-all
destroy-all: ## destroy one/all images
	docker rmi -f $(docker images -a -q)
