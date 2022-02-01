from typing import TypedDict

class Application(TypedDict, total=False):
    email_address: str
    password: str
    job_title: str
    job_location: str
    full_name: str
    cover_letter: str
    target_cv_name: str