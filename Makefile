PROJECT=conifer
COMPOSE_ARGS=-p ${PROJECT} -f docker-compose.yml

clean:
	docker compose ${COMPOSE_ARGS} down -v --remove-orphans
	docker compose ${COMPOSE_ARGS} rm -f
	rm -rf api/.venv
	rm -rf api/**/__pycache__

build: clean
	docker compose ${COMPOSE_ARGS} build

shell: clean
	docker compose ${COMPOSE_ARGS} run --rm api shell

run: clean
	docker compose ${COMPOSE_ARGS} up
