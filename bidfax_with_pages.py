from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = Driver(uc=True)
url = 'https://en.bidfax.info/bmw/335/f/from-year=2013/to-year=2018/'
driver.uc_open_with_reconnect(url, 30)
driver.uc_gui_click_captcha()

time.sleep(10)

df = pd.DataFrame(columns=['Name', 'Price', 'Auction Type', 'Date of Sale', 'Condition', 
                           'Mileage', 'Seller', 'Documents', 'Location', 'Primary Damage', 
                           'Secondary Damage', 'Transmission', 'Keys', 'Link'])
dict_list = []
print(driver)


WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'thumbnail')))
car_listings = driver.find_elements(By.CLASS_NAME, 'thumbnail')
# Loop through each car listing and extract relevant information
print(f"Cars found: {len(car_listings)}")


# Max page: 99
for car in car_listings:
    
    print(car)
    
    if car.find_elements(By.TAG_NAME, 'ins'):
        print("Ad element found, skipping")
        continue
    
    print("Actual car, gathering information")   
        
    name = car.find_element(By.TAG_NAME, 'h1').text
    price = car.find_element(By.CLASS_NAME, 'prices').text
    auction_type = car.find_elements(By.XPATH, ".//p[contains(text(), 'Auction')]/span")[0].text
    sale_date = car.find_elements(By.XPATH, ".//p[contains(text(), 'Date of sale')]/span").text
    condition = car.find_element(By.XPATH, ".//p[contains(text(),'Condition')]/span").text
    mileage = car.find_element(By.XPATH, ".//p[contains(text(),'Mileage')]/span").text
    seller = car.find_element(By.XPATH, ".//p[contains(text(),'Seller')]/span").text
    documents = car.find_element(By.XPATH, ".//p[contains(text(),'Documents')]/span").text
    location = car.find_elements(By.XPATH, ".//p[contains(text(), 'Auction')]/span")[-1].text
    primary_damage = car.find_element(By.XPATH, ".//p[contains(text(),'Primary Damage')]/span").text
    secondary_damage = car.find_element(By.XPATH, ".//p[contains(text(),'Secondary Damage')]/span").text
    transmission = car.find_element(By.XPATH, ".//p[contains(text(),'Transmission')]/span").text
    keys = car.find_element(By.XPATH, ".//p[contains(text(),'Keys')]/span").text
    link = car.find_element(By.XPATH, ".//div[@class='caption']/a").get_attribute('href')
    
    print('Information gathered successfully, appending DataFrame')
    
    new_row = {'Name': name, 'Price': price, 'Auction Type': auction_type, 'Date of Sale': sale_date, 
               'Condition': condition, 'Mileage': mileage, 'Seller': seller, 'Documents': documents,
               'Location': location, 'Primary Damage': primary_damage, 'Secondary Damage': secondary_damage,
                'Transmission': transmission, 'Keys': keys, 'Link': link}
    dict_list.append(new_row)
    
    print("Information has been appended into DataFrame")        

df = pd.DataFrame.from_dict(dict_list)

print('Full page was parsed')
df.to_csv('bidfax.csv', index=False)
print("Data has been saved to 'bidfax.csv'")
if len(driver.window_handles) > 0:
    driver.close()
    driver.quit()

