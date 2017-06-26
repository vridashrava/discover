# -*- coding: utf-8 -*-
# from crawlers.db import DB
from lxml import html
import json,logging
def json_formatting(each_data,website):
	logging.basicConfig(filename="logs/"+website+".log",level=logging.DEBUG)
	json_list = []
	if "jabong" in website:
		spec_dict = process_specification(each_data['specifications'],website)
		each_data['specifications'] = spec_dict
		product_id = spec_dict.get("SKU","")
		breadcrumb_dict = process_breadcrumbs(each_data['breadcrumb'],website)
		each_data['breadcrumb'] = breadcrumb_dict
		each_data['product_id'] = product_id
		if each_data['mrp'] == []:
			each_data['mrp'] = each_data['selling_price']
			each_data['discount'] = 0
	elif "shopclues" in website:
		try:
			spec_dict = process_specification(each_data['specifications'],website)
			each_data['specifications'] = spec_dict
		except Exception as e:
			logging.warning("Error processing specifications at"+each_data['url'])

		breadcrumb_dict = process_breadcrumbs(each_data['breadcrumb'],website)
		each_data['breadcrumb'] = breadcrumb_dict
		if each_data['mrp'] == []:
			each_data['mrp'] = each_data['selling_price']
			each_data['discount'] = 0
	elif "myntra" in website:
		if each_data['mrp'] == []:
			each_data['mrp'] = each_data['selling_price']
			each_data['discount'] = 0
	return each_data

def process_specification(spec_data,website):
	html_selector = html.fromstring(spec_data)
	if "jabong" in website:
		specs_list = html_selector.xpath("//ul[@class='prod-main-wrapper']/li")
		spec_dict = {}
		for specification in specs_list[:-1]:
			spec_list = []
			spec_text = html.tostring(specification)
			spec_selector = html.fromstring(spec_text)
			spec_list = spec_selector.xpath("//span/text()")
			spec_dict[spec_list[0]]=spec_list[-1]
		return spec_dict
	elif "shopclues" in website:
		specs_key = html_selector.xpath("//tbody/tr/td[@width='20%']/span/text()")
		specs_value = html_selector.xpath("//tbody/tr/td[@width='80%']/span/text()")
		spec_dict = {}
		for spec_key in specs_key:
			spec_key_index = specs_key.index(spec_key)
			# print (bread_crumb_text_list,bread_crumb_link_list)
			spec_dict[spec_key] = specs_value[spec_key_index]
		return spec_dict


def process_breadcrumbs(breadcrumb_data,website):
	html_selector = html.fromstring(breadcrumb_data)
	if "jabong" in website:
		bread_crumbs_order = html_selector.xpath("//ol[@class='breadcrumb']/li")
		breadcrumb_dict = {}
		for bread_crumb in bread_crumbs_order:
			bread_crumb_text = html.tostring(bread_crumb)
			bread_crumb_selector = html.fromstring(bread_crumb_text)
			bread_crumb_link_list = bread_crumb_selector.xpath("//a/@href")
			bread_crumb_text_list = bread_crumb_selector.xpath("//a/span/text()")
			# print (bread_crumb_text_list,bread_crumb_link_list)
			breadcrumb_dict[bread_crumb_text_list[0]] = bread_crumb_link_list[0]
		return breadcrumb_dict
	elif "shopclues" in website:
		bread_crumbs_order = html_selector.xpath("//div[@class='breadcrums']/ul/li")
		breadcrumb_dict = {}
		for bread_crumb in bread_crumbs_order:
			try:
				bread_crumb_text = html.tostring(bread_crumb)
				print (bread_crumb_text)
				bread_crumb_selector = html.fromstring(bread_crumb_text)
				bread_crumb_link_list = bread_crumb_selector.xpath("//a/@href")
				bread_crumb_text_list = bread_crumb_selector.xpath("//a/span/text()")
				# print (bread_crumb_text_list,bread_crumb_link_list)
				breadcrumb_dict[bread_crumb_text_list[0]] = bread_crumb_link_list[0]
			except:
				print ("Error in Breadcrumb")
		return breadcrumb_dict
