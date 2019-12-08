import logging
import pytest
from selenium.webdriver.support.wait import WebDriverWait

from ui_tests import get_driver, BrowserType, is_element_present, baseURL, outputDir
from ui_tests.pages.LoginPage import LoginPage
from ui_tests.pages.RegistrationPage import RegistrationPage
from faker import Faker

fake = Faker()


# @pytest.mark.skip("no valid users yet")
def test_registration_not_allowed(selenium_driver):
    testPage = RegistrationPage(selenium_driver)
    testPage.goto_page()

    randomUser = fake.profile(fields=['username', 'mail'])
    logging.info(randomUser)

    testPage.enter_registration_creds(randomUser['username'], randomUser['mail'], fake.password())

    testPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_registration_not_allowed.__name__, selenium_driver.name, 'pre-reg'))

    testPage.driver.find_element(*testPage.locators['_SignInButton']).click()

    assert is_element_present(testPage.driver, *testPage.locators['_VerifyRegistrationNotAllowed'])
    testPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_registration_not_allowed.__name__, selenium_driver.name, 'post-reg'))

    wait = WebDriverWait(selenium_driver, 10)
    wait.until(lambda driver: driver.current_url != testPage.pageURL)
    assert(selenium_driver.current_url == baseURL) # redirected to home page
