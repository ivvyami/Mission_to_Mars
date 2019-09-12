from splinter import Browser
from bs4 import Beautiful Soup
import os

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
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitter_url)

    soup = BeautifulSoup(response.content, "html.parser")



    
    

