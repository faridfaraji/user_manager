PROJECT_NAME = user_manager
TOPDIR = $(shell git rev-parse --show-toplevel)

default: help


help: # Display help
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST) | sort


run: ## Start the service locally
	uvicorn user_manager.main:app --reload --port 9003

run-celery:
	./entrypoint.sh $(NUM_WORKERS)
