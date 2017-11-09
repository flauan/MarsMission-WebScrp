#-----------------------------------------------
#  Web Scraping and web rendering  with MongoDB   
#  Main Web Scraper
#  Initial Version:                         2017               
#  by Fervis lauan                                
#-----------------------------------------------

# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pymongo



def scrape():
    #-----------------#
    # NASA Mars News  #
    #-----------------#
    from bs4 import BeautifulSoup
    import requests
    from splinter import Browser
    from bs4 import BeautifulSoup
    import pymongo

    url = 'https://mars.nasa.gov/news/'

    response = requests.get(url)

    soup = BeautifulSoup(response.text,'html')
    print(soup)

    results = soup.find_all('div', class_='content_title')
    i=1
    for result in results:
        if i==1:
            news_title=result.a.text        
        i=i+1

    results = soup.find_all('div', class_='rollover_description_inner')
    i=1
    for result in results:
        if i==1:
            news_par=result.text        
        i=i+1
    print("Completed: NASA Mars News")
    #-----------------------------------------#
    # JPL Mars Space Images - Featured Image  #
    #-----------------------------------------#

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    jpls_elem=soup.find_all('footer')
    next_link='https://www.jpl.nasa.gov'+jpls_elem[0].a['data-link']
    print(next_link)
    fullsz_pg = requests.get(next_link)
    soup = BeautifulSoup(fullsz_pg.text, 'lxml')
    fullsz_elem=soup.find_all('figure',class_='lede')
    featured_image_url='https://www.jpl.nasa.gov'+fullsz_elem[0].a['href']

    print("Completed: Featured Image")

    #---------------#
    # Mars Weather  #
    #---------------#
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    results = soup.find_all('div', class_='js-tweet-text-container')
    mars_weather=results[0].p.text

    print("Completed: Mars Weather")


    #--------------#
    # Mars Facts   #
    #--------------#
    import pandas as pd
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Description', 'Values']
    # mars_facts_df.to_html('mars_facts.html',index=False)
    # mars_facts_df
    mars_facts_str=mars_facts_df.to_html(index=False)

    print("completed: Mars Facts")


    #------------------#
    # Mars Hemispheres #
    #------------------#
    from splinter import Browser
    from bs4 import BeautifulSoup

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    i=1
    hem_img_urls=[]
    while i<=4:
        if i==1:
            browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
        elif i==2:
            browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
        elif i==3:
            browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
        else:
            browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')     
            
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        title=soup.title.text.replace("| USGS Astrogeology Science Center","")    
        img_results = soup.find_all('div', class_='downloads')
        img_url=img_results[0].a['href']
        hem_img_urls.append({"title":title,"img_url":img_url})
        browser.click_link_by_partial_text('Back')    
        i=i+1
    print("Completed: Hemispheres")


    #------------------------#
    # Create listing         #
    #------------------------#  
    post = {'new_title': news_title.replace('\n',''),
            'news_par': news_par.replace('\n',''),
            'featrd_img_url': featured_image_url,
            'mars_weather': mars_weather.replace('\n',''),
            'mars_facts': mars_facts_str.replace('\n',''),
            'hem_img_urls':hem_img_urls        
        }
    print("Completed: Final dictionary")
       
    return post
    
