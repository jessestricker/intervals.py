set windows-shell := ["powershell.exe", "-Command"]

default: format type-check lint

format:
    poetry run -- black .
    poetry run -- isort .
    poetry run -- pydocstringformatter .

type-check:
    poetry run -- mypy .

lint:
    poetry run -- pylint ./intervals ./tests

test:
    poetry run -- pytest .
