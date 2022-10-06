#!/bin/bash
echo "Dropping old environment..."
rm -R .venv

echo "Recreate new virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Install requirements..."
pip3 install -r requirements.txt

echo "Initialization finished! Activate virtual environment via: source .venv/bin/activate"