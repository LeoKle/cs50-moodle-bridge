#!/bin/bash
# Quick start script for running the frontend in mock mode

echo "🧪 Starting CS50 Moodle Bridge Frontend in MOCK mode..."
echo "No backend required - using sample data"
echo ""

export USE_MOCK_SERVICES=true
uv run streamlit run src/app.py
