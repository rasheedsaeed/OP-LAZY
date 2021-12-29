from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

import time


class GetJob:
    def __init__(self, application: "Application"):
        self.driver = self.setup_driver()
        self.application = application

        # Results
        self.number_of_search_results_page = 1
        self.all_job_applications_urls = []
        self.total_number_of_jobs_applied = 0

    def find_and_apply_for_jobs(self):
        """Our main function that executes our methods to apply for jobs"""
        self.login()

        # Now that we're setup, we have to find out how many page results there are.
        # We need to do this to find the hyperlinks for the job application(s) themselves
        # So we simply do a init search_for_job which gives us the number of pages as the bottom of the page
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

            # Submit the application
            full_name_form_element.send_keys(Keys.ENTER)

            # If I don't put a sleep here the application doesn't go through? Not a fuck what's happening
            time.sleep(1)
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
        """Loads a job search result webpage with a job title, job location, and page number (default = 1)"""
        job_query_url = f"https://findajob.dwp.gov.uk/search?st=30000&cti=full_time&q={self.application.job_title}&w={self.application.job_location}&p={page_number}&pp=50"

        try:
            self.driver.get(job_query_url)
        except TimeoutException:
            print(f"Session timed out! Oh well. Page number: {page_number}")

    def login(self):
        """Login to the https://findajob.dwp.gov.uk/ using the Application's credentials"""
        print("Logging in...")
        self.driver.get("https://findajob.dwp.gov.uk/sign-in")

        # Enter credentials
        email_input_form_id = "email"
        email_input_form_element = self.driver.find_element_by_id(email_input_form_id)
        email_input_form_element.clear()
        email_input_form_element.send_keys(self.application.email_address)

        password_input_form_id = "password"
        password_input_form_element = self.driver.find_element_by_id(
            password_input_form_id
        )
        password_input_form_element.clear()

        # Once we've entered our password, we'll hit ENTER to login... this saves us finding and clicking the submit button
        password_input_form_element.send_keys(self.application.password, Keys.ENTER)

        time.sleep(3)
        if self.driver.title == "Sign in":
            raise ValueError("Invalid login credentials!")
        else:
            print("Sucessfully logged in")

    def setup_driver(self) -> webdriver:
        """Creates a driver with detatch mode; this helps us see if the script is working well whilst developing."""
        driver = webdriver.Firefox()
        driver.set_page_load_timeout(6)
        return driver

    def get_number_of_pages_from_search_for_jobs_results(self) -> int:
        """Grabs the last item from the pager-items to determine the number of pages"""
        xpath_str = "//ul[@class='pager-items']/li[last()]"
        element = self.driver.find_element_by_xpath(xpath_str)

        element_value = element.text
        number_of_pages = int(element_value)

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


def find_and_apply_for_jobs(application: "Application"):
    """Creates a GetJob obj using an Application obj then begins finding and applying for jobs."""
    job_application: GetJob = GetJob(application)
    job_application.find_and_apply_for_jobs()
