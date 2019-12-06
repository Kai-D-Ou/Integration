from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC	
from selenium.common.exceptions import StaleElementReferenceException

import threading
import pickle
import time
import json
import requests


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


chrome_options = Options()
#accept any prompts by default
chrome_options.set_capability('unhandledPromptBehavior', 'accept')
#accept any notification requests by default
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs", prefs)
#set browser to headless
#chrome_options.headless = True
#set the options to chrome_options
browser = webdriver.Chrome(options = chrome_options)
#browser.maximize_window()
browser.get('https://partner.swiggy.com/')

database = 0

def fetch_database():
	# Fetch the service account key JSON file contents
	cred = credentials.Certificate('E:/My_Fun_Projects/Python/SwiggyZomatoIntegration-t18.json')

	# Initialize the app with a service account, granting admin privileges
	firebase_admin.initialize_app(cred, {
	    'databaseURL': 'https://swiggyzomatointegration-e489e.firebaseio.com'
	})

	# As an admin, the app has access to read and write all data, regradless of Security Rules
	ref = db.reference('paths')
	return ref

####---------------------------DECLARING ELEMENT PATH VARIABLES----------------------------####
####----------------------DECLARING SWIGGY ELEMENT PATH VARIABLES------------------------####
swiggy_dashboard_url = 'https://partner.swiggy.com/orders'
swiggy_order_settings_page = 'https://partner.swiggy.com/settings/orders'
swiggy_show_orders_toggle = '/html/body/div/div[8]/div[2]/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div'

swiggy_no_orders_container = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div/div/div/h2'

swiggy_new_order_id_path = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/h3/span[1]'
swiggy_new_orders_list = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/div'
swiggy_restaurant_name_path = ''
swiggy_cash_collection_path = ''
swiggy_totals_path = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div[4]/div/div'
swiggy_grand_total_path = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/p/span/span'
swiggy_ordered_items_list_path = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div'
swiggy_accept_order_button_path = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div[2]'
swiggy_confirm_preperation_time = ''

swiggy_previous_order_id_path = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/div[1]/h3/span[1]'
swiggy_cancelled_orders_info = '/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/div[1]'
swiggy_preparing_orders_number = '/html/body/div/div[8]/div[2]/div/div/div[1]/div/div/ul/li[3]/a/span[3]'
swiggy_ready_orders_number = '/html/body/div/div[8]/div[2]/div/div/div[1]/div/div/ul/li[1]/a/span[2]'
swiggy_past_orders_number = '/html/body/div/div[8]/div[2]/div/div/div[1]/div/div/ul/li[7]/a/span[3]'

####----------------------DECLARING ZOMATO ELEMENT PATH VARIABLES------------------------####
zomato_dashboard_url = 'https://www.zomato.com/clients/merchant_order_dashboard.php'
zomato_cookie_check = '/html/body/div[4]/div/div[1]/header/div[1]/div/div[2]/a[3]/span'
zomato_order_confirmation_display_path = '/html/body/div[5]'
zomato_order_id_path = '/html/body/div[5]/div[1]/div/div[2]'
zomato_restaurant_name_path = '/html/body/div[5]/div[1]/div/div[3]'
zomato_cash_collection_path = '/html/body/div[5]/div[1]/div/div[4]/div'
zomato_totals_path = '/html/body/div[5]/div[2]/div[3]/div[2]/ul[2]/li'
zomato_ordered_items_list_path = '/html/body/div[5]/div[2]/div[3]/div[2]/ul[1]/li'
zomato_accept_order_button_path = '/html/body/div[5]/div[3]/div/button[1]'
zomato_confirm_preperation_time = '/html/body/div[7]/div[2]/div/button'


