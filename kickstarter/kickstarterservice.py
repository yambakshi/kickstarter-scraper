import os
import re
import selenium as se
from django.utils import timezone
from django.conf import settings
from selenium import webdriver
from kickstarter.models import PopularCampaign
from datetime import datetime, timedelta


def scrape():
    options = se.webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(
        executable_path=os.path.join(settings.BASE_DIR, 'chromedriver_win32\\chromedriver.exe'), chrome_options=options)
    driver.set_window_size(1920, 1080)
    driver.get('https://www.kickstarter.com/discover/popular')

    campaigns = []
    campaigns_ids = [c.get_attribute('id') for c in driver.find_elements_by_css_selector(
        '#projects_list > div:nth-child(1) > div:nth-child(-n+10)')]

    # Iterate campaign elements IDs
    for id in campaigns_ids:
        campaign = driver.find_element_by_id(id)
        thumbnail = campaign.find_element_by_css_selector(
            'div > div > div > div.relative.self-start > a.block.img-placeholder.w100p > img').get_attribute('src')
        campaign.find_element_by_css_selector(
            'div > div > div > div.relative.self-start > a.block.img-placeholder.w100p').click()
        name = driver.find_element_by_css_selector(
            '#react-project-header > div > div > div.grid-row.pt9-lg.mt3.mt0-lg.mb6-lg.order-2-md.order-1-lg > div > div.grid-row.hide.flex-md.flex-column.flex-row-md.relative > div.col-20-24.block-md.order-2-md.col-lg-14-24 > h2').text
        pledged = driver.find_element_by_css_selector(
            '#react-project-header > div > div > div.grid-row.grid-row.mb5-lg.mb0-md.order-0-md.order-2-lg > div.col-full.hide.block-lg.col-md-8-24 > div.flex.flex-column-lg.mb4.mb5-sm > div:nth-child(1) > div.flex.items-center > span > span').text
        backers = driver.find_element_by_css_selector(
            '#react-project-header > div > div > div.grid-row.grid-row.mb5-lg.mb0-md.order-0-md.order-2-lg > div.col-full.hide.block-lg.col-md-8-24 > div.flex.flex-column-lg.mb4.mb5-sm > div.ml5.ml0-lg.mb2-lg > div > span').text

        pledged = int(re.sub("[^0-9]", "", pledged))
        backers = int(backers.replace(',', ''))
        driver.execute_script("window.history.go(-1)")

        campaigns.append(
            PopularCampaign(name=name, thumbnail=thumbnail, backers=backers, pledged=pledged))

    PopularCampaign.objects.bulk_create(campaigns)


def get_campaigns(hour=0):
    if (hour > 24):
        return {'err': 'Max hours ago is 24'}

    now = timezone.localtime(timezone.now())
    min_datetime = now - timedelta(hours=hour+1)
    max_datetime = now - timedelta(hours=hour)
    results = PopularCampaign.objects.filter(
        created_at__range=(min_datetime, max_datetime))

    campaigns = []
    for campaign in results:
        campaigns.append({
            'name': campaign.name,
            'pledged': campaign.pledged,
            'backers': campaign.backers
        })
    return {'campaigns': campaigns}
