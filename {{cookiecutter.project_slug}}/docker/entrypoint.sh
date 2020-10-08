#!/usr/bin/env sh

uvicorn app.main:app --port 5050 --host 0.0.0.0 --reload