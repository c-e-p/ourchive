import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class OurchiveIndex(ChromeDriverManager):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators in login page for github              #Locator types for reference
    _LoginLink = "//a[@href='/login']"  # xpath
    _UsernameField = "username"  # name
    _PasswordField = "password"  # name
    _SignInButton = "//input[@class='uk-input']/following::input[@class='uk-button uk-button-default']"  # xpath
    _VerifyLogin = "//div[text()='Login successful.']"  # xpath

    def ClickLoginLink(self):
        self.elementClick(self._LoginLink, locatorType="xpath")

    def FillEmailField(self, email):
        self.sendKeys(email, self._UsernameField, locatorType="name")

    def FillPasswordField(self, password):
        self.sendKeys(password, self._PasswordField, locatorType="name")

    def ClickSignInbutton(self):
        self.elementClick(self._SignInButton, locatorType="xpath")

    def VerifyLogin(self):
        element = self.isElementPresent(self._VerifyLogin, locatorType="xpath")
        return element

    def VerifyOnPage(self):

        return False

    def UserLogin(self, email, password):
        self.ClickLoginLink()
        self.FillEmailField(email)
        self.FillPasswordField(password)
        self.ClickSignInbutton()
