from selenium import webdriver

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

    email_input_form_id = "email"
    password_input_form_id = "password"

