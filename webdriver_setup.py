"""
This scripts sets up Selenium to access a website and brings up the listings of properties available for sale 
in the state of Morelos, Mexico
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

## Popular website in Mexico to find properties 
url = 'https://www.inmuebles24.com'
property_type = 'Casa'
location = 'Mor'

## Specific path is not needed since chromedriver is in the same directory
#path = 'D:\data_eng\home_webscraper'

## Start webdirver with Chrome
option = webdriver.ChromeOptions()
## Removes navigation.webdriver flag 
option.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=option)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get(url)

## XPaths for navigating landing page
## Button to click on "Comprar", On Sale properties
xpath_property_button = '//button[@value="1"]'
## Selection list for properties
xpath_list_type_property = '//select[@id="propertyType"]'
## Input desired location
xpath_location_text_box = '//input[@aria-label="Buscá por ubicación o palabra clave"]'
## List of sugestions
xpath_list_sugestions = '//mark[@class="rbt-highlight-text"]'
## Search button
xpath_search_button = '//button[@data-qa="search-button"]'

## Click on "Comprar"
property_button = driver.find_element(By.XPATH, value=xpath_property_button).click()

## Selecting "Casa" from property list
type_property_list = driver.find_element(By.XPATH, value=xpath_list_type_property)
select_property = Select(type_property_list)
select_property.select_by_visible_text(property_type)

## Input "Morelos" as location
location_search_box = driver.find_element(By.XPATH, value=xpath_location_text_box)
location_search_box.click()
time.sleep(3)
location_search_box.send_keys(location)
wait = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_list_sugestions)))

## Click on selected location
location_select = driver.find_element(By.XPATH, xpath_list_sugestions).click()

# Click on "Buscar"
search_button = driver.find_element_by_xpath(xpath_search_button).click()


time.sleep(10)
