#!/usr/bin/env bash
set -euo pipefail

# Run the full DataForge demo from the backend directory.
# This creates the demo repo, applies a model change, and prints the analysis.

cd "$(dirname "$0")/.."

python_exec="./.venv/bin/python"
if [ ! -x "$python_exec" ]; then
  python_exec="$(command -v python3 || command -v python)"
fi

echo "Running demo script..."
"$python_exec" demo/demo.py

echo
 echo "Running dataforge analyze-change..."
"$python_exec" ./dataforge analyze-change demo/sample_dbt_repo --markdown
