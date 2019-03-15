lint:
	pylint ask_fandom

test:
	pytest -vv tests/

server:
	FLASK_APP=server.py flask run --host=0.0.0.0 --port=5050
