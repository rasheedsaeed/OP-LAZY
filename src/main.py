from application_class import Application
from apply_for_jobs_script import apply_for_jobs

if __name__ == "__main__":
    email_address = "wnvpgxegqfvqzbftxd@bvhrk.com"
    password = "Password1!"
    job_title = ""
    job_location = "UK"
    full_name = "Claire Shakeshaft"
    cover_letter = """
    I have over 20 years of customer experiance and many years of supervisor & managerial experiance. 

    I am willing to relocate and prefer a possibility to live-in.
    """
    target_cv_name = "Claire_Shakeshaft___CV.pdf"

    application = Application(
        email_address=email_address,
        password=password,
        job_title=job_title,
        job_location=job_location,
        full_name=full_name,
        cover_letter=cover_letter,
        target_cv_name=target_cv_name,
    )
    apply_for_jobs(application)
