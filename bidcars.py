# Import required modules
from seleniumbase import Driver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Function to extract the data
def extracting_data(MAX_PAGES = 21):
    # Url of website page to scrap
    
    login_url = ''
    scrape_url = 'https://bid.cars/en/search/archived/results?search-type=filters&type=Automobile&make=BMW&model=3+Series&year-from=2013&year-to=2019&airbags=Intact&order-by=dateDesc'
    
    # Initialize a DataFrame to store scraped data
    df = pd.DataFrame(columns=[
                'Name', 'Price', 'Auction Type', 'Date of Sale', 'Sold by', 
                'Condition', 'Mileage', 'Seller', 'Location', 'Damage', 
                'Transmission', 'VIN'
            ])
    
    # Intitialization of page count
    page_count = 1
    
    # Intitialization of Selenium driver
    driver = Driver(uc=True)
    driver.uc_open_with_reconnect(scrape_url, 10)
    
    
    
    
    
    # Loop to scrape multiple pages, up to MAX_PAGES
    while page_count < MAX_PAGES:
        
        # Parse the current page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        # Extract all car data from the page
        data = soup.find_all('div', class_ = 'item-horizontal lots-search')
        print(f'Number of cars found on page {page_count}: {len(data)}')

        # Process the last 50 cars on the page
        for car in data[-50:]:
        
            try:   
                # Extract details of the car  
                name = car.find('a', class_='damage-info').text
                price = car.find('div', class_='price-box').text.split(':')[1].strip() if car.find('div', class_='price-box') else "N/A"
                auction_name = car.find('span', class_='item-seller').text
                sale_date = car.find('div', class_='date no-wrap-text-ellipsis').text
                condition =car.find('strong').text
                info = car.find_all('li', class_='no-wrap-text-ellipsis')
                mileage = info[1].text.split(':')[1].strip() # if len(info) > 1 else info
                vin = info[0].text.split(':')[1].strip() # if len(info) > 0 else 'N/A'
                seller = info[3].text.split(':')[1].strip() # if len(info) > 3 else 'N/A'
                location = info[2].text.split(':')[1].strip() # if len(info) > 2 else 'N/A'
                info2 = car.find_all('li', class_='damage-info')
                documents = info2[0].text.split(':')[1].strip() # if len(info2) > 0 else info2
                damage = info2[1].text.split(':')[1].strip() # if len(info2) > 1 else 'N/A'
                sold_by = car.find('div', class_='bid-status status-orange').text
                
                # Store car details in dictionary
                car_data = {
                        'Name': name, 'Price': price, 
                        'Auction Name': auction_name, 
                        'Date of Sale': sale_date, 
                        'Condition': condition, 'VIN': vin, 
                        'Mileage': mileage, 'Seller': seller, 
                        'Documents': documents, 'Location': location, 
                        'Damage': damage, 'Auction Type': sold_by
                }    

                # Append the car data to the DataFrame
                df = pd.concat([df, pd.DataFrame([car_data])], ignore_index=True)
                
                # Sleep for two seconds
                time.sleep(3)
            except Exception as e:
                # Handle any exceptions to ensure the code does not crash
                print(f'Error in the process: {e}')    
        
        # Save the scraped data to a CSV file after each page
        print(f'Saving data from page {page_count} to csv...') 
        df.to_csv('bidcars.csv', index=False)
        
        # Click on the "Load More" button to load more items
        try:
            load_more = driver.find_element('link text', 'Load More...')
            load_more.click()
            print(f'Reached the end of page {page_count}, loading more content...')
            time.sleep(3)
            
            # Wait for the next set of cars to load
            WebDriverWait(driver, 30).until(
                lambda driver: len(driver.find_elements(By.CLASS_NAME, 'item-horizontal')) > len(data)
            )
            # Increment page count     
            page_count +=1
        except Exception as e:
            # Handle the case where the "Load More" button doesn't exist
            print(f'No more content to load. Stopping scrapping process. Error: {e}')
            break

    # Close the driver after all pages are processed
    driver.close()
    driver.quit()
        


# Main function
def main():
    start_time = time.time()
    extracting_data()
    print('*'*40)
    print(f'\n\nTime to complete the scraping: {time.time()- start_time}\n\n')
    print('*'*40)

# Entry point of the script
if __name__ == '__main__':
    main()