import logging
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from ui_tests import get_driver, BrowserType, is_element_present, baseURL, outputDir
from ui_tests.pages.LoginPage import LoginPage
from ui_tests.pages.RegistrationPage import RegistrationPage
from faker import Faker

from ui_tests.pages.WorksPage import WorksPage


def test_can_navigate_to_works_list(selenium_driver):
    testPage = WorksPage(selenium_driver)
    testPage.goto_page()

    testPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_can_navigate_to_works_list.__name__, selenium_driver.name, 'navi-works'))
