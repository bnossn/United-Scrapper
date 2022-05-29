# https://www.youtube.com/watch?v=YKennHXZyJU&ab_channel=Codifike
from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from traceback import format_exc

from csv import DictReader
from csv import DictWriter

import datetime
import time
import requests
import smtplib
import email.message
from bs4 import BeautifulSoup


def check_float(potential_float):
    try:
        float(potential_float)

        return True
    except ValueError:
        return False

def remove_price_duplicates(list_of_elements):
	# Let's filter out all prices that are duplicate
	list_prices = []
	list_unique_elements = []
	for elem in list_of_elements:
		next_price = elem.find_element(by=By.TAG_NAME, value='span').get_attribute("innerHTML")[1:]
		next_price = next_price.replace(',','')

		if check_float(next_price):
			next_price = float(next_price)
			
			if not next_price in list_prices:
				list_prices.append(next_price)
				list_unique_elements.append(elem)
	return list_unique_elements
	# /Let's filter out all prices that are duplicate

def find_element_with_lowest_cost(list_of_elements):
	# Find lowest cost!
	list_prices = []

	for elem in list_of_elements:
		price = elem.find_element(by=By.TAG_NAME, value='span').get_attribute("innerHTML")[1:]
		price = price.replace(',','')

		if check_float(price):
			list_prices.append(float(price))
		
	list_prices.sort()
	lowest_price = list_prices[0]

	for elem in list_of_elements:
		price_to_check = elem.find_element(by=By.TAG_NAME, value='span').get_attribute("innerHTML")[1:]
		price_to_check = price_to_check.replace(',','')
		price_to_check = float(price_to_check)
		
		if 	lowest_price == price_to_check:
			element_with_lowest_cost = elem

	return element_with_lowest_cost
	# /Find lowest cost!

def find_parent_by_tag(element, parent_tag):
	local_element = element

	while not local_element.tag_name == parent_tag:
		local_element = local_element.find_element(by=By.XPATH, value="..")
	
	return local_element

def find_lowest_cost_button(driver):
	# Wait for element to appear
	element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'app-components-Shopping-PriceCard-styles__priceValue--21Ki_')))

	list_of_elements =	driver.find_elements(by=By.CLASS_NAME, value='app-components-Shopping-PriceCard-styles__priceValue--21Ki_')
	
	list_unique_elements = remove_price_duplicates(list_of_elements)
	element_with_lowest_cost = find_element_with_lowest_cost(list_unique_elements)

	# \/ get the price to return it along with the button
	price = element_with_lowest_cost.find_element(by=By.TAG_NAME, value='span').get_attribute("innerHTML")[1:]
	price = price.replace(',','')
	price = float(price)
	# /\ get the price to return it along with the button		

	button_with_lowest_cost:WebElement = find_parent_by_tag(element_with_lowest_cost, 'button')

	return button_with_lowest_cost, price

def find_economy_button(driver):
	
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'atm-c-modal__content')))
		economy_buttons = driver.find_elements(by=By.XPATH, value="//*[contains(text(), 'Economy from')]")

		economy_button = economy_buttons[1]
		economy_button:WebElement = find_parent_by_tag(economy_button, 'button')

		return economy_button
	except:
		return False

def flights_found(driver):
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'app-components-Shopping-NoFlights-styles__noFlightWrapper--1CKJd')))

		return False
	except:
		return True

def airports_found(driver):
	try:
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='atm-c-alert atm-c-alert--error']")))

		return False
	except:
		return True

def get_time():
	e = datetime.datetime.now()
	return "%s" % e

def get_last_recorded_trip():
	with open('OutputFile.csv', 'r') as read_obj_pers:
		# pass the file object to DictReader() to get the DictReader object
		dict_reader_pers = DictReader(read_obj_pers)
		# iterate over each line as a ordered dictionary
		last_record = ''
		for row in dict_reader_pers:
			# row variable is a dictionary that represents a row in csv
			last_record = row
		
		read_obj_pers.close()
		return last_record

# URL = "https://www.united.com/en/us/fsr/choose-flights?itip=GRU_ORD_2022-08-03*ORD_MCO_2023-01-10&sc=7%2C7&st=bestmatches&cbm=-1&cbm2=-1&ft=0&cp=0&tt=2&ct=0&px=1&taxng=1&clm=7&EditSearchCartId=01C1239E-4C3C-4641-AC4A-B88535E835BD"

