# main.py
import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def test_goto_ourchive_index():
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(driver_path)
    driver.get("http://host.docker.internal:8000/")

    title = driver.find_element_by_css_selector(css_selector='h1')
    logging.info(title.text)

    sidenav = driver.find_element_by_id('sidenav').find_elements_by_css_selector('li')

    for elem in sidenav:
        logging.info(elem.text)



    driver.close()
