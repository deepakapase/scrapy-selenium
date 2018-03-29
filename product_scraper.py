  
# The requests library
import requests
import json
from os.path import isfile
import os

class ProductScraper:
    scraped_items = []
    URL = "https://redsky.target.com/v1/plp/search/?channel=web&visitorId=01602E03E8670201824D2E9549AE113C"
    #?category=5xsxv&pageId=%2Fc%2F5xsxv"
    def get_cat_item_count(self, cat_id):
        response = requests.get(self.URL + '&count=10&offset=0&category=' + cat_id)
        jdata = response.json()['search_response']['metaData']
        for entry in jdata:
            if(entry['name'] == 'total_results'): 
                return entry['value']
        return 0;
    def get_stores_info(self, cat_id, page, size):
        # Making the post request
        offset = page * size;
         
        #response = requests.get(self.WINE_URL,  data = {'count':count, 'offset':offset})
        url = self.URL + '&count=' + `size` + '&offset=' + `offset` + '&category=' + cat_id
        response = requests.get(url)
        print page
        return response.json()['search_response']['items']
    
    def parse_json_field(self, item, field):
        try:
            return item[field]
        except (ValueError, KeyError, TypeError):
            return ''
    
        
    def parse_items(self, data, cat):
        # Creating an lxml Element instance
        for item in data['Item']:
            # The lxml etree css selector always returns a list, so we get
            # just the first item
            title = self.parse_json_field(item, "title")
            url = self.parse_json_field(item, "url")
            description = self.parse_json_field(item, "description")
            brand = self.parse_json_field(item, "brand")
            tcin = self.parse_json_field(item, "tcin")
            dpci = self.parse_json_field(item, "dpci")
            upc = self.parse_json_field(item, "upc")
            bullet_description = self.parse_json_field(item, "bullet_description")
            if bullet_description == '':
                bullet_description = []
            soft_bullets = self.parse_json_field(item, "soft_bullets")
            if soft_bullets == '':
                soft_bullets = {}
            available_to_purchase_date_time = self.parse_json_field(item, "available_to_purchase_date_time")
            temp = self.parse_json_field(item, "child_items")
            package_dimensions = self.parse_json_field(temp, "package_dimensions")
            release_date = self.parse_json_field(temp, "release_date")
            images = self.parse_json_field(item, "images")
            categories = cat
            # now we add all the info to a dict
            item_info = {
                        'title': title,
                        'url': url,
                        'brand': brand,
                        'upc': upc,
                        'tcin': tcin,
                        'dpci': dpci,
                        'release_date': release_date,
                        'bullet_description': bullet_description,
                        'soft_bullets': soft_bullets,
                        'description': description,
                        'available_to_purchase_date_time': available_to_purchase_date_time,
                        'package_dimensions': package_dimensions,
                        'images': images,
                        'categories': categories
                        }
            
            self.scraped_items.append(item_info)
    
    
    def merge_all_same_category_files(self, catName):
        arr = os.listdir(".");
        items = []
        for a in arr:
            if(a.startswith( catName )):
                print "processing file " + a
                items_in_file = self.readfile(a);
                items.extend(items_in_file)
        
        print "writting in combined file"
        with open(catName + ".json", 'w') as json_file:
            json.dump(items, json_file, indent=4)
            
    def readfile(self, fname):
        with open(fname) as json_data:
            d = json.load(json_data)
            json_data.close()
            return d
    
    def scrape(self, url, cat):
        # check if this category is already crawled
        if(isfile('_'.join(cat).replace(" ", "-") + ".json")):
            return
        self.scraped_items = []
        size = 90
        cat_id = None
        try:
            cat_id = self.get_cat_id_from_url(url)
            total = int(self.get_cat_item_count(cat_id))
            if(total == 0):
                return
        except (RuntimeError): 
            return
        
        pages = int(total / size) + (total % size > 0)
        try:
            for page in range(pages):
                # Retrieving the data
                data = self.get_stores_info(cat_id, page, size)
                # Parsing it
                self.parse_items(data, cat)
                #print('scraped the page' + data)
            
                self.save_data(cat)
        except(RuntimeError, KeyError):
            print "FAILED**********"
            print "failed to scrape url: " + url
            self.save_data(cat) 

    def get_cat_id_from_url(self, url):
        tokens = url.split("?")[0].split("/")
        return tokens[len(tokens) - 1].split("-")[1]
    
    def save_data(self, cat):
        with open('_'.join(cat).replace(" ", "-").replace("/", "-") + ".json", 'w') as json_file:
            json.dump(self.scraped_items, json_file, indent=4)

if __name__ == '__main__':
    scraper = ProductScraper()
    scraper.merge_all_same_category_files("personal-care")
    #scraper = ProductScraper()
    #url = "https://www.target.com/c/air-fresheners-household-essentials/-/N-5xsz0?lnk=Airfresheners"
    #cat = ["household essentials", "air fresheners"]
    #scraper.scrape(url, cat)
