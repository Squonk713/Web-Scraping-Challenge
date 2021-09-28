from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests

#define function to intiate "light" browser for nav
def init_browser():
    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path, headless=False)

    return browser


#define the scrape function
def scrape():

  #### Get news title and body ####

    # Get page HTML into a Soup
    browser = init_browser()
    url_to_scrape = "https://redplanetscience.com/"
    browser.visit(url_to_scrape)
    html = browser.html
    soup = bs(html,'html.parser')

    # Get all news items
    news_items = soup.find_all('div', class_='list_text')

    news_title = news_items[0].find('div', class_='content_title').text
    news_p = news_items[0].find('div', class_='article_teaser_body').text

  #### Get Featured Image ####

    # Get page HTML into a Soup
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')
    #assing source url to variable
    featured_image_url = soup.find_all('img', class_='headerimage fade-in')[0]["src"]

  #### Get Table ####

    # Get page HTML into a Soup
    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)
    #scrape to pd.dataframe
    df2 = tables[1]
    #assign column headers
    df2.columns = ["Mars", "Value"]
    #convert to html
    mars_html_table = df2.to_html()

  #### Get Hemispheres ####

    # Get page HTML into a Soup
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Get all news items
    hemispheres = soup.find_all('div', class_='item')
    #create empty list to append dictionaries
    hemisphere_image_urls = []
    #loop through each iteration of hemispheres
    for hemisphere in hemispheres:

        hemisphere = hemisphere.find('div', class_="description")
        #Get title
        title = hemisphere.h3.text
        #Assign sub-url for page nav
        link = hemisphere.a["href"]
        #navigate
        browser.visit(url + link)
        # Get page HTML into a Soup
        html = browser.html
        soup = bs(html, 'html.parser')
        #Get image url
        image_link = soup.find('div', class_='downloads')
        image_url = image_link.find('li').a["href"]
        #create dictionary to hold values
        image_dict = {}
        #add values
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        #append to list
        hemisphere_image_urls.append(image_dict)
        #trim variable
        hemisphere_images = hemisphere_image_urls

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
