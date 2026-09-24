#!/usr/bin/env bash
# One-command setup: creates the venv, installs dependencies, and installs
# the Chromium browser Playwright needs for the login step.
set -e

cd "$(dirname "$0")"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
playwright install chromium

echo
echo "Setup complete. Run the app with:"
echo "  source venv/bin/activate"
echo "  python3 run.py"
