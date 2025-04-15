web: gunicorn myproject.wsgi --log-file -
release: python -m spacy download en_core_web_sm && python manage.py migrate 