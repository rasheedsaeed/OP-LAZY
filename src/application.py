from typing_extensions import NotRequired, TypedDict


from typing import TypedDict

class JobApplication(TypedDict):
    email_address: str
    password: str
    job_title: str
    job_location: str
    full_name: str
    cover_letter: NotRequired[str]
    target_cv_name: str

