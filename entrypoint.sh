#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

poetry run task seed organizations

poetry run task seed users

poetry run task seed events

poetry run task seed categories_main

poetry run task seed categories

poetry run task seed posts

# Inicia a aplicação
poetry run uvicorn --host 0.0.0.0 --port 8000 fast_rafa.app:app
