#!/bin/bash

FILE='voice-db.sqlite3';
USERNAME='admin';
EMAIL='admin@thevoice.com.au';
PASSWORD='pass123word';

if [ -f $FILE ]; then
    echo "Deleting old database";
    rm $FILE;
fi

echo "Rebuilding database & schema";
./manage.py migrate;

echo "Creating admin user"
echo "from voice_app.accounts.models import User; User.objects.create_superuser('$USERNAME', '$EMAIL', '$PASSWORD')" | python manage.py shell

echo "Loading mentors, teams, candidates, activities..."
./manage.py load_test_candidates
-0
echo "Database provisioned!"