# URL = "https://www.united.com/en/us/fsr/choose-flights?tt=2&st=bestmatches&clm=7&cbm2=-1&taxng=1&px=1&cp=0&EditSearchCartId=01C1239E-4C3C-4641-AC4A-B88535E835BD&ft=0&cbm=-1&sc=7%2C7&ct=0&itip=GRU_AOO_2022-08-03*ORD_MCO_2023-01-10&idx=1"

FIRST_TRIP_FROM = 'GRU'
FIRST_TRIP_TO = 'DTW'

MAX_NUMBER_OF_NOT_FOUND = 50

def main():
	try:
		driver=webdriver.Chrome()
		driver.maximize_window()
		actions = ActionChains(driver)
		ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)

		# \/ open file in read mode to run the program
		read_obj_from = open('AirportsDataset.csv', 'r')
		dict_reader_from = DictReader(read_obj_from)
		read_obj_to = open('AirportsDataset.csv', 'r')
		dict_reader_to = DictReader(read_obj_to)
		last_from = ''
		last_to = ''
		# /\ open file in read mode to run the program

		# \/ Open your CSV output file in append mode
		field_names = ['Record Time','1st trip from','1st trip to','1st trip cost','2nd trip from','2nd trip to', '2nd trip cost', 'total cost']
		write_output_file = open('OutputFile.csv', 'a');
		dictwriter_object = DictWriter(write_output_file, fieldnames=field_names)
		# /\ Open your CSV output file in append mode


		# \/ Persistent data -> Read last record from CSV
		last_recorded_trip = get_last_recorded_trip()
		from_airport_pers = ''
		to_airport_pers = ''
		if last_recorded_trip:
			from_airport_pers = last_recorded_trip['2nd trip from']
			to_airport_pers= last_recorded_trip['2nd trip to']
		first_from_airport_of_list_found = False
		first_to_airport_of_list_found = False
		# /\ Persistent data -> Read last record from CSV


		# \/ DATA: Count number of not found - only from beginning of list
		count_errors = False
		number_of_errors = 0
		# /\ DATA: Count number of not found - only from beginning of list


		print('last from airport ' + from_airport_pers)
		print('last to airport ' + to_airport_pers)

		for from_airport in dict_reader_from:

			# Read 'from' persistent 
			if from_airport_pers and not first_from_airport_of_list_found:
				if (from_airport_pers != from_airport['local_code']):
					continue
				else:
					first_from_airport_of_list_found = True
			# /\ Read 'from' persistent 

			for to_airport in dict_reader_to:

				# \/ Count number of not founds - only from beginning of list
				if to_airport['local_code'] == 'ABQ' or to_airport['local_code'] == 'ADW':
					count_errors = True
					number_of_errors = 0
				# /\ Count number of not founds - only from beginning of list

				# Read 'to' persistent 
				if to_airport_pers and not first_to_airport_of_list_found:
					if (to_airport_pers != to_airport['local_code']):
						continue
					else:
						first_to_airport_of_list_found = True
				# /\ Read 'to' persistent 

				if from_airport['id'] != to_airport['id']:
					last_from = from_airport
					last_to = to_airport

					print('airport: ' + from_airport['local_code'] + '/' + to_airport['local_code'] )

					URL = f"https://www.united.com/en/us/fsr/choose-flights?itip={FIRST_TRIP_FROM}_{FIRST_TRIP_TO}_2022-08-03*{from_airport['local_code']}_{to_airport['local_code']}_2023-01-10&sc=7%2C7&st=bestmatches&cbm=-1&cbm2=-1&ft=0&cp=0&tt=2&ct=0&px=1&taxng=1&clm=7&EditSearchCartId=01C1239E-4C3C-4641-AC4A-B88535E835BD"

					driver.get(URL)

					# The order of the terms of the 'if' below impacts the performance
					if airports_found(driver) and flights_found(driver):

						# \/ Page 1
						button_with_lowest_cost, first_trip_cost = find_lowest_cost_button(driver)
						actions.move_to_element(button_with_lowest_cost).perform();
						button_with_lowest_cost.click()

						print('passed page 1')

						# Check if it opened the pop up or a new page for #Page 1
						economy_button = find_economy_button(driver)
						if economy_button:
							actions.move_to_element(economy_button).perform()
							economy_button.click()

						print('passed economy page 1')
						# /\ Page 1


						# \/ Page 2
						button_with_lowest_cost, second_trip_cost = find_lowest_cost_button(driver)
						actions.move_to_element(button_with_lowest_cost).perform()
						button_with_lowest_cost.click()

						print('passed page 2')

						# Check if it opened the pop up or a new page for #Page 2
						economy_button = find_economy_button(driver)
						if economy_button:
							actions.move_to_element(economy_button).perform()
							economy_button.click()

						print('passed economy page 2')
						# /\ Page 2


						# \/ Gets the total price 

						total_price_class_name = 'app-components-VerticalShoppingCart-styles__divRight--G9dbq app-components-VerticalShoppingCart-styles__divRightWithOldPrice--1k5bf'

						# Wait until the total price is visible
						WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, f"//div[@class='{total_price_class_name}']")))

						price_elements = driver.find_elements(by=By.XPATH, value=f"//div[@class='{total_price_class_name}']")
						
						price_element:WebElement = price_elements[2]
						total_price = price_element.text

						print(total_price)
						# /\ Gets the total price 

						output_dict = {'Record Time': get_time(),'1st trip from':FIRST_TRIP_FROM,'1st trip to': FIRST_TRIP_TO,'1st trip cost': first_trip_cost,'2nd trip from': from_airport['local_code'],'2nd trip to': to_airport['local_code'], '2nd trip cost': second_trip_cost, 'total cost': total_price}
						dictwriter_object.writerow(output_dict)

						print('Total Price Succesfully Recorded')
						if count_errors: count_errors = False
					else:
						print('airports or flights not found!')

						# \/ Count number of not founds - only from beginning of list
						if count_errors: 
							number_of_errors += 1
							print('Number of sequential errors: ' + str(number_of_errors))
							if number_of_errors > MAX_NUMBER_OF_NOT_FOUND:
								break
						# /\ Count number of not founds - only from beginning of list

						output_dict = {'Record Time': get_time(),'1st trip from':FIRST_TRIP_FROM,'1st trip to': FIRST_TRIP_TO,'1st trip cost':'none','2nd trip from': from_airport['local_code'],'2nd trip to': to_airport['local_code'], '2nd trip cost': 'none', 'total cost': 'flights/airport not found'}
						dictwriter_object.writerow(output_dict)
					
			# \/ Renew the 'to' iterator when necessary
			read_obj_to.seek(0)
			next(dict_reader_to)
			# /\ Renew the 'to' iterator when necessary

		while True:
			print('reached the end')
			time.sleep(120)
			
	except Exception as e: # work on python 3.x
		print('error: '+ repr(e))
		print('Traceback: '+ format_exc())
		print('airport: ' + last_from['local_code'] + '/' + last_to['local_code'] )
	finally:
		read_obj_from.close()
		read_obj_to.close()
		write_output_file.close()
		driver.quit()


