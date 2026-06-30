#!/usr/bin/env bash
set -euo pipefail

# Run the full DataForge demo from the backend directory.
# This creates the demo repo, applies a model change, and prints the analysis.

cd "$(dirname "$0")/.."

echo "Running demo script..."
uv run python demo/demo.py

echo
echo "Running dataforge analyze-change..."
./dataforge analyze-change
