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
            category_urls[website_name][category] += sg.get_categories(url,category,url_settings)
    sg.close_sel()
    # category_urls = dict(category_urls)
    return [url,category_urls]

# print (json.dumps(get_category_urls(),indent=4))

def get_items_data(category_url,category_dict,homepage,test):
    # gets all the items in category page
    # this will be run as celery task
    running_list = []
    sg = selenium_getdata()
    try:    
        sg(category_url)
    except Exception as e:
        print ("Error",e)
        sg.close_sel()
        db = DB()
        running_urls = db.get_cursor("running_urls")
        try:
            running_list = db.read_data(running_urls,{})[0]['urls']
        except:
            running_list = []
            if running_list:
                running_list.remove(category_url)
                db.replace_cateogrical_data(running_urls,"urls",{"urls":running_list})
        return []
    data =sg.get_items(category_dict,homepage,test)
    # except Exception as e:
    # print("Error in opening URL",e)
    # wait for the elements to be visible
    sg.close_sel()
    db = DB()
    running_urls = db.get_cursor("running_urls")
    try:
        running_list = db.read_data(running_urls,{})[0]['urls']
    except:
        running_list = []
        if running_list:
            running_list.remove(category_url)
            db.replace_cateogrical_data(running_urls,"urls",{"urls":running_list})
    return data

@app.task
def crawl_link(category_url,category,homepage,test=False):
    # category_urls = json.load(open(BASE_DIR+"/crawlers/cat.json",'r'))
    data_file = []
    try:
        data_file = get_items_data(category_url,category,homepage,test)
    except:
        db = DB()
        running_list = []
        running_urls = db.get_cursor("running_urls")
        try:
            running_list = db.read_data(running_urls,{})[0]['urls']
        except:
            running_list = []
        if running_list:
            running_list.remove(category_url)
            db.replace_cateogrical_data(running_urls,"urls",{"urls":running_list})
    # get_items_data(category_urls['http://www.jabong.com']['MEN'][2],urls_cat['http://www.jabong.com'],'http://www.jabong.com')
    return data_file
@app.task
def crawl_category(website_name,data_template):
    data = get_category_urls(website_name,data_template)
    return data[1]