if __name__ == '__main__':
    main()

# Google -> "my browser agent"
# headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

# site = requests.get(URL, headers=headers)

# soup = BeautifulSoup(site.content, 'html.parser')

# title = soup.find('div', class_ = 'app-components-Shopping-PriceCard-styles__priceValue--21Ki_').getText().strip()

# print(title)


# title = soup.find('h1', class_ = 'col-12 name no-medium').getText().strip()
# price = soup.find('strong', class_ = 'sale-price')
# price = price.contents[1].getText().strip()

# num_price = price[3:]
# num_price = num_price.replace('.','')
# num_price = num_price.replace(',','.')
# num_price = float(num_price)

# def send_email():
# 	email_content = "https://www.brasiltronic.com.br/kit-camera-sony-alpha-a6600-com-lente-sony-e-pz-18-105mm-f-4-g-oss-p1328183"
# 	msg = email.message.Message()
# 	msg['Subject'] = "Preço Camera Sony BAIXOU!!!"
# 	msg['From'] = 'meuemail@gmail.com'
# 	msg['To'] = 'meuemail@gmail.com'
# 	password = 'meupassword'
# 	msg.add_header('Content-Type', 'text/html')
# 	msg.set_payload(email_content)

# 	s = smtplib.SMTP('smtp.gmail.com : 587')
# 	s.startls()
# 	s.login(msg['From'], password)
# 	s.sendmail(msg['From'], [msg['To']], msg.as_string())


# if (num_price < 15000):
# 	send_email()

