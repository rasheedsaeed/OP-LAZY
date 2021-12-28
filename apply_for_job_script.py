from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def apply_for_job(application: "Application"):
    driver = setup_driver()
    logged_in = login(driver, application)

def setup_driver() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    return driver

def login(driver: webdriver, application: "Application"):
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





