from django.test import TestCase
import time
# Create your tests here.
from crawl import selenium_getdata
import json
from collections import defaultdict
from db import DB
data_fields = json.load(open("data_template.json","r+"))
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
            for category in categories_list:    
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

# from docprocessing import json_formatting
category_urls = get_category_urls()
cat_data = json.dump(category_urls,open("cat.json",'w'),indent=4)
# category_urls = json.load(open('cat.json','r'))
# data_inlist = get_items_data(category_urls['https://www.myntra.com/']['Men'][1],urls_cat['https://www.myntra.com/'],'https://www.myntra.com/')
# print (data_inlist)
# print (json_formatting(data_inlist,"https://www.myntra.com/"))
# for website,category_data in category_urls.items():
#     for category,category_urls in category_data.items():
#         for category_url in category_urls[:2]:
#             data_inlist = get_items_data(category_url,urls_cat[website],website)
#             if data_inlist:
#                print (json_formatting(data_inlist,website))
# data_inlist = get_items_data(category_urls['http://www.shopclues.com']['Men'][2],urls_cat['http://www.shopclues.com'],'http://www.shopclues.com')
# data_inlist = get_items_data(category_urls['http://www.jabong.com']['MEN'][2],urls_cat['http://www.jabong.com'],'http://www.jabong.com')
# import json
# from pymongo import MongoClient
# client = MongoClient('localhost',27017)
# db =client['ecom_db']
# for index,each in enumerate(db['jabong'].find()):
#     print (each,index)