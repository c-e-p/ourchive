import logging
import pytest
from selenium.webdriver.common.by import By
from ui_tests import get_driver, BrowserType, is_element_present, baseURL, outputDir
from ui_tests.pages.HeaderNav import HeaderNav


class RegistrationPage(HeaderNav):

    def __init__(self, driver):
        super().__init__(driver)
        self.pageURL = baseURL + '/register/'
        self.driver = driver

        self.locators = {
            "_UsernameField": (By.NAME, 'username'),
            "_EmailField": (By.NAME, 'email'),
            "_PasswordField": (By.NAME, 'password'),
            "_SignInButton": (
                By.XPATH, "//input[@class='uk-input']/following::input[@class='uk-button uk-button-default']"),
            #"_VerifyRegistration": (By.XPATH, "//div[text()='Login successful.']"),
            #"_VerifyFailure" : (By.XPATH, "//div[text()='Login unsuccessful. Please try again.']")
            "_VerifyRegistrationNotAllowed" : (By.XPATH, "//div[text()='Registration is not permitted at this time. Please contact site admin.']")
        }

    def enter_registration_creds(self, username, email, password):
        username_field = self.driver.find_element(*self.locators['_UsernameField'])
        email_field = self.driver.find_element(*self.locators['_EmailField'])
        password_field = self.driver.find_element(*self.locators['_PasswordField'])
        signin_button = self.driver.find_element(*self.locators['_SignInButton'])
        logging.debug('{} : {}'.format(username_field, username_field.is_displayed()))
        logging.debug('{} : {}'.format(email_field, email_field.is_displayed()))
        logging.debug('{} : {}'.format(password_field, password_field.is_displayed()))
        logging.debug('{} : {}'.format(signin_button, signin_button.is_displayed()))

        username_field.send_keys(username)
        email_field.send_keys(email)
        password_field.send_keys(password)
