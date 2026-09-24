#!/usr/bin/env bash
# One-command setup + run: creates the venv, installs dependencies,
# installs the Chromium browser Playwright needs, then runs the app.
set -e

cd "$(dirname "$0")"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
playwright install chromium

echo
python3 run.py
