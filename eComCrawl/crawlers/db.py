# -*- coding:utf-8 -*-
import json
from pymongo import MongoClient
##################################DATABASE SCHEMA ####################

# client = MongoClient('localhost',27017)
# db_handle = client['shopclues']

class DB(object):
	def __init__(self):
		self.client = MongoClient('localhost',27017)
		self.db_handle = self.client['ecom_db']

	def get_cursor(self,collection_name):
		return self.db_handle[collection_name]		

	def insert_data(self,cursor,data):
		cursor.insert_one(data)

	def read_data(self,cursor,query_dict):
		query_data = []
		try:
			query_data = cursor.find(query_dict)
		except Exception as e:
			print ("Error",e)
		return query_data
	def replace_cateogrical_data(self,cursor,url,data_dict):
		value = ""
		try:
			value = cursor.find_one_and_replace({url:{'$exists':True}},data_dict)
			if not value:
				self.insert_data(cursor,data_dict)
		except Exception as e:
			print ("Error",e)
		return



