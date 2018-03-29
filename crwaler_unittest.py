'''
Created on Mar 21, 2018

@author: skawale
'''
import unittest
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("https://www.target.com/c/personal-care/-/N-5xtzq")
        #tree = html.fromstring(driver.page_source)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        ulTag = soup.find("ul", attrs={ "data-test" : "pictureNavigationFeatured"})
        aTags = ulTag.find_all("a");
        for aTag in aTags:
            print aTag["href"]
            #sibling = aTag.next_sibling
            #siblingString = str(sibling).strip()
            #if len(siblingString) > 0:
             #   print siblingString 

    def test_homepage_categories(self):
        driver = self.driver
        driver.get("https://www.target.com")
        #tree = html.fromstring(driver.page_source)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        ulTag = soup.find("ul", attrs={ "data-test" : "pictureNavigationFeatured"})
        aTags = ulTag.find_all("a");
        for aTag in aTags:
            print aTag["href"]
            #sibling = aTag.next_sibling
            #siblingString = str(sibling).strip()
            #if len(siblingString) > 0:
             #   print siblingString 

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()