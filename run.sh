#!/usr/bin/env bash
# 어느 위치에서 실행하든 프로젝트 루트를 기준으로 uvicorn 기동
cd "$(dirname "$0")"
exec .venv/bin/python -m uvicorn jb.main:app --reload "$@"
