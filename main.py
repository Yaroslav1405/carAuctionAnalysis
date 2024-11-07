from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functions import collect_car_info
import time
import pandas as pd

def get_car_links():
    driver = Driver(uc=True)
    driver.uc_gui_click_captcha()
    df = pd.DataFrame(columns=[
            'Name', 'Price', 'Auction Type', 'Date of Sale', 'Condition',
            'Mileage', 'Seller', 'Documents', 'Location', 'Primary Damage',
            'Secondary Damage', 'Transmission', 'Keys'
        ])
    df.to_csv('bidfax.csv', index=False)
    for page_index in range(1,11): # parse first 10 pages
        print(f'Processing page {page_index}')
        driver.uc_open_with_reconnect(f'https://en.bidfax.info/bmw/335/f/from-year=2013/to-year=2018/page/{page_index}', 10) # Increase to 30 when using proxy
        

        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'thumbnail'))) # Increase time to 15 when using proxy
        car_listings = driver.find_elements(By.CLASS_NAME, 'thumbnail')
        driver.sleep(2)
        car_urls = []

        for listing in car_listings:
            if listing.find_elements(By.TAG_NAME, 'ins'):
                print("Ad element found, skipping")
                continue
            find_url = listing.find_element(By.XPATH, ".//div[@class='caption']/a")
            car_urls.append(find_url.get_attribute("href"))
        print("URLs have been scrapped")
        
        
        for i, url in enumerate(car_urls):
            processing_car_timestamp = time.time()
            car_data = collect_car_info(driver=driver, url=url)
            if car_data:
                print(f'Processing car {i}...')
                df = pd.concat([df, pd.DataFrame([car_data])], ignore_index=True)
                print('Car data was successfully appended into a dataframe.')
                print(f'Time to process car {i}: {time.time() - processing_car_timestamp}')
            driver.sleep(3)
        print('All data processed, saving to the csv...')
        print(df)
        df.to_csv('bidfax.csv', mode='a', header = False, index=False) 
        print(f"Data saved after processing page {page_index}'")
            
            
    driver.close()
    driver.quit()


def main():
    start_time = time.time()
    get_car_links()
    print('*'*40)
    print(f'\n\nTime to complete the scraping: {time.time()- start_time}\n\n')
    print('*'*40)


if __name__ == '__main__':
    main()