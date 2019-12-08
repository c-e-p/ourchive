import logging
import pytest
from selenium.webdriver.common.by import By
from ui_tests import get_driver, BrowserType, is_element_present, baseURL, outputDir


class HeaderNav:

    def __init__(self, driver):
        self.driver = driver

        self.menu_locators = {
            "_HomeLink": (By.XPATH, "//a[@href='/']"),
            "_WorksLink": (By.XPATH, "//a[@href='/works']"),
            "_BookmarksLink": (By.XPATH, "//a[@href='/bookmarks']"),
            "_SearchLink": (By.XPATH, "//a[@href='/search']"),
            "_LoginLink": (By.XPATH, "//a[@href='/login']"),
            "_RegistrationLink": (By.XPATH, "//a[@href='/register']"),
        }

    def menu_is_displayed(self):
        for key, value in self.menu_locators.items():
            if 'Verify' not in key:
                elem = self.driver.find_element(*self.menu_locators[key])
                logging.info('{}: {}'.format(elem, elem.is_displayed()))
                if elem.is_displayed():
                    return True
        return False

    def is_on_page(self):
        for key, value in self.locators.items():
            if 'Verify' not in key:
                elem = self.driver.find_element(*self.locators[key])
                logging.info('{}: {}'.format(elem, elem.is_displayed()))
                if elem.is_displayed():
                    return True
        return False

    def goto_page(self):
        self.driver.get(self.pageURL)
        #login_link = self.driver.find_element(*self.locators['_LoginLink'])
        # logging.info(login_link.text)
        #login_link.click()

        assert self.menu_is_displayed()
        assert self.is_on_page()
