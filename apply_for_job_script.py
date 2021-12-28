from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

def apply_for_job(application: "Application"):
    driver = setup_driver()
    login(driver, application)

    # Now that we're setup, we want to do the following:
    # 1. Find out how many pages there are
    # 2. Then go through each page grabbing every job url
    # 3. Go to those urls, see if we can apply through the gov website, and if so, fill out form then submit
    search_for_jobs(driver, application)
    number_of_pages = get_number_of_pages_from_search_for_jobs_results(driver)
    print(number_of_pages)

def setup_driver() -> webdriver:
    """Creates a driver with detatch mode; this helps us see if the script is working well whilst developing."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    return driver

def login(driver: webdriver, application: "Application"):
    """Login to the https://findajob.dwp.gov.uk/ using the Application's credentials"""
    driver.get("https://findajob.dwp.gov.uk/sign-in")

    # Enter credentials
    email_input_form_id = "email"
    email_input_form_element = driver.find_element_by_id(email_input_form_id)
    email_input_form_element.clear()
    email_input_form_element.send_keys(application.email_address)

    password_input_form_id = "password"
    password_input_form_element = driver.find_element_by_id(password_input_form_id)
    password_input_form_element.clear()

    # Once we've entered our password, we'll hit ENTER to login... this saves us finding and clicking the submit button
    password_input_form_element.send_keys(application.password, Keys.ENTER)

    time.sleep(5)

def search_for_jobs(driver, application):
    job_query_url = f"https://findajob.dwp.gov.uk/search?q={application.job_title}&w={application.job_location}&p=1"
    driver.get(job_query_url)

def get_number_of_pages_from_search_for_jobs_results(driver) -> int:
    """Grabs the last item from the pager-items to determine the number of pages"""
    xpath_str = "//ul[@class='pager-items']/li[last()]"
    element = driver.find_element_by_xpath(xpath_str)

    element_value = element.text
    number_of_pages = int(element_value)

    return number_of_pages

pass



