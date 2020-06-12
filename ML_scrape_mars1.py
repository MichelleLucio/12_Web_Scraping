import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
import pymongo
from splinter import Browser
import re
import time


def initiate_browser():
    #for windows users for splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)



#function called scrape that will execute all scraping code & return 1 python dictionary
def scrape_all():
        # Initiate headless driver for deployment
    browser = initiate_browser()

 

    # NASA Mars News 
    #url for mars hemispheres
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_title_results = soup.find_all('div', class_='content_title')[1].text
    news_body_results = soup.find_all('div', class_='article_teaser_body')[0].text
    print(f"Latest news title: {news_title_results}")
    print(f"Latest news text: {news_body_results}")



# # JPL Mars Space Images - Featured Image
    feat_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(feat_img_url)
    time.sleep(5)
    # find url for featured image
    image_url = browser.find_by_css('article')['style'].replace('background-image: url("', '').replace('");', '')
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + image_url
    print(f"Featured image url: {featured_image_url}")



# # Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(10)
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')
 
    mars_weather = weather_soup.find(attrs={"data-testid" : "tweet"})
    weather_text = mars_weather.text
    mars_weather_list = weather_text.split("InSight")
    mars_weather_today = (mars_weather_list[1])

    print(f"Latest Mars Weather Report: {mars_weather_today}") 



# # Mars Facts Table
    facts_table_url = 'https://space-facts.com/mars/'
    browser.visit(facts_table_url)
    time.sleep(10)

    facts_html = browser.html
    facts_soup = bs(facts_html, 'html.parser')

    # read facts table from url
    facts_table = pd.read_html(facts_table_url)
    facts_table

    # convert html table into dataframe
    facts_df = facts_table[0]
    facts_df.columns = ['Description', 'Value']
    facts_df.set_index('Description', inplace=True)
    facts_df.head()

    # convert dataframe into html table
    mars_html_table = facts_df.to_html()
    mars_html_table

    mars_html_table.replace('\n', '')
    facts_df.to_html('./templates/mars_facts_table.html')



#Mars Hemispheres
    #url for mars hemispheres
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)
    time.sleep(5)

    #use beautifulsoup to be able to pull info
    mars_hemisphere_html = browser.html
    hemisphere_soup = bs(mars_hemisphere_html, 'html.parser')
    
    hemispheres = hemisphere_soup.find_all('div', class_='item')
    mars_hemisphere_list = []
    
    #run thru the url for each hemisphere
    for each in hemispheres:
        hemi_name = each.find('h3').text
        split = hemi_name.split('Enhanced')
        hemisphere_name = split[0]
        browser.click_link_by_partial_text(hemi_name)
        hemi_page_html = browser.html
        hemi_soup = bs(hemi_page_html, "html.parser")
        download = hemi_soup.find('div', class_="downloads")
        hemi_url = download.a["href"]
        hemisphere_dict = {"name": hemisphere_name, "image_url": hemi_url}
        mars_hemisphere_list.append(hemisphere_dict)
        browser.back()
        time.sleep(3)

    print(mars_hemisphere_list)



    mars_scrape_data = {
        "news_title": news_title_results,
        "news_body": news_body_results,
        "featured_image": featured_image_url,
        "mars_weather": mars_weather_today,
        "mars_fact_table": mars_html_table,
        "mars_hemispheres": mars_hemisphere_list
    }
    print(mars_scrape_data)
    browser.quit()
    return mars_scrape_data

