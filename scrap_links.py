from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd


def get_car_links():
    driver = Driver(uc=True)
    driver.uc_open_with_reconnect(f'https://en.bidfax.info/bmw/335/f/from-year=2013/to-year=2018/page/{1}', 30)
    driver.uc_gui_click_captcha()
    driver.implicitly_wait(5)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'thumbnail')))
    car_listings = driver.find_elements(By.CLASS_NAME, 'thumbnail')

    try:
        find_url = car_listings.find_elements(By.CLASS_NAME, "btn btn-default btn-more pull-right")
        car_urls = list(set([f'{link.get_attribute('href')}' for link in find_url]))
        print("Urls have been scrapped")
    except:
        print('SOmething went wrong with scrapping urls')
        
    car_url_dict = {}
    for k,v in enumerate(car_urls):
        car_url_dict.update({k:v})
        
    with open('car_url_dict.json', 'w', encoding='utf-8'):
        json.dump(car_url_dict, 'file', indent=4, ensure_ascii=False)
        

