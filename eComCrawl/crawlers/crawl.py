# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from lxml import html
import time,json,os,re
import timeit,sys,random
from collections import defaultdict
import urllib
from crawlers.db import DB
from crawlers.docprocessing import json_formatting
import logging
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# data_fields = json.load(open(os.path.join(BASE_DIR,"dataformat.json"),'r+'))

class selenium_getdata:
    def __init__(self):
        self.url = ""
        # self.driver = webdriver.Remote(command_executor="http://198.58.124.206:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME)
        self.driver = webdriver.Chrome("/home/ashmit/chromedriver")
        self.driver.set_page_load_timeout(45)

    def __call__(self,url):
        self.url = url
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver,40).until(EC.presence_of_all_elements_located((By.XPATH,"//body")))
        except TimeoutException:
            time.sleep(1)
        self.website_name = self.get_website()
        logging.basicConfig(filename="logs/"+self.website_name+".log",filemode="w",level=logging.DEBUG)

    def get_data(self,selector,items_dict,result,homepage):
        def get_xpath(c_xpath,attr):
            item_data = selector.xpath(c_xpath)
            if item_data== [] and attr != "image":
                return []
            if attr == "text":
                return item_data[0].xpath(c_xpath+"/text()")
            elif attr=="html":
                return str(html.tostring(item_data[0]))
            elif attr =="href":
                return urllib.parse.urljoin(homepage,item_data[0])
            elif attr == "image" or attr == "list":
                # print (item_data)
                return item_data
            else:
                return item_data[0]
            return []
        # get the data based on TEXT, HTML, HREF, IMAGE etc
        for item_field,item_dict in items_dict.items():
            attr = item_dict['xpath_type']
            c_xpath = item_dict['xpath']
            data = get_xpath(c_xpath,attr)
            if data == [] and item_dict.get('xpath2','')!='':
                data = get_xpath(items_dict['xpath2'],attr)
            result[item_field] = data
            # improve iteration to three or even four xpaths
        return result

    
    def get_items(self,category_dict,homepage):
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
        item_list_click_path = items_dict['click_xpath']
        # time.sleep(15)
        self.wait_for_elements(items_dict['xpath'])
        # PAGINATION HERE
        try:
            self.pagination(category_dict['pagination'])
        except:
            time.sleep(1)
        items_data = self.driver.find_elements_by_xpath(item_list_xpath)
        # print (len(items_data))
        
        if items_data == []:
            item_list_xpath = items_dict.get('xpath2','')
            item_list_click_path = items_dict.get('click_xpath2','')
            if item_list_xpath!="":
                items_data = self.driver.find_elements_by_xpath(item_list_xpath)
            else:
                return []
        db = DB()
        self.website_name = self.get_website()
        db_cursor = db.get_cursor(self.website_name)
        for item in items_data:
            item_index = items_data.index(item)
            listing_dict = {}
            items_html = item.get_attribute("outerHTML")
            # print (items_html)
            items_selector = html.fromstring(items_html)
            listing_dict = self.get_data(items_selector,items_dict['fields']['listing'],listing_dict,homepage)
            # focus_element = self.driver.find_element_by_xpath("//body")
            # focus_element.click()
            result.append(listing_dict)
        final_result = []
        for listing_dict in result:
            try:
                item_url = listing_dict['url']
                html_dict = self.get_follow(listing_dict['url'])
                product_selector = html.fromstring(html_dict['data'])
                final_data = self.get_data(product_selector,items_dict['fields']['product'],listing_dict,homepage)
                logging.info("Page Visited "+listing_dict['url'])
            except Exception as e:
                logging.warning("Crawling Aborted "+listing_dict['url']+" because of "+str(e))
            try:
                final_data = json_formatting(final_data,self.website_name)
                db.insert_data(db_cursor,final_data)
                if final_data!={}:
                    logging.info("Crawling Completed"+listing_dict['url'])
            except:
                logging.warning("Website data not inserted in Mongo from page" + str(final_data['url']))
                time.sleep(2)
        # if items_dict['approach'] == 'click':
        #     action = ActionChains(self.driver)
        #     focus_element = self.driver.find_elements_by_xpath(item_list_click_path)[item_index]
        #     action.key_down(Keys.CONTROL).click(focus_element).key_up(Keys.CONTROL).perform()
        # else:
        #     self.driver.find_element_by_xpath("//body").send_keys(Keys.COMMAND + "t")
            
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        # html_dict = self.get_follow(listing_dict['url'])
        # product_selector = html.fromstring(html_dict['data'])
        # listing_dict = self.get_data(product_selector,items_dict['fields']['product'],listing_dict,homepage)
        # print (json.dumps(listing_dict,indent=4))
        # self.driver.close()
        # self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)
        logging.info("Crawling Completed :"+self.url)
        return final_result

    def get_categories(self,homepage,category_title,hover=False):
        # this function will return all the URL for the respective sub categories
        urls = self.driver.find_element_by_link_text(category_title)
        final_urls = []
        if hover:
            hover = ActionChains(self.driver).move_to_element(urls)
            hover.perform()
            time.sleep(5)
        parent = urls.find_element_by_xpath("..")
        category_urls = parent.get_attribute("outerHTML")
        category_urls_selector = html.fromstring(category_urls)
        urls_list = category_urls_selector.xpath("//a/@href")
        if len(urls_list) < 2:
            links = self.driver.find_elements_by_xpath("//a[contains(@href,'"+"/"+category_title.lower()+"')]")
            urls_list = []
            for each in links:
                urls_list.append(each.get_attribute("href"))
        for url in urls_list:
            final_urls.append(urllib.parse.urljoin(homepage,url))
        return final_urls

    def pagination(self,paginate):
        pagination_type = paginate.get("type","")
        if pagination_type == "step_scroll":
            pagination_xpath = paginate['paginate_parameters']['load_more_xpath']
            pagination_product_count_xpath = paginate['paginate_parameters']['products_path_count']
            pagination_product_count = self.driver.find_element_by_xpath(pagination_product_count_xpath).text
            pagination_count = int(re.findall(r'\d+',pagination_product_count)[0])//40
            actions = ActionChains(self.driver)
            for i in range(pagination_count):
                self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
                time.sleep(2)
                more_button = self.driver.find_element_by_xpath(pagination_xpath)
                actions.move_to_element(more_button).perform()
                time.sleep(2)
        elif pagination_type == "re-request":
            self.driver.get(self.url+paginate['paginate_parameters']['re_request_url'])
            time.sleep(5)
        elif pagination_type == "infinite_scroll":
            pagination_product_count_xpath = paginate['paginate_parameters']['products_path_count']
            pagination_product_count = self.driver.find_element_by_xpath(pagination_product_count_xpath).text
            pagination_count = int(re.findall(r'\d+',pagination_product_count)[0])//40
            for i in range(pagination_count):
                self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
                time.sleep(3)
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
        if "jabong" in self.driver.current_url:
            return "jabong"
        elif "myntra" in self.driver.current_url:
            return "myntra"
        else:
            return "shopclues"

    def close_sel(self):
        try:
            self.driver.close()
        except:
            logging.warning("Error closing window, Forcing shut down")
            self.driver.close()
            self.driver.quit()
