import pytest
import logging
from ui_tests import BrowserType, get_driver

def pytest_addoption(parser):
	parser.addoption(
		"--browser", action="store", default="Chrome", help="browser options: CHROME, FireFox"
	)


@pytest.fixture
def selenium_driver(request):
	requestedBrowser = request.config.getoption("--browser")
	logging.info(requestedBrowser)

	for name, value in BrowserType.__members__.items():
		logging.info(name.casefold())
		if requestedBrowser.casefold() == name.casefold():
			driver = get_driver(value)


	yield driver
	
	driver.close()



'''
use to add more info to header
'''
#def pytest_report_header(config):
#    return True