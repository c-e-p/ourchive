import logging
import pytest
from selenium.webdriver.common.by import By
from ui_tests import get_driver, BrowserType, is_element_present, baseURL, outputDir
from ui_tests.pages.HeaderNav import HeaderNav


class WorksPage(HeaderNav):

    def __init__(self, driver):
        super().__init__(driver)

        self.pageURL = baseURL + 'works/'

        self.locators = {
            "_WorksList": (By.XPATH, "(//div[contains(.,'works list placeholder')])"),
        }
