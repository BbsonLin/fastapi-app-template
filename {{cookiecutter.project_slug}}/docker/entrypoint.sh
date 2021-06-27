#!/usr/bin/env sh

alembic upgrade head && uvicorn app.main:app --port 5050 --host 0.0.0.0 --reload
