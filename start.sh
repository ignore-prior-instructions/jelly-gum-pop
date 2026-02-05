#!/bin/bash
# Quick start script for jellygumpop.party

set -e

echo "✨🦄💖 jellygumpop.party startup ✨🦄💖"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
    echo "Then run this script again."
    exit 1
fi

# Check if API key is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  ANTHROPIC_API_KEY not set in .env file"
    echo "Please edit .env and add your API key, then run this script again."
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Check if db.sqlite3 exists
if [ ! -f db.sqlite3 ]; then
    echo "📦 Running migrations..."
    python manage.py migrate
    echo ""
fi

echo "🚀 Starting server..."
echo ""
echo "Visit http://localhost:8000 to start making quizzes!"
echo ""

python manage.py runserver
