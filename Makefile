lint:
	pylint ask_fandom

test:
	pytest -vv tests/

server:
	FLASK_APP=server.py flask run
