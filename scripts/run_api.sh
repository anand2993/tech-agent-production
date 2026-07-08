#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH=.
adk api_server --host 0.0.0.0 --port "${PORT:-8080}" tech_agent
