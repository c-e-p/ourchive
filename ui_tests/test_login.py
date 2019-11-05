import logging
import pytest

from ui_tests import get_driver, BrowserType, is_element_present, baseURL, outputDir
from ui_tests.pages.LoginPage import LoginPage


@pytest.mark.skip
# @pytest.mark.parametrize("input", BrowerType)
def test_unit_get_driver(input):
    result = get_driver(input)
    logging.info(result)
    assert (result is not None)

@pytest.mark.skip("no valid user set up yet")
@pytest.mark.parametrize("browser", BrowserType)
def test_can_login_valid_user(browser):
    loginPage = LoginPage(browser)
    loginPage.goto_page()

    for key, value in loginPage.locators.items():
        if 'Verify' not in key:
            elem = loginPage.driver.find_element(*loginPage.locators[key])
            logging.info('{}: {}'.format(elem, elem.is_displayed()))

    loginPage.enter_login_creds('bob@bob.com', 'Admin1234!')

    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_can_login_valid_user.__name__, browser.name, 'before-login'))

    loginPage.driver.find_element(*loginPage.locators['_SignInButton']).click()

    assert is_element_present(loginPage.driver, *loginPage.locators['_VerifyLogin'])
    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_can_login_valid_user.__name__, browser.name, 'post-login'))

    loginPage.driver.close()


@pytest.mark.parametrize("browser", BrowserType)
def test_cannot_login_empty_user(browser):
    loginPage = LoginPage(browser)
    loginPage.goto_page()

    for key, value in loginPage.locators.items():
        if 'Verify' not in key:
            elem = loginPage.driver.find_element(*loginPage.locators[key])
            logging.info('{}: {}'.format(elem, elem.is_displayed()))

    loginPage.enter_login_creds('', '')

    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_cannot_login_empty_user.__name__, browser.name, 'before-login'))

    loginPage.driver.find_element(*loginPage.locators['_SignInButton']).click()

    assert is_element_present(loginPage.driver, *loginPage.locators['_VerifyFailure'])
    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_cannot_login_empty_user.__name__, browser.name, 'post-login'))

    loginPage.driver.close()


@pytest.mark.parametrize("browser", BrowserType)
def test_cannot_login_invalid_user(browser):
    loginPage = LoginPage(browser)
    loginPage.goto_page()

    for key, value in loginPage.locators.items():
        if 'Verify' not in key:
            elem = loginPage.driver.find_element(*loginPage.locators[key])
            logging.info('{}: {}'.format(elem, elem.is_displayed()))

    loginPage.enter_login_creds('boogetyboo', 'No1LuvSUN3RDS')

    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_cannot_login_empty_user.__name__, browser.name, 'before-login'))

    loginPage.driver.find_element(*loginPage.locators['_SignInButton']).click()

    assert is_element_present(loginPage.driver, *loginPage.locators['_VerifyFailure'])
    loginPage.driver.save_screenshot(
        outputDir + '/{}-{}-{}.png'.format(test_cannot_login_empty_user.__name__, browser.name, 'post-login'))

    loginPage.driver.close()