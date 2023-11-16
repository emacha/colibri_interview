# Colibri Tech Test

Tech test for Colibri

## Pre requisites

Make sure you have the following installed:

- Python 3.11
- [Poetry](https://python-poetry.org/docs/#installation)
- [Make](https://en.wikipedia.org/wiki/Make_%28software%29)

## Alternatives

### Poetry

If you can't or don't want to install poetry, you can use the `requirements.txt` file to install the dependencies.

### Make

If you don't have `make`, just open the `Makefile` and run the commands manually.

## Setup

### Virtual environment

```shell
poetry install
poetry shell
```

### Data

Put the `MOCK_DATA.json` file in the root of the project.

## Running the code

- `make lint` to lint the code
- `make test` to run the tests
- `make generate-db` to create a fresh sqlite db populated with `MOCK_DATA`.