def get_swiggy_paths(): 
	swiggy_paths = database.get()["swiggy"]
	swiggy_dashboard_url = swiggy_paths["swiggy_dashboard_url"]
	swiggy_order_settings_page = swiggy_paths["swiggy_order_settings_page"]
	swiggy_show_orders_toggle = swiggy_paths["swiggy_show_orders_toggle"]

	swiggy_no_orders_container = swiggy_paths["swiggy_no_orders_container"]

	swiggy_new_order_id_path = swiggy_paths["swiggy_new_order_id_path"]
	swiggy_new_orders_list = swiggy_paths["swiggy_new_orders_list"]
	swiggy_restaurant_name_path = ''
	swiggy_cash_collection_path = ''
	swiggy_totals_path = swiggy_paths["swiggy_totals_path"]
	swiggy_grand_total_path = swiggy_paths["swiggy_grand_total_path"]
	swiggy_ordered_items_list_path = swiggy_paths["swiggy_ordered_items_list_path"]
	swiggy_accept_order_button_path = swiggy_paths["swiggy_accept_order_button_path"]
	swiggy_confirm_preperation_time = ''

	swiggy_previous_order_id_path = swiggy_paths["swiggy_previous_order_id_path"]
	swiggy_cancelled_orders_info = swiggy_paths["swiggy_cancelled_orders_info"]
	swiggy_preparing_orders_number = swiggy_paths["swiggy_preparing_orders_number"]
	swiggy_ready_orders_number = swiggy_paths["swiggy_ready_orders_number"]
	swiggy_past_orders_number = swiggy_paths["swiggy_past_orders_number"]

####----------------------DECLARING ZOMATO ELEMENT PATH VARIABLES-----------------------####
def get_zomato_paths():
	zomato_paths = database.get()["zomato"]
	zomato_dashboard_url = zomato_paths["zomato_dashboard_url"]
	zomato_cookie_check = zomato_paths["zomato_cookie_check"]
	zomato_order_confirmation_display_path = zomato_paths["zomato_order_confirmation_display_path"]
	zomato_order_id_path = zomato_paths["zomato_order_id_path"]
	zomato_restaurant_name_path = zomato_paths["zomato_restaurant_name_path"]
	zomato_cash_collection_path = zomato_paths["zomato_cash_collection_path"]
	zomato_totals_path = zomato_paths["zomato_totals_path"]
	zomato_ordered_items_list_path = zomato_paths["zomato_ordered_items_list_path"]
	zomato_accept_order_button_path = zomato_paths["zomato_accept_order_button_path"]
	zomato_confirm_preperation_time = zomato_paths["zomato_confirm_preperation_time"]
	zomato_logged_out_text_path = zomato_paths["zomato_logged_out_text_path"]

######------------------COUNT-----------------------------#########
count=0

#saves swiggy cookies
def save_swiggy_cookies():
	time.sleep(100)
	pickle.dump( browser.get_cookies() , open("Swiggy_cookies.pkl","wb"))
	print(browser.get_cookies())
	print('Sswiggy cookies saved successfully')



#load cookies to the browser
def load_swiggy_cookies():
	try:
		cookies = pickle.load(open("Swiggy_cookies.pkl", "rb"))
		for cookie in cookies:
			if 'expiry' in cookie:
				cookie['expiry'] = int(cookie['expiry'])
				#print(cookie['expiry'])
			browser.add_cookie(cookie)
		browser.refresh()
	#print 'error' if there is an error
	except Exception as e:
		print(repr(e))
		print('Error loading swiggy cookies')
	#redirect to zomato dashboard
	finally:
		print('Swiggy cookies added succesfully')
		browser.get(swiggy_dashboard_url)

#saves zomato cookies
def save_zomato_cookies():
	time.sleep(100)
	pickle.dump( browser.get_cookies() , open("Zomato_cookies.pkl","wb"))
	print(browser.get_cookies())
	print('Zomato cookies saved successfully')



#load cookies to the browser
def load_zomato_cookies():
	try:
		cookies = pickle.load(open("Zomato_cookies.pkl", "rb"))
		for cookie in cookies:
			if 'expiry' in cookie:
				cookie['expiry'] = int(cookie['expiry'])
				#print(cookie['expiry'])
			browser.add_cookie(cookie)
		browser.refresh()
		browser.find_element_by_xpath(zomato_cookie_check).get_attribute('innerHTML') != 'Dashboard'
	except Exception as e:
		print(repr(e))
		print('Error loading zomato cookies')
		save_zomato_cookies()
	#redirect to zomato dashboard
	finally:
		browser.get(zomato_dashboard_url)


