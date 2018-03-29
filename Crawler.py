'''
Created on Mar 21, 2018

@author: skawale
'''
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import Queue
from types import NoneType
from product_scraper import ProductScraper

class ScapeUrls:

    scrapped = []
    SITE_URL= "https://www.target.com"
    START_URL = "/c/school-office-supplies/-/N-5xsxr"
    START_CAT = ["school & office supplies "]
    url_map = {}
    q = Queue.Queue()
    driver = webdriver.Firefox()    
    def open_page_return_source(self, url):
        driver = self.driver
        driver.get(url)
        #tree = html.fromstring(driver.page_source)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        return soup
    
    def get_categories_on_page(self, soup):
        ulTag = soup.find("ul", attrs={ "data-test" : "pictureNavigationFeatured"})
        return ulTag
    
    def extract_categories_from_ul(self, ulTag, parent_url):
        if (ulTag is None and ulTag is NoneType):
            return
            #alist.append(jdata)
        category = None
        try:
            aTags = ulTag.find_all("a");            
            for aTag in aTags:
                divTag = aTag.select_one("div:nth-of-type(4)")
                #jdata = {}
                if divTag is not None:
                    #jdata['category'] = divTag.text
                    category = divTag.text
                #jdata['url'] = aTag["href"]
                url = self.SITE_URL + aTag["href"]
                self.q.put(url);
                self.add_in_url_map(url, category, parent_url)
        except (AttributeError):
            return category
        return category

    def add_in_url_map(self, url, cat, parent_url):
        parent_cat = self.url_map[parent_url]
        new_list = parent_cat[:]
        new_list.append(cat)
        self.url_map[url] = new_list
    
    def scrape_products_on_url(self, url):
        #no more categories..
        #time to scrape products
        print "*****"
        print "scraping products from category " + url
        print "*****"
        cat = self.url_map.get(url)
        pScraper = ProductScraper()
        pScraper.scrape(url, cat)
    
    def run(self):
        self.q.put(self.SITE_URL + self.START_URL)
        self.url_map[self.SITE_URL + self.START_URL] = self.START_CAT
        visited = set()
        while not self.q.empty():
            # Retrieving the data
            url = self.q.get()
            if url in visited:
                continue
            print "scraping " + url
            try:
                data = self.open_page_return_source(url)
                ulTag = self.get_categories_on_page(data)        
                categories = self.extract_categories_from_ul(ulTag, url)
                if(categories is None):
                    self.scrape_products_on_url(url)
                visited.add(url)
            except(RuntimeError):
                visited.add(url)
            #self.scrapped.append(jdata)
            # Parsing it
            #print('scraped the page' + data)

        self.save_data()
        self.driver.close()

    def save_data(self):
        with open('categories.json', 'w') as json_file:
            json.dump(self.url_map, json_file, indent=4)    
if __name__ == '__main__':
    scraper = ScapeUrls()
    scraper.run()
                    