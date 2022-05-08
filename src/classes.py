from typing import List
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from typed_dicts import LoginCredentials


class JobApplication:
    def __init__(
        self,
        job_title: str,
        job_location: str,
        full_name: str,
        cv: str,
        message: str = ""
    ) -> None:
        # Job login
        self.job_title: str = job_title
        self.job_location: str = job_location

        # Job application form
        self.full_name: str = full_name
        self.message: str = message
        self.cv: str = cv

        # Applications we've applied for
        self.sucessful_applications: List[str] = []

    def sucessful_job_application(self, url: str) -> None:
        """Add which job we have sucessfully applied for"""
        self.sucessful_applications.append(url)

    def number_of_successful_application(self) -> int:
        return len(self.sucessful_applications)


class GovFindAJobSelenium:
    URLS = {"login": "https://findajob.dwp.gov.uk/sign-in"}

    PAGE_ELEMENTS_IDENTIFIERS = {
        # Login form
        "login_email_id": "email",
        "login_password_id": "password",
        # Job application form
        "job_application_full_name_id": "full_name",
        "job_application_message_id": "message",
        "job_application_cv_id": "cv_id",
        "job_application_submit_button": "govuk-button",
    }

    XPATH = {
        "number_of_pages_from_search_result": "//ul[@class='pager-items']/li[last()]",
        "get_job_url_from_job_listing": "//div[@class='search-result']/h3[last()]/a[last()]",
    }

    def __init__(
        self, job_application: JobApplication, login_credentials: LoginCredentials
    ) -> None:
        self.application: JobApplication = job_application
        self.login_credentials: LoginCredentials = login_credentials

        # Webdriver
        self.web_driver: webdriver = None

        # If we've logged into the account
        self.logged_in: bool = False

    def find_and_apply_for_jobs(self) -> None:
        """Our runner function that handles the whole process for us"""
        if not self.web_driver:
            self.setup_web_driver()

        if not self.is_logged_in():
            self.login()

        number_of_search_results_page: int = (
            self.number_of_listing_pages_from_search_results()
        )

        # Now we have the number of pages, we can go through each page and extract each job application url
        job_urls: List[str] = self.get_job_urls_from_page_listing(
            number_of_search_results_page
        )

        for job_url in job_urls:
            self.apply_for_job(job_url)
            print(f"Number of successful applications: {self.application.number_of_successful_application()}")
            
        print(
            f"Total number of jobs applied for: {self.application.number_of_successful_application()}"
        )

    def apply_for_job(self, job_url: str) -> None:
        if self.job_application_is_on_findajob_website(job_url):
            self.fill_out_findajob_form()
            print(f"Successfully applied for {job_url}")


    def fill_out_findajob_form(self) -> None:
        print(f"Applying for job: {self.web_driver.current_url}")

        if "findajob.dwp.gov.uk/apply" not in self.web_driver.current_url:
            print(f"Invalid url: {self.web_driver.current_url}")
            return

        try:
            # Full name
            try:
                full_name_form_element = self.web_driver.find_element_by_id(
                    GovFindAJobSelenium.PAGE_ELEMENTS_IDENTIFIERS[
                        "job_application_full_name_id"
                    ]
                )
                self.selenium_clear_element_and_send_keys(
                    full_name_form_element, self.application.full_name
                )
            except Exception as e:
                raise Exception(f"Unable to send full name! {e}")

            # Message
            try:
                message_form_element = self.web_driver.find_element_by_id(
                    GovFindAJobSelenium.PAGE_ELEMENTS_IDENTIFIERS[
                        "job_application_message_id"
                    ]
                )
                self.selenium_clear_element_and_send_keys(
                    message_form_element, self.application.message
                )
            except Exception as e:
                raise Exception(f"Unable to send cover letter! {e}")

            # CV
            try:
                cv_dropdown_form_element = self.web_driver.find_element_by_id(
                    GovFindAJobSelenium.PAGE_ELEMENTS_IDENTIFIERS[
                        "job_application_cv_id"
                    ]
                )
                cv_dropdown_form_element_Select = Select(cv_dropdown_form_element)

                time.sleep(2)  # If we don't do this then it breaks... brilliant!
                cv_dropdown_form_element_Select.select_by_visible_text(
                    self.application.cv
                )
            except Exception as e:
                raise Exception(f"Unable to select cv! {e}")

            # Submit the application
            try:
                # We grab the last button as the webpage may display "accept cookies" which uses the same class
                submit_button = self.web_driver.find_elements_by_class_name(
                    GovFindAJobSelenium.PAGE_ELEMENTS_IDENTIFIERS[
                        "job_application_submit_button"
                    ]
                )[-1]
                submit_button.click()
            except Exception as e:
                raise Exception(f"Couldn't click submit button! {e}")

            # If I don't put a sleep here the application doesn't go through? Not a fuck what's happening
            time.sleep(4)
            self.application.sucessful_job_application(self.web_driver.current_url)
            print(f"Sucessfully applied for for job: {self.web_driver.current_url}")

        except Exception as e:
            print(
                f"Unknown exception happened when applying for {self.web_driver.current_url}. {e}"
            )

    def job_application_is_on_findajob_website(self, job_application_url: str) -> bool:
        try:
            print(f"Determining if {job_application_url} is on findajob... loading")
            self.web_driver.get(job_application_url)

            # Sometimes the application is gone but the page still exists!
            # This causes the browser to freeze for some reason... handle this
            if self.web_driver.current_url == "https://findajob.dwp.gov.uk/error.html":
                print("This is an error page! The job no longer exists")
                return False

            if "findajob.dwp.gov.uk" in self.web_driver.current_url:
                print(f"{job_application_url} is on findajob!")
                return True
        except Exception as e:
            print(f"Unknonw exception: {e}")

        return False

    def search_for_jobs(self, page_number=1) -> None:
        """Search for jobs based of obj's job title and location, from a job listing page (default 1)."""
        job_search_url: str = f"https://findajob.dwp.gov.uk/search?q={self.application.job_title}&w={self.application.job_location}&p={page_number}&pp=50"

        try:
            self.web_driver.get(job_search_url)
        except Exception as e:
            raise Exception(f"Coulnd't search for jobs! {e}")

    def is_logged_in(self) -> bool:
        if self.logged_in:
            return True

        return False

    def login(self) -> None:
        """Login to the https://findajob.dwp.gov.uk/ using passed crendetials"""
        print("Logging in...")
        try:
            self.web_driver.get(GovFindAJobSelenium.URLS["login"])
        except Exception as e:
            raise Exception(
                f"Exception happened whilst try to load the login page! Exception: {e}"
            )

        # Enter credentials
        try:
            email_input_form_element = self.web_driver.find_element_by_id(
                GovFindAJobSelenium.PAGE_ELEMENTS_IDENTIFIERS["login_email_id"]
            )
            self.selenium_clear_element_and_send_keys(
                email_input_form_element, self.login_credentials["email"]
            )
        except Exception as e:
            raise Exception(f"Couldn't log in using email! {e}")

        try:
            password_input_form_element = self.web_driver.find_element_by_id(
                GovFindAJobSelenium.PAGE_ELEMENTS_IDENTIFIERS["login_password_id"]
            )
            self.selenium_clear_element_and_send_keys(
                password_input_form_element, self.login_credentials["password"]
            )
        except Exception as e:
            raise Exception(f"Couldn't log in using password! {e}")

        # Once we've entered our password, we'll hit ENTER to login... this saves us finding and clicking the submit button
        try:
            password_input_form_element.send_keys(Keys.ENTER)
        except Exception as e:
            raise Exception(f"Couldn't submit login form! {e}")

        time.sleep(
            3
        )  # If we don't have this, despite actually logging in, the title doesn't load and it executes as False... so keep this.
        if self.web_driver.title == "Sign in":
            raise ValueError("Invalid login credentials!")
        else:
            print("Sucessfully logged in!")
            self.is_logged_in = True

    def selenium_clear_element_and_send_keys(self, element, keys) -> None:
        try:
            element.clear()
            element.send_keys(keys)
        except Exception as e:
            # How have you messed this up you retard?
            raise Exception("Couldn't clear and send key to selenium element! {e}")

    def setup_web_driver(self) -> None:
        """Creates a selenium [Firefox] webdriver instances."""
        if self.web_driver != None:
            print("Driver already setup!")
            return self.web_driver

        try:
            driver: webdriver.Firefox = webdriver.Firefox()
            driver.minimize_window()
        except Exception as error:
            # Handle the errors yourself m8
            raise Exception(error)

        self.web_driver = driver

    def destroy_web_driver(self) -> None:
        if self.web_driver is None:
            raise ValueError("Web driver is already destroyed!")

        self.web_driver.quit()

    def number_of_listing_pages_from_search_results(self) -> int:
        """Grabs the last item from the pager-items to determine the number of pages"""
        print("Grabbing number of pages from search result")

        # A [valid] search results gives us number of pages with job listings
        self.search_for_jobs()

        try:
            selenium_element = self.web_driver.find_element_by_xpath(
                GovFindAJobSelenium.XPATH["number_of_pages_from_search_result"]
            )
        except Exception as e:
            raise Exception(f"Coulnd't grab last page number from search result! {e}")

        number_of_pages: int = int(selenium_element.text)

        print(f"Number of listing pages found: {number_of_pages} ")
        return number_of_pages

    def get_job_urls_from_page_listing(
        self, number_of_search_results_page: int
    ) -> List[str]:
        print("Finding jobs listings...")

        job_application_urls: list = []
        for page_number in range(1, number_of_search_results_page + 1):
            self.search_for_jobs(page_number)

            selenium_elements = self.web_driver.find_elements_by_xpath(
                GovFindAJobSelenium.XPATH["get_job_url_from_job_listing"]
            )

            print(f"Number of urls: {len(selenium_elements)}")
            for selenium_element in selenium_elements:
                url: str = selenium_element.get_attribute("href")

                # The url we find is like: https://findajob.dwp.gov.uk/details/7784066; this url doesn't direct to the form but to the job details
                # But if we change the "details" to "apply" then it takes us to the application... so change this
                url = url.replace("details", "apply")
                job_application_urls.append(url)

        print(f"Number of found applications: {len(job_application_urls)}")
        return job_application_urls
