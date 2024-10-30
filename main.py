from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functions import collect_car_info
import time
import json
import pandas as pd


def get_car_links():
    driver = Driver(uc=True)
    start_time = time.time()
    print(f'Start time: {start_time}')
    driver.uc_open_with_reconnect(f'https://en.bidfax.info/bmw/335/f/from-year=2013/to-year=2018/page/{1}', 30)
    timestamp_1 = time.time()
    print(f"Timestamp 1: {timestamp_1-start_time}")
    driver.uc_gui_click_captcha()
    driver.implicitly_wait(5)
    timestamp_2 = time.time()
    print(f"Timestamp 2: {timestamp_2 - timestamp_1}")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'thumbnail')))
    timestamp_3 = time.time()
    print(f"Timestamp 3: {timestamp_3 - timestamp_2}")
    car_listings = driver.find_elements(By.CLASS_NAME, 'thumbnail')
    driver.sleep(2)
    timestamp_4 = time.time()
    print(f"Timestamp 4: {timestamp_4 - timestamp_3}")
    car_urls = []
    try:
        for listing in car_listings:
            temp_timestamp = time.time()
            if listing.find_elements(By.TAG_NAME, 'ins'):
                print("Ad element found, skipping")
                continue
            find_url = listing.find_element(By.XPATH, ".//div[@class='caption']/a")
            car_urls.append(find_url.get_attribute("href"))
            print(f'Timestamp after iteration: {time.time() - temp_timestamp}')
        print("URLs have been scrapped")
    except Exception as e:
        print(f'Something went wrong with scrapping URLs: {e}')
        
    car_url_dict = {k: v for k, v in enumerate(car_urls)}
        
    with open('car_url_dict.json', 'w', encoding='utf-8') as file:
        json.dump(car_url_dict, file, indent=4, ensure_ascii=False)
    driver.sleep(2)
    
    df = pd.DataFrame(columns=[
        'Name', 'Price', 'Auction Type', 'Date of Sale', 'Condition',
        'Mileage', 'Seller', 'Documents', 'Location', 'Primary Damage',
        'Secondary Damage', 'Transmission', 'Keys'
    ])
    
    for i, url in enumerate(car_urls):
        # print(f'URL: {url}')
        processing_car_timestamp = time.time()
        car_data = collect_car_info(driver=driver, url=url)
        # print(car_data)
        if car_data:
            print(f'Processing car {i}...')
            df = pd.concat([df, pd.DataFrame([car_data])], ignore_index=True)
            print('Car data was successfully appended into a dataframe.')
            print(f'Timestamp after processed {i} car: {time.time() - processing_car_timestamp}')
        driver.sleep(3)

        
    df.to_csv('bidfax.csv', index=False) #mode='a', header = not pd.read_csv('bidfax.csv').empty if 'bidfax.csv' else True,
    #print(f"Data saved after processing page {page_index}'")
    driver.close()
    driver.quit()


def main():
    # start_time = time.time()
    get_car_links()
    time.sleep(5)
    # print('*'*40)
    # print(f'\n\nTime to process 10 vehicles: {time.time()- start_time}\n\n')
    # print('*'*40)


if __name__ == '__main__':
    main()