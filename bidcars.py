# Import required modules
from seleniumbase import Driver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to extract the data
def extracting_data(MAX_PAGES = 2):
    url = 'https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&make=BMW&model=3%20Series&year-from=2013&year-to=2019&order-by=dateDesc'
    df = pd.DataFrame(columns=[
                'Name', 'Price', 'Auction Type', 'Date of Sale', 'Sold by', 
                'Condition', 'Mileage', 'Seller', 'Location', 'Damage', 
                'Transmission', 'VIN'
            ])
    page_count = 0
    
    while page_count < MAX_PAGES:
        
        driver = Driver(uc=True)
        driver.uc_open_with_reconnect(url, 10)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        data = soup.find_all('div', class_ = 'item-horizontal lots-search')
        for car in data:
            try:
                name = car.find('a', class_='damage-info').text
                price = car.find('div', class_='price-box').text.split(':')[1].strip()
                auction_name = car.find('span', class_='item-seller').text
                sale_date = car.find('div', class_='date no-wrap-text-ellipsis').text
                condition =car.find('strong').text
                info = car.find_all('li', class_='no-wrap-text-ellipsis')
                mileage = info[1].text.split(':')[1].strip()
                vin = info[0].text.split(':')[1].strip()
                seller = info[3].text.split(':')[1].strip()
                location = info[2].text.split(':')[1].strip()
                info2 = car.find_all('li', class_='damage-info')
                documents = info2[0].text.split(':')[1].strip()
                damage = info2[1].text.split(':')[1].strip()
                sold_by = car.find('div', class_='bid-status status-orange').text
                
                car_data = {
                        'Name': name, 'Price': price, 
                        'Auction Name': auction_name, 
                        'Date of Sale': sale_date, 
                        'Condition': condition, 'VIN': vin, 
                        'Mileage': mileage, 'Seller': seller, 
                        'Documents': documents, 'Location': location, 
                        'Damage': damage, 'Auction Type': sold_by
                }    
            
                df = pd.concat([df, pd.DataFrame([car_data])], ignore_index=True)
                time.sleep(1)
            except Exception as e:
                print(f'Error in the process: {e}')
        page_count +=1
        
        try:
            driver.find_element('link text', 'Load More...').click()
            time.sleep(20)
        except Exception as e:
            print('Error when pressing Load More... button')
            
        df.to_csv('bidcars.csv', index=False)

        driver.close()
        driver.quit()
        


# Main function
def main():
    start_time = time.time()
    extracting_data()
    print('*'*40)
    print(f'\n\nTime to complete the scraping: {time.time()- start_time}\n\n')
    print('*'*40)


if __name__ == '__main__':
    main()