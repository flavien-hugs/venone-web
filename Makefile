MANAGE := FLASK_APP=run.py


.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	pipenv shell

.PHONY: install
install: ## Install or update dependencies
	pipenv install

freeze: ## Pin current dependencies
	pipenv requirements > requirements.txt

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
