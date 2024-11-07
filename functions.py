from bs4 import BeautifulSoup


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
    driver.uc_open_with_reconnect(url, 8) # Increase to 15 when using proxy
    driver.uc_gui_click_captcha()
    # BS4

    soup = BeautifulSoup(driver.page_source, 'lxml')
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
