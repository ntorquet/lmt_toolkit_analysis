#!/bin/bash

if [ "$SERVICE_ROLE" = "web" ]; then

    echo "🛠️ Running makemigrations..."
    python3 manage.py makemigrations lmt_toolkit_analysis --noinput

    echo "📦 Applying migrations..."
    python3 manage.py migrate --noinput

    # 🚨 Explicit check of critical tables before loading data
    DB_NAME="db.sqlite3"

    echo "📋 Listing all tables in $DB_NAME..."
    sqlite3 "$DB_NAME" ".tables"

    echo "🔍 Verifying that all required tables exist before loading fixtures..."
    REQUIRED_TABLE="lmt_toolkit_analysis_version"
    TABLE_EXISTS=$(sqlite3 "$DB_NAME" "SELECT name FROM sqlite_master WHERE type='table' AND name='$REQUIRED_TABLE';")


    if echo "$TABLE_EXISTS" | grep -q "$REQUIRED_TABLE"; then
        echo "✅ Table $REQUIRED_TABLE found, safe to load fixture."
    else
        echo "❌ Required table $REQUIRED_TABLE does not exist. Migration may have failed. Aborting fixture load."
        exit 1
    fi

    REQUIRED_TABLE="lmt_toolkit_analysis_eventdocumentation"
    TABLE_EXISTS=$(sqlite3 "$DB_NAME" "SELECT name FROM sqlite_master WHERE type='table' AND name='$REQUIRED_TABLE';")

    if echo "$TABLE_EXISTS" | grep -q "$REQUIRED_TABLE"; then
        echo "✅ Table $REQUIRED_TABLE found, safe to load fixture."
    else
        echo "❌ Required table $REQUIRED_TABLE does not exist. Migration may have failed. Aborting fixture load."
        exit 1
    fi

    # ✅ Loading fixtures conditionnel si la table est vide
    if [ -n "$FIXTURE_FILE" ] && [ -f "$FIXTURE_FILE" ]; then
        echo "🔍 Checking if the corresponding table is empty before loading fixture..."

        TABLE_NAME="lmt_toolkit_analysis_version"
        ROW_COUNT1=$(sqlite3 "$DB_NAME" "SELECT COUNT(*) FROM $TABLE_NAME;")

        TABLE_NAME="lmt_toolkit_analysis_eventdocumentation"
        ROW_COUNT2=$(sqlite3 "$DB_NAME" "SELECT COUNT(*) FROM $TABLE_NAME;")

    #    if [ "$ROW_COUNT1+$ROW_COUNT2" -eq 0 ]; then
        echo "📥 Table $TABLE_NAME is empty. Loading fixture from $FIXTURE_FILE..."
        python3 manage.py loaddata "$FIXTURE_FILE"
    #    else
    #        echo "✅ Table $TABLE_NAME already contains data ($ROW_COUNT1+$ROW_COUNT2 rows). Skipping fixture loading."
    #    fi
    else
        echo "⚠️ Fixture file not found or not defined. Skipping fixture loading."
    fi

    # ✅ Starting the server
    if [ "$(echo "$DEBUG" | tr '[:upper:]' '[:lower:]')" = "false" ]; then
        echo "🧪 Collecting static files..."
        python3 manage.py collectstatic --noinput

        echo "🚀 Starting Gunicorn server..."
        exec gunicorn lmt_toolkit_analysis.asgi:application --bind 0.0.0.0:8000 --timeout 420 -k uvicorn.workers.UvicornWorker
    else
        echo "⚙️ Starting development server..."
        exec python3 manage.py runserver 0.0.0.0:8000
    fi
elif [ "$SERVICE_ROLE" = "worker" ]; then
    echo "⏳ Waiting for RabbitMQ..."
    until nc -z rabbit 5672; do
      sleep 1
    done

    echo "✅ RabbitMQ is up. Starting Celery..."
    exec celery -A lmt_toolkit_analysis worker -l info -P gevent
fi
exec "$@"