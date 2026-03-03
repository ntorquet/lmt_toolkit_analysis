# Created by Nicolas Torquet at 02/03/2025
# nicolas.torquet@igbmc.fr
# Copyright: CNRS - INSERM - UNISTRA
# CNRS - PHEN-ICS
# PHENOMIN, CNRS UAR2062, INSERM US66, Université de Strasbourg
# Code under GPL v3.0 licence

#!/bin/bash

set -e

FIXTURE_FILE=./lmt_toolkit_api/fixtures/export_data_v1_2.json
DEPLOY=false
UPDATE=false
RESET_DB=false

# Parse arguments
for arg in "$@"; do
    if [[ "$arg" == "deploy" ]]; then
        DEPLOY=true
    elif [[ "$arg" == "update" ]]; then
        UPDATE=true
    elif [[ "$arg" == "reset" ]]; then
        RESET_DB=true
    fi
done

echo "Fixture file to load: $FIXTURE_FILE"

# Load env
if [ -f lmt_toolkit_analysis.env ]; then
    export $(grep -v '^#' lmt_toolkit_analysis.env | xargs)
elif [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "No .env or lmt_toolkit_analysis.env file found!"
    exit 1
fi


# Check DB vars
if [ -z "$DB_NAME" ]; then
    echo "❌ DB_NAME is not set."
    exit 1
fi


# Install Python deps
if [ "$UPDATE" == true ] || ! python3 -c "import lmt_toolkit_api" &>/dev/null || ! python3 -c "import django" &>/dev/null; then
    echo "📦 Installing/reinstalling Python dependencies..."
    pip install --upgrade pip
    pip install -e .
else
    echo "✅ Python dependencies already installed."
fi

# Migrations
echo "🐍 Running Django migrations..."
python3 manage.py makemigrations lmt_toolkit_api --noinput
python3 manage.py migrate --noinput

# Fixtures (conditional load)
if [ -f "$FIXTURE_FILE" ]; then
    echo "🔍 Checking if the table is empty before loading fixture..."
    ROW_COUNT=$(echo "SELECT COUNT(*) FROM lmt_toolkit_analysis_version;" | sqlite -u "$DB_USER" -N)

    if [ "$ROW_COUNT" -eq 0 ]; then
        echo "📥 Table is empty. Loading fixture from $FIXTURE_FILE..."
        python3 manage.py loaddata "$FIXTURE_FILE"
    else
        echo "✅ Table already contains $ROW_COUNT rows. Skipping fixture loading."
    fi
else
    echo "⚠️ Fixture file not found. Skipping fixture loading."
fi


# Run server
if [ "$DEPLOY" == "true" ]; then
    if [ "$DEBUG" == "false" ]; then
        echo "🚀 Starting Gunicorn server..."
        exec gunicorn lmt_toolkit_api.asgi:application --bind 0.0.0.0:8000 --timeout 420 -k uvicorn.workers.UvicornWorker
    else
        echo "⚙️ Starting development server..."
        exec python3 manage.py runserver 0.0.0.0:8000
    fi
else
    echo "✅ Setup complete. Server not started (no 'deploy' flag)."
fi