def new_tab():
	browser.execute_script('window.open("about:blank", "_blank");')


def change_tab(i):
	browser.switch_to.window(browser.window_handles[i])

def load_cookies():
	try:
		load_swiggy_cookies()
	except Exception as e:
		print(repr(e))
		print("Error while loading swiggy cookies")
	try:
		new_tab()
	except Exception as e:
		print(repr(e))
		print('Error while making new tab')
	try:
		change_tab(1)
		browser.get('https://www.zomato.com/hyderabad')
		load_zomato_cookies()
	except Exception as e:
		print(repr(e))
		print("Error while loading cookies")



########------------------SWIGGY----------------------------#############
#Switch on orders and open orders pages
def swiggy_switch_on_orders():
	browser.get(swiggy_order_settings_page)
	switchOnOrders = browser.find_element_by_xpath(swiggy_show_orders_toggle).click()
	browser.get(swiggy_dashboard_url)

#neworder
def swiggy_new_order(total):
	payload = {'rid':'abb42af8f780814e2fb040918d709ea9','type':'new_order','tableno':'0','waiterid':'aa3945199ce2d20b2a9f69e1075cff7b','total':'','oid':'','otype':'swiggy','ddata':''}
	payload['total'] = total
	resp = requests.post("https://restobell.com/restaurant/common.php", data=payload)
	data = resp.json()
	oid = data['oid']
	return oid
	


#newdish
def swiggy_new_dish(order_Id, quantity, dishname, unitprice):
	payload = {'rid':'abb42af8f780814e2fb040918d709ea9','type':'new_dish','orderid':'','quantity':'','dishname':'','dishid':'','dtype':'temp','price':'','note':''}
	payload['orderid'] = order_Id
	payload['quantity'] = quantity
	payload['dishname'] = dishname
	payload['price'] = unitprice
	resp = requests.post("https://restobell.com/restaurant/common.php", data=payload)
	
#notification for new order
def swiggy_new_order_notification():
	payload = {'rid':'abb42af8f780814e2fb040918d709ea9','type':'notify', 'token':''}
	resp = requests.post("https://restobell.com/restaurant/common.php", data=payload)
	

def swiggy_number_of_new_orders():
	try:
		newOrdersList = browser.find_elements_by_xpath('swiggy_new_orders_list')
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/div/div[2]/button
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/div[1]
		try:
			if(newOrdersList[1].find_element_by_xpath('.//div/div/div/div[2]/button').get_attribute('innerHTML') == 'SHOW'):
				return len(newOrdersList) - 1
			else:
				return len(newOrdersList)
		except Exception as e:
			print(repr(e))
			print('no cancelled orders present')
			return len(newOrdersList)
	except Exception as e:
		print(repr(e))
		print('Error occured while fetching number of new orders')

def swiggy_confirm_order():
	try:
		time.sleep(4.0)
		acceptOrderButton = browser.find_element_by_xpath(swiggy_accept_order_button_path).click()
#			browser.execute_script("arguments[0].click();", acceptOrderButton)
		print('order accepted successfully \n')
	except Exception as e:
		print(repr(e))
		print('Error occured while accepting the order')

def swiggy_fetch_items(itemsList, order_Id):
	print('there are ', len(itemsList), ' itmes in the order')
	for i in range(len(itemsList)):
#		item name
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/span
		try:
			itemName= itemsList[i].find_element_by_xpath('.//div/div/div/div/div/div[2]/span').get_attribute('innerHTML').replace('\'','')
			print(itemName)
		except Exception as e:
			print(repr(e))
			print('Error occured while fetching item name')
#		item category
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/p[1]
		try:
			itemCategory = itemsList[i].find_element_by_xpath('.//div/div/div/div/div/div[2]/p[1]').get_attribute('textContent').strip()
			print(itemCategory)
		except Exception as e:
			print(repr(e))
			print('Error occured while fetching item category')
