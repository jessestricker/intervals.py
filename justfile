set windows-shell := ["powershell.exe", "-Command"]

default: format lint type-check
all: format lint type-check test

format:
    poetry run -- black .
    poetry run -- isort .
    poetry run -- pydocstringformatter .

lint:
    poetry run -- pylint ./intervals ./tests

type-check:
    poetry run -- mypy .

test:
    poetry run -- pytest .
