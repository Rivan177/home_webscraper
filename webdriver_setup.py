"""
This scripts sets up Selenium to access a website and scrapes the listings of properties available for sale 
in the state of Morelos, Mexico. It then writes a csv file with the obtained information. 
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv

## Functions 
## To obtain a list of elements
def page_elements(xpath: str):
    """
    This funtion return a list of all the elements with argument xpath as string
    """
    elements = driver.find_elements(By.XPATH, value=xpath)
    return elements

## To obtain a single of element
def page_element(xpath: str):
    """
    This funtion returns an element in the argument's xpath
    """
    elements = driver.find_element(By.XPATH, value=xpath)
    return elements

## To go to the next page
def click_next_page(xpath: str):
    """
    This funciton finds the next page button in xpath and click on it
    """
    next_page = page_element(xpath)
    next_page.click()
    sleep(10)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_characteristics)))


## Popular website in Mexico to find properties 
url = 'https://www.inmuebles24.com'
## Inputs for property type and location
property_type = 'Casa'
location_input = 'Morelos'

## XPaths for navigating landing page
## Button to click on "Comprar", On Sale properties
xpath_property_button = '//button[@value="1"]'
## Selection list for properties
xpath_list_property_type = '//select[@id="propertyType"]'
## Input desired location
xpath_location_text_box = '//input[@aria-label="Buscá por ubicación o palabra clave"]'
## List of sugestions
xpath_list_sugestions = '//mark[@class="rbt-highlight-text"]'
## Search button
xpath_search_button = '//button[@data-qa="search-button"]'
## Next page button
xpath_next_page = '//a[contains(@class, "gzANxl")]'

## XPATHS for retreving information
xpath_total_listings = '//h1[contains(@class, "postingsTitle")]'
xpath_price = '//div[contains(@class, "components__Price-")]'
xpath_characteristics = '//div[contains(@class, "PostingMain")]'
xpath_location = '//div[contains(@class, "LocationLocation")]'

## Specific path is not needed since chromedriver is in the same directory
#path = 'D:\data_eng\home_webscraper'

## Start webdirver with Chrome
option = webdriver.ChromeOptions()
## Removes navigation.webdriver flag 
option.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=option)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.get(url)

## Wait for page to load, checking for property button present
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_property_button)))

## Click on "Comprar"
property_button = page_element(xpath_property_button)
property_button.click()

## Selecting "Casa" from property list
type_property_list = page_element(xpath_list_property_type)
select_property = Select(type_property_list)
select_property.select_by_visible_text(property_type)

## Input "Morelos" as location
location_search_box = page_element(xpath_location_text_box)
location_search_box.click()
sleep(3)
location_search_box.send_keys(location_input)
## Wait for autosuggestion list to appear
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_list_sugestions)))

## Click on first item in location suggestions
location_select = page_element(xpath_list_sugestions)
location_select.click()

# Click on "Buscar", search button
search_button = page_element(xpath_search_button)
search_button.click()

## Allow time for resutls to load
sleep(10)
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_characteristics)))

## Skip page 1 to avoid adds
# click_next_page(xpath_next_page)
# sleep(10)
# WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_characteristics)))


"""
Start scraping information about houses
"""
## Get total number of listings
total_string = page_element(xpath_total_listings).text
total_string = total_string[:6].replace(',', '')
total_pages = round(int(total_string) / 20)

print(f'This script will scrape {total_pages} pages, expecting {int(total_string) - 5} reults')

## Testing code to get a single element   
# price1 = page_results[1].find_element(By.CLASS_NAME, "price").text
# print(f'Second home element{page_results[1]}')
# print(f'Second home price {price1}')


with open('ind_home.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    page = 1

    while page < total_pages+1:
        print(f'Scrapping page {page}...')
        print(f'{total_pages - page} pages pending to scrape')

        price_values = page_elements(xpath_price)
        characteristics_values = page_elements(xpath_characteristics)
        location_values = page_elements(xpath_location)

        for price, characteritics, location in zip(price_values, characteristics_values, location_values):
            temp_list = [price.text, characteritics.text, location.text]
            writer.writerow(temp_list)
            sleep(0.1)

        click_next_page(xpath_next_page)
        page += 1

# def get_item_by_class(page_results, value):
#     '''
#     This funtions gets the text from determinated instances using the class
#     '''
#     info_list = list()
#     for result in page_results:
#         try:
#             item = result.find_element(By.CLASS_NAME, value).getText()
#             info_list.append(item)
#         except:
#             info_list.append('Null')
#     print(info_list)
#     return info_list

# get_item_by_class(page_results, "price")

### Work in progress, add checks for elements, add function to handle nulls. add function to page through based on the total results. 

driver.quit()