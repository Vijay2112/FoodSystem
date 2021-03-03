from django.db import models

# Create your models here.

class Bill():

	# 1 - place order
	def create_order(self, customer_name, restaurant, item, instructions):
		orderx = {}
		orderx['customer_name'] = customer_name
		orderx['restaurant'] = restaurant
		orderx['item'] = item
		orderx['instructions'] = instructions
		return orderx

	def create_bill(self,orderx,delv,id):
		billx = {}
		billx['_id'] = id
		billx["order_details"] = orderx
		billx['delivery person'] = delv
		return billx


