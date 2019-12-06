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
browser.get('https://www.zomato.com/hyderabad')


####DECLARING ELEMENT PATH VARIABLES####
zomato_dashboard_url = 'https://www.zomato.com/clients/merchant_order_dashboard.php'
zomato_order_confirmation_display_path = '/html/body/div[5]'
zomato_order_id_path = '/html/body/div[5]/div[1]/div/div[2]'
zomato_restaurant_name_path = '/html/body/div[5]/div[1]/div/div[3]'
zomato_cash_collection_path = '/html/body/div[5]/div[1]/div/div[4]/div'
zomato_totals_path = '/html/body/div[5]/div[2]/div[3]/div[2]/ul[2]/li'
zomato_ordered_items_list_path = '/html/body/div[5]/div[2]/div[3]/div[2]/ul[1]/li'
zomato_accept_order_button_path = '/html/body/div[5]/div[3]/div/button[1]'
zomato_confirm_preperation_time = '/html/body/div[7]/div[2]/div/button'

####USEFUL GLOBAL VARIABLES####



#saves zomato cookies
def save_zomato_cookies():
	time.sleep(100)
	pickle.dump( browser.get_cookies() , open("Zomato_cookies.pkl","wb"))
	print('cookies saved successfully')
	print(browser.get_cookies())
save_zomato_cookies()

'''
#load cookies to the browser
def load_zomato_cookies:
	try:
		cookies = pickle.load(open("Zomato_cookies.pkl", "rb"))
		for cookie in cookies:
			if 'expiry' in cookie:
				cookie['expiry'] = int(cookie['expiry'])
				#print(cookie['expiry'])
			browser.add_cookie(cookie)
		browser.refresh()
	#print 'error' if there is an error
	except:
		print('error loading cookies')
		save_zomato_cookies()
	#redirect to zomato dashboard
	finally:
		print('cookies added succesfully')
		browser.get(zomato_dashboard_url)


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
	actions = ActionChains(browser)
	actions.key_down(Keys.CONTROL)
	actions.key_down(Keys.TAB)
	actions.key_up(Keys.TAB)
	actions.key_up(Keys.CONTROL).perform()
	if browser.find_element_by_xpath(zomato_order_confirmation_display_path).value_of_css_property('display') == 'block':
		try:
			order_Id = int(browser.find_element_by_xpath(zomato_order_id_path).get_attribute('textContent').replace('Order ID:', '').strip())
			print(order_Id)
		except:
			print('no order_Id element')
			
		try:
			restaurantName = browser.find_element_by_xpath(zomato_restaurant_name_path).get_attribute('innerHTML')
			print(restaurantName)
		except:
			print('no restaurantName element')
			
		try:
			cashCollection = browser.find_element_by_xpath(zomato_cash_collection_path).get_attribute('innerHTML')
			print(cashCollection)
		except:
			print('no cashCollection element')
		try:
			totals = browser.find_elements_by_xpath(zomato_totals_path)
			lengthTotals = len(totals)
			print('totals length: ', lengthTotals)
			grandTotalElement = totals[lengthTotals-3].find_element_by_xpath('.//span[2]')
			orderGrandTotal = float(grandTotalElement.get_attribute('innerHTML').replace('₹',''))/1.05
			print(orderGrandTotal)
		except:
			print('no orderGrandTotal element')
		try:
			orderedItems = browser.find_elements_by_xpath(zomato_ordered_items_list_path)
		except:
			print('no orderedItems element')
		try:
			#CREATE A NEW ORDER IN RESTOBELL AND RETURN order_Id
			order_Id = zomato_new_order(orderGrandTotal)
		except:
			print('error while placing new order')
		try:
			#ADD NEW DISH IN RESTOBELL
			zomato_fetch_items(orderedItems, order_Id)
		except:
			print('error while adding new dishes')
		try:
			zomato_new_order_notification()
		except:
			print('error sending new order notification')
		try:
			time.sleep(4.0)
			acceptOrderButton = browser.find_element_by_xpath(zomato_accept_order_button_path)
			browser.execute_script("arguments[0].click();", acceptOrderButton)
			print('accepted order')
		except:
			print('accept button not found')
		
		try:
			time.sleep(2.0)
			confirm = browser.find_element_by_xpath(zomato_confirm_preperation_time).click()
			print('preperation time set')
		except:
			print('confirm buttom not found')
	try:
		threading.Timer(1.0, zomato_check_for_new_order).start()
	except StaleElementReferenceException as e:
		print(e)
		time.sleep(5.0)
		zomato_check_for_new_order()
		


load_zomato_cookies()
zomato_check_for_new_order()
'''