from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from eComCrawl.tasks import crawl_link,crawl_category,get_names
from crawlers.db import DB
import logging,json
import requests
import json,re,os,time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def form(request):
    return render(request, 'form.html', {})

def viewform(data_dict):
  data =  data_dict
  sitemap_dict = {}
  if "sitemap_urlname" in data_dict:
    urlname = data_dict.get("sitemap_urlname","")
    sitemap_dict["sitemap_urlname"] = urlname
    sitemap_dict["url"] = data_dict.get("url","")
    sitemap_dict["sitemap_url"] = data_dict.get("sitemap_url","")
    category_count = data_dict.get("category_count",2)
    category_count = int(category_count)
    sitemap_dict["category_count"] = category_count
    sitemap_dict["type"] = data_dict.get("submit","")
    for i in range(1,category_count+1):
      sitemap_dict["sitemap_sub_cat_count_"+str(i)] = data_dict.get("sitemap_sub_cat_count_"+str(i),"")
      sitemap_dict["sitemap_xpath_category_"+str(i)] = data_dict.get("sitemap_xpath_category_"+str(i))
    sitemap_category = crawl_category.delay(urlname,{sitemap_dict["sitemap_url"]:sitemap_dict})
    result = sitemap_category.get()
    return result
  xpath_forced = data.get("xpath_forced",False)
  website_hover = False
  click_xpath = ""
  categories_xpath = ""
  category_dict = {}
  category_xpath_list = []
  if xpath_forced == False:
    category_xpath_list = data.getlist("cat")
    category_xpath_list = [each for each in category_xpath_list if each]
    categorical_url_dict = {"category_name":"category_xpath"}
  else:
    category_xpath_list = data.get("categories")
    categorical_url_dict = data.get("categorical_url_dict")  
    ## hilson has to get these data and call this function

  # print (category_list)
  website_url_approach = data.get('categoryType','')
  # print (website_url_approach)
  if website_url_approach == "hover":
      website_hover = True
  elif "clickhover" in website_url_approach:
      website_hover = True
      click_xpath = data.get("xpath","")
      # print (click_xpath)
  elif website_url_approach == "xpath":
      website_hover = False
      categories_xpath = data.get("xpath","")

  website_type = data.get('type','')
  website = data.get("url","")
  website_name = data.get("urlname","")
  website_dict = {}
  if website_name:
      website_dict[website] = {'categories':category_xpath_list,'hover':website_hover,'type':website_type,"xpath":click_xpath,
                              "categories_xpath":categories_xpath,"url_approach":website_url_approach,"xpath_forced":xpath_forced,
                              "category_url_dict":categorical_url_dict,"url":website,"urlname":website_name}

      category_task = crawl_category.delay(website_name,website_dict)
      category_dict = category_task.get()
  # print (category_dict[website_name])
  # # db_handle =db.get_cursor(website_name+"_categories")
  # # logging.info("Categorical URLs Gathered for "+data[0])
  # # db.replace_cateogrical_data(db_handle,website_name,data[-1])
  # # logging.info("Categorical URLs Updated for "+data[0])
  return category_dict

def viewdata(category_url,website_name,test=False,website_settings={}):
    # category_result = category_result.dict()
    crawl_dict = {}
    crawl_task = []
    if not test:
      website_settings = json.load(open(BASE_DIR+"/eComCrawl/jsons/"+website_name+".json","r+"))
    homepage = website_settings["url"]
    if not test:
        crawl_task = crawl_link.delay(category_url,website_settings,homepage,test)
    else:
        crawl_task = crawl_link.delay(category_url,website_settings,homepage,test)
        crawl_dict = crawl_task.get()
    return crawl_dict

def get_category_names(category_post):
  category_dict = category_post
  category_sitemap = {}
  final_data = {}
  if "sitemap_urlname" in category_post:
    category_sitemap['url'] = category_post.get("url","")
    category_sitemap['sitemap_xpath_url'] = category_post.get("sitemap_xpath_url","")
    category_sitemap['sitemap_url'] = category_post.get("sitemap_url","")
    category_sitemap['category_xpath'] = category_post.get("category_xpath","")
    category_sitemap['category_count'] = category_post.get("category_count","")
    category_sitemap['sitemap_urlname'] = category_post.get("sitemap_urlname","")
    category_dict = category_sitemap
  elif "urlname" in category_post:
    category_dict['url'] = category_post.get("url","")
    category_dict['urlname'] = category_post.get("urlname","")
    category_dict['category_count'] = category_post.get("category_count",2)
    category_dict['category_xpath'] = category_post.get("category_xpath","")
    category_dict['categoryType'] = category_post.get("categoryType","")
    category_dict['xpath'] = category_post.get("xpath","")
  data = get_names.delay(category_dict)
  final_data = data.get()
  return final_data
#Function created by Ramesh Tiwari Starts Here
#For Local Testing
# tasksURL = open("/home/gunner/Documents/tasks.json").read()
# tasksJson = json.loads(tasksURL)

#Request from Flower API
def tasksOutput():
  tasksURL = requests.get("http://192.168.0.108:5555/api/tasks")
  tasksJson = tasksURL.json()
  tasksDict = {}
  resultList = []
  for taskid, tasksDict in tasksJson.items():
    args = tasksDict['args']
    if "crawl_category" in tasksDict['name']:
      args = re.findall(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,‌​3}[.]|[a-z0-9.\-]+[.‌​][a-z]{2,4}/)(?:[^\s‌​()<>]+|(([^\s()<‌​>]+|(([^\s()<>]+‌​)))*))+(?:&#‌​40;([^\s()<>]+|((‌​;[^\s()<>]+)))*&‌​#41;|[^\s`!()[&#‌​93;{};:'".,<>?«»“”‘’‌​]))""",args)[0]
    else:
      args = args.split(",")[0].replace("('","")[:-1]
    
    data1 = {
      "task": tasksDict['name'].replace("eComCrawl.tasks.","").upper(),
      "website": args,
      "site": "Undefined Right Now",
      "status": tasksDict['state'].lower(),
      "started": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tasksDict['started'])),
      "completed": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tasksDict['succeeded'])),
      "elapsed": str(tasksDict['runtime']).split(".")[0]
      }
    resultList.append(data1)
  return resultList

def save_xpath_data(request):
  json_data = request.session['page_4_data']
  json_name = json_data['urlname']
  json.dump(json_data,open(BASE_DIR+"/eComCrawl/jsons/"+json_name+".json","w"),indent=4)
  clearSessionData(request)
  return HttpResponseRedirect(reverse("websites"))

def clearSessionData(request):
  if "page_1_data" in request.session:
    del request.session["page_1_data"]
  if "page_2_data" in request.session:
    del request.session["page_2_data"]
  if "page_3_data" in request.session:
    del request.session["page_3_data"]
  if "page_4_data" in request.session:
    del request.session["page_4_data"]