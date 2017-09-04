from django.test import TestCase
import time
# Create your tests here.
from crawl import selenium_getdata
import json,re
from collections import defaultdict
from db import DB
data_fields = json.load(open("data_template.json","r+"))
urls_cat = data_fields['urls']

def get_category_name(category_dict):
  category_urls = {}
  sg = selenium_getdata()
  url = category_dict.get("url","")
  # urls_cat = [[url,url_settings] for url,url_settings in urls_cat.items()]
  # url,url_settings = urls_cat[0]
  try:  
    sg(url)
  except Exception as e:
    print("Error in opening URL",e)
  time.sleep(2)
  category_dict = sg.get_category_names(category_dict)
  # print (url)
  # category_urls[website_name] = defaultdict(list)
  # if url_settings['type'] == 'category':
  #   categories_list = url_settings['categories']
  #   # testing only one category for now
  #   for category in categories_list:  
  #     category_urls[website_name][category] += sg.get_categories(url,category,url_settings)
  sg.close_sel()
  # category_urls = dict(category_urls)
  return category_dict
def get_category_urls(website_name,catgry_name_xpath_dict,urls_cat):
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
        category_urls = sg.get_categories(url_settings,catgry_name_xpath_dict)
        # categories_list = url_settings['categories']
        # # testing only one category for now
        # for category in categories_list:    
        #     category_urls[website_name][category] += sg.get_categories(url,category,url_settings)
    sg.close_sel()
    # category_urls = dict(category_urls)
    return [url,category_urls]

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
def get_possible_xpaths(category_xpath):
  possible_xpaths = []
  if category_xpath:
    categories_xpath_list = category_xpath.split("/")
    for tag in categories_xpath_list[::-1]:
      tag_real_index = categories_xpath_list.index(tag)
      index_present = re.findall(r"\[\d+\]",tag)
      if index_present:
        new_tag = tag[:tag.index("[")]
        print (tag,new_tag)
        categories_xpath_list.pop(tag_real_index)
        categories_xpath_list.insert(tag_real_index,new_tag)
        print (categories_xpath_list)
        possible_xpaths.append("/".join(categories_xpath_list))
  return possible_xpaths
category_data_dict = get_category_name({"category_xpath":'//*[@id="menucontents"]/ul/li[6]/div/span','url':"https://www.infibeam.com/",
          "urlname":"infibeam","categoryType":"clickhover","type":"category","category_count":"8","cat":[],"xpath":'//*[@id="infibeam-navigation"]/div[1]/a'})
# get_category_name({"category_xpath":'//*[@id="nav-fl2yout-shopAll"]/div[2]/span[5]'})


# from docprocessing import json_formatting
# category_urls = get_category_urls()
# cat_data = json.dump(category_urls,open("cat.json",'w'),indent=4)
# category_urls = json.load(open('cat.json','r'))
# data_inlist = get_items_data(category_urls['https://www.myntra.com/']['Men'][1],urls_cat['https://www.myntra.com/'],'https://www.myntra.com/')
# print (data_inlist)
# print (json_formatting(data_inlist,"https://www.myntra.com/"))
# for website,category_data in category_urls.items():
#   for category,category_urls in category_data.items():
#     for category_url in category_urls[:2]:
#       data_inlist = get_items_data(category_url,urls_cat[website],website)
#       if data_inlist:
#        print (json_formatting(data_inlist,website))
# data_inlist = get_items_data(category_urls['http://www.shopclues.com']['Men'][2],urls_cat['http://www.shopclues.com'],'http://www.shopclues.com')
# data_inlist = get_items_data(category_urls['http://www.jabong.com']['MEN'][2],urls_cat['http://www.jabong.com'],'http://www.jabong.com')
# import json
# from pymongo import MongoClient
# client = MongoClient('localhost',27017)
# db =client['ecom_db']
# for index,each in enumerate(db['shopclues_categories'].find()):
  # print (each)
