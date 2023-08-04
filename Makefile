PROJECT=conifer
COMPOSE_ARGS=-p ${PROJECT} -f docker-compose.yml

build:
	docker compose ${COMPOSE_ARGS} build

shell:
	docker compose ${COMPOSE_ARGS} run --rm api shell

clean:
	docker compose ${COMPOSE_ARGS} down -v --remove-orphans
	docker compose ${COMPOSE_ARGS} rm -f
	rm -rf conifer/.venv

run: clean
	docker compose ${COMPOSE_ARGS} up
