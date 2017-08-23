from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from eComCrawl.tasks import crawl_link,crawl_category
from crawlers.db import DB
import logging,json
import requests
import json,re,os,time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def form(request):
    return render(request, 'form.html', {})

def viewform(data_dict):
    website_hover = False
    click_xpath = ""
    categories_xpath = ""
    data =  data_dict
    # print (data)
    category_dict = {}
    category_list = data.getlist("cat")
    category_list = [each for each in category_list if each]
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
    if website:
        website_dict[website] = {'categories':category_list,'hover':website_hover,'type':website_type,"xpath":click_xpath,
                                "categories_xpath":categories_xpath,"url_approach":website_url_approach}

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

#Function created by Ramesh Tiwari Starts Here
#For Local Testing
# tasksURL = open("/home/gunner/Documents/tasks.json").read()
# tasksJson = json.loads(tasksURL)

#Request from Flower API
def tasksOutput():
  tasksURL = requests.get("http://192.168.0.105:5555/api/tasks")
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