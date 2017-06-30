import time,sys,os
import json
from collections import defaultdict
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from eComCrawl.celery_settings import app
from crawlers.crawl import selenium_getdata
from crawlers.db import DB
import logging
data_fields = json.load(open(BASE_DIR+"/crawlers/data_template.json","r+"))
urls_cat = data_fields['urls']

def get_category_urls(website_name,urls_cat):
    category_urls = {}
    sg = selenium_getdata()
    urls_cat = [[url,url_settings] for url,url_settings in urls_cat.items()]
    url,url_settings = urls_cat[0]
    try:    
        sg(url)
    except Exception as e:
        print("Error in opening URL",e)
    time.sleep(2)
    print (url)
    category_urls[website_name] = defaultdict(list)
    if url_settings['type'] == 'category':
        categories_list = url_settings['categories']
        # testing only one category for now
        for category in categories_list:    
            category_urls[website_name][category] += sg.get_categories(url,category,url_settings['hover'])
    sg.close_sel()
    # category_urls = dict(category_urls)
    return [url,category_urls]

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
    sg.close_sel()
    return data

@app.task
def crawl_link(website,category,category_url):
	# category_urls = json.load(open(BASE_DIR+"/crawlers/cat.json",'r'))
	get_items_data(category_url,category,website)
	# get_items_data(category_urls['http://www.jabong.com']['MEN'][2],urls_cat['http://www.jabong.com'],'http://www.jabong.com')
	return
@app.task
def crawl_category(website_name,data_template):
    db = DB()
    data = get_category_urls(website_name,data_template)
    db_handle =db.get_cursor(website_name+"_categories")
    logging.info("Categorical URLs Gathered for "+data[0])
    db.replace_cateogrical_data(db_handle,website_name,data[-1])
    logging.info("Categorical URLs Updated for "+data[0])
    return

