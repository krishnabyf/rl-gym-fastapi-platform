#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

curl --fail "${BASE_URL}/api/v1/health"
curl --fail "${BASE_URL}/api/v1/environments"

