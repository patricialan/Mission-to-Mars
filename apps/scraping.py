# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome', executable_path ='chromedriver', headless=True)

    ### Summary of Latest News Article

    def mars_news(browser):
        # Visit mars nasa news site
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

        # Convert browser html to soup object and then quit the browser
        html = browser.html
        news_soup = BeautifulSoup(html, 'html.parser')

        # Try/except for error handling
        try:
            slide_elem = news_soup.select_one('ul.item_list li.slide')
            
            # Assign title and summary text to variables
            slide_elem.find('div', class_='content_title')

            # Use the parent element to find the first <a> tag and save it as `news_title`
            news_title = slide_elem.find("div", class_='content_title').get_text()

            # Use the parent element to find the paragraph text
            news_paragraph = slide_elem.find('div', class_="article_teaser_body").get_text()
        
        except AttributeError:
                return None, None

        return news_title, news_paragraph

    ### Featured Images

    def featured_image(browser):
        
        # Visit nasa images URL
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        # Find and click the full image button
        full_image_elem = browser.find_by_id('full_image')
        full_image_elem.click()

        # Find the more info button and click that
        browser.is_element_present_by_text('more info', wait_time=1)
        more_info_elem = browser.links.find_by_partial_text('more info')
        more_info_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        try: 
            # Find the relative image url
            img_url_rel = img_soup.select_one('figure.lede a img').get("src")

        except AttributeError:
            return None

        # Use the base URL to create an absolute URL
        img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

        return img_url

    ### Mars Facts Table

    def mars_facts():

        try:
            # use 'read_html' to scrape facts table into dataframe
            df = pd.read_html('http://space-facts.com/mars/')[0]

        except BaseException:
            return None

        # Assign columns and set index of dataframe
        df.columns=['description', 'value']
        df.set_index('description', inplace=True)

        # Convert dataframe to html format, add bootstrap
        return df.to_html()
    
    # Create variable for data dictionary (for mongo)
    news_title, news_paragraph = mars_news(browser)

    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now()
    }

    # Quit automated browser
    browser.quit()

    # return data dictionary
    return data

### Hemispheres Titles & Images

def hemis_data():
    # Initiate headless driver for deployment
    browser = Browser('chrome', executable_path ='chromedriver', headless=True)

    def hemis_dict(hemisphere):
        hemis_dict = {}
    
        # Visit hemisphere images url
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        # Click hemisphere link
        browser.is_element_present_by_text(f'{hemisphere} Hemisphere Enhanced', wait_time=1)
        hemis_elem = browser.links.find_by_partial_text(f'{hemisphere} Hemisphere Enhanced')
        hemis_elem.click()

        # Parse html with soup
        html = browser.html
        hemis_titleImg_soup = BeautifulSoup(html, 'html.parser')

        # Get hemisphere title
        hemis_title = hemis_titleImg_soup.find("h2", class_="title").get_text()
        hemis_dict['title'] = hemis_title
                
        # Get hemisphere image url
        hemis_imgUrl = hemis_titleImg_soup.select_one('div.content dl dd a').get("href")
        hemis_dict['img_url'] = hemis_imgUrl

        return hemis_dict
        
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']

    hemis_data = [hemis_dict(hemisphere) for hemisphere in hemispheres]

    # Quit automated browser
    browser.quit()

    # Return hemis_data list of dictionaries
    return hemis_data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all(), hemis_data())