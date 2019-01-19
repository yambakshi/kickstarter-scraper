from __future__ import absolute_import, unicode_literals
from celery import shared_task, periodic_task
from datetime import timedelta
from kickstarter import kickstarterservice


@task(name='scrape')
def scrape_kickstarter():
    kickstarterservice.scrape()
