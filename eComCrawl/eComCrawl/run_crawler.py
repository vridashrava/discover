# -*- coding: utf-8 -*-
import argparse
import json,os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from eComCrawl.tasks import crawl_link,crawl_category
from crawlers.db import DB
category_urls = {}
data_fields = json.load(open(BASE_DIR+"/crawlers/data_template.json","r+"))
urls_cat = data_fields['urls']
db = DB()
parser = argparse.ArgumentParser(description="Ecommerce Crawler")
parser.add_argument("-w",required=True,help="Website name")
parser.add_argument("lc",nargs='?',help="List Website Categories")
# parser.add_argument("-cc",nargs='?',help="Crawl Website Categories")
parser.add_argument("-c", help="Select Categores to Crawl from")
parser.add_argument("li",nargs='?',help="List Category URLs with index number")
parser.add_argument("-i",help="Start Crawling Category URL with given index number")

args = parser.parse_args()

website = ""
category = ""
index = 0
website_hash = {'shopclues':"http://www.shopclues.com/","jabong":"http://www.jabong.com/","myntra":"https://www.myntra.com/"}
if args.w:
	website = website_hash[args.w]
# category_urls
data_fields = json.load(open(BASE_DIR+"/eComCrawl/jsons/"+args.w+".json","r+"))
urls_cat = data_fields
try:
	db_handle = db.get_cursor(args.w+"_categories")
	# print (db.db_handle.collection_names())
	category_urls = db.read_data(db_handle,{args.w:{'$exists':True}})[0]
except:
	crawl_category.delay(args.w,data_fields)
	db_handle = db.get_cursor(args.w+"_categories")
	category_urls = db.read_data(db_handle,{args.w:{'$exists':True}})[0]
if args.c:
	if args.i:
		index = int(args.i)
		category_url = category_urls[args.w][args.c][index]
		print (category_url)
		print (urls_cat)
		crawl_link.delay(website,urls_cat[website],category_url)
	elif args.li:
		for index,url in enumerate(category_urls[args.w][args.c]):
			print (index,url)
else:
	if args.lc:
		print (list(category_urls[args.w].keys()))
