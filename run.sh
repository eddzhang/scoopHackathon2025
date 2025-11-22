#!/bin/bash

# Nexus AI Council - Run Script

echo "🏛️ NEXUS AI COUNCIL LAUNCHER"
echo "============================="
echo ""
echo "Select an option:"
echo "1) Run CLI interface"
echo "2) Start web dashboard"
echo "3) Install dependencies"
echo "4) Setup environment"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo "Starting CLI interface..."
        if [ -z "$1" ]; then
            python nexus_council.py
        else
            python nexus_council.py "$@"
        fi
        ;;
    2)
        echo "Starting web dashboard..."
        echo "Opening http://localhost:8000 in your browser..."
        python web_app.py
        ;;
    3)
        echo "Installing dependencies..."
        pip install -r requirements.txt
        echo "✅ Dependencies installed"
        ;;
    4)
        echo "Setting up environment..."
        if [ ! -f .env ]; then
            cp .env.example .env
            echo "✅ Created .env file"
            echo "⚠️  Please edit .env and add your API keys"
        else
            echo "⚠️  .env file already exists"
        fi
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
