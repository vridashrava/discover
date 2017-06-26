# -*- coding: utf-8 -*-
import argparse
import json,os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from eComCrawl.tasks import crawl_link

category_urls = json.load(open(BASE_DIR+"/crawlers/cat.json",'r'))
data_fields = json.load(open(BASE_DIR+"/crawlers/data_template.json","r+"))
urls_cat = data_fields['urls']

parser = argparse.ArgumentParser(description="Ecommerce Crawler")
parser.add_argument("-w",required=True,help="Website name")
parser.add_argument("lc",nargs='?')
parser.add_argument("-c", help="List Categories")
parser.add_argument("li",nargs='?')
parser.add_argument("-i")

args = parser.parse_args()

website = ""
category = ""
index = 0

if args.w == "shopclues":
	website = "http://www.shopclues.com"
elif args.w == "jabong":
	website = "http://www.jabong.com"
elif args.w == "myntra":
	website = "https://www.myntra.com/"

if args.lc and args.li == "":
	print (list(category_urls[website].keys()))
if args.c:
	if args.i:
		index = int(args.i)
		category_url = category_urls[website][args.c][index]
		print (category_url)
		crawl_link.delay(website,urls_cat[website],category_url)
	elif args.li:
		for index,url in enumerate(category_urls[website][args.c]):
			print (index,url)
