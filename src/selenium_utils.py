from ctypes import create_unicode_buffer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from typing import Dict, NoReturn

import logging, time

from utils.typeddicts_utils import Credentials, JobApplication

WEBPAGE_ELEMENT_SELECTOR: Dict[str] = {
    "email_input_form_id": "email",
    "password_input_form_id": "password",
}


def setup_driver() -> webdriver:
    """Creates and returns a Chromium webdriver"""
    driver: webdriver = webdriver.Firefox()
    driver.minimize_window()
    driver.set_page_load_timeout(3)

    return driver


def login(driver: webdriver, credentials: Credentials) -> bool:
    """Login to findajob"""
    try:
        driver.get("https://findajob.dwp.gov.uk/sign-in")
    except Exception as e:
        logging.error(f"Couldn't load loin page. Exception: {e}")
        return False

    # Insert email
    email_input_form_element = driver.find_element_by_id(
        WEBPAGE_ELEMENT_SELECTOR["email_input_form_id"]
    )
    email_input_form_element.clear()
    email_input_form_element.send_keys(Credentials["email"])

    # Insert password
    password_input_form_element = driver.find_element_by_id(
        WEBPAGE_ELEMENT_SELECTOR["password_input_form_id"]
    )
    password_input_form_element.clear()
    password_input_form_element.send_keys(Credentials["password"])

    # Submit form
    password_input_form_element.send_keys(Keys.ENTER)

    time.sleep(3)  # I don't know exactly why, but this is required
    if driver.title == "Sign in":
        return False
    else:
        logging.info("Sucessfully logged in!")
        return True


def find_and_apply_for_jobs(driveR: webdriver, job_application: JobApplication):
    pass


def search_for_jobs(driver: webdriver, job_application: JobApplication, page_number: int = 1):
    # TODO: Insert docstring
    job_query_url = f"https://findajob.dwp.gov.uk/search?q={self.application.job_title}&w={self.application.job_location}&p={page_number}&pp=50"
    try:
        driver.get(job_query_url)
    except Exception as e:
        pass
