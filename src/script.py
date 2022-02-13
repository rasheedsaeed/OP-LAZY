
from typed_dicts import LoginCredentials
from classes import JobApplication, GovFindAJobSelenium

if __name__ == "__main__":
    # Credentials
    login_details: LoginCredentials = {
        "email": "hfzcvdfhzmfbqjaiap@kvhrr.com", 
        "password": "nevergonnagiveyouup1"
    }

    # Job specific
    job_title: str = "Cleaner"
    job_location: str = "Wirral"

    # Details to fill out form
    full_name: str = "TONDO EIGHTEEN"
    message: str = "Hello daddy!"
    cv: str = "TONDO_CV.pdf"

    application = JobApplication(
        job_title=job_title,
        job_location=job_location,
        full_name=full_name,
        cv=cv,
        message=message
    )
    
    runner = GovFindAJobSelenium(application, login_details)
    runner.find_and_apply_for_jobs()

    
