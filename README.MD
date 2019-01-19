Run command to start Celery Beat periodic scraping task
celery -A kickstarter worker -B -l DEBUG -f ./celerybeat.log