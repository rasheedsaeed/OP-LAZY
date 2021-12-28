from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class JobApplication:
    def __init__(self, application: "Application"):
        self.driver = self.setup_driver()
        self.application = application

        # Results
        self.number_of_search_results_page = 1
        self.all_job_urls = []

    def apply_for_jobs(self):
        """Our main function that executes our methods to apply for jobs"""
        self.login()

        # Now that we're setup, we have to find out how many page results there are.
        # We need to do this to find the hyperlinks for the job application(s) themselves
        # So we simply do a init search_for_job which gives us the number of pages as the bottom of the page
        self.search_for_jobs()
        self.number_of_search_results_page = self.get_number_of_pages_from_search_for_jobs_results()

        # Now we have the number of pages, we can go through each page and extract each job application url
        self.get_all_jobs_urls()

    def search_for_jobs(self, page_number=1):
        """Loads a job search result webpage with a job title, job location, and page number (default = 1)"""
        job_query_url = f"https://findajob.dwp.gov.uk/search?q={self.application.job_title}&w={self.application.job_location}&p={page_number}"
        self.driver.get(job_query_url)
        time.sleep(2)

    def login(self):
        """Login to the https://findajob.dwp.gov.uk/ using the Application's credentials"""
        self.driver.get("https://findajob.dwp.gov.uk/sign-in")

        # Enter credentials
        email_input_form_id = "email"
        email_input_form_element = self.driver.find_element_by_id(email_input_form_id)
        email_input_form_element.clear()
        email_input_form_element.send_keys(self.application.email_address)

        password_input_form_id = "password"
        password_input_form_element = self.driver.find_element_by_id(password_input_form_id)
        password_input_form_element.clear()

        # Once we've entered our password, we'll hit ENTER to login... this saves us finding and clicking the submit button
        password_input_form_element.send_keys(self.application.password, Keys.ENTER)

        time.sleep(5)
        if self.driver.title == "Sign in":
            raise ValueError("Invalid login credentials!")
        else:
            print("Sucessfully logged in")

    def setup_driver(self) -> webdriver:
        """Creates a driver with detatch mode; this helps us see if the script is working well whilst developing."""
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)
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

        for page_number in range(1, self.number_of_search_results_page + 1):
            self.search_for_jobs(page_number)
            elements = self.driver.find_elements_by_xpath(xpath_str)

            for element in elements:
                url = element.get_attribute("href")

                # The urls we get is like: https://findajob.dwp.gov.uk/details/7784066; it doesn't actually direct to the form, just details
                # But if we change the "details" to "apply" then it takes us to the application... so change this
                url = url.replace("details", "apply")
                self.all_job_urls.append(url)

        print("Number of found applications: %i" % len(self.all_job_urls))

        
def apply_for_jobs(application: "Application"):
    job_application = JobApplication(application)
    job_application.apply_for_jobs()




