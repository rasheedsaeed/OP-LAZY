
from src.typed_dicts import LoginCredentials
from src.classes import JobApplication, GovFindAJobSelenium

if __name__ == "__main__":
    # Credentials
    login_details: LoginCredentials = {
        "email": "", 
        "password": ""
    }

    # Job specific
    job_title: str = ""
    job_location: str = "Petoria"

    # Details to fill out form
    full_name: str = ""
    message: str = """I cannot get enough break
    """.replace("   ", "") # Do this because we get weird formatting...
    cv: str = "cv.pdf"

    application = JobApplication(
        job_title=job_title,
        job_location=job_location,
        full_name=full_name,
        cv=cv,
        message=message
    )
    
    runner = GovFindAJobSelenium(application, login_details)
    runner.find_and_apply_for_jobs()

    
