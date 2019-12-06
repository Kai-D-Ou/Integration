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

chrome_options = Options()
#accept any prompts by default
chrome_options.set_capability('unhandledPromptBehavior', 'accept')
#accept any notification requests by default
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
#set browser to headless
#chrome_options.headless = True
#set the options to chrome_options
browser = webdriver.Chrome(options = chrome_options)
#browser.maximize_window()
browser.get('https://partner.swiggy.com/')



####DECLARING ELEMENT PATH VARIABLES####
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


####USEFUL GLOBAL VARIABLES####



#saves swiggy cookies
def save_swiggy_cookies():
	time.sleep(100)
	pickle.dump( browser.get_cookies() , open("Swiggy_cookies.pkl","wb"))
	print('cookies saved successfully')
	print(browser.get_cookies())



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
	except:
		print('error loading cookies')
	#redirect to zomato dashboard
	finally:
		print('cookies added succesfully')
		browser.get(swiggy_dashboard_url)

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
		except:
			print('no cancelled orders present')
			return len(newOrdersList)
	except:
		print('Error occured while fetching number of new orders')

def swiggy_confirm_order():
	try:
		time.sleep(4.0)
		acceptOrderButton = browser.find_element_by_xpath(swiggy_accept_order_button_path).click()
#			browser.execute_script("arguments[0].click();", acceptOrderButton)
		print('order accepted successfully \n')
	except:
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
		except:
			print('Error occured while fetching item name')
#		item category
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/p[1]
		try:
			itemCategory = itemsList[i].find_element_by_xpath('.//div/div/div/div/div/div[2]/p[1]').get_attribute('textContent').strip()
			print(itemCategory)
		except:
			print('Error occured while fetching item category')
#		item price
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/p[2]
		try:
			itemPrice = itemsList[i].find_element_by_xpath('.//div/div/div/div/div/div[2]/p[2]').get_attribute('innerHTML').replace('₹','').strip()
			print(itemPrice)
		except:
			print('Error occured while fetching item price')
#		item quantity
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div/div/span/span
		try:
			itemQuantity = itemsList[i].find_element_by_xpath('.//div/div/span/span').get_attribute('innerHTML')
			print('X ', itemQuantity)
		except:
			print('Error occured while fetching item quantity')
		try:
			swiggy_new_dish(order_Id, itemQuantity, itemName, itemPrice)
		except:
			print('Error while placing new order')
	swiggy_confirm_order()


def swiggy_fetch_order_details():
	try:
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/h3/span[1]
		orderId = browser.find_element_by_xpath(swiggy_new_order_id_path).get_attribute('innerHTML').replace('#','')
		print(orderId)
	except:
		print('Error occured while fetching new order id')
	try:
		grandTotal = browser.find_element_by_xpath(swiggy_grand_total_path).get_attribute('innerHTML').replace('for ₹','').strip()
		grandTotal = float(grandTotal)/1.05
		print('Grand Total: ', grandTotal)
	except:
		print('Error occured while fetching grand total')
	try:
#		/html/body/div/div[8]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div
		orderedItems = browser.find_elements_by_xpath(swiggy_ordered_items_list_path)
		swiggy_fetch_items(orderedItems, swiggy_new_order(grandTotal))
	except:
		print('Error occured while fetching ordered itmes')
	try:
		swiggy_new_order_notification()
	except:
		print('Error while sending new order notification')

#print innerHTML of the orderDetailsDisplay and call got_swiggy_new_order()
def swiggy_check_for_new_order():
	try:
		noNewOrders = browser.find_element_by_xpath(swiggy_no_orders_container).get_attribute('textContent')
	except:
		try:
			acceptClickable = WebDriverWait(browser, 5).until(
					EC.element_to_be_clickable((By.XPATH, swiggy_accept_order_button_path))
				)
			swiggy_fetch_order_details()
		except:	
			print('Error while accepting order')
	threading.Timer(1.0, swiggy_check_for_new_order).start()


load_swiggy_cookies()
swiggy_switch_on_orders()
swiggy_check_for_new_order()