from django.shortcuts import render
from django.http import HttpResponse
from .models import Bill
import order.variables as variables
from .db_setup import MongoConnection,MyCollection
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from order.db_setup import insert_one_doc,find_doc,update_doc
import uuid

class Order(View):

	dbconnection = None

	@csrf_exempt
	def get(self, request):
		return self.place_order(request)

	@csrf_exempt
	def post(self, request, *args, **kwargs):
		return self.db_update(request)

	@csrf_exempt
	def place_order(self,request):
		return render(request,"order/order_info.html")

	@csrf_exempt
	def db_update(self,request):

		""" 1 - place order"""

		customer_name = request.POST.get('customer_name', None)
		restaurant = request.POST.get('restaurant', None)
		item  = request.POST.get('item', None)
		instructions = request.POST.get('instructions', None)

		bill = Bill()
		order_x = bill.create_order(customer_name, restaurant, item, instructions)
		id = str(uuid.uuid4())
		#id = variables.id
		order_x['_id'] = id
		#id_dummy = id
		#id+=1

		#Create db connection
		self.dbconnection = MyCollection()

		#inserting order into MongoDB
		self.insert(order_x,1)

		""" 2 - Get confirmation from Restaurant """
		res_avail = self.restaurant_status("name",restaurant)["availability"]

		""" 3 - Assign Delivery executive"""

		if res_avail:
			delv_list = self.assign_delv()
			if delv_list[0]:
				pass
			else:
				return HttpResponse("<h3>Delivery Executives not Available</h3>")
		else:
			return HttpResponse("<h3>Restaurant not Available</h3>")

		#persist
		bill_x = bill.create_bill(order_x,delv_list[1],id)
		self.insert(bill_x,2)
		return self.display_bills()

	def insert(self,item,i):

		if i==1:
			orders = self.dbconnection.get_collection("Orders")
			insert_one_doc(orders,item)
		elif i==2:
			bills = self.dbconnection.get_collection("Bills")
			insert_one_doc(bills,item)
		else:
			pass

	def restaurant_status(self,key,value):
		restaurants = self.dbconnection.get_collection("Restaurants")
		return find_doc(restaurants,key,value)

	def display_bills(self):
		bills = self.dbconnection.get_collection("Bills")
		return JsonResponse(find_doc(bills),safe=False)

	def assign_delv(self):
		delv_exe = self.dbconnection.get_collection("DeliveryExe")
		delv_list =  find_doc(delv_exe)
		avail_list = []
		for delv in delv_list:
			if delv["availability"] == True:
				avail_list.append(delv)

		if len(avail_list) == 0:
			return [False,]
		else:
			delv = random.choice(avail_list)
			update_doc(delv_exe,"_id",delv["_id"])
			return [True,delv["name"]]




