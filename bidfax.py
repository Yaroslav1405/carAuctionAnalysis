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

df = pd.DataFrame(columns=['Name', 'Price', 'Condition', 'Damage', 'Mileage'])
dict_list = []
print(driver)

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'thumbnail')))
car_listings = driver.find_elements(By.CLASS_NAME, 'thumbnail')
# Loop through each car listing and extract relevant information
print(f"Cars found: {len(car_listings)}")
for car in car_listings:
    
    print(car)
    
    if car.find_elements(By.TAG_NAME, 'ins'):
        print("Ad element found, skipping")
        continue
    
    print("Actual car, gathering information")   
        
    name = car.find_element(By.TAG_NAME, 'h2').text
    location = car.find_elements(By.XPATH, ".//p[contains(text(), 'Auction')]/span")[-1].text
    price = car.find_element(By.CLASS_NAME, 'prices').text
    condition = car.find_element(By.XPATH, ".//p[contains(text(),'Condition')]/span").text
    damage = car.find_element(By.XPATH, ".//p[contains(text(),'Damage')]/span").text
    mileage = car.find_element(By.XPATH, ".//p[contains(text(),'Mileage')]/span").text
    
    print('Information gathered successfully, appending DataFrame')
    
    new_row = {'Name': name, 'Price': price, 'Condition': condition, 'Damage': damage, 'Mileage': mileage}
    dict_list.append(new_row)
    
    print("Information has been appended into DataFrame")        

df = pd.DataFrame.from_dict(dict_list)

print('Full page was parsed')
df.to_csv('bidfax.csv', index=False)
print("Data has been saved to 'bidfax.csv'")
if len(driver.window_handles) > 0:
    driver.quit()

