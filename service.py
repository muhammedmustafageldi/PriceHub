import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from product import Product
from validator import Validator


class PriceService:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.webDriverWait = WebDriverWait(self.driver, 10)

    def get_price_from_trendyol(self, search_value):

        self.driver.maximize_window()
        self.driver.get('https://trendyol.com')

        self.webDriverWait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'V8wbcUhU')))
        search_bar = self.driver.find_element(By.CLASS_NAME, 'V8wbcUhU')
        search_bar.send_keys(search_value)

        search_bar.send_keys(Keys.ENTER)

        # If show the data hider popup ->
        self.webDriverWait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'prdct-cntnr-wrppr')))
        self.driver.execute_script("window.scrollTo(0, 200)")

        empty_area = self.driver.find_element(By.CLASS_NAME, 'prdct-cntnr-wrppr')
        empty_area.click()

        # Get results by two line title ->
        found_elements = self.driver.find_elements(By.CLASS_NAME, 'two-line-text')
        result = Validator.elements_validator_trendyol(required_name=search_value, found_elements=found_elements)

        if result:
            result.click()

            try:
                new_window = self.driver.window_handles[-1]
                self.driver.switch_to.window(new_window)

                self.webDriverWait.until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, 'base-product-image')))
                product_img_container = self.driver.find_element(By.CLASS_NAME, 'base-product-image')

                # Get image src
                self.webDriverWait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'img')))
                product_img = product_img_container.find_element(By.TAG_NAME, 'img')
                img_src = product_img.get_attribute('src')

                # Get information container of the product
                self.webDriverWait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'pr-in-cn')))
                information_container = self.driver.find_element(By.CLASS_NAME, 'pr-in-cn')

                # Get product name
                product_name = self.driver.find_element(By.CLASS_NAME, 'pr-new-br').text

                # Get product price
                product_price = information_container.find_element(By.CLASS_NAME, 'prc-dsc').text

                # Get product seller
                product_seller = self.driver.find_element(By.CLASS_NAME, 'seller-name-text').text

                # Get product url
                product_url = self.driver.current_url

                product = Product(name=product_name, store=product_seller, img_url=img_src, price=product_price,
                                  product_url=product_url)

                return product

            except IndexError:
                print('Error! The request is timeout.')
                self.driver.close()
        else:
            print('Error! Product is not found.')

    def get_price_from_amazon(self, search_value):
        self.driver.execute_script("window.open('', '_blank');")
        new_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_tab)

        self.driver.get('https://www.amazon.com.tr/')

        # if show the cookies pop-up
        self.amazon_close_pop_up()

        # Get search bar and enter product name
        self.webDriverWait.until(expected_conditions.visibility_of_element_located((By.ID, 'twotabsearchtextbox')))
        search_bar = self.driver.find_element(By.ID, 'twotabsearchtextbox')
        search_bar.send_keys(search_value)
        search_bar.send_keys(Keys.ENTER)

        # if show the cookies pop-up
        self.amazon_close_pop_up()

        # Get results of search
        self.webDriverWait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'puis-padding-left-small')))
        found_elements = self.driver.find_elements(By.CLASS_NAME, 'puis-padding-left-small')

        # Select the valid
        result = Validator.elements_validator_amazon(required_name=search_value, found_elements=found_elements)

        if result:
            result.click()

            # Find container of product and get product info
            self.webDriverWait.until(expected_conditions.visibility_of_element_located((By.ID, 'centerCol')))
            product_container = self.driver.find_element(By.ID, 'centerCol')

            product_title_element = product_container.find_element(By.ID, 'title_feature_div')
            product_price_element = product_container.find_element(By.ID, 'apex_desktop')

            # Get product title
            product_title = product_title_element.text

            # Get product price
            product_price = product_price_element.text.splitlines()[0] + '.' + product_price_element.text.splitlines()[
                1]
            tl_index = product_price.find('TL')
            clear_price = product_price[:tl_index + 2]

            # Get image url
            product_img_container = self.driver.find_element(By.ID, 'imgTagWrapperId')
            product_img_element = product_img_container.find_element(By.TAG_NAME, 'img')
            img_url = product_img_element.get_attribute('src')

            # Get product seller
            product_seller = self.driver.find_element(By.ID, 'sellerProfileTriggerId').text

            # Get product url
            product_url = self.driver.current_url

            product = Product(product_title, product_seller, img_url, clear_price, product_url)

            return product
        else:
            print("Product is not found!")

    def get_price_from_hepsiburada(self, search_value):

        # Open new tab
        self.driver.execute_script("window.open('', '_blank');")
        new_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_tab)

        self.driver.get('https://www.hepsiburada.com/')

        # If showing the cookies bar
        try:
            cookies_bar = self.webDriverWait.until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, 'ot-sdk-row')))
            if cookies_bar.is_displayed():
                accept_button = self.driver.find_element(By.ID, 'onetrust-accept-btn-handler')
                accept_button.click()
        except TimeoutException:
            print('The pop-up window was not shown. Continuing...')

        time.sleep(4)

        # Find search bar
        self.webDriverWait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'searchBoxOld-M1esqHPyWSuRUjMCALPK')))
        search_bar = self.driver.find_element(By.CLASS_NAME, 'searchBoxOld-M1esqHPyWSuRUjMCALPK')

        search_bar.click()

        input_bar = self.webDriverWait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'theme-IYtZzqYPto8PhOx3ku3c')))
        input_bar.send_keys(search_value)
        input_bar.send_keys(Keys.ENTER)

        # Get results ->
        self.webDriverWait.until(expected_conditions.visibility_of_element_located((By.ID, 'i0')))
        found_elements = self.driver.find_elements(By.TAG_NAME, 'h3')

        result = Validator.elements_validator_hepsiburada(required_name=search_value, found_elements=found_elements)
        result.click()

        # Switch to new window
        new_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window)

        # Get product name
        self.webDriverWait.until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'best-price-trick')))
        product_title_element = self.driver.find_element(By.CLASS_NAME, 'best-price-trick')
        product_title = product_title_element.text

        # Get price
        self.webDriverWait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'price')))
        product_price = self.driver.find_element(By.CLASS_NAME, 'price').text

        # Get Image url
        image_container = self.webDriverWait.until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'owl-item')))
        img_element = image_container.find_element(By.TAG_NAME, 'img')
        img_src = img_element.get_attribute('src')

        # Get product seller
        self.webDriverWait.until(
            expected_conditions.visibility_of_element_located((By.CLASS_NAME, 'seller-container')))
        seller_container = self.driver.find_element(By.CLASS_NAME, 'seller-container')
        product_seller = seller_container.find_element('tag name', 'span').text

        seller_prefix = 'Satıcı:'
        if product_seller.startswith(seller_prefix):
            product_seller = product_seller[len(seller_prefix):].strip()

        # Get product url
        product_url = self.driver.current_url

        product = Product(product_title, product_seller, img_src, product_price, product_url)

        return product

    def get_prices(self, search_value):
        product_trendyol = self.get_price_from_trendyol(search_value=search_value)
        product_amazon = self.get_price_from_amazon(search_value=search_value)
        product_hepsiburada = self.get_price_from_hepsiburada(search_value=search_value)

        return {'product_trendyol': product_trendyol, 'product_amazon': product_amazon,
                'product_hepsiburada': product_hepsiburada}

    def amazon_close_pop_up(self):
        try:
            pop_up = self.webDriverWait.until(expected_conditions.presence_of_element_located((By.ID, 'sp-cc')))
            if pop_up.is_displayed():
                accept_button = self.driver.find_element(By.ID, 'sp-cc-accept')
                accept_button.click()

        except TimeoutException:
            print('The pop-up window was not shown. Continuing...')

    def quit_driver(self):
        self.driver.quit()
