import sys

from application_class import Application
from apply_for_jobs_script import apply_for_jobs

def unpack_sys_arg_values(values: list):
    return (values[1], values[2], values[3], values[4]) 

if __name__ == "__main__":
    email_address = "wnvpgxegqfvqzbftxd@bvhrk.com"
    password = "Password1!"
    job_title = "Cleaner"
    job_location = "Wirral"
    full_name = "Claire Shakeshaft"
    message = "I have 20 years of experiance with many years of supervising & managamenet."
    target_cv_name = "Claire_Shakeshaft___CV.pdf"

    application = Application(
        email_address = email_address,
        password = password,
        job_title = job_title,
        job_location = job_location,
        full_name = full_name,
        message = message,
        target_cv_name = target_cv_name
    )
    apply_for_jobs(application)