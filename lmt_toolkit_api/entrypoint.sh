#!/bin/bash

echo "🛠️ Running makemigrations..."
python3 manage.py makemigrations mousetube_api --noinput

echo "📦 Applying migrations..."
python3 manage.py migrate --noinput

# 🚨 Explicit check of critical tables before loading data
echo "🔍 Verifying that all required tables exist before loading fixtures..."
REQUIRED_TABLE="mousetube_api_protocol"
TABLE_EXISTS=$(echo "SHOW TABLES LIKE '$REQUIRED_TABLE';" | mariadb -h db -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME")

if echo "$TABLE_EXISTS" | grep -q "$REQUIRED_TABLE"; then
    echo "✅ Table $REQUIRED_TABLE found, safe to load fixture."
else
    echo "❌ Required table $REQUIRED_TABLE does not exist. Migration may have failed. Aborting fixture load."
    exit 1
fi

# ✅ Loading fixtures conditionnel si la table est vide
if [ -n "$FIXTURE_FILE" ] && [ -f "$FIXTURE_FILE" ]; then
    echo "🔍 Checking if the corresponding table is empty before loading fixture..."

    TABLE_NAME="mousetube_api_protocol"

    ROW_COUNT=$(echo "SELECT COUNT(*) FROM $TABLE_NAME;" | mariadb -h db -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -N)

    if [ "$ROW_COUNT" -eq 0 ]; then
        echo "📥 Table $TABLE_NAME is empty. Loading fixture from $FIXTURE_FILE..."
        python3 manage.py loaddata "$FIXTURE_FILE"
    else
        echo "✅ Table $TABLE_NAME already contains data ($ROW_COUNT rows). Skipping fixture loading."
    fi
else
    echo "⚠️ Fixture file not found or not defined. Skipping fixture loading."
fi

# ✅ Starting the server
if [ "$(echo "$DEBUG" | tr '[:upper:]' '[:lower:]')" = "false" ]; then
    echo "🧪 Collecting static files..."
    python3 manage.py collectstatic --noinput

    echo "🚀 Starting Gunicorn server..."
    exec gunicorn mousetube_api.asgi:application --bind 0.0.0.0:8000 --timeout 420 -k uvicorn.workers.UvicornWorker
else
    echo "⚙️ Starting development server..."
    exec python3 manage.py runserver 0.0.0.0:8000
fi