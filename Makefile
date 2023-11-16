lint:
	ruff format src scripts api tests -q
	ruff src scripts api tests --fix

generate-db:
	python scripts/generate_db.py

test:
	# We'd do it differently in a real project.
	make generate-db
	pytest
