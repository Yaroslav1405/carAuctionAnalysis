from bs4 import BeautifulSoup
import time

def safe_extract_text(soup, selector, multiple=False, index=0):
    try:
        if multiple:
            elements = soup.select(selector)
            return elements[index].get_text() if elements else 'N/A'
        else:
            element = soup.select_one(selector)
            return element.get_text() if element else 'N/A'
    except Exception:
        return 'N/A'


def collect_car_info(driver, url):
    driver.uc_open_with_reconnect(url, 30)
    driver.uc_gui_click_captcha()
    # BS4

    soup = BeautifulSoup(driver.page_source, 'lxml')
    # All below Convert to function 
    name = safe_extract_text(soup, 'h1')
    price = safe_extract_text(soup, '.prices')
    auction_type = safe_extract_text(soup, "p:-soup-contains('Auction') span", multiple=True)
    sale_date = safe_extract_text(soup, "p:-soup-contains('Date of sale') span")
    condition = safe_extract_text(soup, "p:-soup-contains('Condition') span")
    mileage = safe_extract_text(soup, "p:-soup-contains('Mileage') span")
    seller = safe_extract_text(soup, "p:-soup-contains('Seller') span")
    documents = safe_extract_text(soup, "p:-soup-contains('Documents') span")
    location = safe_extract_text(soup, "p:-soup-contains('Location') span", multiple=True, index=-1)
    primary_damage = safe_extract_text(soup, "p:-soup-contains('Primary Damage') span")
    secondary_damage = safe_extract_text(soup, "p:-soup-contains('Secondary Damage') span")
    transmission = safe_extract_text(soup, "p:-soup-contains('Transmission') span")
    keys = safe_extract_text(soup, "p:-soup-contains('Keys') span")
        
    print('Information gathered successfully, appending DataFrame')

    car_data = {
            'Name': name, 'Price': price, 
                'Auction Type': auction_type, 
                'Date of Sale': sale_date, 
                'Condition': condition, 
                'Mileage': mileage, 'Seller': seller, 
                'Documents': documents, 'Location': location, 
                'Primary Damage': primary_damage, 
                'Secondary Damage': secondary_damage,
                'Transmission': transmission, 'Keys': keys
    }    
    return car_data  






"""
# Selenium
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


# new_row = {'Name': name, 'Price': price, 'Auction Type': auction_type, 'Date of Sale': sale_date, 
#            'Condition': condition, 'Mileage': mileage, 'Seller': seller, 'Documents': documents,
#            'Location': location, 'Primary Damage': primary_damage, 'Secondary Damage': secondary_damage,
#             'Transmission': transmission, 'Keys': keys}
"""