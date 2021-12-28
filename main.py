import sys

from application_class import Application
from apply_for_jobs_script import apply_for_jobs

def unpack_sys_arg_values(values: list):
    return (values[1], values[2], values[3], values[4]) 

if __name__ == "__main__":
    email_address, password, job_title, job_location = unpack_sys_arg_values(sys.argv)
    application = Application(email_address, password, job_title, job_location)

    apply_for_jobs(application)