# -*- coding: utf-8 -*-
# from crawlers.db import DB
from lxml import html, etree
import json, logging
import re




def jointexts(l, space = False):
  r = ""
  for e in l:
    if type(l) == list:
      if space:
        r += " " + jointexts(e)
      else:
        r += jointexts(e)
    else:
      r += e
  return r.strip()

def extract(root):
  r = []
  for element in root:
    innerTextFromElements = []
    try:
      innerTextFromElements = extract(element)
    except ValueError:
      pass

    if innerTextFromElements == []:
      innerTextFromElements = element.text_content().strip()

    r.append(innerTextFromElements)
  # print("---")
  # print(root.text_content().strip())
  # print(jointexts(r))
  a = root.text_content().strip()
  b = jointexts(r)
  if a > b:
    return [a]
  else:
    return r


def clearify(l):
  if type(l) == list:
    if len(l) == 1:
      return clearify(l[0])
    else:
      r = []
      for i in l:
        r.append(clearify(i))
      return r
  else:
    return l

def flatten(l):
    try:
        return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
    except IndexError:
        return []

def full_extract(html_str):
  html_str = html_str.replace("\n", "")
  html_str = re.sub(' +',' ',html_str)

  root = html.fromstring(html_str)
  for bad in root.xpath("//script"):
    bad.getparent().remove(bad)
  for bad in root.xpath("//style"):
    bad.getparent().remove(bad)
  r = clearify(extract(root))
  return r
  # output_html = ""

  # for e in r:
  #   if type(e) == str:
  #     output_html += "<div><span>" + e + "</span></div>"
  #   elif type(e) == list:
  #     output_html += "<div>"
  #     for f in e:
  #       output_html += "<span>" + (" ".join(flatten(f)) if type(f) == list else f) + "</span>"
  #     output_html += "</div>"
  # return output_html






def json_formatting(each_data,website):
	logging.basicConfig(filename="logs/"+website+".log",level=logging.DEBUG)
	json_list = []
	product_id = ""
	if "jabong" in website:
		try:
			spec_dict = process_specification(each_data['specifications'],website)
			each_data['specifications'] = spec_dict
		except Exception as e:
			logging.warning("Error processing specifications at "+each_data['url'])
			each_data['specifications'] = each_data['specifications']
		try:
			breadcrumb_dict = process_breadcrumbs(each_data['breadcrumb'],website)
			# print (breadcrumb_dict)
			each_data['breadcrumb'] = breadcrumb_dict
			product_id = breadcrumb_dict.get("SKU","")
		except Exception as e:
			each_data['breadcrumb'] = each_data['breadcrumb']
			logging.warning("Error processing breadcrumbs at "+each_data['url'])
		each_data['product_id'] = product_id
		if each_data['mrp'] == []:
			each_data['mrp'] = each_data['selling_price']
			each_data['discount'] = 0
	elif "shopclues" in website:
		try:
			spec_dict = process_specification(each_data['specifications'],website)
			each_data['specifications'] = spec_dict
		except Exception as e:
			logging.warning("Error processing specifications at "+each_data['url'])
			each_data['specifications'] = each_data['specifications']
		try:
			breadcrumb_dict = process_breadcrumbs(each_data['breadcrumb'],website)
			each_data['breadcrumb'] = breadcrumb_dict
		except Exception as e:
			each_data['breadcrumb'] = each_data['breadcrumb']
			logging.warning("Error processing breadcrumbs at "+each_data['url'])
		if each_data['mrp'] == []:
			each_data['mrp'] = each_data['selling_price']
			each_data['discount'] = 0
	elif "myntra" in website:
		if each_data['mrp'] == []:
			each_data['mrp'] = each_data['selling_price']
			each_data['discount'] = 0
	return each_data

def process_specification(spec_data, website):
	return full_extract(spec_data)


	# html_selector = html.fromstring(spec_data)
	# if "jabong" in website:
	# 	specs_list = html_selector.xpath("//ul[@class='prod-main-wrapper']/li")
	# 	spec_dict = {}
	# 	for specification in specs_list[:-1]:
	# 		spec_list = []
	# 		spec_text = html.tostring(specification)
	# 		spec_selector = html.fromstring(spec_text)
	# 		spec_list = spec_selector.xpath("//span/text()")
	# 		spec_dict[spec_list[0]]=spec_list[-1]
	# 	return spec_dict
	# elif "shopclues" in website:
	# 	specs_key = html_selector.xpath("//tbody/tr/td[@width='20%']/span/text()")
	# 	specs_value = html_selector.xpath("//tbody/tr/td[@width='80%']/span/text()")
	# 	spec_dict = {}
	# 	for spec_key in specs_key:
	# 		spec_key_index = specs_key.index(spec_key)
	# 		# print (bread_crumb_text_list,bread_crumb_link_list)
	# 		spec_dict[spec_key] = specs_value[spec_key_index]
	# 	return spec_dict


def process_breadcrumbs(breadcrumb_data,website):
  root = html.fromstring(breadcrumb_data)
  breadcrumbs = root.findall(".//a[@href]")
  return [(breadcrumb.text_content().strip(), breadcrumb.attrib["href"]) for breadcrumb in breadcrumbs if breadcrumb.text_content() != None and breadcrumb.attrib["href"] != None]

	# html_selector = html.fromstring(breadcrumb_data)
	# if "jabong" in website:
	# 	bread_crumbs_order = html_selector.xpath("//ol[@class='breadcrumb']/li")
	# 	breadcrumb_dict = {}
	# 	for bread_crumb in bread_crumbs_order[:-1]:
	# 		bread_crumb_text = html.tostring(bread_crumb)
	# 		bread_crumb_selector = html.fromstring(bread_crumb_text)
	# 		bread_crumb_link_list = bread_crumb_selector.xpath("//a/@href")
	# 		bread_crumb_text_list = bread_crumb_selector.xpath("//a/span/text()")
	# 		# print (bread_crumb_text_list,bread_crumb_link_list)
	# 		breadcrumb_dict[bread_crumb_text_list[0]] = bread_crumb_link_list[0]
	# 	return breadcrumb_dict
	# elif "shopclues" in website:
	# 	bread_crumbs_order = html_selector.xpath("//div[@class='breadcrums']/ul/li")
	# 	breadcrumb_dict = {}
	# 	for bread_crumb in bread_crumbs_order[:-1]:
	# 		try:
	# 			bread_crumb_text = html.tostring(bread_crumb)
	# 			# print (bread_crumb_text)
	# 			bread_crumb_selector = html.fromstring(bread_crumb_text)
	# 			bread_crumb_link_list = bread_crumb_selector.xpath("//a/@href")
	# 			bread_crumb_text_list = bread_crumb_selector.xpath("//a/span/text()")
	# 			print (bread_crumb_text_list,bread_crumb_link_list)
	# 			breadcrumb_dict[bread_crumb_text_list[0]] = bread_crumb_link_list[0]
	# 		except:
	# 			print ("Error in Breadcrumb")
	# 	return breadcrumb_dict

