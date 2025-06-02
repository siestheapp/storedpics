#!/bin/bash
# Remove any old venvs
rm -rf venv .venv

# Create and activate a new venv
python3 -m venv venv
source venv/bin/activate

# Install requirements and supervisor
pip install -r requirements.txt
pip install supervisor

# Kill any old supervisor or python processes
pkill -9 supervisord || true
pkill -9 python || true

# Remove old supervisor pid file if it exists
rm -f logs/supervisord.pid

# Start supervisor
supervisord -c supervisor.conf

# Show status
supervisorctl status 