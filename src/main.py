from application_class import Application
from apply_for_jobs_script import find_and_apply_for_jobs

if __name__ == "__main__":
    # Credentials
    email_address: str = "wnvpgxegqfvqzbftxd@bvhrk.com"
    password: str = "Password1!"

    # Job specific
    job_title: str = ""
    job_location: str = ""

    # Details to fill out form
    full_name: str = ""
    cover_letter: str = ""
    target_cv_name: str = ""

    application = Application(
        email_address=email_address,
        password=password,
        job_title=job_title,
        job_location=job_location,
        full_name=full_name,
        cover_letter=cover_letter,
        target_cv_name=target_cv_name,
    )
    find_and_apply_for_jobs(application)
