
from typed_dicts import Credentials
from classes import JobApplication, GovFindAJobSelenium

if __name__ == "__main__":
    # Credentials
    login_details: Credentials = {
        "email": "hfzcvdfhzmfbqjaiap@kvhrr.com", 
        "password": "nevergonnagiveyouup1"
    }

    # Job specific
    job_title: str = "Cleaner"
    job_location: str = "Wirral"

    # Details to fill out form
    full_name: str = "TONDO EIGHTEEN"
    cover_letter: str = """
    """
    target_cv_name: str = "TONDO_CV.pdf"

    application = JobApplication(
        job_title,
        job_location,
        full_name,
        target_cv_name,
        cover_letter
    )
    runner = GovFindAJobSelenium([application], login_details)
    runner.setup_web_driver()
