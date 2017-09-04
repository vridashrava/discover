# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from lxml import html,etree
import time,json,os,re
import timeit,sys,random
from collections import defaultdict
import urllib
from crawlers.db import DB
from crawlers.docprocessing import json_formatting
import logging,datetime
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# from pyvirtualdisplay import Display
# data_fields = json.load(open(os.path.join(BASE_DIR,"dataformat.json"),'r+'))
class selenium_getdata:
  def __init__(self):
    self.url = ""
    # self.display = Display(visible=0,size=(1024,768))
    # self.display.start()
    # self.driver = webdriver.Remote(command_executor="http://198.58.124.206:4444/wd/hub",desired_capabilities=DesiredCapabilities.PHANTOM)
    co = Options()
    co.add_argument("--start-maximized")
    co.add_argument("disable-infobars")
    co.add_argument("--user-agent=%s"% "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1")
    self.driver = webdriver.Chrome("/home/ashmit/chromedriver",desired_capabilities=co.to_capabilities())
    self.driver.set_page_load_timeout(45)

  def __call__(self,url):
    self.url = url
    try:
      self.driver.get(self.url)
      WebDriverWait(self.driver,40).until(EC.presence_of_all_elements_located((By.XPATH,"//body")))
    except TimeoutException:
      time.sleep(1)
    self.website_name = self.get_website()
    # print (self.website_name)
    self.remove_alerts(self.website_name)
    logging.basicConfig(filename=BASE_DIR+"/logs/"+self.website_name+".log",filemode="w",level=logging.DEBUG)
    return

  def get_data(self,selector,items_dict,result,homepage):
    def get_xpath(c_xpath,attr):
      item_data = selector.xpath(c_xpath)
      print (attr,item_data,homepage)
      if item_data== []:
        return []
      if attr == "text":
        return [item_data[0].text_content()]
      elif attr=="html":
        return str(html.tostring(item_data[0]))
      elif attr =="href":
        item_data = selector.xpath(c_xpath+"/@href")
        return urllib.parse.urljoin(homepage,item_data[0])
      elif (attr == "src") or ("image" in attr):
        return [selector.xpath(c_xpath+"/@"+attr)[0]]
      else:
        item_list = []
        for each_item in item_data:
          item_list+=each_item.xpath("//@"+attr)
        return item_list
    # get the data based on TEXT, HTML, HREF, IMAGE etc
    for item_field,item_dict in items_dict.items():
      # print (item_field)
      attr = item_dict.get('xpath_type','')
      c_xpath = item_dict.get('xpath','')
      if attr:
        try:
          data = get_xpath(c_xpath,attr)
          if data == [] and item_dict.get('xpath2','')!='':
            data = get_xpath(items_dict['xpath2'],attr)
          result[item_field] = data
        except Exception as e:
          # print (item_field,e)
          result[item_field] = []
    return result
  def find_by_text(self,text):
    element ="" 
    try:
      element = self.driver.find_element_by_link_text(text)
    except:
      # element = self.driver.find_element_by_xpath(('//*[contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{0}")]').format(text))
      element = self.driver.find_element_by_xpath('.//*[contains(text(),"%s")]'%text)
    return element

  
  def get_items(self,category_dict,homepage,test):
    print (category_dict["items"])
    logging.info("Acquiring listings for page: "+str(self.driver.current_url))
    items_urls = []
    items_data = []
    items_dict = category_dict['items']
    result = []
    item_list_xpath = items_dict['xpath']
    self.wait_for_elements(items_dict['xpath'])
    if category_dict['pagination']['type'] != "xpath":
      try:
        self.pagination(category_dict['pagination'],test)
        items_data = self.driver.find_elements_by_xpath(item_list_xpath)
      except:
        time.sleep(1)
    items_data = self.driver.find_elements_by_xpath(item_list_xpath)
    if items_data == []:
      item_list_xpath = items_dict.get('xpath2','')
      if item_list_xpath!="":
        items_data = self.driver.find_elements_by_xpath(item_list_xpath)
      else:
        return []
    db = DB()
    self.website_name = category_dict.get("urlname")
    db_cursor = db.get_cursor(self.website_name)
    # categorical_url_data = db.get_categorical_data(db,cursor,homepage,)
    # print ("reached HERE tho")
    if test:
      items_data = items_data[:10]
    # print (items_data)
    for item in items_data:
      item_index = items_data.index(item)
      listing_dict = {}
      items_html = item.get_attribute("outerHTML")
      items_selector = html.fromstring(items_html)
      listing_dict = self.get_data(items_selector,items_dict['fields']['listing'],listing_dict,homepage)
      if category_dict['pagination']['type'] == "xpath":
        try:
          self.pagination(category_dict['pagination'],test)
        except:
          break
      result.append(listing_dict)
    logging.info("Items Found: "+str(len(items_data)))
    final_result = []
    counter = 0
    final_data = {}
    for listing_dict in result:
      try:
        item_url = listing_dict['url']
        html_dict = self.get_follow(item_url)
        product_selector = html.fromstring(html_dict['data'])
        final_data = self.get_data(product_selector,items_dict['fields']['product'],listing_dict,homepage)
        logging.info("Page Visited "+item_url)
      except Exception as e:
        print (e)
        logging.warning("Crawling Aborted :"+self.driver.current_url)
      try:
        # final_data = json_formatting(final_data,self.website_name)
        if final_data!={}:
          final_data['crawled_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          logging.info("Crawling Completed "+item_url)
          counter =+ 1
          if test:
            final_result.append(final_data)
            logging.info("Test on Page Completed for "+item_url)
          else:
            db.insert_data(db_cursor,final_data)
      except:
        logging.warning("Website data not inserted in Mongo from page ")
        time.sleep(2)

      time.sleep(5)
    logging.info("Crawling Completed :"+self.url+", total crawled items " +str(len(items_data)))
    return final_result
  
  def get_possible_xpaths(self,category_xpath):
    possible_xpaths = []
    if category_xpath:
      categories_xpath_list = category_xpath.split("/")
      for tag in categories_xpath_list[::-1]:
        tag_real_index = categories_xpath_list.index(tag)
        index_present = re.findall(r"\[\d+\]",tag)
        if index_present:
            new_tag = tag[:tag.index("[")]
            categories_xpath_list.pop(tag_real_index)
            categories_xpath_list.insert(tag_real_index,new_tag)
            possible_xpaths.append("/".join(categories_xpath_list))
    if possible_xpaths == []:
      possible_xpaths = [category_xpath]
    return possible_xpaths

  def get_category_names(self,category_dict):
    category_xpath = category_dict.get("category_xpath","")
    category_count = category_dict.get("category_count",2)
    category_count = int(category_count)
    possible_xpaths = self.get_possible_xpaths(category_xpath)
    category_name_xpath = {}
    category_elements = {}
    tree = ""
    if possible_xpaths:
      category_url_action = category_dict.get("categoryType","")
      if "sitemap_url" in category_dict:
        category_url_action = "sitemap"
      for possible_xpath in possible_xpaths:
        print (possible_xpaths,"\n")
        if "clickhover" in category_url_action:
          category_click_xpath = category_dict["xpath"]
          # print (category_click_xpath)
          click_button = self.driver.find_element_by_xpath(category_click_xpath)
          # print (click_button.text)
          # click_perform = ActionChains(self.driver).move_to_element(click_button)
          click_perform = ActionChains(self.driver).move_to_element(click_button)
          page_data =self.driver.page_source
          click_perform.perform()
          # page_data = re.sub(r"<!--.*?-->", "", page_data)
          root = html.fromstring(page_data)
          tree = root.getroottree()
          category_elements = root.xpath(possible_xpath)
          time.sleep(3)
        else:
          page_data =self.driver.page_source
          root = html.fromstring(page_data)
          tree = root.getroottree()
          category_elements = root.xpath(possible_xpath)
        if len(category_elements) >= category_count:
          break
      for category_index,category_element in enumerate(category_elements):
        category_name = category_element.text_content()
        print (category_name)
        if type(category_name) == list:
          category_name = max(each for each in category_name)
        if not category_name in category_name_xpath:
          category_name_xpath[category_name] = tree.getpath(category_element)
    return category_name_xpath
  def slice_xpath(self,xpath):
   return "/".join(each_urls_xpath.split("/")[:-1])
  def get_sitemap_urls(self,sitemap_dict):
    homepage = sitemap_dict.get("url","")
    website_name = sitemap_dict.get("sitemap_urlname","")
    category_count = sitemap_dict.get("category_count",2)
    category_count = int(category_count)
    page_data_dict = {}
    for i in range(1,category_count+1):
      each_category_count = sitemap_dict.get("sitemap_sub_cat_count_"+str(i),"")
      each_category_count = int(each_category_count)
      each_urls_xpath = sitemap_dict.get("sitemap_xpath_category_"+str(i),"")
      each_category_name = sitemap_dict.get("sitemap_category_name_"+str(i),"")
      # slice the xpath from bottom here
      # each_urls_xpath_sliced = "/".join(each_urls_xpath.split("/")[])
      print (each_urls_xpath)
      urls = self.driver.find_element_by_xpath(each_urls_xpath)
      category_name,categries_url = self.get_urls(urls,homepage,each_category_name,each_category_count)
      print (categries_url, category_name)
      page_data_dict[category_name] = categries_url
    return page_data_dict

  def get_categories(self,category_dict):
    # this function will return all the URL for the respective sub categories
    print ("categories",category_dict)
    category_name_xpath = category_dict.get("categories")
    category_xpath = ""
    click_perform = ""
    urls = ""
    force_xpath = category_dict.get("xpath_forced",False)

    final_urls = []
    homepage = category_dict.get("url")
    category_url_action = category_dict.get("url_approach","")
    hover = category_dict['hover']
    category_data_dict= {}
    category_url_dict = ""
    if category_url_action == "clickhover":
      category_click_xpath = category_dict["xpath"]
      click_button = self.driver.find_element_by_xpath(category_click_xpath)
      click_perform = ActionChains(self.driver).move_to_element(click_button)
      click_perform.perform()
      for category_xpath in category_name_xpath:
        print (category_xpath)
        time.sleep(3)
        click_perform.move_to_element(self.driver.find_element_by_xpath(category_xpath)).perform()
        # click_perform.perform()
        time.sleep(5)
        urls = self.driver.find_element_by_xpath(category_xpath)
        category_name,url_list = self.get_urls(urls,homepage)
        category_data_dict[category_name] = url_list
        if force_xpath:
          category_url_dict = category_dict.get("category_url_dict","")
          urls_xpath = category_url_dict[category_name]
          category_possible_xpaths = self.get_possible_xpaths(urls_xpath)
          for category_possible_xpath in category_possible_xpaths:
            urls = self.driver.find_element_by_xpath(category_possible_xpath)
            category_name,url_list = self.get_urls(urls,homepage,category_name)
            if len(url_list) > 5:
              break
          category_data_dict[category_name] = url_list

    elif category_url_action == "xpath":
      category_xpath = category_dict.get("xpath","")
    elif category_url_action == "hover":
      for category_xpath in category_name_xpath:
        urls = self.driver.find_element_by_xpath(category_xpath)
        # urls = self.driver.find_element_by_xpath("//*[contains(text(),'"+category_title+"']")
        hover = ActionChains(self.driver).move_to_element(urls)
        hover.perform()
        time.sleep(5)
        urls = self.driver.find_element_by_xpath(category_xpath)
        category_name,url_list = self.get_urls(urls,homepage)
        if force_xpath:
          category_url_dict = category_dict.get("category_url_dict","")
          urls_xpath = category_url_dict[category_name]
          category_possible_xpaths = self.get_possible_xpaths(urls_xpath)
          for category_possible_xpath in category_possible_xpaths:
            hover = ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath(category_xpath))
            hover.perform()
            urls = self.driver.find_elements_by_xpath(category_possible_xpath)
            time.sleep(3)
            # category_name,url_list = self.get_urls(urls,homepage,category_name)
            if len(urls) > 5:
              break
          category_data_dict[category_name] = [each.get_attribute("href") for each in urls]
        else:
          category_data_dict[category_name] = url_list
    else:
      for category_xpath in category_name_xpath:
        urls = self.driver.find_element_by_xpath(category_xpath)
        category_name,url_list = self.get_urls(urls,homepage)
        category_data_dict[category_name] = url_list

    return category_data_dict

  def get_urls(self,urls,homepage,category_name="",category_count=4):
    final_urls = []
    if category_name == "":
      category_name = urls.text.strip()

    parent = urls.find_element_by_xpath("..")
    category_urls = parent.get_attribute("outerHTML")
    category_urls_selector = html.fromstring(category_urls)
    urls_list = category_urls_selector.xpath("//a/@href")
    urls_list = list(set(urls_list))
    if len(urls_list) < category_count:
      grand_parent = parent.find_element_by_xpath("..")
      category_urls = grand_parent.get_attribute("outerHTML")
      category_urls_selector = html.fromstring(category_urls)
      urls_list = category_urls_selector.xpath("//a/@href")
    if len(urls_list)>=category_count:
      for url in urls_list:
        final_urls.append(urllib.parse.urljoin(homepage,url))

    time.sleep(1)
    final_urls = self.post_category_processing(final_urls)
    final_urls = list(set(final_urls))
    time.sleep(5)
    return [category_name,final_urls]

  def post_category_processing(self,urllist):
    final_list = []
    if "infibeam" in self.driver.current_url:
      for url in urllist:
        final_list.append(urllib.parse.urljoin(url,"search"))
      urllist = final_list
    return urllist

  def perform_actions(self,element_identity,element_type,element_action):
    hover_element = ""
    if element_type == "text":
      hover_element = self.driver.find_element_by_link_text(element_identity)
    elif element_type == "xpath":
      hover_element = self.driver.find_element_by_xpath(element_identity)
    if element_action == "hover":
      hover = ActionChains(self.driver).move_to_element(hover_element)
      hover.perform()
      time.sleep(5)
    elif element_action == "click and hover":
      time.sleep(5)

  def pagination(self,paginate,test):
    pagination_type = paginate.get("type","")
    pagination_product_count = 500
    if pagination_type == "step_scroll":
      pagination_xpath = paginate['paginate_parameters']['load_more_xpath']
      pagination_product_count_xpath = paginate['paginate_parameters'].get('products_path_count','')
      if pagination_product_count_xpath:
        pagination_product_count = self.driver.find_element_by_xpath(pagination_product_count_xpath).text
        # print (pagination_product_count)
      listing_count = paginate['paginate_parameters'].get('page_listing',50)
      pagination_count = int(re.findall(r'\d+',pagination_product_count)[0])//listing_count
      wait_time = paginate['paginate_parameters'].get('scroll_time_wait',15)
      actions = ActionChains(self.driver)
      if test:
        pagination_count = 3
      for i in range(pagination_count):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
        # print ("loading more")
        time.sleep(wait_time)
        try:
          more_button = self.driver.find_element_by_xpath(pagination_xpath)
          actions.move_to_element(more_button).click(more_button).perform()
          self.driver.switch_to.window(self.driver.window_handles[0])
          time.sleep(2)
        except:
          break
        self.driver.switch_to.window(self.driver.window_handles[0])
    elif pagination_type == "re-request":
      self.driver.get(self.url+paginate['paginate_parameters']['re_request_url'])
      time.sleep(5)
    elif pagination_type == "infinite_scroll":
      pagination_product_count_xpath = paginate['paginate_parameters'].get('products_path_count','')
      if pagination_product_count_xpath:
        pagination_product_count = self.driver.find_element_by_xpath(pagination_product_count_xpath).text
      listing_count = paginate['paginate_parameters'].get('page_listing',50)
      pagination_count = int(re.findall(r'\d+',pagination_product_count)[0])//listing_count
      wait_time = paginate['paginate_parameters'].get('scroll_time_wait',15)
      if test:
        pagination_count = 3
      for i in range(pagination_count):
        self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
        time.sleep(3)
    elif pagination_type == "xpath":
      pagination_xpath = paginate['paginate_parameters']['load_more_xpath']
      actions = ActionChains(self.driver)
      more_button = self.driver.find_element_by_xpath(pagination_xpath)
      actions.move_to_element(more_button).click(more_button).perform()
      self.driver.switch_to.window(self.driver.window_handles[0])
      time.sleep(5)

  def get_follow(self,url=""):
    # acquires the follow pages from the sub-category URLs
    try:
      if url!="":  
        self.driver.get(url)
      time.sleep(4)
    except TimeoutException:
      time.sleep(4)
      logging.debug("Time Out on opening url "+url)
    except WebDriverException:
      logging.warning("Error while acquiring html data from "+url)
    page_data =self.driver.page_source
    page_data = re.sub(r"<!--.*?-->", "", page_data)
    return {
        'data':page_data,
        'url':self.driver.current_url
        }
  def wait_for_elements(self,xpath):
    try:
      WebDriverWait(self.driver,20).until(EC.presence_of_all_elements_located((By.XPATH,xpath)))
    except:
      time.sleep(2)
  def get_website(self):
    website_name = urllib.parse.urlparse(self.driver.current_url)
    website_name = website_name.netloc
    return website_name.split(".")[-2]

  def remove_alerts(self,website_name):
    if website_name == "gadgetsnow":
      self.driver.execute_script('$(".ntfc_overlay").hide();')
    elif website_name == "ezoneonline":
      self.driver.execute_script('$("#colorbox").hide();')
      self.driver.execute_script('$("#cboxOverlay").hide();')
      # self.driver.execute_script('window.alert("test");')
  def close_sel(self):
    try:
      self.driver.close()
    except:
      logging.warning("Error closing window, Forcing shut down")
      self.driver.close()
      self.driver.quit()
    # self.display.stop()

# $(".ntfc_overlay").hide()
