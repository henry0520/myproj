#!/bin/bash
python manage.py collectstatic --noinput
echo "Apply database migrations"
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('testuser', 'testuser@venn.bio', '1234')" | python manage.py shell
