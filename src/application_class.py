class Application:
    """Application class"""
    def __init__(
        self,
        email_address: str,
        password: str,
        full_name: str,
        cover_letter: str,
        target_cv_name: str,
        job_title: str,
        job_location: str,
    ) -> None:
        """Instantiates the passed variables"""
        # Credentials
        self.email_address: str = email_address
        self.password: str = password

        # Job specific
        self.job_title: str = job_title
        self.job_location: str = job_location

        # Details to fill out form
        self.full_name: str = full_name
        self.cover_letter: str = cover_letter
        self.target_cv_name: str = target_cv_name

    def __str__(self) -> str:
        """Returns the email address, job title, and job location is a clearly conveyed sentence"""
        return (
            f"{self.email_address}. Wants a {self.job_title} job in {self.job_location}"
        )
