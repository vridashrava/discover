import time,sys,os
import json
from collections import defaultdict
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from eComCrawl.celery_settings import app
from crawlers.crawl import selenium_getdata
from crawlers.db import DB

data_fields = json.load(open(BASE_DIR+"/crawlers/data_template.json","r+"))
urls_cat = data_fields['urls']

def get_category_urls():
    category_urls = defaultdict(list)
    sg = selenium_getdata()
    for url,url_settings in urls_cat.items():
        try:    
            sg(url)
        except Exception as e:
            print("Error in opening URL",e)
            continue
        time.sleep(2)
        print (url)
        category_urls[url] = defaultdict(list)
        if url_settings['type'] == 'category':
            categories_list = url_settings['categories']
            # testing only one category for now
            for category in categories_list[:1]:    
                category_urls[url][category] += sg.get_categories(url,category,url_settings['hover'])
    sg.close_sel()
    return category_urls

# print (json.dumps(get_category_urls(),indent=4))

def get_items_data(category_url,category_dict,homepage):
    # gets all the items in category page
    # this will be run as celery task
    sg = selenium_getdata()
    try:    
        sg(category_url)
    except Exception as e:
        print ("Error",e)
        sg.close_sel()
        return []
    data =sg.get_items(category_dict,homepage)
    # except Exception as e:
    # print("Error in opening URL",e)
    # wait for the elements to be visible
    return data

@app.task
def crawl_link(website,category,category_url):
	category_urls = json.load(open(BASE_DIR+"/crawlers/cat.json",'r'))
	get_items_data(category_url,category,website)
	# get_items_data(category_urls['http://www.jabong.com']['MEN'][2],urls_cat['http://www.jabong.com'],'http://www.jabong.com')
	return