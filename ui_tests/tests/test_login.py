import logging
import pytest

from ui_tests import get_driver, BrowserType, is_element_present, baseURL, outputDir
from ui_tests.pages.LoginPage import LoginPage


def test_unit_get_driver(selenium_driver):
    result = (selenium_driver)
    logging.info(result)
    assert (result is not None)


@pytest.mark.skip("no valid users yet")
def test_can_login_valid_user(selenium_driver):
    loginPage = LoginPage(selenium_driver)
    loginPage.goto_page()

    loginPage.enter_login_creds('bob@bob.com', 'Admin1234!')

    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_can_login_valid_user.__name__, selenium_driver.name, 'before-login'))

    loginPage.driver.find_element(*loginPage.locators['_SignInButton']).click()

    assert is_element_present(loginPage.driver, *loginPage.locators['_VerifyLogin'])
    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_can_login_valid_user.__name__, selenium_driver.name, 'post-login'))


def test_cannot_login_empty_user(selenium_driver):
    loginPage = LoginPage(selenium_driver)
    loginPage.goto_page()

    assert loginPage.is_on_page()

    loginPage.enter_login_creds('', '')

    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_cannot_login_empty_user.__name__, selenium_driver.name, 'before-login'))

    loginPage.driver.find_element(*loginPage.locators['_SignInButton']).click()

    assert is_element_present(loginPage.driver, *loginPage.locators['_VerifyFailure'])
    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_cannot_login_empty_user.__name__, selenium_driver.name, 'post-login'))


def test_cannot_login_invalid_user(selenium_driver):
    loginPage = LoginPage(selenium_driver)
    loginPage.goto_page()

    assert loginPage.is_on_page()

    loginPage.enter_login_creds('boogetyboo', 'No1LuvSUN3RDS')

    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_cannot_login_invalid_user.__name__, selenium_driver.name,
                                           'before-login'))

    loginPage.driver.find_element(*loginPage.locators['_SignInButton']).click()

    assert is_element_present(loginPage.driver, *loginPage.locators['_VerifyFailure'])
    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_cannot_login_invalid_user.__name__, selenium_driver.name, 'post-login'))
