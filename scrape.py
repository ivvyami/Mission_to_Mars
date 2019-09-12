from splinter import Browser
from bs4 import Beautiful Soup
import os
import requests
import pymongo
import pandas as pd

def init_browser(): 
    #path for chrome driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape(): 
    browser = init_browser()
    mars_online = {}

#NASA MARS NEWS
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #Get into the response that you need   
    response_list = soup.find('li', class_='slide')
    #Collect the latest News Title and Paragraph Text
    div_title = response_list.find('div',class_='content_title')
    mars_online["news_title"] = div_title.find('a').get_text()

    div_par = response_list.find('div', class_='article_teaser_body')
    mars_online["news_p"] = div_par.gt_text()

## JLP Mars Pace Images
    url_1 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url_1)

    soup = BeautifulSoup(response.content, "html.parser")
    #Get to the response with the image
    img_a = soup.find('a', class_='button fancybox')

    #get the link for the image
    img_link = img_a['data-fancybox-href']

    mars_online["featured_image_url"] = print(f"https://www.jpl.nasa.gov{img_link}")

#MARS WEATHER
    # twitter_url = 'https://twitter.com/marswxreport?lang=en'
    # response = requests.get(twitter_url)

    # soup = BeautifulSoup(response.content, "html.parser")

#MARS FACTS
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)

    #Get the table
    mars_facts = tables[0]
    mars_facts.columns = ['Info', 'Mars', 'Earth']
    mars_facts.set_index('Info', inplace=True)
    mars_facts.drop(columns= 'Earth')
    mars_html_table = mars_facts.to_html()

    mars_online["mars_html_table"] = mars_html_table

#MARS HEMISPHERES
    pic_url = 'https://astrology.usgs.gov'

    hemisphere_image_urls = [
    {"title": "Cerberus Hemisphere Enhanced", "img_url": f"{pic_url}/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg"}, 
    {"title": "Schiaparelli Hemisphere Enhanced", "img_url": f"{pic_url}/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere Enhanced", "img_url": f"{pic_url}/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg"},
    {"title": "Valles Marineris Hemisphere Enhanced", "img_url": f"{pic_url}/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg"}
    ]


    mars_online["hemisphere_image_urls"] = hemisphere_image_urls
    
    #quit browser after scraping
    browser.quit()

    #return scraping to dictionary 
    return mars_online