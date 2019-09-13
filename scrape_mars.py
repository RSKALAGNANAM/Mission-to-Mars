from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import time
import pymongo

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

# define the function that will return all scraped information
def scrape():
    browser = init_browser()

    # Visit 'https://mars.nasa.gov/news/'
    url_mars_news = "https://mars.nasa.gov/news/"
    browser.visit(url_mars_news)

    # define the functionality that will capture the links for latest news title and blurb

    time.sleep(1)

    #Create BeautifulSoup object; parse with 'html.parser' 
    
    soup = BeautifulSoup(browser.html, 'lxml')

    # results are returned as an iterable list 
    
    result = soup.find('div', class_="list_text")

    # get the title of the latest news

    news_title = result.find('div', class_="content_title").text

    # get the paragraph text of the latest news

    news_p = result.find('div', class_="article_teaser_body").text

    #store the results in a dictionary

    mars_news_items = {
        "news_title":news_title,
        "news_desc":news_p
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    #return mars-news

    # define the functionality that will return the link for the JPL Featured Space Image

    # Reinitialize the browser

    browser = init_browser()

    # Visit 'https://www.jpl.nasa.gov/spaceimages/?search=&Category=Mars'
    url_mars_jpl_image = "https://www.jpl.nasa.gov/spaceimages/?search=&Category=Mars"
    browser.visit(url_mars_jpl_image)

    time.sleep(1)

    #Create BeautifulSoup object; parse with 'html.parser' 
    
    soup = BeautifulSoup(browser.html, 'lxml')

    # results are returned as an iterable list 
    
    result = soup.find('div', class_="carousel_items")

    #Extract the url for the JPL image

    featured_image_url = result.find('a', class_="button fancybox")['data-fancybox-href']

    #Concatenate "https://www.jpl.nasa.gov" to get the complete url

    complete_jpl_image_url = "https://www.jpl.nasa.gov"+featured_image_url

    # Close the browser after scraping
    browser.quit()

    # define the functionality that will return the link for latest weather on Mars

    # Reinitialize the browser

    browser = init_browser()

    # Visit 'https://twitter.com/marswxreport?lang=en'
    url_mars_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_mars_weather)

    time.sleep(1)

    #Create BeautifulSoup object; parse with 'html.parser' 
    
    soup = BeautifulSoup(browser.html, 'lxml')

    # results are returned as an iterable list 
    
    result = soup.find('div', class_="js-tweet-text-container")

    #Extract the weather information
    mars_weather = result.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # Close the browser after scraping
    browser.quit()

    #define the functionality that will return the Mars facts
    #Reinitialize the browser

    browser = init_browser()

    # Visit 'https://space-facts.com/mars/'
    url_mars_facts = "https://space-facts.com/mars/"
    browser.visit(url_mars_facts)

    #Pass the url to the pd.read_html() method and retrieve all tables in the url_mars_facts
    
    tables = pd.read_html(url_mars_facts)

    #as confirmed from Jupyter notebook,tables is a List; tables[0] is the one that contains 
    #Mars-Earth comparison
    #tables[1] is the table that we want because this has Mars facts

    #define a dataframe mars_facts_df to store the tables[1]

    mars_facts_df = tables[1]
    mars_facts_df.columns = ['Entity', 'Value']

    #Reset the index to "Entity"

    mars_facts_df.set_index('Entity', inplace=True)

    # delete the index name because of the inconsistency of display

    del mars_facts_df.index.name

    #convert dataframe to a dictionary

    mars_facts_table = mars_facts_df.to_html()
    
    #mars_facts_dict = mars_facts_dict['Value']


    # Close the browser after scraping
    browser.quit()

    # define the functionality that will return the links for hemispheres

    #Reinitialize the browser

    browser = init_browser()

    #There are four separate urls and each one needs to be visited separately to scrape information

    # Get Cerberus Hemisphere link
    # Visit 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    url_cerberus = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    browser.visit(url_cerberus)

    time.sleep(1)

    #Create BeautifulSoup object; parse with 'html.parser' 
    
    soup = BeautifulSoup(browser.html, 'lxml')

    # results are returned as an iterable list

    results_cerberus = soup.find_all('a')

    #When we inspect the site, we see that the <a> tag which has the title "Sample" is the one we want
    #The enhanced version is a very large file (21 MB)
    #Therefore parse based on the text of the <a> tag being the word "Sample" and extract the href for that <a> tag

    for a in results_cerberus:
        if a.text == "Sample":
            image_cerberus_url = a['href']

    # Close the browser after scraping
    browser.quit()
    
    # Get Schiaparelli Hemisphere link
    # Visit 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    # Reinitialize the browser
    browser = init_browser()
    url_schiaparelli = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    browser.visit(url_schiaparelli)

    time.sleep(1)

    #Create BeautifulSoup object; parse with 'html.parser' 
    
    soup = BeautifulSoup(browser.html, 'lxml')

    # results are returned as an iterable list

    results_schiaparelli = soup.find_all('a')

    #Iterate using a for loop similar to what was done for Cerberus

    for a in results_schiaparelli:
        if a.text == "Sample":
            image_schiaparelli_url = a['href']

    # Close the browser after scraping
    browser.quit()

    # Get Syrtis Major Hemisphere link
    # Visit 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    #Reinitialize the browser
    browser = init_browser()
    url_syrtis_major = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    browser.visit(url_syrtis_major)

    time.sleep(1)

    #Create BeautifulSoup object; parse with 'html.parser' 
    
    soup = BeautifulSoup(browser.html, 'lxml')

    # results are returned as an iterable list

    results_syrtis_major = soup.find_all('a')

    #Iterate using a for loop similar to what was done for Cerberus

    for a in results_syrtis_major:
        if a.text == "Sample":
            image_syrtis_major_url = a['href']

    # Close the browser after scraping
    browser.quit()

    # Get Valles Marineris Hemisphere link
    # Visit 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    #Reinitialize the browser
    browser = init_browser()
    url_valles_marineris = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    browser.visit(url_valles_marineris)

    time.sleep(1)

    #Create BeautifulSoup object; parse with 'html.parser' 
    
    soup = BeautifulSoup(browser.html, 'lxml')

    # results are returned as an iterable list

    results_valles_marineris = soup.find_all('a')

    #Iterate using a for loop similar to what was done for Cerberus

    for a in results_valles_marineris:
        if a.text == "Sample":
            image_valles_marineris_url = a['href']

    # Close the browser after scraping
    browser.quit()

    # Store data in a list of dictionaries
    mars_hemispheres = [
        {"title": "Cerberus Hemisphere","img_url": image_cerberus_url},
        {"title": "Schiaparelli Hemisphere","img_url": image_schiaparelli_url},
        {"title": "Syrtis Major Hemisphere","img_url": image_syrtis_major_url},
        {"title": "Valles Marineris Hemisphere","img_url": image_valles_marineris_url}
    ]

    # Define the dictionary that contains all scraped information

    mars_data_result = {"mars_news":mars_news_items,"featured_image_url":complete_jpl_image_url,\
        "mars_weather":mars_weather,"mars_facts":mars_facts_table,"mars_hemispheres":mars_hemispheres}

    #db.collection.insert_one({mars_data_result})

    return mars_data_result