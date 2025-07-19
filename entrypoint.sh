#!/bin/bash
cd backend
poetry run alembic upgrade head

exec uvicorn src.app:app --host 0.0.0.0 --port 8000
