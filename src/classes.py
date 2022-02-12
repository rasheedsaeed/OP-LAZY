from __future__ import annotations
from typing import List
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from src.typed_dicts import Credentials

class JobApplication:
    def __init__(self, job_title: str, job_location: str, full_name: str, target_cv_name: str, cover_letter: str = "") -> None:
        # Job login
        self.job_title: str = job_title
        self.job_location: str = job_location

        # Cover letter
        self.full_name: str = full_name
        self.target_cv_name: str = target_cv_name
        self.cover_letter: str = cover_letter

        # Applications we've applied for 
        self.sucessful_applications: List[str] = []

    def job_applied_for(self, url: str) -> None:
        self.sucessful_applications.append(url)


class GovFindAJobSelenium:
    URLS = {
        "login": "https://findajob.dwp.gov.uk/sign-in"
    }

    PAGE_ELEMENTS_IDENTIFIERS = {
        # Login
        "login_email_id": "email",
        "login_password_id": "password"

    }
    def __init__(self, job_applications: List[JobApplication], login_credentials: Credentials) -> None:
        self.application: List[JobApplication] = job_applications
        self.login_credentials: Credentials = login_credentials

        # Webdriver
        self.web_driver: webdriver = None

        # If we've logged into the account
        self.logged_in = False

        # Results
        self.number_of_search_results_page: int = 1
        self.all_job_applications_urls: list = []
        self.total_number_of_jobs_applied: int = 0

    def find_and_apply_for_jobs(self):
        """Our main function that executes our methods to apply for jobs"""
        self.driver = self.setup_web_driver

        if not self.is_logged_in():
            self.login() 

        self.search_for_jobs()
        self.number_of_search_results_page = (
            self.get_number_of_pages_from_search_for_jobs_results()
        )

        # Now we have the number of pages, we can go through each page and extract each job application url
        self.get_all_jobs_urls()
        self.apply_to_all_jobs()

        print(f"Total number of jobs applied for: {self.total_number_of_jobs_applied}")

    def apply_to_all_jobs(self):
        number_of_job_applications_urls = len(self.all_job_applications_urls)
        for job_counter, job_application_url in enumerate(
            self.all_job_applications_urls
        ):
            print(f"Job number {job_counter} out of {number_of_job_applications_urls}")
            if self.job_application_is_on_findajob_website(job_application_url):
                self.fill_out_findajob_form()

        print(self.total_number_of_jobs_applied)

    def fill_out_findajob_form(self):
        print(f"Applying for job: {self.driver.current_url}")
        if "findajob.dwp.gov.uk/apply" not in self.driver.current_url:
            print("Invalid url: %s" % self.driver.current_url)
            return

        try:
            # Full name
            full_name_form_id = "full_name"
            full_name_form_element = self.driver.find_element_by_id(full_name_form_id)
            full_name_form_element.clear()
            full_name_form_element.send_keys(self.application.full_name)

            # cover_letter
            cover_letter_form_id = "cover_letter"
            cover_letter_form_element = self.driver.find_element_by_id(
                cover_letter_form_id
            )
            cover_letter_form_element.clear()
            cover_letter_form_element.send_keys(self.application.cover_letter)

            # CV
            cv_dropdown_id = "cv_id"
            cv_dropdown_select_element = Select(
                self.driver.find_element_by_id(cv_dropdown_id)
            )
            cv_dropdown_select_element.select_by_visible_text(
                self.application.target_cv_name
            )
            #cv_dropdown_select_element.send_keys(Keys.ENTER)

            
            # Submit the application
            full_name_form_element.send_keys(Keys.ENTER)

            # If I don't put a sleep here the application doesn't go through? Not a fuck what's happening
            self.total_number_of_jobs_applied += 1
            print(f"Sucessfully applied for for job: {self.driver.current_url}")
            
        except Exception as e:
            print(
                "Unknown exception happened when applying for {self.driver.current_url}. Error: {e}"
            )

    def job_application_is_on_findajob_website(self, job_application_url: str) -> bool:

        try:
            print(f"Determining if {job_application_url} is on findajob... loading")
            self.driver.get(job_application_url)
            print("Loaded!")

            # Sometimes the application is gone but the page still exists!
            # This causes freezes for some reason...
            if self.driver.current_url == "https://findajob.dwp.gov.uk/error.html":
                print("This is an error page! The job no longer exists")
                return False

            if "findajob.dwp.gov.uk" in self.driver.current_url:
                print(f"{job_application_url} is on findajob!")
                return True
        except Exception as e:
            print(f"Unknonw exception: {e}")

        return False

    def search_for_jobs(self, page_number=1):
        """Loads a job title and location results with a page number (default 1)"""
        job_query_url = f"https://findajob.dwp.gov.uk/search?q={self.application.job_title}&w={self.application.job_location}&p={page_number}&pp=50"
        self.driver.get(job_query_url)

    def is_logged_in(self) -> bool:
        if self.logged_in:
            return True
        
        return False

    def login(self) -> None:
        """Login to the https://findajob.dwp.gov.uk/ using passed crendetials"""
        print("Logging in")
        try:
            self.driver.get(GovFindAJobSelenium.URLS["login"])
        except Exception as e:
            raise Exception(f"Exception happened whilst try to load the login page! Exception: {e}")

        # Enter credentials
        try:
            email_input_form_element = self.driver.find_element_by_id(GovFindAJobSelenium.PAGE_ELEMENTS_IDENTIFIERS["login_email_id"])
            self.selenium_clear_element_and_send_keys(email_input_form_element, self.login_credentials.email)
        except Exception as e:
            raise Exception(f"Couldn't log in using email! {e}")

        try:
            password_input_form_element = self.driver.find_element_by_id(
                GovFindAJobSelenium.PAGE_ELEMENTS_IDENTIFIERS["login_password_id"]
            )
            self.selenium_clear_element_and_send_keys(password_input_form_element, self.application.password)
        except Exception as e:
            raise Exception(f"Couldn't log in using password! {e}")

        # Once we've entered our password, we'll hit ENTER to login... this saves us finding and clicking the submit button
        try:
            password_input_form_element.send_keys(Keys.ENTER)
        except Exception as e:
            raise Exception(f"Couldn't submit login form! {e}")

        time.sleep(3) # I don't know exactly why, bu this is required
        if self.driver.title == "Sign in":
            raise ValueError("Invalid login credentials!")
        else:
            print("Sucessfully logged in!")
            self.is_logged_in = True

    def selenium_clear_element_and_send_keys(element, key) -> None:
        element.clear()
        element.send_keys(key)

    def setup_web_driver(self) -> webdriver:
        """Creates a selenium [Firefox] webdriver instances."""
        if self.web_driver != None:
            print("Driver already setup!")
            return self.web_driver

        try:
            driver: webdriver.Firefox = webdriver.Firefox()
            driver.minimize_window()
            driver.set_page_load_timeout(3)
        except Exception as error:
            # Handle the errors yourself m8
            raise Exception(error)

        return driver

    def destroy_web_driver(self) -> None:
        if self.web_driver is None:
            raise ValueError("Driver is already destroyed!")

        self.web_driver.quit()
        

    def get_number_of_pages_from_search_for_jobs_results(self) -> int:
        """Grabs the last item from the pager-items to determine the number of pages"""
        xpath_str: str = "//ul[@class='pager-items']/li[last()]"
        element: "WebElement" = self.driver.find_element_by_xpath(xpath_str)
        
        element_value: str = element.text
        number_of_pages: int = int(element_value)

        logging.info(f"Grabbing number of pages from a search result. {number_of_pages} found!")
        return number_of_pages

    def get_all_jobs_urls(self):
        xpath_str = "//div[@class='search-result']/h3[last()]/a[last()]"
        print("Finding jobs listings...")

        for page_number in range(1, self.number_of_search_results_page + 1):
            self.search_for_jobs(page_number)
            elements = self.driver.find_elements_by_xpath(xpath_str)

            for element in elements:
                url = element.get_attribute("href")

                # The urls we get is like: https://findajob.dwp.gov.uk/details/7784066; it doesn't actually direct to the form, just details
                # But if we change the "details" to "apply" then it takes us to the application... so change this
                url = url.replace("details", "apply")
                self.all_job_applications_urls.append(url)

        print("Number of found applications: %i" % len(self.all_job_applications_urls))



def find_and_apply_for_jobs(application: "Application") -> None:
    job_application: GetJob = GetJob(application)
    job_application.find_and_apply_for_jobs()

