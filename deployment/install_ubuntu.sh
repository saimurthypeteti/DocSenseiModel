#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y python3.12 python3.12-venv python3-pip git

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

cp -n .env.example .env || true
echo "Edit .env with your LLM API key, then run: streamlit run app.py"
