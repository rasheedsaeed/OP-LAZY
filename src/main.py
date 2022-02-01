from apply_for_jobs_script import find_and_apply_for_jobs
from utils import Application

if __name__ == "__main__":
    # Credentials
    email_address: str = "hfzcvdfhzmfbqjaiap@kvhrr.com"
    password: str = "nevergonnagiveyouup1"

    # Job specific
    job_title: str = "Cleaner"
    job_location: str = "Wirral"

    # Details to fill out form
    full_name: str = "TONDO EIGHTEEN"
    cover_letter: str = """
    """
    target_cv_name: str = "TONDO_CV.pdf"

    application_details: Application = {
        email_address: email_address,
        password: password,
        job_title: job_title,
        job_location: job_location,
        full_name: full_name,
        cover_letter: cover_letter,
        target_cv_name: target_cv_name
    }
    
    find_and_apply_for_jobs(application)
