import logging
from enum import Enum, auto
from pathlib import Path
import pytest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

#baseURL = "http://host.docker.internal:8000/"
#baseURL = 'http://127.0.0.1:8000'
baseURL = 'http://ourchive-dev.stopthatimp.net/'


def set_dir():
    dirName = Path('.').joinpath('output').absolute()
    if not dirName.exists():
        dirName.mkdir()
    return dirName.absolute().as_posix()


outputDir = set_dir()

"""
enum for different browser drivers
chrome = latest
firefox = latest
"""


class BrowserType(Enum):
    CHROME = auto()
    FIREFOX = auto()


"""
Takes a BrowserType enum, returns a webdriver instance
"""


def get_driver(input):
    # return [name for name, member in BrowerType.__members__.items() if member.name == input]
    logging.info('browser type is {}'.format(input.name))
    if input == BrowserType.CHROME:
        driver_path = ChromeDriverManager().install()
        return webdriver.Chrome(driver_path)
    elif input == BrowserType.FIREFOX:
        return webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise Exception('Cannot find the browser driver for ' + input)


def is_element_present(driver, how, what):
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True
