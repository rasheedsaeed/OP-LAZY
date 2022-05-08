
from typed_dicts import LoginCredentials
from classes import JobApplication, GovFindAJobSelenium

if __name__ == "__main__":
    # Credentials
    login_details: LoginCredentials = {
        "email": "claireshakeshaft1975@gmail.com", 
        "password": "Mychildren_1975"
    }

    # Job specific
    job_title: str = "Live in carer"
    job_location: str = "UK"

    # Details to fill out form
    full_name: str = "Claire Shakeshaft"
    message: str = """I am a live in career, but open to any other live in employment. Willing to relocate across the UK. 
    My preferred method of contact is via my mobile number: 07754242334. I am DBS cleared.
    """.replace("   ", "")
    cv: str = "Claire_Shakeshaft___CV.pdf"

    application = JobApplication(
        job_title=job_title,
        job_location=job_location,
        full_name=full_name,
        cv=cv,
        message=message
    )
    
    runner = GovFindAJobSelenium(application, login_details)
    runner.find_and_apply_for_jobs()
    print(application.number_of_successful_application())

    
