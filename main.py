from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from product import Product
from validator import Validator
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# Main color -> #FFEBC8

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
webDriverWait = WebDriverWait(driver, 10)


def get_price_from_trendyol(search_value):
    driver.maximize_window()
    driver.get('https://trendyol.com')

    webDriverWait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'V8wbcUhU')))
    search_bar = driver.find_element(By.CLASS_NAME, 'V8wbcUhU')
    search_bar.send_keys(search_value)

    search_bar.send_keys(Keys.ENTER)

    # If show the data hider popup ->
    webDriverWait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'prdct-cntnr-wrppr')))
    driver.execute_script("window.scrollTo(0, 200)")

    empty_area = driver.find_element(By.CLASS_NAME, 'prdct-cntnr-wrppr')
    empty_area.click()

    # Get results by two line title ->
    found_elements = driver.find_elements(By.CLASS_NAME, 'two-line-text')
    result = Validator.elements_validator_trendyol(required_name=search_value, found_elements=found_elements)

    if result:
        result.click()

        try:
            new_window = driver.window_handles[-1]
            driver.switch_to.window(new_window)

            webDriverWait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'base-product-image')))
            product_img_container = driver.find_element(By.CLASS_NAME, 'base-product-image')

            # Get image src
            webDriverWait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'img')))
            product_img = product_img_container.find_element(By.TAG_NAME, 'img')
            img_src = product_img.get_attribute('src')

            # Get information container of the product
            webDriverWait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'pr-in-cn')))
            information_container = driver.find_element(By.CLASS_NAME, 'pr-in-cn')

            # Get product name
            product_name = driver.find_element(By.CLASS_NAME, 'pr-new-br').text

            # Get product price
            product_price = information_container.find_element(By.CLASS_NAME, 'prc-dsc').text

            # Get product url
            product_url = driver.current_url

            product = Product(name=product_name, store='Trendyol', img_url=img_src, price=product_price,
                              product_url=product_url)

            print(product)
            print('------------------------')

        except IndexError:
            print('Error! The request is timeout.')
            driver.close()

        get_price_from_amazon(search_value)

    else:
        print('Error! Product is not found.')


def get_price_from_amazon(search_value):
    driver.execute_script("window.open('', '_blank');")
    new_tab = driver.window_handles[-1]
    driver.switch_to.window(new_tab)

    driver.get('https://www.amazon.com.tr/')

    # if show the cookies pop-up
    try:
        pop_up = webDriverWait.until(expected_conditions.presence_of_element_located((By.ID, 'sp-cc')))
        if pop_up.is_displayed():
            accept_button = driver.find_element(By.ID, 'sp-cc-accept')
            accept_button.click()

    except TimeoutException:
        print('The pop-up window was not shown. Continuing...')

    # Get search bar and enter product name
    webDriverWait.until(expected_conditions.visibility_of_element_located((By.ID, 'twotabsearchtextbox')))
    search_bar = driver.find_element(By.ID, 'twotabsearchtextbox')
    search_bar.send_keys(search_value)

    search_bar.send_keys(Keys.ENTER)

    # Get results of search
    webDriverWait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'puis-padding-left-small')))
    found_elements = driver.find_elements(By.CLASS_NAME, 'puis-padding-left-small')

    # Select the valid
    result = Validator.elements_validator_amazon(required_name=search_value, found_elements=found_elements)

    if result:
        result.click()

        # Find container of product and get product info
        webDriverWait.until(expected_conditions.visibility_of_element_located((By.ID, 'centerCol')))
        product_container = driver.find_element(By.ID, 'centerCol')

        product_title_element = product_container.find_element(By.ID, 'title_feature_div')
        product_price_element = product_container.find_element(By.ID, 'apex_desktop')

        # Get product title
        product_title = product_title_element.text

        # Get product price
        product_price = product_price_element.text.splitlines()[0] + '.' + product_price_element.text.splitlines()[1]
        tl_index = product_price.find('TL')
        clear_price = product_price[:tl_index + 2]

        # Get image url
        product_img_container = driver.find_element(By.ID, 'imgTagWrapperId')
        product_img_element = product_img_container.find_element(By.TAG_NAME, 'img')
        img_url = product_img_element.get_attribute('src')

        # Get product url
        product_url = driver.current_url

        product = Product(product_title, 'Amazon', img_url, clear_price, product_url)
        print(product)
        print('------------------------')

        get_price_from_hepsiburada(search_value)
    else:
        print("Product is not found!")


def get_price_from_hepsiburada(search_value):
    try:
        # Open new tab
        driver.execute_script("window.open('', '_blank');")
        new_tab = driver.window_handles[-1]
        driver.switch_to.window(new_tab)

        driver.get('https://www.hepsiburada.com/')

        # If showing the cookies bar
        try:
            cookies_bar = webDriverWait.until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, 'ot-sdk-row')))
            if cookies_bar.is_displayed():
                accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
                accept_button.click()
        except TimeoutException:
            print('The pop-up window was not shown. Continuing...')

        # Find search bar
        webDriverWait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'searchBoxOld-M1esqHPyWSuRUjMCALPK')))
        search_bar = driver.find_element(By.CLASS_NAME, 'searchBoxOld-M1esqHPyWSuRUjMCALPK')

        search_bar.click()

        webDriverWait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'theme-IYtZzqYPto8PhOx3ku3c')))
        search_input_element = driver.find_element(By.CLASS_NAME, 'theme-IYtZzqYPto8PhOx3ku3c')
        search_input_element.send_keys(search_value)
        search_input_element.send_keys(Keys.ENTER)

        # Get results ->
        webDriverWait.until(expected_conditions.visibility_of_element_located((By.ID, 'i0')))
        found_elements = driver.find_elements(By.TAG_NAME, 'h3')

        result = Validator.elements_validator_hepsiburada(required_name=search_value, found_elements=found_elements)
        result.click()

        # Switch to new window
        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)

        # Get product name
        webDriverWait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'best-price-trick')))
        product_title_element = driver.find_element(By.CLASS_NAME, 'best-price-trick')
        product_title = product_title_element.text

        # Get price
        webDriverWait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'price')))
        product_price = driver.find_element(By.CLASS_NAME, 'price').text

        # Get Image url
        image_container = webDriverWait.until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'owl-item')))
        img_element = image_container.find_element(By.TAG_NAME, 'img')
        img_src = img_element.get_attribute('src')

        # Get product url
        product_url = driver.current_url

        product = Product(product_title, 'Hepsiburada', img_src, product_price, product_url)
        print(product)
    except TimeoutException:
        print('The data extraction timed out.')


get_price_from_trendyol("playstation 5")

while True:
    continue
