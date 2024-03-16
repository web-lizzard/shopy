.PHONY: *

BACKEND_RUN := @docker compose run --rm server 

test: 
	${BACKEND_RUN} pytest -s


