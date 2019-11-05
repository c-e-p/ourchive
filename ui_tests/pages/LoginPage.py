import logging
import pytest
from selenium.webdriver.common.by import By
from ui_tests import get_driver, BrowserType, is_element_present, baseURL, outputDir


class LoginPage:

    def __init__(self, browser):
        self.pageURL = baseURL + ''
        self.driver = get_driver(browser)

        self.locators = {
            "_LoginLink": (By.XPATH, "//a[@href='/login']"),
            "_UsernameField": (By.NAME, 'username'),
            "_PasswordField": (By.NAME, 'password'),
            "_SignInButton": (
                By.XPATH, "//input[@class='uk-input']/following::input[@class='uk-button uk-button-default']"),
            "_VerifyLogin": (By.XPATH, "//div[text()='Login successful.']"),
            "_VerifyFailure" : (By.XPATH, "//div[text()='Login unsuccessful. Please try again.']")
        }

    def goto_page(self):
        self.driver.get(self.pageURL)
        login_link = self.driver.find_element(*self.locators['_LoginLink'])
        # logging.info(login_link.text)
        login_link.click()

    def enter_login_creds(self, username, password):
        username_field = self.driver.find_element(*self.locators['_UsernameField'])
        password_field = self.driver.find_element(*self.locators['_PasswordField'])
        signin_button = self.driver.find_element(*self.locators['_SignInButton'])
        logging.debug('{} : {}'.format(username_field, username_field.is_displayed()))
        logging.debug('{} : {}'.format(password_field, password_field.is_displayed()))
        logging.debug('{} : {}'.format(signin_button, signin_button.is_displayed()))

        username_field.send_keys(username)
        password_field.send_keys(password)
