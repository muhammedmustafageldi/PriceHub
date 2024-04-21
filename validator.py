from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class Validator:
    @staticmethod
    def elements_validator_hepsiburada(required_name, found_elements):
        for element in found_elements:

            if required_name.lower() in element.text.lower():
                return element

    @staticmethod
    def elements_validator_amazon(required_name, found_elements):
        for element in found_elements:
            try:
                # Check if there is price information
                name_item = element.find_element(By.CLASS_NAME, 'a-size-base-plus')
                print(name_item.text)
                # If there isn't price info throw exception
                price_element = element.find_element(By.CLASS_NAME, 'a-price-whole')

                if required_name.lower() in name_item.text.lower():
                    return price_element

            except NoSuchElementException:
                pass

    @staticmethod
    def elements_validator_trendyol(required_name, found_elements):
        for element in found_elements:

            brand_title = element.find_element(By.CLASS_NAME, 'prdct-desc-cntnr-ttl').text
            desc_title = element.find_element(By.CLASS_NAME, 'prdct-desc-cntnr-name').text
            product_full_name = f'{brand_title} {desc_title}'.lower()

            if required_name.lower() in product_full_name.lower():
                return element
