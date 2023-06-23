set windows-shell := ["powershell.exe", "-Command"]

default: format lint type-check
all: format lint type-check test

format:
    poetry run -- black .
    poetry run -- isort .
    poetry run -- pydocstringformatter --write .

format-check:
    poetry run -- black --check .
    poetry run -- isort --check .
    poetry run -- pydocstringformatter --exit-code .

lint:
    poetry run -- pylint ./intervals ./tests

type-check:
    poetry run -- mypy .

test:
    poetry run -- pytest .
