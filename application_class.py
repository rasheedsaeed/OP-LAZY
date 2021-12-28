class Application:
    def __init__(self, email_address: str, password: str, job_title: str, job_location: str) -> None:
        self.email_address = email_address
        self.password = password
        self.job_title = job_title
        self.job_location = job_location

    def __str__(self) -> str:
        return f"{self.email_address}. Wants a {self.job_title} job in {self.job_location}"



