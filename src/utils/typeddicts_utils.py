from typing import TypedDict, NotRequired

class Credentials(TypedDict):
    email: str
    password: str

class JobApplication(TypedDict, total=False):
    job_title: str
    job_location: str
    full_name: str
    target_cv: str
    cover_letter: NotRequired[str]
