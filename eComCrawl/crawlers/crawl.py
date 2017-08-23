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
from lxml import html
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
      # print (attr,item_data)
      if item_data== []:
        return []
      if attr == "text":
        return item_data[0].xpath(c_xpath+"/text()")
      elif attr=="html":
        return str(html.tostring(item_data[0]))
      elif attr =="href":
        item_data = item_data[0].xpath(c_xpath+"/@href")
        return urllib.parse.urljoin(homepage,item_data[0])
      elif attr == "src" or "image" in attr:
        image_list = []
        for each_item in item_data:
          image_list+=each_item.xpath(c_xpath+"/"+attr)
        return image_list
      else:
        item_list = []
        for each_item in item_data:
          item_list+=each_item.xpath(c_xpath+"/"+attr)
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
    # driver loads the category url
    # we find the items and the data
    # apply pagination rules
    # grab each data on tab
    logging.info("Acquiring listings for page: "+str(self.driver.current_url))
    items_urls = []
    items_data = []
    items_dict = category_dict['items']
    result = []
    item_list_xpath = items_dict['xpath']
    # item_list_click_path = items_dict['click_xpath']
    # time.sleep(15)
    # SKIP if Batch Testing the data:
    self.wait_for_elements(items_dict['xpath'])
    # if not test:
      # PAGINATION HERE
    if category_dict['pagination']['type'] != "xpath":
      try:
        self.pagination(category_dict['pagination'],test)
        items_data = self.driver.find_elements_by_xpath(item_list_xpath)
      except:
        time.sleep(1)
    items_data = self.driver.find_elements_by_xpath(item_list_xpath)
  
    # print (len(items_data))
    # print (items_data)
    
    if items_data == []:
      item_list_xpath = items_dict.get('xpath2','')
      # item_list_click_path = items_dict.get('click_xpath2','')
      if item_list_xpath!="":
        items_data = self.driver.find_elements_by_xpath(item_list_xpath)
      else:
        return []
    db = DB()
    self.website_name = category_dict.get("urlname")
    db_cursor = db.get_cursor(self.website_name)
    # print ("reached HERE tho")
    if test:
      items_data = items_data[:10]
    # print (items_data)
    for item in items_data:
      item_index = items_data.index(item)
      listing_dict = {}
      items_html = item.get_attribute("outerHTML")
      # print (items_html)
      items_selector = html.fromstring(items_html)
      listing_dict = self.get_data(items_selector,items_dict['fields']['listing'],listing_dict,homepage)
      if category_dict['pagination']['type'] == "xpath":
        try:
          self.pagination(category_dict['pagination'],test)
        except:
          break
      # focus_element = self.driver.find_element_by_xpath("//body")
      # focus_element.click()
      result.append(listing_dict)
    logging.info("Items Found: "+str(len(items_data)))
    final_result = []
    for listing_dict in result:
      try:
        item_url = listing_dict['url']
        html_dict = self.get_follow(listing_dict['url'])
        product_selector = html.fromstring(html_dict['data'])
        final_data = self.get_data(product_selector,items_dict['fields']['product'],listing_dict,homepage)
        logging.info("Page Visited "+listing_dict['url'])
      except Exception as e:
        logging.warning("Crawling Aborted :"+self.driver.current_url)
      try:
        final_data = json_formatting(final_data,self.website_name)
        if final_data!={}:
          final_data['crawled_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          logging.info("Crawling Completed "+listing_dict['url'])
          if test:
            final_result.append(final_data)
            logging.info("Test on Page Completed for "+listing_dict['url'])
          else:
            db.insert_data(db_cursor,final_data)
      except:
        logging.warning("Website data not inserted in Mongo from page ")
        time.sleep(2)

      time.sleep(5)
    logging.info("Crawling Completed :"+self.url+", total crawled items " +str(len(items_data)))
    return final_result

  def get_categories(self,homepage,category_title,category_dict):
    # this function will return all the URL for the respective sub categories
    category_xpath = ""
    click_perform = ""
    urls = ""
    final_urls = []
    category_url_action = category_dict.get("url_approach","")
    hover = category_dict['hover']
    if category_url_action == "clickhover":
      category_click_xpath = category_dict["xpath"]
      # print (category_click_xpath)
      click_button = self.driver.find_element_by_xpath(category_click_xpath)
      # print (click_button.text)
      # click_perform = ActionChains(self.driver).move_to_element(click_button)
      click_perform = ActionChains(self.driver).move_to_element(click_button)
      click_perform.perform()
      time.sleep(3)
      click_perform.move_to_element(self.find_by_text(category_title)).perform()
      # click_perform.perform()
      time.sleep(5)
      urls = self.find_by_text(category_title)
    elif category_url_action == "xpath":
      category_xpath = category_dict.get("xpath","")
    elif category_url_action == "hover":
      urls = self.find_by_text(category_title)
      # urls = self.driver.find_element_by_xpath("//*[contains(text(),'"+category_title+"']")
      hover = ActionChains(self.driver).move_to_element(urls)
      hover.perform()
      time.sleep(5)
      urls = self.find_by_text(category_title)
    else:
      urls = self.driver.find_element_by_xpath(category_xpath)
    parent = urls.find_element_by_xpath("..")
    category_urls = parent.get_attribute("outerHTML")
    category_urls_selector = html.fromstring(category_urls)
    urls_list = category_urls_selector.xpath("//a/@href")
    urls_list = list(set(urls_list))
    if len(urls_list) < 3:
      grand_parent = parent.find_element_by_xpath("..")
      category_urls = grand_parent.get_attribute("outerHTML")
      category_urls_selector = html.fromstring(category_urls)
      urls_list = category_urls_selector.xpath("//a/@href")
      # urls_list = []
      # for each in links:
        # urls_list.append(each.get_attribute("href"))
    if len(urls_list)>=5:
      for url in urls_list:
        final_urls.append(urllib.parse.urljoin(homepage,url))
    time.sleep(1)
    final_urls = self.post_category_processing(final_urls)
    final_urls = list(set(final_urls))
    time.sleep(5)
    return final_urls
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
      pagination_count = int(re.findall(r'\d+',pagination_product_count)[0])//40
      actions = ActionChains(self.driver)
      if test:
        pagination_count = 3
      for i in range(pagination_count):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
        # print ("loading more")
        time.sleep(2)
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
      pagination_product_count_xpath = paginate['paginate_parameters']['products_path_count']
      pagination_product_count = self.driver.find_element_by_xpath(pagination_product_count_xpath).text
      pagination_count = int(re.findall(r'\d+',pagination_product_count)[0])//40
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

  def get_follow(self,url):
    # acquires the follow pages from the sub-category URLs
    try:  
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
