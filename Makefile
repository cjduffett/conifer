PROJECT=conifer
COMPOSE_ARGS=-p ${PROJECT} -f docker-compose.yml

clean_py:
	rm -rf api/.venv
	rm -rf api/**/__pycache__

clean_docker:
	docker compose ${COMPOSE_ARGS} down -v --remove-orphans
	docker compose ${COMPOSE_ARGS} rm -f

build: clean_py
	docker compose ${COMPOSE_ARGS} build

shell: clean_docker
	docker compose ${COMPOSE_ARGS} run --rm api shell

run: clean_docker
	docker compose ${COMPOSE_ARGS} up
