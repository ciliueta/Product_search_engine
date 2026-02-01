#!/bin/bash
# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
echo "Installing dependencies..."
./venv/bin/pip install -r requirements.txt

# Run the app
echo "Starting application..."
# Kill any process running on port 5000
if command -v fuser &> /dev/null; then
    fuser -k 5000/tcp > /dev/null 2>&1
fi
./venv/bin/python run.py
