
import logging
from enum import Enum

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import unittest
import time

"""
enum for different browser drivers
chrome = latest
firefox = latest
"""
class BrowerType(Enum):
    CHROME = 1
    FIREFOX = 2

def get_driver(input):
    return [name for name, member in BrowerType.__members__.items() if member.name == input]

@pytest.mark.parametrize("input", [10, "CHROME", "FIREFOX", "OPERA"])
def test_unit_get_driver(input):
    result = get_driver(input)
    logging.info(result)
    assert(result is not None)

@pytest.mark.parametrize("browser", BrowerType)
def test_02(browser):
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(driver_path)
    baseURL = "http://host.docker.internal:8000/"
    driver.get(baseURL)
