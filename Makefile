.PHONY: *

DOCKER_SERVER_RUN := @docker compose run --rm server 
POETRY_LOCAL_RUN := @poetry run 


test: 
	${DOCKER_SERVER_RUN} pytest -s

alembic_revision: # add new database migration
	$(DOCKER_SERVER_RUN) alembic revision --autogenerate -m "$(MESSAGE)"

alembic_upgrade: # apply database migrations
	$(DOCKER_SERVER_RUN) alembic upgrade head

alembic_downgrade: # revert last database migration
	$(DOCKER_SERVER_RUN) alembic downgrade -1

lint:
	${DOCKER_SERVER_RUN} black ./