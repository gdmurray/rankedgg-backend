web: python3 manage.py collectstatic --noinput; gunicorn --env DJANGO_SETTINGS_MODULE=ranked.prod ranked.wsgi
release: python3 manage.py migrate