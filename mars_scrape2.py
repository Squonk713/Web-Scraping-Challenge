from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests

def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path, headless=False)

def scrape():
    # Get page HTML into a Soup
    browser = init_browser()
    mars_dict ={}

    # Get news title and body

    url_to_scrape = "https://redplanetscience.com/"
    response = browser.visit(url_to_scrape)
    html = browser.html
    soup = bs(html,'html.parser')
    news_items = soup.find_all('div', class_='list_text')

    title = []
    paragraph = []

    for news in news_items:
        
        news_title = news.find('div', class_='content_title').text
        news_p = news.find('div', class_='article_teaser_body').text

    #print(news_title)
    #print(news_p)

    # Get featured image

    url = "https://spaceimages-mars.com/"
    response = browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    featured_image_url = soup.find_all('img', class_='headerimage fade-in')[0]["src"]

    #print(featured_image_url)

    # Get table

    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)
    #tables
    df2 = tables[1]
    df2.columns = ["Mars", "Value"]
    mars_html_table = df2.to_html()
    clean_table = mars_html_table.replace('\n', '')
    #print(mars_html_table)

    # Get hemispheres

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    hemispheres = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for hemisphere in hemispheres:

        hemisphere = hemisphere.find('div', class_="description")
        title = hemisphere.h3.text
        #print(title)
        link = hemisphere.a["href"]    
        browser.visit(url + link)
        html = browser.html
        soup = bs(html, 'html.parser')
        image_link = soup.find('div', class_='downloads')
        image_url = image_link.find('li').a["href"]
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        hemisphere_image_urls.append(image_dict)
        #print(hemisphere_image_urls)

        hemisphere_images = hemisphere_image_urls[0:4]

        #print(hemisphere_images)

        # Store data in dictionary
        mars_dict = {
                "news_title": news_title,
                "news_p": news_p,
                "featured_image_url": featured_image_url,
                "table": str(mars_html_table),
                "hemisphere_images": hemisphere_images
            }

        # Return results
        return mars_dict