#		item price
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/p[2]
		try:
			itemPrice = itemsList[i].find_element_by_xpath('.//div/div/div/div/div/div[2]/p[2]').get_attribute('innerHTML').replace('₹','').strip()
			print(itemPrice)
		except Exception as e:
			print(repr(e))
			print('Error occured while fetching item price')
#		item quantity
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/span/span
		try:
			itemQuantity = itemsList[i].find_element_by_xpath('.//div/div/span/span').get_attribute('innerHTML')
			print('X ', itemQuantity)
		except Exception as e:
			print(repr(e))
			print('Error occured while fetching item quantity')
		try:
			swiggy_new_dish(order_Id, itemQuantity, itemName, itemPrice)
		except Exception as e:
			print(repr(e))
			print('Error while placing new order')
	swiggy_confirm_order()


def swiggy_fetch_order_details():
	print('############--------------------SWIGGY ORDER----------------------################')
	try:
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/h3/span[1]
		orderId = browser.find_element_by_xpath(swiggy_new_order_id_path).get_attribute('innerHTML').replace('#','')
		print(orderId)
	except Exception as e:
		print(repr(e))
		print('Error occured while fetching new order id')
	try:
		grandTotal = browser.find_element_by_xpath(swiggy_grand_total_path).get_attribute('innerHTML').replace('for ₹','').strip()
		grandTotal = float(grandTotal)/1.05
		print('Grand Total: ', grandTotal)
	except Exception as e:
		print(repr(e))
		print('Error occured while fetching grand total')
	try:
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div
		orderedItems = browser.find_elements_by_xpath(swiggy_ordered_items_list_path)
		swiggy_fetch_items(orderedItems, swiggy_new_order(grandTotal))
	except Exception as e:
		print(repr(e))
		print('Error occured while fetching ordered itmes')
	try:
		swiggy_new_order_notification()
	except Exception as e:
		print(repr(e))
		print('Error while sending new order notification')

#print innerHTML of the orderDetailsDisplay and call got_swiggy_new_order()
def swiggy_check_for_new_order():
	try:
		noNewOrders = browser.find_element_by_xpath(swiggy_no_orders_container).get_attribute('textContent')
	except Exception as e:
		print(repr(e))
		try:
			acceptClickable = WebDriverWait(browser, 5).until(
					EC.element_to_be_clickable((By.XPATH, swiggy_accept_order_button_path))
				)
			swiggy_fetch_order_details()
		except Exception as e:
			print(repr(e))	
			print('Error while accepting order')
#	threading.Timer(1.0, swiggy_check_for_new_order).start()



######---------------------------ZOMATO-------------------------------#########

#neworder
def zomato_new_order(total):
	payload = {'rid':'abb42af8f780814e2fb040918d709ea9','type':'new_order','tableno':'0','waiterid':'aa3945199ce2d20b2a9f69e1075cff7b','total':'','oid':'','otype':'zomato','ddata':''}
	payload['total'] = total
	resp = requests.post("https://restobell.com/restaurant/common.php", data=payload)
	data = resp.json()
	oid = data['oid']
	return oid
	


#newdish
def zomato_new_dish(order_Id, quantity, dishname, unitprice):
	payload = {'rid':'abb42af8f780814e2fb040918d709ea9','type':'new_dish','orderid':'','quantity':'','dishname':'','dishid':'','dtype':'temp','price':'','note':''}
	payload['orderid'] = order_Id
	payload['quantity'] = quantity
	payload['dishname'] = dishname
	payload['price'] = unitprice
	resp = requests.post("https://restobell.com/restaurant/common.php", data=payload)
	
#notification for new order
def zomato_new_order_notification():
	payload = {'rid':'abb42af8f780814e2fb040918d709ea9','type':'notify', 'token':''}
	resp = requests.post("https://restobell.com/restaurant/common.php", data=payload)
	
	


#add items to order id in restobell
def zomato_fetch_items(list, order_Id):
	print('items = ', len(list))
	for i in range(len(list)):
		item = list[i]
		itemName = item.find_element_by_xpath('.//span').get_attribute('innerHTML').replace('\'','').strip()
		print(itemName)
		itemQuantity, seperator, itemUnitPrice = item.find_element_by_xpath('.//div[1]').get_attribute('textContent').partition('x ₹')
		print(itemQuantity.strip(), ' x ', itemUnitPrice.strip())
		itemQuantity = int(itemQuantity.strip())
		itemUnitPrice = int(itemUnitPrice.strip())
		#zomato_new_dish(id, quantity, dishname, unitprice)
		zomato_new_dish(order_Id, itemQuantity, itemName, itemUnitPrice)
		

#CHECKS IF DISPLAY PROPERTY IS 'block' AND PRINTS VARIABLES#### ##MAJOR DEPENCENCY##
def zomato_check_for_new_order():
	if browser.find_element_by_xpath(zomato_order_confirmation_display_path).value_of_css_property('display') == 'block':
		print('############--------------------ZOMATO ORDER----------------------################')
		try:
			order_Id = int(browser.find_element_by_xpath(zomato_order_id_path).get_attribute('textContent').replace('Order ID:', '').strip())
			print(order_Id)
		except Exception as e:
			print(repr(e))
			print('no order_Id element')
			
		try:
			restaurantName = browser.find_element_by_xpath(zomato_restaurant_name_path).get_attribute('innerHTML')
			print(restaurantName)
		except Exception as e:
			print(repr(e))
			print('no restaurantName element')
			
		try:
			cashCollection = browser.find_element_by_xpath(zomato_cash_collection_path).get_attribute('innerHTML')
			print(cashCollection)
		except Exception as e:
			print(repr(e))
			print('no cashCollection element')
		try:
			totals = browser.find_elements_by_xpath(zomato_totals_path)
			lengthTotals = len(totals)
			print('totals length: ', lengthTotals)
			grandTotalElement = totals[lengthTotals-3].find_element_by_xpath('.//span[2]')
			orderGrandTotal = float(grandTotalElement.get_attribute('innerHTML').replace('₹',''))/1.05
			print(orderGrandTotal)
		except Exception as e:
			print(repr(e))
			print('no orderGrandTotal element')
		try:
			orderedItems = browser.find_elements_by_xpath(zomato_ordered_items_list_path)
		except Exception as e:
			print(repr(e))
			print('no orderedItems element')
		try:
			#CREATE A NEW ORDER IN RESTOBELL AND RETURN order_Id
			order_Id = zomato_new_order(orderGrandTotal)
		except Exception as e:
			print(repr(e))
			print('error while placing new order')
		try:
			#ADD NEW DISH IN RESTOBELL
			zomato_fetch_items(orderedItems, order_Id)
		except Exception as e:
			print(repr(e))
			print('error while adding new dishes')
		try:
			zomato_new_order_notification()
		except Exception as e:
			print(repr(e))
			print('error sending new order notification')
		try:
			time.sleep(4.0)
			acceptOrderButton = browser.find_element_by_xpath(zomato_accept_order_button_path)
			browser.execute_script("arguments[0].click();", acceptOrderButton)
			print('accepted order')
		except Exception as e:
			print(repr(e))
			print('accept button not found')
		
		try:
			time.sleep(2.0)
			confirm = browser.find_element_by_xpath(zomato_confirm_preperation_time).click()
			print('preperation time set')
		except Exception as e:
			print(repr(e))
			print('confirm buttom not found')
#	threading.Timer(1.0, zomato_check_for_new_order).start()



def check_for_new_order(count):
	change_tab(count%2)
	if(count%2):
		get_zomato_paths()
		zomato_check_for_new_order()
	else: 
		get_swiggy_paths()
		swiggy_check_for_new_order()
	count = count+1
	threading.Timer(1.0, check_for_new_order,(count,)).start()

database = fetch_database()
#get_swiggy_paths()
#get_zomato_paths()
load_cookies()
change_tab(0)
try:
	swiggy_switch_on_orders()
except Exception as e:
	print(repr(e))

check_for_new_order(count)




